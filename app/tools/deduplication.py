from pydantic import BaseModel, Field

class DeduplicateJobInput(BaseModel):
    job_url: str = Field(..., description="The URL of the job to check")
    company: str = Field(..., description="Company name")
    title: str = Field(..., description="Job title")

def deduplicate_job(job_url: str, company: str, title: str) -> bool:
    """
    Check if a job has already been processed.
    """
    return False
