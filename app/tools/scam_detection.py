from typing import List, Dict, Any
from pydantic import BaseModel, Field

class DetectScamInput(BaseModel):
    job_data: Dict[str, Any] = Field(..., description="Dictionary containing job details")

def detect_scam(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a job posting for scam indicators.
    """
    return {"score": 0, "flags": []}
