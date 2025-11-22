from typing import Dict, Any
from pydantic import BaseModel, Field

class GenerateCoverLetterInput(BaseModel):
    job_data: Dict[str, Any] = Field(..., description="Job details")
    resume: str = Field(..., description="Resume content")
    personality: str = Field(default="professional", description="Tone of the cover letter")

def generate_cover_letter(job_data: Dict[str, Any], resume: str, personality: str = "professional") -> str:
    """
    Generate a personalized cover letter.
    """
    return "Dear Hiring Manager, ..."
