from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class JobStatus(enum.Enum):
    SCRAPED = "scraped"
    POTENTIAL_SCAM = "potential_scam"
    PARSED = "parsed"
    MATCHED = "matched"
    IGNORED = "ignored" # Low match score
    APPLYING = "applying"
    APPLIED = "applied"
    FAILED = "failed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    posted_date = Column(DateTime)
    scraped_at = Column(DateTime, default=datetime.utcnow)
    
    # Content
    raw_description = Column(Text)
    parsed_data = Column(JSON) # Structured JD: skills, seniority, etc.
    
    # Analysis
    is_scam = Column(Boolean, default=False)
    scam_reason = Column(String, nullable=True)
    match_score = Column(Float, default=0.0)
    match_details = Column(JSON) # Breakdown of score
    
    status = Column(String, default=JobStatus.SCRAPED.value)
    
    application = relationship("Application", back_populates="job", uselist=False)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    url = Column(String)
    source = Column(String) # GitHub, Kaggle, etc.
    keywords = Column(JSON) # List of tags/skills
    added_at = Column(DateTime, default=datetime.utcnow)

class ResumeVersion(Base):
    __tablename__ = "resume_versions"

    id = Column(Integer, primary_key=True, index=True)
    base_resume_id = Column(Integer, nullable=True) # If versioned from a master
    content = Column(Text, nullable=False) # Markdown or JSON representation
    created_at = Column(DateTime, default=datetime.utcnow)
    
    applications = relationship("Application", back_populates="resume_version")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    resume_version_id = Column(Integer, ForeignKey("resume_versions.id"))
    
    cover_letter_text = Column(Text)
    personality_used = Column(String)
    
    status = Column(String) # Submitted, Interview, Rejected, Offer
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    job = relationship("Job", back_populates="application")
    resume_version = relationship("ResumeVersion", back_populates="applications")

# Analytics can be derived from aggregations on the above tables, 
# but we can store daily snapshots if needed.
class DailyMetric(Base):
    __tablename__ = "daily_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    jobs_scraped = Column(Integer, default=0)
    jobs_matched = Column(Integer, default=0)
    jobs_applied = Column(Integer, default=0)
    scams_flagged = Column(Integer, default=0)
