from typing import Dict, Any
from pydantic import BaseModel, Field

class RewriteResumeInput(BaseModel):
    resume: str = Field(..., description="Current resume content")
    jd_data: Dict[str, Any] = Field(..., description="Job description data to target")

def rewrite_resume_to_match_jd(resume: str, jd_data: Dict[str, Any]) -> str:
    """
    Tailor a resume to match a specific job description.
    """
    return resume
