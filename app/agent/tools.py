"""
LangChain Tools for Career Agent
Implements all tool-calling functions defined in the system prompt.
"""
from langchain.tools import tool
from typing import List, Dict, Optional, Any
import hashlib
from datetime import datetime
from sqlalchemy import func

# Import services
from app.services.scraper import scraper_service
from app.services.adzuna import adzuna_service
from app.services.scam_detector import scam_detector_service
from app.services.parser import parser_service
from app.services.matcher import matcher_service
from app.services.project_finder import project_finder_service
from app.services.resume_enhancer import resume_enhancer_service
from app.services.cover_letter_generator import cover_letter_service
from app.services.auto_apply import auto_apply_service

# Import DB
from app.db.session import SessionLocal
from app.db.models import Job, Project, Application, ActivityLog


@tool
async def scrape_jobs(role: str, region: str, platforms: List[str], since_timestamp: Optional[str] = None) -> Dict:
    """
    Scrapes job listings from specified platforms (e.g., LinkedIn, Indeed, Adzuna) for a given role and region.
    Returns a summary of jobs found and saved.
    """
    all_jobs = []
    
    # 1. Try Adzuna API first (Fast & Reliable)
    print(f"Searching Adzuna for {role} in {region}...")
    adzuna_jobs = await adzuna_service.search_jobs(role, region)
    if adzuna_jobs:
        print(f"Found {len(adzuna_jobs)} jobs on Adzuna")
        all_jobs.extend(adzuna_jobs)
    
    # 2. Fallback/Supplement with Playwright Scraper if requested or if Adzuna yielded few results
    if "indeed" in platforms or "linkedin" in platforms:
        print(f"Scraping other platforms: {platforms}...")
        scraped_jobs = await scraper_service.scrape_jobs(role, region, platforms)
        all_jobs.extend(scraped_jobs)

    if not all_jobs:
        return {"message": "No jobs found.", "jobs_found": 0}

    # 3. Process and Save Jobs
    db: Session = SessionLocal()
    saved_count = 0
    
    try:
        for job_data in all_jobs:
            # Deduplicate by URL
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if existing:
                continue
                
            # Parse Description (if available)
            parsed_data = {}
            if job_data.get("description"):
                # For API jobs, we might have a shorter description, but still useful to parse
                parsed_data = parser_service.parse_job_description(job_data["description"])
            
            # Calculate Match Score (Basic)
            match_score = matcher_service.compute_match_score(job_data.get("description", ""), ["python", "react", "fastapi"]) # TODO: Get actual user skills
            
            new_job = Job(
                id=f"job_{datetime.now().timestamp()}_{saved_count}", # Simple ID generation
                title=job_data["title"],
                company=job_data["company"],
                location=job_data["location"],
                url=job_data["url"],
                source=job_data["source"],
                raw_text=job_data.get("description"),
                parsed_data=parsed_data,
                match_score=match_score,
                is_scam=False # Default to False for now
            )
            db.add(new_job)
            saved_count += 1
            
        db.commit()
    except Exception as e:
        print(f"Error saving jobs to DB: {e}")
        db.rollback()
    finally:
        db.close()

    return {
        "message": f"Successfully found and processed {saved_count} new jobs.",
        "jobs_found": saved_count,
        "sources": list(set(j["source"] for j in all_jobs))
    }
@tool
def parse_jd(job_text: str) -> Dict:
    """
    Parses raw job description into structured data.
    Extracts skills, responsibilities, salary, requirements, etc.
    
    Args:
        job_text: Raw job description text
        
    Returns:
        Structured dict with required_skills, preferred_skills, salary, etc.
    """
    return parser_service.parse_job_description(job_text)


@tool
def compute_match_score(resume: str, structured_jd: Dict, projects: List[Dict]) -> Dict:
    """
    Computes a comprehensive match score (0-100) using multiple factors.
    
    Args:
        resume: User's resume content
        structured_jd: Parsed job description
        projects: List of user projects
        
    Returns:
        Dict with 'score' (int), 'breakdown' (dict with component scores)
    """
    return matcher_service.compute_score(resume, structured_jd, projects)


@tool
async def search_projects(jd_keywords: List[str]) -> List[Dict]:
    """
    Searches for relevant projects across GitHub, HuggingFace, Kaggle, etc.
    
    Args:
        jd_keywords: Keywords from job description to search for
        
    Returns:
        List of projects with title, description, tech_stack, link, source
    """
    return await project_finder_service.search_projects(jd_keywords)


@tool
def add_projects_to_resume(base_resume: str, selected_projects: List[Dict]) -> Dict:
    """
    Adds selected projects to the resume and returns metadata.
    
    Args:
        base_resume: Original resume content
        selected_projects: Projects to add
        
    Returns:
        Dict with 'new_resume' (str) and 'project_metadata' (list)
    """
    new_resume = resume_enhancer_service.add_projects(base_resume, selected_projects)
    metadata = [
        {
            "title": p.get("title"),
            "tech_stack": p.get("tech_stack"),
            "link": p.get("link"),
            "reason_matched": p.get("reason_matched", "Relevant to JD"),
            "autogenerated": p.get("autogenerated", False),
            "date_added": datetime.now().isoformat()
        }
        for p in selected_projects
    ]
    return {
        "new_resume": new_resume,
        "project_metadata": metadata
    }


@tool
def store_project_metadata(project_record: Dict) -> bool:
    """
    Stores project metadata in the database.
    
    Args:
        project_record: Project data to store
        
    Returns:
        True if successful
    """
    db = SessionLocal()
    try:
        # Create new project record
        # Ensure tech_stack is handled correctly (it's JSON now)
        project = Project(
            title=project_record.get("title"),
            description=project_record.get("description"),
            tech_stack=project_record.get("tech_stack"),
            link=project_record.get("link"),
            is_autogenerated=project_record.get("autogenerated", False),
            metadata_json=project_record,
            user_id=project_record.get("user_id") # Assuming user_id is passed or we handle it
        )
        db.add(project)
        db.commit()
        return True
    except Exception as e:
        print(f"Error storing project: {e}")
        db.rollback()

@tool
def generate_cover_letter(job_data: Dict, tailored_resume: str, personality: str) -> str:
    """
    Generates a personalized cover letter.
    
    Args:
        job_data: Job details (title, company, description)
        tailored_resume: The tailored resume
        personality: professional, friendly, technical, direct, creative, relocation_friendly
        
    Returns:
        Generated cover letter text
    """
    return cover_letter_service.generate(job_data, tailored_resume, personality)


@tool
async def submit_application(job_url: str, form_data: Dict, files: Dict) -> Dict:
    """
    Submits job application using browser automation.
    
    Args:
        job_url: URL of job application page
        form_data: Form fields to fill
        files: Files to attach (resume, cover_letter)
        
    Returns:
        Dict with 'status', 'confirmation', 'screenshot' (optional)
    """
    return await auto_apply_service.submit_application(job_url, form_data, files)


@tool
def store_application_status(job_id: str, status: str, metadata: Dict) -> bool:
    """
    Logs application status to database.
    
    Args:
        job_id: Job ID
        status: Application status
        metadata: Additional metadata
        
    Returns:
        True if successful
    """
    db = SessionLocal()
    try:
        # Check if application exists
        application = db.query(Application).filter(Application.job_id == job_id).first()
        
        if application:
            application.status = status
            application.response_data = metadata
        else:
            # Create new application record
            # We might need user_id and resume_id here, assuming they are in metadata or context
            application = Application(
                job_id=job_id,
                status=status,
                response_data=metadata,
                user_id=metadata.get("user_id"),
                resume_id=metadata.get("resume_id")
            )
            db.add(application)
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error storing application status: {e}")
        db.rollback()
        return False
    finally:
        db.close()


@tool
def dashboard_metrics() -> Dict:
    """
    Returns aggregated analytics metrics for the dashboard.
    
    Returns:
        Dict with total_scraped, matched, applied, etc.
    """
    db = SessionLocal()
    try:
        total_scraped = db.query(Job).count()
        total_applied = db.query(Application).count()
        scams_detected = db.query(Job).filter(Job.is_scam == True).count()
        
        # Calculate average match score
        avg_score = db.query(func.avg(Job.match_score)).scalar() or 0
        
        return {
            "total_scraped": total_scraped,
            "total_matched": total_scraped, # Simplified for now
            "total_applied": total_applied,
            "scams_detected": scams_detected,
            "duplicates_avoided": 0, # Hard to track without a separate log
            "avg_match_score": int(avg_score)
        }
    except Exception as e:
        print(f"Error fetching metrics: {e}")
        return {
            "total_scraped": 0,
            "total_matched": 0,
            "total_applied": 0,
            "scams_detected": 0,
            "duplicates_avoided": 0,
            "avg_match_score": 0
        }
    finally:
        db.close()


# Define the complete list of tools
tools = [
    scrape_jobs,
    deduplicate_job,
    detect_scam,
    parse_jd,
    compute_match_score,
    search_projects,
    add_projects_to_resume,
    store_project_metadata,
    rewrite_resume_to_match_jd,
    generate_cover_letter,
    submit_application,
    store_application_status,
    dashboard_metrics
]
