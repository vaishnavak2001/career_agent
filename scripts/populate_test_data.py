"""
Script to populate the database with test data for testing the Career Agent API.
This creates sample jobs, resumes, and applications.
"""
import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db import models
from datetime import datetime, timedelta
import random


def create_test_user(db: Session):
    """Create a test user for owning test data."""
    print("Creating test user...")
    
    # Check if test user already exists
    test_user = db.query(models.User).filter(models.User.email == "test@example.com").first()
    
    if test_user:
        print("✅ Test user already exists")
        return test_user
    
    # Simple password hash - using a short password to avoid bcrypt issues
    test_user = models.User(
        email="test@example.com",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0L HDk1.VG0k/8xPQDy0v.0uY.A2kCZ4Q4L2", # "test123"  
        full_name="Test User",
        settings={"theme": "dark", "notifications": True}
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)
    
    print(f"✅ Created test user with email: test@example.com")
    return test_user


def create_test_jobs(db: Session, count: int = 10):
    """Create test job listings."""
    print(f"Creating {count} test jobs...")
    
    companies = [
        "TechCorp", "DataSystems Inc", "AI Innovations", "CloudScale",
        "DevOps Pro", "CyberSecure", "QuantumSoft", "NeuralNet Labs"
    ]
    
    job_titles = [
        "Senior Software Engineer",
        "Data Scientist",
        "Machine Learning Engineer",
        "Full Stack Developer",
        "DevOps Engineer",
        "Backend Developer",
        "Frontend Developer",
        "AI Research Scientist"
    ]
    
    locations = [
        "San Francisco, CA",
        "New York, NY",
        "Seattle, WA",
        "Austin, TX",
        "Boston, MA",
        "Remote",
        "Chicago, IL"
    ]
    
    jobs_created = []
    
    for i in range(count):
        # Create parsed_data matching expected schema
        parsed_data = {
            "requirements": random.choice([
                ["Python", "Django", "PostgreSQL", "Docker"],
                ["Python", "TensorFlow", "PyTorch", "Machine Learning"],
                ["React", "Node.js", "TypeScript", "MongoDB"],
                ["AWS", "Kubernetes", "CI/CD", "Terraform"],
                ["Java", "Spring Boot", "Microservices", "Redis"],
                ["Python", "FastAPI", "SQL", "Git"],
                ["JavaScript", "Vue.js", "CSS", "REST APIs"]
            ]),
            "salary_range": f"${random.randint(80, 200)}k - ${random.randint(120, 250)}k",
            "job_type": random.choice(["Full-time", "Contract", "Part-time"])
        }
        
        job = models.Job(
            source="test_data",
            external_id=f"TEST-{i:04d}",
            url=f"https://example.com/jobs/{i}",
            title=random.choice(job_titles),
            company=random.choice(companies),
            location=random.choice(locations),
            posted_date=datetime.utcnow() - timedelta(days=random.randint(0, 30)),
            raw_text=f"We are looking for a talented professional to join our team. "
                     f"This role involves working on cutting-edge technology and collaborating "
                     f"with a diverse team of engineers.",
            parsed_data=parsed_data,
            match_score=random.randint(50, 95),
            is_scam=False,
            scraped_at=datetime.utcnow() - timedelta(days=random.randint(0, 30))
        )
        db.add(job)
        jobs_created.append(job)
    
    db.commit()
    print(f"✅ Created {count} test jobs")
    return jobs_created


def create_test_resumes(db: Session, user, count: int = 3):
    """Create test resumes."""
    print(f"Creating {count} test resumes...")
    
    resume_templates = [
        {
            "version_name": "Base Resume - Software Engineer",
            "content": "Professional software engineer with 5+ years of experience in Python, JavaScript, and cloud technologies...",
            "is_base": True
        },
        {
            "version_name": "Data Science Focused",
            "content": "Data scientist specializing in machine learning, statistical analysis, and big data technologies...",
            "is_base": False
        },
        {
            "version_name": "Full Stack Developer",
            "content": "Full-stack developer proficient in modern web technologies, API design, and database management...",
            "is_base": False
        }
    ]
    
    resumes_created = []
    
    for i in range(min(count, len(resume_templates))):
        template = resume_templates[i]
        resume = models.Resume(
            user_id=user.id,
            version_name=template["version_name"],
            content=template["content"],
            is_base=template["is_base"],
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
        )
        db.add(resume)
        resumes_created.append(resume)
    
    db.commit()
    print(f"✅ Created {count} test resumes")
    return resumes_created


def create_test_applications(db: Session, user, jobs, resumes, count: int = 15):
    """Create test job applications."""
    print(f"Creating {count} test applications...")
    
    statuses = ["pending", "submitted", "in_review", "interview_scheduled", "rejected", "offer_received"]
    
    applications_created = []
    
    for i in range(count):
        if not jobs or not resumes:
            print("No jobs or resumes available to create applications")
            break
            
        application = models.Application(
            user_id=user.id,
            job_id=random.choice(jobs).id,
            resume_id=random.choice(resumes).id,
            status=random.choice(statuses),
            cover_letter_content=f"Dear Hiring Manager,\n\nI am excited to apply for this position...\n\nBest regards,\n{user.full_name}",
            response_data={"submitted": True, "confirmation_id": f"CONF-{i:05d}"},
            applied_at=datetime.utcnow() - timedelta(days=random.randint(0, 45))
        )
        db.add(application)
        applications_created.append(application)
    
    db.commit()
    print(f"✅ Created {count} test applications")
    return applications_created


def create_test_projects(db: Session, user, jobs, count: int = 5):
    """Create test projects for portfolio."""
    print(f"Creating {count} test projects...")
    
    projects = [
        {
            "title": "E-Commerce Platform",
            "description": "Full-stack e-commerce application with payment integration",
            "tech_stack": ["React", "Node.js", "MongoDB", "Stripe"],
            "link": "https://github.com/user/ecommerce-platform",
            "is_autogenerated": False
        },
        {
            "title": "AI Chatbot",
            "description": "Natural language processing chatbot using transformer models",
            "tech_stack": ["Python", "TensorFlow", "FastAPI", "Docker"],
            "link": "https://github.com/user/ai-chatbot",
            "is_autogenerated": False
        },
        {
            "title": "Data Analytics Dashboard",
            "description": "Real-time analytics dashboard with interactive visualizations",
            "tech_stack": ["Python", "Plotly", "Pandas", "PostgreSQL"],
            "link": "https://github.com/user/analytics-dashboard",
            "is_autogenerated": False
        },
        {
            "title": "Mobile Fitness App",
            "description": "Cross-platform mobile app for fitness tracking",
            "tech_stack": ["React Native", "Firebase", "Redux"],
            "link": "https://github.com/user/fitness-app",
            "is_autogenerated": True
        },
        {
            "title": "DevOps Automation Suite",
            "description": "CI/CD pipeline automation and infrastructure as code",
            "tech_stack": ["Terraform", "Kubernetes", "GitHub Actions", "AWS"],
            "link": "https://github.com/user/devops-suite",
            "is_autogenerated": False
        }
    ]
    
    projects_created = []
    
    for i in range(min(count, len(projects))):
        project_data = projects[i]
        project = models.Project(
            user_id=user.id,
            job_id=random.choice(jobs).id if i % 2 == 0 and jobs else None,  # Associate some with jobs
            title=project_data["title"],
            description=project_data["description"],
            tech_stack=project_data["tech_stack"],
            link=project_data["link"],
            is_autogenerated=project_data["is_autogenerated"],
            metadata_json={"stars": random.randint(10, 500), "forks": random.randint(5, 100)},
            added_at=datetime.utcnow() - timedelta(days=random.randint(30, 365))
        )
        db.add(project)
        projects_created.append(project)
    
    db.commit()
    print(f"✅ Created {count} test projects")
    return projects_created


def main():
    """Main function to populate all test data."""
    print("=" * 60)
    print("POPULATING TEST DATA FOR CAREER AGENT")
    print("=" * 60)
    
    # Create tables if they don't exist
    print("\nCreating database tables...")
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables ready")
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_jobs = db.query(models.Job).count()
        if existing_jobs > 0:
            response = input(f"\n⚠️  Database already has {existing_jobs} jobs. Clear and recreate? (y/n): ")
            if response.lower() == 'y':
                print("Clearing existing data...")
                db.query(models.Application).delete()
                db.query(models.Project).delete()
                db.query(models.Resume).delete()
                db.query(models.Job).delete()
                db.commit()
                print("✅ Existing data cleared")
            else:
                print("Keeping existing data and adding new data...")
        
        print("\n" + "=" * 60)
        print("CREATING TEST DATA")
        print("=" * 60 + "\n")
        
        # Create test user first
        user = create_test_user(db)
        
        # Create test data
        jobs = create_test_jobs(db, count=15)
        resumes = create_test_resumes(db, user, count=3)
        projects = create_test_projects(db, user, jobs, count=5)
        applications = create_test_applications(db, user, jobs, resumes, count=20)
        
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"✅ Jobs created: {len(jobs)}")
        print(f"✅ Resumes created: {len(resumes)}")
        print(f"✅ Projects created: {len(projects)}")
        print(f"✅ Applications created: {len(applications)}")
        print("=" * 60)
        print("\n🎉 Test data population completed successfully!")
        print("\nYou can now test your API endpoints:")
        print("  - GET /api/v1/jobs/")
        print("  - GET /api/v1/resumes/")
        print("  - GET /api/v1/applications/")
        print("  - GET /api/v1/projects/")
        print("  - GET /api/v1/dashboard/stats")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
