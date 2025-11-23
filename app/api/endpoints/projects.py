from typing import List
from fastapi import APIRouter, Depends
from app.services.project_finder import project_finder_service

router = APIRouter()

@router.post("/search")
async def search_projects(keywords: List[str]):
    """
    Search for relevant projects.
    """
    projects = await project_finder_service.search_projects(keywords)
    return {"projects_found": len(projects), "projects": projects}
