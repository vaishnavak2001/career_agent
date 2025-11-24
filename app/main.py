from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print("[STARTUP] Starting Career Agent API...")
    
    # Start background scheduler
    from app.scheduler import start_scheduler
    start_scheduler()
    print("[STARTUP] Background scheduler started")
    
    yield  # Application runs
    
    # Shutdown
    print("[SHUTDOWN] Stopping Career Agent API...")
    from app.scheduler import stop_scheduler
    stop_scheduler()
    print("[SHUTDOWN] Background scheduler stopped")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
cors_origins = settings.get_cors_origins()
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
@app.head("/")
def root():
    return {"message": "Welcome to the Autonomous AI Job Application Agent API"}

@app.get("/health")
@app.head("/health")
def health_check():
    """Health check endpoint for monitoring services."""
    return {"status": "healthy", "service": "Career Agent API"}

@app.get("/scheduler/status")
def scheduler_status():
    """Get scheduler status."""
    from app.scheduler import get_scheduler_status
    return get_scheduler_status()
