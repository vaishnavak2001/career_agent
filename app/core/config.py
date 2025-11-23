import os
from typing import List, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Autonomous AI Job Application Agent"
    API_V1_STR: str = "/api/v1"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/career_agent")

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # External APIs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Job Board APIs
    ADZUNA_API_ID: Optional[str] = os.getenv("ADZUNA_API_ID")
    ADZUNA_API_KEY: Optional[str] = os.getenv("ADZUNA_API_KEY")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
