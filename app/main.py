from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.database import engine, Base, get_db
from app.models import Job, Application, DailyMetric
from app.agent import get_agent_executor
from app.tools.job_tools import scrape_jobs

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Career Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Career Agent API"}

@app.get("/jobs")
def list_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs

@app.post("/agent/run")
async def run_agent(input_data: Dict[str, str]):
    """
    Trigger the autonomous agent with a high-level goal.
    Example: {"input": "Find Python jobs in NY and apply to the best one"}
    """
    executor = get_agent_executor()
    result = await executor.ainvoke({"input": input_data["input"]})
    return result

@app.post("/jobs/scrape")
def trigger_scrape(region: str, role: str, background_tasks: BackgroundTasks):
    """
    Manually trigger a scrape job (runs in background or immediately via tool).
    """
    # For simplicity, calling the tool function directly here, 
    # but in production this should be an async task.
    jobs = scrape_jobs.invoke({"region": region, "role": role})
    return {"message": f"Scraped {len(jobs)} jobs", "jobs": jobs}

@app.get("/dashboard/stats")
def get_stats(db: Session = Depends(get_db)):
    total_jobs = db.query(Job).count()
    total_apps = db.query(Application).count()
    return {
        "jobs_scraped": total_jobs,
        "applications_sent": total_apps,
        "interviews": 0,
        "scams_blocked": 0
    }
