from typing import Optional
from pydantic import BaseModel, Field

class SubmitApplicationInput(BaseModel):
    url: str = Field(..., description="Job application URL")
    resume_content: str = Field(..., description="Content of the resume to submit")
    cover_letter: Optional[str] = Field(None, description="Cover letter content")

def submit_application(url: str, resume_content: str, cover_letter: Optional[str] = None) -> Dict[str, Any]:
    """
    Automated application submission.
    """
    return {"status": "submitted", "confirmation": "12345"}
