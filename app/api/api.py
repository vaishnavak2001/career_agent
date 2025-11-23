from app.api.endpoints import jobs, resumes, applications, dashboard, projects

api_router = APIRouter()

api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
# Alias for analytics to match test_api.py expectation if needed, or update test_api.py
api_router.include_router(dashboard.router, prefix="/analytics", tags=["analytics"])
