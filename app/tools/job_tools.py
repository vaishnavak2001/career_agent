"""Job scraping, parsing, and validation tools."""
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from datetime import datetime
import re
from sqlalchemy.orm import Session
from app.models import Job
from app.database import SessionLocal


def scrape_jobs(region: str, role: str, platforms: List[str]) -> List[Dict[str, Any]]:
    """
    Scrapes job listings from specified platforms.
    
    NOTE: This is a simplified implementation. In production:
    - Use Selenium/Playwright for dynamic content
    - Implement rate limiting and respect robots.txt
    - Handle platform-specific authentication
    - Use proper error handling and retries
    """
    jobs = []
    
    # Mock implementation - returns sample data
    # In production, this would actually scrape from LinkedIn, Indeed, etc.
    sample_jobs = [
        {
            "url": f"https://example.com/jobs/{role.replace(' ', '-').lower()}-{region.replace(' ', '-').lower()}-1",
            "title": f"Senior {role}",
            "company": "TechCorp Inc",
            "location": region,
            "posted_date": datetime.now(),
            "raw_description": f"""
            We are looking for a {role} to join our team in {region}.
            
            Required Skills:
            - Python, FastAPI, PostgreSQL
            - 5+ years of experience
            - Strong problem-solving skills
            
            Responsibilities:
            - Design and build scalable systems
            - Collaborate with cross-functional teams
            - Mentor junior developers
            
            Salary: $120,000 - $160,000
            """
        },
        {
            "url": f"https://example.com/jobs/{role.replace(' ', '-').lower()}-{region.replace(' ', '-').lower()}-2",
            "title": f"{role} - Remote",
            "company": "StartupXYZ",
            "location": "Remote",
            "posted_date": datetime.now(),
            "raw_description": f"""
            Join our fast-growing startup as a {role}!
            
            What we're looking for:
            - Experience with React, Node.js, TypeScript
            - 3+ years in software development
            - Startup mindset
            
            What you'll do:
            - Build features from scratch
            - Own projects end-to-end
            - Work directly with founders
            
            Competitive salary + equity
            """
        }
    ]
    
    jobs.extend(sample_jobs)
    
    # Store in database
    db = SessionLocal()
    try:
        for job_data in jobs:
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if not existing:
                job = Job(**job_data, status="scraped")
                db.add(job)
        db.commit()
    finally:
        db.close()
    
    return jobs


def parse_jd(job_text: str) -> Dict[str, Any]:
    """
    Parses a job description into structured data.
    Extracts skills, seniority level, keywords, etc.
    
    In production, this would use LLM or advanced NLP.
    """
    # Simple keyword extraction
    skills = []
    keywords = []
    
    # Common tech skills
    tech_skills = [
        "Python", "JavaScript", "TypeScript", "React", "Node.js", "FastAPI",
        "PostgreSQL", "MongoDB", "AWS", "Docker", "Kubernetes", "Git",
        "Machine Learning", "AI", "LangChain", "LLM", "RAG"
    ]
    
    for skill in tech_skills:
        if skill.lower() in job_text.lower():
            skills.append(skill)
    
    # Determine seniority
    seniority = "Mid-Level"
    if any(word in job_text.lower() for word in ["senior", "lead", "principal", "staff"]):
        seniority = "Senior"
    elif any(word in job_text.lower() for word in ["junior", "entry", "associate"]):
        seniority = "Junior"
    
    # Extract keywords (simple approach)
    words = re.findall(r'\b[A-Z][a-z]+\b', job_text)
    keywords = list(set(words))[:10]
    
    # Extract years of experience
    experience_match = re.search(r'(\d+)\+?\s*years?', job_text, re.IGNORECASE)
    years_required = int(experience_match.group(1)) if experience_match else None
    
    return {
        "skills": skills,
        "seniority": seniority,
        "keywords": keywords,
        "years_required": years_required,
        "has_remote": "remote" in job_text.lower(),
        "has_equity": "equity" in job_text.lower() or "stock" in job_text.lower()
    }


def detect_scam(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detects potential scam signals in job postings.
    """
    is_scam = False
    reasons = []
    
    description = job_data.get("raw_description", "") or job_data.get("description", "")
    company = job_data.get("company", "")
    
    # Check for suspicious patterns
    scam_indicators = [
        (r"pay.*up.*front", "Requests upfront payment"),
        (r"send.*money", "Asks to send money"),
        (r"bank.*account.*details", "Requests bank details"),
        (r"guaranteed.*income", "Promises guaranteed income"),
        (r"\$\d{6,}", "Unrealistic salary for role")
    ]
    
    for pattern, reason in scam_indicators:
        if re.search(pattern, description, re.IGNORECASE):
            is_scam = True
            reasons.append(reason)
    
    # Check for missing company info
    if not company or len(company) < 3:
        is_scam = True
        reasons.append("Missing or invalid company name")
    
    # Check email domain
    email_match = re.search(r'@([a-zA-Z0-9.-]+)', description)
    if email_match:
        domain = email_match.group(1).lower()
        if domain in ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]:
            reasons.append("Uses personal email domain")
    
    return {
        "is_scam": is_scam,
        "confidence": len(reasons) * 0.25,
        "reasons": reasons if is_scam else None
    }


def deduplicate_job(job_url: str, company: str, title: str) -> bool:
    """
    Checks if a job has already been processed.
    Returns True if duplicate, False if new.
    """
    db = SessionLocal()
    try:
        # Check by URL
        existing = db.query(Job).filter(Job.url == job_url).first()
        if existing:
            return True
        
        # Check by company + title combination
        existing = db.query(Job).filter(
            Job.company == company,
            Job.title == title
        ).first()
        if existing:
            return True
        
        return False
    finally:
        db.close()
