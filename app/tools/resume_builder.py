from typing import List, Dict, Any
from pydantic import BaseModel, Field

class AddProjectsToResumeInput(BaseModel):
    base_resume: str = Field(..., description="Original resume content")
    projects: List[Dict[str, Any]] = Field(..., description="List of projects to add")

def add_projects_to_resume(base_resume: str, projects: List[Dict[str, Any]]) -> str:
    """
    Add selected projects to a resume.
    """
    return base_resume + "\n\nProjects:\n" + str(projects)
