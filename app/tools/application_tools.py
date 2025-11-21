"""Application submission and cover letter generation tools."""
from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Application, Job, ResumeVersion
from app.database import SessionLocal


PERSONALITY_TEMPLATES = {
    "professional": {
        "opening": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the {title} position at {company}.",
        "body": "With my background in {skills}, I am confident I can contribute significantly to your team. {experience}",
        "closing": "I look forward to the opportunity to discuss how my skills and experience align with your needs.\n\nSincerely,"
    },
    "friendly": {
        "opening": "Hi there!\n\nI'm excited to apply for the {title} role at {company}!",
        "body": "I've been working with {skills} for several years and I'm really passionate about {focus}. {experience}",
        "closing": "I'd love to chat more about how I can help the team. Looking forward to hearing from you!\n\nBest,"
    },
    "technical": {
        "opening": "Dear Hiring Team,\n\nI am applying for the {title} position. Here's why I'm a strong technical fit:",
        "body": "Technical Expertise:\n- {skills}\n\nRelevant Experience:\n{experience}",
        "closing": "I'm eager to dive deeper into the technical requirements and discuss architecture decisions.\n\nRegards,"
    },
    "direct": {
        "opening": "Re: {title} at {company}",
        "body": "Quick summary:\n- Skills: {skills}\n- Experience: {experience}\n- Why me: {value_prop}",
        "closing": "Let's talk.\n\nThanks,"
    },
    "creative": {
        "opening": "Hey {company} team! 👋\n\nYour {title} role caught my eye, and here's why we might be a great match:",
        "body": "I bring {skills} to the table, plus a creative approach to problem-solving. {experience}\n\nWhat makes me different? {unique_angle}",
        "closing": "Let's create something amazing together!\n\nCheers,"
    },
    "relocation_friendly": {
        "opening": "Dear Hiring Manager,\n\nI am writing regarding the {title} position at {company}. I am prepared to relocate for the right opportunity.",
        "body": "I bring {skills} and am excited about the prospect of joining your team in {location}. {experience}\n\nRelocation: I am ready to move within 30 days of an offer.",
        "closing": "I look forward to discussing this opportunity and my relocation plans.\n\nBest regards,"
    }
}


def generate_cover_letter(job_data: Dict[str, Any], resume: str, personality: str = "professional") -> str:
    """
    Generates a tailored cover letter based on job data and resume.
    Uses different personality templates based on user preference.
    """
    template = PERSONALITY_TEMPLATES.get(personality, PERSONALITY_TEMPLATES["professional"])
    
    # Extract key information
    title = job_data.get("title", "the position")
    company = job_data.get("company", "your company")
    location = job_data.get("location", "your location")
    
    # Get skills from parsed JD
    parsed_data = job_data.get("parsed_data", {})
    skills = ", ".join(parsed_data.get("skills", ["relevant technologies"])[:3])
    
    # Extract experience from resume (simple approach)
    experience = "I have extensive experience building scalable systems and working with cross-functional teams."
    
    # Format the letter
    letter = template["opening"].format(
        title=title,
        company=company,
        location=location
    )
    
    letter += "\n\n"
    
    letter += template["body"].format(
        title=title,
        company=company,
        skills=skills,
        experience=experience,
        focus="building robust, scalable solutions",
        value_prop="I ship fast and iterate based on feedback",
        unique_angle="I've shipped products from 0 to 1 multiple times",
        location=location
    )
    
    letter += "\n\n"
    letter += template["closing"]
    
    return letter


def submit_application(url: str, resume_content: str, cover_letter: str) -> str:
    """
    Submits the job application.
    
    In production, this would:
    - Use Playwright/Selenium to automate form filling
    - Handle file uploads (PDF generation)
    - Handle authentication/login
    - Take screenshots for verification
    - Implement retry logic
    
    NOTE: Browser automation for applications should be done carefully
    to respect platform terms of service.
    """
    # Mock implementation
    # In production, use playwright to:
    # 1. Navigate to application URL
    # 2. Fill in personal information
    # 3. Upload resume (convert to PDF)
    # 4. Paste cover letter
    # 5. Submit form
    # 6. Capture confirmation
    
    print(f"[MOCK] Submitting application to: {url}")
    print(f"[MOCK] Resume length: {len(resume_content)} chars")
    print(f"[MOCK] Cover letter length: {len(cover_letter)} chars")
    
    # Simulate submission
    return "success"


def store_application_status(job_id: int, resume_version_id: int, cover_letter: str, 
                            personality: str, status: str = "applied") -> int:
    """
    Stores the application status in the database.
    """
    db = SessionLocal()
    try:
        application = Application(
            job_id=job_id,
            resume_version_id=resume_version_id,
            cover_letter_text=cover_letter,
            personality_used=personality,
            status=status,
            submitted_at=datetime.utcnow()
        )
        db.add(application)
        db.commit()
        db.refresh(application)
        return application.id
    finally:
        db.close()


def get_application_by_job_id(job_id: int) -> Dict[str, Any]:
    """
    Retrieves application details for a specific job.
    """
    db = SessionLocal()
    try:
        application = db.query(Application).filter(Application.job_id == job_id).first()
        if not application:
            return None
        
        return {
            "id": application.id,
            "job_id": application.job_id,
            "status": application.status,
            "personality_used": application.personality_used,
            "submitted_at": application.submitted_at.isoformat() if application.submitted_at else None
        }
    finally:
        db.close()
