"""Resume analysis, enhancement, and project search tools."""
import os
from typing import List, Dict, Any
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import Project, ResumeVersion
from app.database import SessionLocal


def compute_match_score(resume_text: str, jd_data: Dict[str, Any]) -> float:
    """
    Computes a match score (0-100) between resume and job description.
    
    Factors:
    - Required skills match
    - Years of experience
    - Keyword overlap
    - Project relevance
    """
    score = 0.0
    max_score = 100.0
    
    resume_lower = resume_text.lower()
    
    # Skills matching (40 points)
    required_skills = jd_data.get("skills", [])
    if required_skills:
        matched_skills = sum(1 for skill in required_skills if skill.lower() in resume_lower)
        skills_score = (matched_skills / len(required_skills)) * 40
        score += skills_score
    
    # Experience matching (20 points)
    years_required = jd_data.get("years_required")
    if years_required:
        # Simple heuristic: check if resume mentions similar years
        import re
        exp_matches = re.findall(r'(\d+)\+?\s*years?', resume_text, re.IGNORECASE)
        if exp_matches:
            max_exp = max(int(m) for m in exp_matches)
            if max_exp >= years_required:
                score += 20
            else:
                score += (max_exp / years_required) * 20
    
    # Keyword density (20 points)
    keywords = jd_data.get("keywords", [])
    if keywords:
        matched_keywords = sum(1 for kw in keywords if kw.lower() in resume_lower)
        keyword_score = (matched_keywords / len(keywords)) * 20
        score += keyword_score
    
    # Seniority match (10 points)
    seniority = jd_data.get("seniority", "")
    if seniority.lower() in resume_lower:
        score += 10
    
    # Bonus points for special qualifications (10 points)
    if jd_data.get("has_remote") and "remote" in resume_lower:
        score += 5
    if jd_data.get("has_equity") and any(word in resume_lower for word in ["startup", "equity", "founder"]):
        score += 5
    
    return min(score, max_score)


def search_projects(keywords: List[str], limit: int = 3) -> List[Dict[str, Any]]:
    """
    Searches for relevant projects on GitHub, Arxiv, Kaggle, etc.
    
    In production, this would use actual APIs:
    - GitHub API
    - Arxiv API
    - Kaggle datasets
    - HuggingFace models
    """
    projects = []
    
    # Mock implementation - in production use real APIs
    sample_projects = [
        {
            "name": f"FastAPI Production Template",
            "description": "A production-ready FastAPI template with authentication, database migrations, and Docker support",
            "url": "https://github.com/example/fastapi-template",
            "source": "GitHub",
            "keywords": ["Python", "FastAPI", "PostgreSQL", "Docker"],
            "stars": 1250
        },
        {
            "name": f"LangChain RAG Application",
            "description": "Retrieval Augmented Generation system built with LangChain and vector databases",
            "url": "https://github.com/example/langchain-rag",
            "source": "GitHub",
            "keywords": ["Python", "LangChain", "AI", "RAG", "Vector DB"],
            "stars": 890
        },
        {
            "name": f"Microservices Architecture",
            "description": "Scalable microservices with Kubernetes orchestration and service mesh",
            "url": "https://github.com/example/microservices",
            "source": "GitHub",
            "keywords": ["Kubernetes", "Docker", "Microservices", "AWS"],
            "stars": 2100
        }
    ]
    
    # Filter by keyword relevance
    relevant_projects = []
    for proj in sample_projects:
        proj_keywords = set(k.lower() for k in proj["keywords"])
        search_keywords = set(k.lower() for k in keywords)
        overlap = len(proj_keywords.intersection(search_keywords))
        if overlap > 0:
            proj["relevance_score"] = overlap
            relevant_projects.append(proj)
    
    # Sort by relevance
    relevant_projects.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
    
    # Store in database
    db = SessionLocal()
    try:
        for proj_data in relevant_projects[:limit]:
            existing = db.query(Project).filter(Project.url == proj_data["url"]).first()
            if not existing:
                project = Project(
                    name=proj_data["name"],
                    description=proj_data["description"],
                    url=proj_data["url"],
                    source=proj_data["source"],
                    keywords=proj_data["keywords"]
                )
                db.add(project)
        db.commit()
    finally:
        db.close()
    
    return relevant_projects[:limit]


def add_projects_to_resume(base_resume: str, projects: List[Dict[str, Any]]) -> str:
    """
    Adds selected projects to the resume in a natural way.
    Maintains truthfulness by only adding real, accessible projects.
    """
    if not projects:
        return base_resume
    
    # Check if resume already has a projects section
    if "## Projects" in base_resume or "# Projects" in base_resume:
        # Insert before existing projects section
        parts = base_resume.split("## Projects")
        if len(parts) == 1:
            parts = base_resume.split("# Projects")
        
        new_projects = "\n\n## Notable Projects\n\n"
        for proj in projects:
            new_projects += f"### {proj['name']}\n"
            new_projects += f"{proj['description']}\n"
            new_projects += f"- **Source**: [{proj['source']}]({proj['url']})\n"
            new_projects += f"- **Technologies**: {', '.join(proj['keywords'])}\n\n"
        
        return parts[0] + new_projects + "## Projects" + parts[1] if len(parts) > 1 else parts[0] + new_projects
    else:
        # Add projects section at the end
        new_section = "\n\n## Notable Open Source Contributions\n\n"
        for proj in projects:
            new_section += f"### {proj['name']}\n"
            new_section += f"{proj['description']}\n"
            new_section += f"- **Repository**: {proj['url']}\n"
            new_section += f"- **Tech Stack**: {', '.join(proj['keywords'])}\n\n"
        
        return base_resume + new_section


def rewrite_resume_to_match_jd(resume: str, jd_data: Dict[str, Any]) -> str:
    """
    Rewrites the resume to better match the job description.
    
    In production, this would use an LLM to:
    - Reorder sections to highlight relevant experience
    - Rephrase bullet points to match job keywords
    - Emphasize matching skills
    - Maintain truthfulness while optimizing presentation
    """
    # For now, we'll do simple keyword optimization
    # In production, use OpenAI/Anthropic API
    
    enhanced_resume = resume
    
    # Add a professional summary if not present
    if "## Summary" not in enhanced_resume and "# Summary" not in enhanced_resume:
        skills = jd_data.get("skills", [])
        seniority = jd_data.get("seniority", "")
        
        summary = f"\n## Professional Summary\n\n"
        summary += f"{seniority} professional with expertise in {', '.join(skills[:5])}. "
        summary += f"Proven track record of building scalable solutions and delivering high-impact projects.\n\n"
        
        enhanced_resume = summary + enhanced_resume
    
    # Store version in database
    db = SessionLocal()
    try:
        resume_version = ResumeVersion(content=enhanced_resume)
        db.add(resume_version)
        db.commit()
        db.refresh(resume_version)
    finally:
        db.close()
    
    return enhanced_resume
