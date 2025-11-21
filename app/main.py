from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base, Job, Application, Project
from app.agent import get_agent_executor
from app.tools.analytics_tools import (
    dashboard_metrics, 
    get_match_score_distribution,
    get_application_timeline
)
from app.tools.job_tools import scrape_jobs, parse_jd, detect_scam
from app.tools.resume_tools import compute_match_score, search_projects
from app.tools.application_tools import generate_cover_letter
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import logging
from contextlib import asynccontextmanager

# Import scheduler and notifications
from app.scheduler import job_monitor, start_scheduler, stop_scheduler
from app.notifications import notification_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)


# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events."""
    # Startup
    logger.info("Starting Career Agent API...")
    start_scheduler()
    logger.info(f"Database: {SessionLocal().bind.engine.url}")
    yield
    # Shutdown
    logger.info("Shutting down Career Agent API...")
    stop_scheduler()


app = FastAPI(
    title="Autonomous Career Agent",
    description="AI-powered job application automation with resume tailoring and scam detection",
    version="2.0.0",
    lifespan=lifespan
)

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Request/Response Models ---

class AgentRequest(BaseModel):
    instruction: str

class JobScrapeRequest(BaseModel):
    region: str
    role: str
    platforms: List[str]

class MatchScoreRequest(BaseModel):
    resume_text: str
    job_id: int

class CoverLetterRequest(BaseModel):
    job_id: int
    resume_text: str
    personality: str = "professional"

class MonitorConfigRequest(BaseModel):
    region: str
    role: str
    platforms: List[str]
    interval_minutes: int = 60

class NotificationTestRequest(BaseModel):
    email: Optional[str] = None



# --- Agent Endpoints ---

@app.get("/", response_class=FileResponse)
def home():
    """Serve the main HTML page."""
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/api")
def api_info():
    """API information endpoint."""
    return {
        "name": "Autonomous Career Agent API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "agent": "/agent/run",
            "dashboard": "/dashboard/stats",
            "jobs": "/jobs",
            "analytics": "/analytics/*"
        }
    }

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
    """
    Trigger the LangChain agent with a specific instruction.
    Example: "Scrape Python jobs in New York and apply to high-match positions."
    """
    try:
        executor = get_agent_executor()
        result = executor.invoke({"input": request.instruction})
        return {"status": "success", "output": result["output"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Job Management Endpoints ---

@app.post("/jobs/scrape")
async def scrape_jobs_endpoint(request: JobScrapeRequest, db: Session = Depends(get_db)):
    """Manually trigger job scraping for specific criteria."""
    try:
        jobs = scrape_jobs(request.region, request.role, request.platforms)
        return {
            "status": "success",
            "jobs_found": len(jobs),
            "jobs": jobs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/jobs")
def list_jobs(
    skip: int = 0, 
    limit: int = 100,
    min_match_score: Optional[float] = None,
    exclude_scams: bool = True,
    db: Session = Depends(get_db)
):
    """List all jobs with optional filtering."""
    query = db.query(Job)
    
    if exclude_scams:
        query = query.filter(Job.is_scam == False)
    
    if min_match_score is not None:
        query = query.filter(Job.match_score >= min_match_score)
    
    jobs = query.offset(skip).limit(limit).all()
    
    return {
        "count": len(jobs),
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "url": job.url,
                "match_score": job.match_score,
                "status": job.status,
                "is_scam": job.is_scam,
                "scraped_at": job.scraped_at.isoformat() if job.scraped_at else None
            }
            for job in jobs
        ]
    }

@app.get("/jobs/{job_id}")
def get_job_details(job_id: int, db: Session = Depends(get_db)):
    """Get detailed information about a specific job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "url": job.url,
        "posted_date": job.posted_date.isoformat() if job.posted_date else None,
        "scraped_at": job.scraped_at.isoformat() if job.scraped_at else None,
        "raw_description": job.raw_description,
        "parsed_data": job.parsed_data,
        "match_score": job.match_score,
        "match_details": job.match_details,
        "is_scam": job.is_scam,
        "scam_reason": job.scam_reason,
        "status": job.status
    }

@app.post("/jobs/{job_id}/analyze")
def analyze_job(job_id: int, db: Session = Depends(get_db)):
    """Parse and analyze a specific job."""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Parse JD
    parsed = parse_jd(job.raw_description)
    job.parsed_data = parsed
    
    # Detect scam
    scam_result = detect_scam({
        "raw_description": job.raw_description,
        "company": job.company
    })
    job.is_scam = scam_result["is_scam"]
    job.scam_reason = ", ".join(scam_result["reasons"]) if scam_result.get("reasons") else None
    
    db.commit()
    db.refresh(job)
    
    return {
        "job_id": job.id,
        "parsed_data": parsed,
        "scam_detection": scam_result
    }

# --- Resume & Matching Endpoints ---

@app.post("/match-score")
def calculate_match_score(request: MatchScoreRequest, db: Session = Depends(get_db)):
    """Calculate match score between resume and a job."""
    job = db.query(Job).filter(Job.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if not job.parsed_data:
        # Parse JD first
        job.parsed_data = parse_jd(job.raw_description)
        db.commit()
    
    score = compute_match_score(request.resume_text, job.parsed_data)
    
    # Update job with score
    job.match_score = score
    db.commit()
    
    return {
        "job_id": job.id,
        "match_score": score,
        "job_title": job.title,
        "company": job.company
    }

@app.post("/projects/search")
def search_projects_endpoint(keywords: List[str], limit: int = 3):
    """Search for relevant projects based on keywords."""
    projects = search_projects(keywords, limit)
    return {
        "keywords": keywords,
        "projects_found": len(projects),
        "projects": projects
    }

@app.get("/projects")
def list_projects(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """List all saved projects."""
    projects = db.query(Project).offset(skip).limit(limit).all()
    return {
        "count": len(projects),
        "projects": [
            {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "url": p.url,
                "source": p.source,
                "keywords": p.keywords,
                "added_at": p.added_at.isoformat() if p.added_at else None
            }
            for p in projects
        ]
    }

# --- Cover Letter Endpoints ---

@app.post("/cover-letter/generate")
def generate_cover_letter_endpoint(request: CoverLetterRequest, db: Session = Depends(get_db)):
    """Generate a cover letter for a specific job."""
    job = db.query(Job).filter(Job.id == request.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job_data = {
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "parsed_data": job.parsed_data or {}
    }
    
    cover_letter = generate_cover_letter(job_data, request.resume_text, request.personality)
    
    return {
        "job_id": job.id,
        "personality": request.personality,
        "cover_letter": cover_letter
    }

# --- Analytics & Dashboard Endpoints ---

@app.get("/dashboard/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Get comprehensive dashboard statistics."""
    try:
        metrics = dashboard_metrics()
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/match-distribution")
def get_match_distribution():
    """Get distribution of match scores across all jobs."""
    try:
        distribution = get_match_score_distribution()
        return {"distribution": distribution}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/timeline")
def get_timeline():
    """Get application timeline showing submission history."""
    try:
        timeline = get_application_timeline()
        return {"timeline": timeline}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/applications")
def list_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all submitted applications."""
    applications = db.query(Application).offset(skip).limit(limit).all()
    
    result = []
    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else None,
            "company": job.company if job else None,
            "status": app.status,
            "personality_used": app.personality_used,
            "submitted_at": app.submitted_at.isoformat() if app.submitted_at else None
        })
    
    return {
        "count": len(result),
        "applications": result
    }


# --- Monitoring & Scheduler Endpoints ---

@app.post("/monitor/configure")
def configure_monitoring(request: MonitorConfigRequest):
    """Configure continuous job monitoring parameters."""
    job_monitor.configure(
        region=request.region,
        role=request.role,
        platforms=request.platforms,
        interval_minutes=request.interval_minutes
    )
    return {
        "status": "configured",
        "config": job_monitor.config
    }

@app.post("/monitor/start")
def start_monitoring():
    """Start continuous job monitoring."""
    job_monitor.start()
    return {
        "status": "started",
        "message": f"Monitoring activated. Jobs will be scraped every {job_monitor.config['interval_minutes']} minutes"
    }

@app.post("/monitor/stop")
def stop_monitoring():
    """Stop continuous job monitoring."""
    job_monitor.stop()
    return {
        "status": "stopped",
        "message": "Monitoring deactivated"
    }

@app.get("/monitor/status")
def get_monitoring_status():
    """Get current monitoring status."""
    return job_monitor.get_status()


# --- Notification Endpoints ---

@app.post("/notifications/test")
def test_notification(request: NotificationTestRequest):
    """Send a test notification email."""
    test_job = {
        "title": "Test Job - Senior Software Engineer",
        "company": "Test Company Inc.",
        "location": "Remote",
        "match_score": 95,
        "url": "http://127.0.0.1:8000",
        "raw_description": "This is a test job notification to verify email configuration.",
        "parsed_data": {
            "skills": ["Python", "FastAPI", "PostgreSQL"],
            "seniority": "Senior"
        }
    }
    
    success = notification_service.notify_high_match_job(test_job)
    
    return {
        "success": success,
        "message": "Test email sent" if success else "Email not configured. Check NOTIFICATIONS_ENABLED and SMTP settings in environment."
    }

@app.get("/notifications/config")
def get_notification_config():
    """Get current notification configuration."""
    return {
        "enabled": notification_service.enabled,
        "smtp_configured": bool(notification_service.sender_email and notification_service.sender_password),
        "recipient": notification_service.recipient_email if notification_service.enabled else "Not configured"
    }
