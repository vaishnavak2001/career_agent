"""Seed test data for Phase 2 testing."""
from app.database import get_db_session
from app.models import User, Job, Resume, Project, Application
from datetime import datetime, timedelta
import random

def seed_test_data():
    """Create test data for all main entities."""
    db = get_db_session()
    
    try:
        print("\n[SEED] Starting data seeding...")
        
        # 1. Create test user
        print("\n[SEED] Creating test user...")
        user = db.query(User).filter(User.email == "test@careeragent.com").first()
        if not user:
            user = User(
                email="test@careeragent.com",
                hashed_password="$2b$12$test_hash",
                full_name="Test User",
                settings={"theme": "dark", "notifications": True}
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"[SUCCESS] Created user: {user.email} (ID: {user.id})")
        else:
            print(f"[INFO] User already exists: {user.email} (ID: {user.id})")
        
        # 2. Create test resume
        print("\n[SEED] Creating test resume...")
        resume = db.query(Resume).filter(Resume.user_id == user.id, Resume.is_base == True).first()
        if not resume:
            resume = Resume(
                user_id=user.id,
                version_name="Base Resume",
                content="""
# John Doe
## Senior Software Engineer

### Skills
- Python, FastAPI, React, PostgreSQL
- LangChain, AI/ML, DevOps
- 5+ years experience

### Education  
- MS Computer Science
- BS Software Engineering

### Projects
- AI Job Application Agent
- E-commerce Platform
- Real-time Chat Application
                """,
                is_base=True
            )
            db.add(resume)
            db.commit()
            db.refresh(resume)
            print(f"[SUCCESS] Created resume: {resume.version_name} (ID: {resume.id})")
        else:
            print(f"[INFO] Resume already exists: ID {resume.id}")
        
        # 3. Create test jobs
        print("\n[SEED] Creating test jobs...")
        job_templates = [
            {
                "title": "Senior Python Developer",
                "company": "Tech Corp",
                "location": "Remote",
                "source": "indeed",
                "url": "https://indeed.com/job/1",
                "raw_text": "We are seeking a Senior Python Developer with FastAPI experience...",
                "parsed_json": {
                    "required_skills": ["Python", "FastAPI", "PostgreSQL"],
                    "preferred_skills": ["React", "Docker"],
                    "salary_min": 100000,
                    "salary_max": 150000,
                    "experience_min_years": 5
                },
                "match_score": 85.5,
                "is_scam": False
            },
            {
                "title": "Full Stack Engineer",
                "company": "StartupXYZ",
                "location": "San Francisco, CA",
                "source": "linkedin",
                "url": "https://linkedin.com/job/2",
                "raw_text": "Join our growing team as a Full Stack Engineer...",
                "parsed_json": {
                    "required_skills": ["React", "Node.js", "MongoDB"],
                    "preferred_skills": ["Python", "AWS"],
                    "salary_min": 90000,
                    "salary_max": 130000
                },
                "match_score": 72.0,
                "is_scam": False
            },
            {
                "title": "AI Engineer",
                "company": "AI Innovations",
                "location": "Remote",
                "source": "glassdoor",
                "url": "https://glassdoor.com/job/3",
                "raw_text": "Looking for AI Engineer to work on LLM applications...",
                "parsed_json": {
                    "required_skills": ["Python", "LangChain", "OpenAI"],
                    "preferred_skills": ["FastAPI", "Docker"],
                    "salary_min": 120000,
                    "salary_max": 180000,
                    "experience_min_years": 3
                },
                "match_score": 92.0,
                "is_scam": False
            },
            {
                "title": "Work From Home - Data Entry",
                "company": "Unknown Ltd",
                "location": "Remote",
                "source": "craigslist",
                "url": "https://craigslist.org/job/scam",
                "raw_text": "Make $5000/week from home! No experience needed!",
                "parsed_json": {},
                "match_score": 5.0,
                "is_scam": True,
                "scam_reason": "Unrealistic salary, suspicious source"
            }
        ]
        
        jobs_created = 0
        for job_data in job_templates:
            existing = db.query(Job).filter(Job.url == job_data["url"]).first()
            if not existing:
                job = Job(
                    title=job_data["title"],
                    company=job_data["company"],
                    location=job_data["location"],
                    source=job_data["source"],
                    url=job_data["url"],
                    raw_text=job_data["raw_text"],
                    parsed_json=job_data["parsed_json"],
                    match_score=job_data["match_score"],
                    is_scam=job_data.get("is_scam", False),
                    scam_reason=job_data.get("scam_reason"),
                    posted_date=datetime.utcnow() - timedelta(days=random.randint(1, 7))
                )
                db.add(job)
                jobs_created += 1
        
        db.commit()
        print(f"[SUCCESS] Created {jobs_created} new jobs")
        
        # 4. Create test projects
        print("\n[SEED] Creating test projects...")
        project_templates = [
            {
                "title": "AI Job Application Agent",
                "description": "Full-stack AI-powered career agent",
                "tech_stack": ["Python", "FastAPI", "React", "PostgreSQL", "LangChain"],
                "link": "https://github.com/user/career-agent",
                "is_autogenerated": False
            },
            {
                "title": "E-commerce Platform",
                "description": "Scalable online shopping platform",
                "tech_stack": ["Node.js", "React", "MongoDB", "AWS"],
                "link": "https://github.com/user/ecommerce",
                "is_autogenerated": False
            }
        ]
        
        projects_created = 0
        for proj_data in project_templates:
            existing = db.query(Project).filter(
                Project.user_id == user.id,
                Project.title == proj_data["title"]
            ).first()
            
            if not existing:
                project = Project(
                    user_id=user.id,
                    title=proj_data["title"],
                    description=proj_data["description"],
                    tech_stack=proj_data["tech_stack"],
                    link=proj_data["link"],
                    is_autogenerated=proj_data["is_autogenerated"]
                )
                db.add(project)
                projects_created += 1
        
        db.commit()
        print(f"[SUCCESS] Created {projects_created} new projects")
        
        # 5. Create test application
        print("\n[SEED] Creating test application...")
        jobs = db.query(Job).filter(Job.is_scam == False).limit(1).all()
        if jobs and resume:
            job = jobs[0]
            existing_app = db.query(Application).filter(
                Application.user_id == user.id,
                Application.job_id == job.id
            ).first()
            
            if not existing_app:
                application = Application(
                    user_id=user.id,
                    job_id=job.id,
                    resume_id=resume.id,
                    status="submitted",
                    applied_at=datetime.utcnow() - timedelta(days=2)
                )
                db.add(application)
                db.commit()
                print(f"[SUCCESS] Created application for job: {job.title}")
            else:
                print(f"[INFO] Application already exists for this job")
        
        # Summary
        print("\n" + "="*60)
        print("[SUMMARY] Data seeding complete!")
        print("="*60)
        print(f"Total Users: {db.query(User).count()}")
        print(f"Total Resumes: {db.query(Resume).count()}")
        print(f"Total Jobs: {db.query(Job).count()}")
        print(f"  - Non-scam: {db.query(Job).filter(Job.is_scam == False).count()}")
        print(f"  - Scams: {db.query(Job).filter(Job.is_scam == True).count()}")
        print(f"Total Projects: {db.query(Project).count()}")
        print(f"Total Applications: {db.query(Application).count()}")
        print("="*60)
        
    except Exception as e:
        print(f"\n[ERROR] Seeding failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("="*60)
    print("TEST DATA SEEDING UTILITY")
    print("="*60)
    print("\nThis will create sample data for testing.")
    print("\n" + "="*60)
    
    seed_test_data()
    print("\n[SUCCESS] Ready for testing!")
