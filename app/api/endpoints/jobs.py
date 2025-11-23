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
    # Import services directly
    from app.services.adzuna import adzuna_service
    from app.services.scraper import scraper_service
    from app.services.parser import parser_service
    from app.services.matcher import matcher_service
    from app.db.models import Job
    
    all_jobs = []
    
    # Try Adzuna API first
    print(f"Searching Adzuna for {role} in {region}...")
    adzuna_jobs = await adzuna_service.search_jobs(role, region)
    if adzuna_jobs:
        print(f"Found {len(adzuna_jobs)} jobs on Adzuna")
        all_jobs.extend(adzuna_jobs)
    
    if not all_jobs:
        return {"message": "No jobs found.", "jobs_found": 0}
    
    # Process and Save Jobs
    saved_count = 0
    
    try:
        for job_data in all_jobs:
            # Deduplicate by URL
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if existing:
                continue
                
            # Parse Description
            parsed_data = {}
            if job_data.get("description"):
                parsed_data = parser_service.parse_job_description(job_data["description"])
            
            # Calculate Match Score
            match_score = matcher_service.compute_match_score(
                job_data.get("description", ""), 
                ["python", "react", "fastapi"]
            )
            
            new_job = Job(
                id=f"job_{datetime.now().timestamp()}_{saved_count}",
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                url=job_data["url"],
                source=job_data["source"],
                raw_text=job_data.get("description"),
                parsed_data=parsed_data,
                match_score=match_score,
                is_scam=False
            )
            db.add(new_job)
            saved_count += 1
            
        db.commit()
    except Exception as e:
        print(f"Error saving jobs to DB: {e}")
        db.rollback()
        return {"error": str(e), "jobs_found": 0}
    
    return {
        "message": f"Successfully found and processed {saved_count} new jobs.",
        "jobs_found": saved_count,
        "sources": list(set(j["source"] for j in all_jobs))
    }
