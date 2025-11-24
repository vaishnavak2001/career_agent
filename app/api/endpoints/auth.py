from datetime import timedelta
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
import httpx
from app.database import get_db
from app.models import User
from app.auth.jwt import create_access_token, verify_password, get_password_hash
from app.auth.dependencies import get_current_user
from app.core.config import settings

router = APIRouter()


# Pydantic schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Login and get access token."""
    # Find user by email (username field in OAuth2PasswordRequestForm)
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify password
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_user_me(
    full_name: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user information."""
    if full_name:
        current_user.full_name = full_name
    
    db.commit()
    db.refresh(current_user)
    return current_user


@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change user password."""
    # Verify current password
    if not verify_password(current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect current password"
        )
    
    # Update password
    current_user.hashed_password = get_password_hash(new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}


# OAuth Settings (Should be in config)
GOOGLE_CLIENT_ID = "mock-google-client-id"
GOOGLE_CLIENT_SECRET = "mock-google-client-secret"
GOOGLE_REDIRECT_URI = "http://localhost:8000/api/v1/auth/callback/google"

LINKEDIN_CLIENT_ID = "mock-linkedin-client-id"
LINKEDIN_CLIENT_SECRET = "mock-linkedin-client-secret"
LINKEDIN_REDIRECT_URI = "http://localhost:8000/api/v1/auth/callback/linkedin"


@router.get("/login/google")
async def login_google():
    """Redirect to Google OAuth login."""
    return RedirectResponse(
        f"https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20email%20profile"
    )


@router.get("/callback/google")
async def callback_google(code: str, db: Session = Depends(get_db)):
    """Handle Google OAuth callback."""
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        
        if "error" in token_data:
            raise HTTPException(status_code=400, detail="Google authentication failed")
            
        # Get user info
        user_response = await client.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_info = user_response.json()
        
        # Find or create user
        email = user_info.get("email")
        name = user_info.get("name")
        
        user = db.query(User).filter(User.email == email).first()
        if not user:
            # Create new user with random password
            import secrets
            random_password = secrets.token_urlsafe(16)
            user = User(
                email=email,
                full_name=name,
                hashed_password=get_password_hash(random_password)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        return RedirectResponse(f"http://localhost:5173/auth/callback?token={access_token}")


@router.get("/login/linkedin")
async def login_linkedin():
    """Redirect to LinkedIn OAuth login."""
    return RedirectResponse(
        f"https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id={LINKEDIN_CLIENT_ID}&redirect_uri={LINKEDIN_REDIRECT_URI}&scope=r_liteprofile%20r_emailaddress"
    )


@router.get("/callback/linkedin")
async def callback_linkedin(code: str, db: Session = Depends(get_db)):
    """Handle LinkedIn OAuth callback."""
    # Exchange code for token
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data={
                "code": code,
                "client_id": LINKEDIN_CLIENT_ID,
                "client_secret": LINKEDIN_CLIENT_SECRET,
                "redirect_uri": LINKEDIN_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        token_data = token_response.json()
        
        if "error" in token_data:
            raise HTTPException(status_code=400, detail="LinkedIn authentication failed")
            
        # Get user info
        user_response = await client.get(
            "https://api.linkedin.com/v2/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        user_info = user_response.json()
        
        # Get email (separate endpoint for LinkedIn)
        email_response = await client.get(
            "https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        email_data = email_response.json()
        email = email_data["elements"][0]["handle~"]["emailAddress"]
        
        name = f"{user_info.get('localizedFirstName')} {user_info.get('localizedLastName')}"
        
        # Find or create user
        user = db.query(User).filter(User.email == email).first()
        if not user:
            import secrets
            random_password = secrets.token_urlsafe(16)
            user = User(
                email=email,
                full_name=name,
                hashed_password=get_password_hash(random_password)
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email},
            expires_delta=access_token_expires
        )
        
        # Redirect to frontend with token
        return RedirectResponse(f"http://localhost:5173/auth/callback?token={access_token}")
