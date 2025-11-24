from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Application, Resume, Job

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve applications.
    """
    apps = db.query(Application).offset(skip).limit(limit).all()
    return [
        {
            "id": a.id,
            "job_id": a.job_id,
            "resume_id": a.resume_id,
            "status": a.status,
            "applied_at": a.applied_at.isoformat() if a.applied_at else None
        } 
        for a in apps
    ]

@router.post("/apply/{job_id}")
def apply_to_job(job_id: int, db: Session = Depends(get_db)):  # Changed to int
    """
    Apply to a specific job.
    """
    # Verify job exists
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    
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
        Application.resume_id == resume.id
    ).first()
    
    if existing:
        return {"message": "Already applied to this job", "application_id": existing.id}

    # Create application  
    # TODO: Get actual user_id from authentication  
    # For now, find or create default user
    from app.models import User
    default_user = db.query(User).first()
    if not default_user:
        # Create a default user for testing
        default_user = User(
            email="demo@careeragent.com",
            hashed_password="placeholder",
            full_name="Demo User"
        )
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
    
    application = Application(
        job_id=job_id,
        resume_id=resume.id,
        user_id=default_user.id,
        status="pending",
        applied_at=datetime.utcnow()
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    
    # TODO: Trigger the actual agent workflow here (background task)
    
    return {
        "message": f"Application submitted for job {job_id}",
        "application_id": application.id
    }
