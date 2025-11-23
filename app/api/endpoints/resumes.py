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

from fastapi import File, UploadFile
import shutil
import os

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload a new resume.
    """
    # For now, we'll just read the text content if it's a text file, 
    # or save it and store the path. 
    # Since we don't have a PDF parser set up in this file, let's assume text/markdown for simplicity
    # or just store the filename as content for now if binary.
    
    content = ""
    try:
        # Simple text read attempt
        content_bytes = await file.read()
        try:
            content = content_bytes.decode('utf-8')
        except:
            content = f"Binary file: {file.filename}"
            
        # Create resume record
        # TODO: Get actual user_id from auth
        resume = Resume(
            version_name=file.filename,
            content=content,
            is_base=True,
            user_id="default_user" 
        )
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return {"id": str(resume.id), "message": "Resume uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
