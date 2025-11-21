"""Job scraping, parsing, and validation tools."""
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import re
from langchain_core.tools import tool
from app.models import Job, JobStatus
from app.database import SessionLocal

@tool
def scrape_jobs(region: str, role: str, platforms: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Scrapes job listings for a given region and role from multiple platforms.
    Returns a list of job dictionaries.
    """
    # In a real scenario, this would call specific scrapers or APIs
    # For now, we simulate with realistic mock data if APIs fail
    
    print(f"Scraping jobs for {role} in {region}...")
    
    # Mock data generation for demonstration
    jobs = [
        {
            "url": f"https://indeed.com/viewjob?jk=mock{i}",
            "title": f"{role} {i}",
            "company": f"Tech Company {i}",
            "location": region,
            "posted_date": datetime.now(),
            "raw_text": f"We are looking for a {role} with Python and React experience...",
            "source": "indeed"
        }
        for i in range(1, 4)
    ]
    
    # Save to DB
    db = SessionLocal()
    saved_jobs = []
    try:
        for job_data in jobs:
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if not existing:
                job = Job(**job_data, status=JobStatus.SCRAPED.value)
                db.add(job)
                saved_jobs.append(job_data)
        db.commit()
    finally:
        db.close()
        
    return saved_jobs

@tool
def detect_scam(job_record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes a job record for scam indicators.
    Returns a dictionary with is_scam boolean and reason.
    """
    text = job_record.get("raw_text", "") or job_record.get("description", "")
    company = job_record.get("company", "")
    
    reasons = []
    is_scam = False
    
    if "send money" in text.lower() or "bank account" in text.lower():
        is_scam = True
        reasons.append("Requests financial info")
        
    if not company or len(company) < 2:
        is_scam = True
        reasons.append("Invalid company name")
        
    return {
        "is_scam": is_scam,
        "reason": "; ".join(reasons) if reasons else None
    }

@tool
def parse_jd(job_text: str) -> Dict[str, Any]:
    """
    Parses a job description text into structured data (skills, seniority, etc).
    """
    # Simple regex-based parsing for now
    skills = []
    if "python" in job_text.lower(): skills.append("Python")
    if "react" in job_text.lower(): skills.append("React")
    if "aws" in job_text.lower(): skills.append("AWS")
    
    seniority = "Mid"
    if "senior" in job_text.lower(): seniority = "Senior"
    if "junior" in job_text.lower(): seniority = "Junior"
    
    return {
        "skills": skills,
        "seniority": seniority,
        "years_experience": 3 # Mock inference
    }

@tool
def compute_match_score(resume_text: str, structured_jd: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculates a match score (0-100) between a resume and a structured JD.
    """
    score = 0
    breakdown = {}
    
    # Mock scoring logic
    jd_skills = set(s.lower() for s in structured_jd.get("skills", []))
    resume_lower = resume_text.lower()
    
    matched_skills = [s for s in jd_skills if s in resume_lower]
    
    if jd_skills:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skill_score = 50 # Neutral if no skills found
        
    score = skill_score
    breakdown["skills_match"] = f"{len(matched_skills)}/{len(jd_skills)}"
    
    return {
        "score": round(score, 2),
        "breakdown": breakdown
    }
