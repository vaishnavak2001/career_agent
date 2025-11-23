from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Job

router = APIRouter()

@router.get("/", response_model=List[dict])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve jobs.
    """
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return [
        {
            "id": str(job.id),
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "match_score": job.match_score,
            "posted_date": job.posted_date.isoformat() if job.posted_date else None,
            "source": job.source,
            "url": job.url,
            "is_scam": job.is_scam,
            "parsed_json": job.parsed_data
        }
        for job in jobs
    ]

@router.post("/scrape")
async def trigger_scrape(region: str, role: str, db: Session = Depends(get_db)):
    """
    Trigger a job scraping task using the unified agent tool (Adzuna + Scraper).
    """
    from app.agent.tools import scrape_jobs
    
    # Call the tool directly
    # Note: The tool handles DB saving internally
    result = await scrape_jobs(role=role, region=region, platforms=["indeed", "linkedin"])
    
    return result
