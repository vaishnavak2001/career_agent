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
    Trigger a job scraping task.
    """
    from app.services.scraper import scraper_service
    from app.services.parser import parser_service
    
    jobs_data = await scraper_service.scrape_jobs(role, region, ["indeed"])
    
    saved_count = 0
    for job_data in jobs_data:
        # Check if job exists
        existing = db.query(Job).filter(Job.url == job_data["url"]).first()
        if not existing:
            # Parse JD (mocking raw text for now as scraper doesn't return full text yet)
            # In real impl, scraper should return raw_text
            raw_text = f"{job_data['title']} at {job_data['company']}. {job_data.get('description', '')}"
            parsed_data = parser_service.parse_job_description(raw_text)
            
            job = Job(
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                url=job_data["url"],
                source=job_data["source"],
                posted_date=datetime.utcnow(),
                raw_text=raw_text,
                parsed_data=parsed_data
            )
            db.add(job)
            saved_count += 1
    
    db.commit()
    return {"message": f"Scraping completed. Found {len(jobs_data)} jobs, saved {saved_count} new jobs."}
