from typing import Dict, Any
from pydantic import BaseModel, Field

class ParseJDInput(BaseModel):
    job_text: str = Field(..., description="The raw text of the job description")

def parse_jd(job_text: str) -> Dict[str, Any]:
    """
    Parse a job description to extract structured information.
    """
    return {
        "skills": ["Python", "FastAPI"],
        "requirements": [],
        "salary": None
    }
