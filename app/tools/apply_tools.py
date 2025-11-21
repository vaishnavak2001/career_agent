from langchain_core.tools import tool
from typing import Dict, Any
from app.database import SessionLocal
from app.models import Application, JobStatus, Job

@tool
def submit_application(job_url: str, form_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates submitting a job application via browser automation.
    """
    print(f"Navigating to {job_url}...")
    print(f"Filling form with: {form_data.keys()}")
    
    # Mock success
    return {
        "status": "submitted",
        "confirmation_id": "APP-12345",
        "screenshot_url": "https://example.com/screenshot.png"
    }
