from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings

Base = declarative_base()

import socket
from urllib.parse import urlparse, urlunparse

# Use SQLite for local dev if DATABASE_URL not set, otherwise Postgres
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./career_agent.db"
else:
    # Fix for Render/Supabase IPv6 issues: Force IPv4 resolution
    try:
        parsed = urlparse(SQLALCHEMY_DATABASE_URL)
        if parsed.hostname and "sqlite" not in parsed.scheme:
            # Resolve hostname to IPv4 address
            ipv4_address = socket.gethostbyname(parsed.hostname)
            # Replace hostname with IPv4 address in the URL
            new_netloc = parsed.netloc.replace(parsed.hostname, ipv4_address)
            parsed = parsed._replace(netloc=new_netloc)
            SQLALCHEMY_DATABASE_URL = urlunparse(parsed)
            print(f"Resolved DB Host {parsed.hostname} to {ipv4_address} to force IPv4")
    except Exception as e:
        print(f"Warning: Failed to resolve DB hostname to IPv4: {e}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
