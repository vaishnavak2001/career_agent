from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Resume, User

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve resumes.
    """
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    return [
        {
            "id": r.id,  # INTEGER
            "version_name": r.version_name,
            "is_base": r.is_base,
            "created_at": r.created_at.isoformat() if r.created_at else None
        } 
        for r in resumes
    ]

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a new resume.
    """
    try:
        # Read file content
        content_bytes = await file.read()
        try:
            content = content_bytes.decode('utf-8')
        except:
            content = f"Binary file: {file.filename}"
            
        # Get or create default user
        from app.models import User
        default_user = db.query(User).first()
        if not default_user:
            default_user = User(
                email="demo@careeragent.com",
                hashed_password="placeholder",
                full_name="Demo User"
            )
            db.add(default_user)
            db.commit()
            db.refresh(default_user)
        
        # Create resume record
        resume = Resume(
            version_name=file.filename,
            content=content,
            is_base=True,
            user_id=default_user.id  # INTEGER FK
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {
            "id": resume.id,  # Return INTEGER
            "version_name": resume.version_name,
            "message": "Resume uploaded successfully"
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
