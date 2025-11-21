"""Enhanced database configuration with PostgreSQL support."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Get database URL from environment or use SQLite as fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./career_agent.db"
)

# Determine if using PostgreSQL
is_postgres = DATABASE_URL.startswith("postgresql")

# Create engine with appropriate configuration
if is_postgres:
    # PostgreSQL configuration
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=10,  # Connection pool size
        max_overflow=20,  # Max overflow connections
        echo=False  # Set to True for SQL debugging
    )
else:
    # SQLite configuration
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool  # Use static pool for SQLite
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_type():
    """Return the current database type."""
    return "PostgreSQL" if is_postgres else "SQLite"


def init_db():
    """Initialize the database with tables."""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized: {get_db_type()}")
