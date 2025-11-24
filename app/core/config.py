"""Application configuration using Pydantic Settings."""
import os
from typing import List, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project Info
    PROJECT_NAME: str = "Autonomous AI Job Application Agent"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "1.0.0"
    
    # CORS - comma-separated string in .env, parsed to list
    BACKEND_CORS_ORIGINS: str = ""

    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as a list."""
        if not self.BACKEND_CORS_ORIGINS:
            return []
        if  isinstance(self.BACKEND_CORS_ORIGINS, list):
            return self.BACKEND_CORS_ORIGINS
        # Parse from comma-separated string
        return [origin.strip() for origin in self.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]

    # Database
    DATABASE_URL: str = ""

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v):
        """Fix DATABASE_URL format."""
        if not v:
            return "sqlite:///./career_agent.db"
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # Security
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # LLM APIs
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4-turbo"
    LLM_TEMPERATURE: float = 0.0
    
    # Job Board APIs
    ADZUNA_API_ID: Optional[str] = None
    ADZUNA_API_KEY: Optional[str] = None

    # Email
    SENDGRID_API_KEY: Optional[str] = None
    EMAIL_FROM: str = "noreply@careeragent.com"
    
    # Agent Settings
    DEFAULT_MATCH_THRESHOLD: float = 70.0
    MAX_PROJECTS_TO_ADD: int = 3
    AUTO_APPLY_ENABLED: bool = False
    
    # Scraping Settings
    SCRAPE_INTERVAL_MINUTES: int = 60
    RESPECT_ROBOTS_TXT: bool = True
    USER_AGENT: str = "CareerAgent/1.0 (Job Application Bot)"
    
    # Application Settings
    DEFAULT_PERSONALITY: str = "professional"
    
    # Safety Settings
    SKIP_SCAM_JOBS: bool = True
    SKIP_DUPLICATES: bool = True
    DRY_RUN: bool = True  # Don't actually submit by default

    # Pydantic v2 config
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )


# Create global settings instance
settings = Settings()
