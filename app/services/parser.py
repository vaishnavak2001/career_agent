from app.core.config import settings
import json

class JobParser:
    """Simple job description parser that works without LLM API keys"""
    
    async def parse_jd(self, raw_text: str) -> dict:
        """
        Parse raw job description text into structured data.
        Uses simple keyword extraction for now.
        """
        # Simple keyword-based extraction
        keywords = raw_text.lower()
        
        # Common tech skills to look for
        tech_skills = []
        skill_keywords = ['python', 'javascript', 'react', 'fastapi', 'node', 'sql', 'mongodb', 
                         'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'java', 'c++', 'golang']
        
        for skill in skill_keywords:
            if skill in keywords:
                tech_skills.append(skill.title())
        
        # Extract experience (simple pattern matching)
        experience = "Not specified"
        if "senior" in keywords:
            experience = "5+ years"
        elif "junior" in keywords or "entry" in keywords:
            experience = "0-2 years"
        elif "mid" in keywords or "intermediate" in keywords:
            experience = "2-5 years"
        
        return {
            "skills": tech_skills if tech_skills else ["General"],
            "experience": experience,
            "salary": "Not specified",
            "summary": raw_text[:200] + "..." if len(raw_text) > 200 else raw_text
        }

parser_service = JobParser()
