from typing import Dict, Any
from pydantic import BaseModel, Field

class StoreProjectMetadataInput(BaseModel):
    project_data: Dict[str, Any] = Field(..., description="Project metadata to store")

class StoreApplicationStatusInput(BaseModel):
    job_id: int = Field(..., description="ID of the job")
    status: str = Field(..., description="New status")
    metadata: Dict[str, Any] = Field(default={}, description="Additional metadata")

def store_project_metadata(project_data: Dict[str, Any]) -> bool:
    """
    Save project information to the database.
    """
    return True

def store_application_status(job_id: int, status: str, metadata: Dict[str, Any] = {}) -> bool:
    """
    Record application details and status.
    """
    return True
