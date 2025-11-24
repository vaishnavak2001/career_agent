from fastapi import APIRouter
from app.api.endpoints import jobs, resumes, applications, dashboard, projects, auth, interview

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(interview.router, prefix="/interview", tags=["interview"])

# Alias for analytics
api_router.include_router(dashboard.router, prefix="/analytics", tags=["analytics"])
