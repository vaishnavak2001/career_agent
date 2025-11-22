from typing import Dict, Any
from pydantic import BaseModel, Field

class ComputeMatchScoreInput(BaseModel):
    resume_text: str = Field(..., description="The content of the candidate's resume")
    jd_data: Dict[str, Any] = Field(..., description="Structured job description data")

def compute_match_score(resume_text: str, jd_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate how well a resume matches a job description.
    """
    return {
        "score": 85,
        "breakdown": {
            "skills": 90,
            "experience": 80
        }
    }
