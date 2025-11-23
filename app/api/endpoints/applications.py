from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Application, Resume

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve applications.
    """
    apps = db.query(Application).offset(skip).limit(limit).all()
    return [{"id": str(a.id), "status": a.status} for a in apps]

from datetime import datetime

@router.post("/apply/{job_id}")
def apply_to_job(job_id: str, db: Session = Depends(get_db)):
    """
    Apply to a specific job.
    """
    # Find a resume to use (default to first base resume)
    resume = db.query(Resume).filter(Resume.is_base == True).first()
    if not resume:
        # Fallback to any resume
        resume = db.query(Resume).first()
        
    if not resume:
        raise HTTPException(status_code=400, detail="No resume found. Please upload a resume first.")
        
    # Check if already applied
    existing = db.query(Application).filter(
        Application.job_id == job_id,
        Application.resume_id == str(resume.id)
    ).first()
    
    if existing:
        return {"message": "Already applied to this job", "application_id": str(existing.id)}

    # Create application
    application = Application(
        job_id=job_id,
        resume_id=str(resume.id),
        user_id="default_user",
        status="pending",
        applied_at=datetime.utcnow()
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    
    # TODO: Trigger the actual agent workflow here (background task)
    
    return {"message": f"Application submitted for job {job_id}", "application_id": str(application.id)}
