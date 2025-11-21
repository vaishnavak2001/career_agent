"""Configuration settings for the Career Agent."""
import os
from typing import Optional


class Settings:
    """Application settings and configuration."""
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./career_agent.db")
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4-turbo")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0"))
    
    # Agent Settings
    DEFAULT_MATCH_THRESHOLD: float = 70.0  # Minimum match score to proceed with application
    MAX_PROJECTS_TO_ADD: int = 3
    AUTO_APPLY_ENABLED: bool = os.getenv("AUTO_APPLY_ENABLED", "false").lower() == "true"
    
    # Scraping Settings
    SCRAPE_INTERVAL_MINUTES: int = int(os.getenv("SCRAPE_INTERVAL_MINUTES", "60"))
    RESPECT_ROBOTS_TXT: bool = True
    USER_AGENT: str = "CareerAgent/1.0 (Job Application Bot)"
    
    # Application Settings
    DEFAULT_PERSONALITY: str = os.getenv("DEFAULT_PERSONALITY", "professional")
    
    # Safety Settings
    SKIP_SCAM_JOBS: bool = True
    SKIP_DUPLICATES: bool = True
    DRY_RUN: bool = os.getenv("DRY_RUN", "true").lower() == "true"  # Don't actually submit by default
    

settings = Settings()
