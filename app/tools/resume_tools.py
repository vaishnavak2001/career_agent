from langchain_core.tools import tool
from typing import Dict, Any, List
from app.database import SessionLocal
from app.models import Resume, Project

@tool
def rewrite_resume(current_resume: str, structured_jd: Dict[str, Any]) -> str:
    """
    Rewrites a resume to better match the provided job description.
    """
    # In a real app, this would use an LLM to rewrite the text.
    # Here we just append a "Tailored for..." section.
    
    tailored = f"{current_resume}\n\n## Tailored Summary\nExperienced professional with skills in {', '.join(structured_jd.get('skills', []))}."
    return tailored

@tool
def add_projects_to_resume(resume_text: str, projects: List[Dict[str, Any]]) -> str:
    """
    Adds a list of projects to the resume text.
    """
    project_section = "\n\n## Relevant Projects\n"
    for p in projects:
        project_section += f"- **{p['title']}**: {p['description']} (Tech: {p.get('tech_stack')})\n"
        
    return resume_text + project_section

@tool
def generate_cover_letter(job_data: Dict[str, Any], resume_text: str, personality: str = "professional") -> str:
    """
    Generates a cover letter for a specific job based on the resume and personality.
    """
    return f"""
Dear Hiring Manager at {job_data.get('company')},

I am writing to express my interest in the {job_data.get('title')} position.
Based on my experience with {', '.join(job_data.get('parsed_json', {}).get('skills', []))}, I believe I am a great fit.

Sincerely,
[Candidate Name]
    """
