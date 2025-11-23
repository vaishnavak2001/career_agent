from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Application

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve applications.
    """
    apps = db.query(Application).offset(skip).limit(limit).all()
    return [{"id": str(a.id), "status": a.status} for a in apps]

@router.post("/apply/{job_id}")
def apply_to_job(job_id: str, resume_id: str, db: Session = Depends(get_db)):
    """
    Apply to a specific job.
    """
    return {"message": f"Applied to job {job_id} with resume {resume_id}"}
