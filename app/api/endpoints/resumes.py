from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Resume

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_resumes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve resumes.
    """
    resumes = db.query(Resume).offset(skip).limit(limit).all()
    return [{"id": str(r.id), "version": r.version_name} for r in resumes]

@router.post("/upload")
def upload_resume(content: str, version_name: str, db: Session = Depends(get_db)):
    """
    Upload a new resume.
    """
    # Placeholder logic
    return {"message": "Resume uploaded"}
