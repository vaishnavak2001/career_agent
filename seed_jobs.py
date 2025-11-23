"""
Simple test script to add sample jobs directly to the database
"""
import sys
import json
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Job
from datetime import datetime
import uuid

def add_sample_jobs():
    db = SessionLocal()
    
    sample_jobs = [
        {
            "title": "Senior Python Engineer",
            "company": "TechCorp Inc",
            "location": "San Francisco, CA",
            "url": f"https://example.com/jobs/{uuid.uuid4()}",
            "source": "indeed",
            "raw_text": "We are looking for a Senior Python Engineer with 5+ years of experience in FastAPI, Django, and PostgreSQL.",
            "parsed_data": json.dumps({
                "skills": ["Python", "FastAPI", "Django", "PostgreSQL"],
                "experience": "5+ years",
                "salary": "$150k-$200k",
                "summary": "Senior Python Engineer role"
            }),
            "match_score": 95,
            "is_scam": False
        },
        {
            "title": "Full Stack Developer",
            "company": "StartupXYZ",
            "location": "Remote",
            "url": f"https://example.com/jobs/{uuid.uuid4()}",
            "source": "linkedin",
            "raw_text": "Join our team as a Full Stack Developer. Must know React, Node.js, and MongoDB.",
            "parsed_data": json.dumps({
                "skills": ["React", "Node", "MongoDB", "Javascript"],
                "experience": "3+ years",
                "salary": "$120k-$160k",
                "summary": "Full Stack Developer position"
            }),
            "match_score": 88,
            "is_scam": False
        },
        {
            "title": "Machine Learning Engineer",
            "company": "AI Solutions LLC",
            "location": "New York, NY",
            "url": f"https://example.com/jobs/{uuid.uuid4()}",
            "source": "glassdoor",
            "raw_text": "Seeking ML Engineer with Python, TensorFlow, PyTorch experience. PhD preferred.",
            "parsed_data": json.dumps({
                "skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning"],
                "experience": "5+ years",
                "salary": "$180k-$250k",
                "summary": "Machine Learning Engineer role"
            }),
            "match_score": 82,
            "is_scam": False
        },
    ]
    
    for job_data in sample_jobs:
        job = Job(
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            url=job_data["url"],
            source=job_data["source"],
            raw_text=job_data["raw_text"],
            parsed_data=job_data["parsed_data"],
            match_score=job_data["match_score"],
            is_scam=job_data["is_scam"],
            posted_date=datetime.utcnow()
        )
        db.add(job)
    
    db.commit()
    print(f"✅ Added {len(sample_jobs)} sample jobs to database")
    db.close()

if __name__ == "__main__":
    add_sample_jobs()
