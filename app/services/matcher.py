from typing import Dict, List

class Matcher:
    def compute_match_score(self, resume_text: str, job_data: Dict) -> int:
        """
        Compute a match score (0-100) between resume and job.
        """
        # Simple keyword matching for now
        score = 0
        max_score = 100
        
        skills = job_data.get("skills", [])
        if not skills:
            return 50 # Default if no skills parsed
            
        matched_skills = [skill for skill in skills if skill.lower() in resume_text.lower()]
        
        if len(skills) > 0:
            score = int((len(matched_skills) / len(skills)) * 100)
        
        # Cap at 100
        return min(score, 100)

matcher_service = Matcher()
