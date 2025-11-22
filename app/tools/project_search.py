from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SearchProjectsInput(BaseModel):
    keywords: List[str] = Field(..., description="Keywords to search for")
    limit: int = Field(default=3, description="Max number of projects to return")

def search_projects(keywords: List[str], limit: int = 3) -> List[Dict[str, Any]]:
    """
    Search for relevant projects.
    """
    return []
