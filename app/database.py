"""Unified database configuration and session management."""
import socket
import os
from urllib.parse import urlparse, urlunparse
from typing import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import Pool

# Import settings from core config
try:
    from app.core.config import settings
except ImportError:
    # Fallback for direct imports
    class FallbackSettings:
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./career_agent.db")
    settings = FallbackSettings()

# Create Base for all model definitions
Base = declarative_base()

# Process DATABASE_URL with intelligent defaults
SQLALCHEMY_DATABASE_URL = getattr(settings, 'DATABASE_URL', os.getenv("DATABASE_URL", "sqlite:///./career_agent.db"))

# Ensure we have a valid URL
if not SQLALCHEMY_DATABASE_URL or SQLALCHEMY_DATABASE_URL == "":
    SQLALCHEMY_DATABASE_URL = "sqlite:///./career_agent.db"
    print("[DB] No DATABASE_URL set, using local SQLite")

# Fix postgres:// → postgresql:// (Heroku/Render compatibility)
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print("[DB] Fixed postgres:// -> postgresql://")

# Fix for Render/Supabase IPv6 issues: Force IPv4 resolution
if "sqlite" not in SQLALCHEMY_DATABASE_URL.lower():
    try:
        parsed = urlparse(SQLALCHEMY_DATABASE_URL)
        if parsed.hostname:
            # Resolve hostname to IPv4 address
            ipv4_address = socket.gethostbyname(parsed.hostname)
            new_netloc = parsed.netloc.replace(parsed.hostname, ipv4_address)
            parsed = parsed._replace(netloc=new_netloc)
            SQLALCHEMY_DATABASE_URL = urlunparse(parsed)
            print(f"[DB] Resolved {parsed.hostname} -> {ipv4_address} (IPv4)")
    except Exception as e:
        print(f"[DB] IPv4 resolution failed: {e}. Using original URL.")

# Determine if using SQLite
is_sqlite = "sqlite" in SQLALCHEMY_DATABASE_URL.lower()

# Create engine with appropriate settings
connect_args = {}
if is_sqlite:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Enable connection health checks
    echo=False,  # Set to True for SQL query logging
    pool_size=5 if not is_sqlite else None,  # Connection pool for PostgreSQL
    max_overflow=10 if not is_sqlite else None
)

# Add connection pool listeners for better debugging
@event.listens_for(Pool, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Log successful database connections."""
    print("[DB] Database connection established")

@event.listens_for(Pool, "checkout")
def receive_checkout(dbapi_conn, connection_record, connection_proxy):
    """Ensure connection is alive on checkout."""
    pass  # pool_pre_ping handles this

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Use with FastAPI Depends().
    
    Example:
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """
    Get a database session for use outside of FastAPI.
    Remember to close the session when done!
    
    Example:
        db = get_db_session()
        try:
            items = db.query(Item).all()
        finally:
            db.close()
    """
    return SessionLocal()


def check_db_connection() -> bool:
    """
    Check if database connection is working.
    Returns True if connection successful, False otherwise.
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("[DB] Database connection OK")
        return True
    except Exception as e:
        print(f"[DB] Database connection failed: {e}")
        return False


# Print database info on import
db_display = SQLALCHEMY_DATABASE_URL.split('@')[0] + "@..." if '@' in SQLALCHEMY_DATABASE_URL else "local"
print(f"[DB] Database: {db_display}")
print(f"[DB] Engine: {'SQLite' if is_sqlite else 'PostgreSQL'}")
