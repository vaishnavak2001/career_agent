from typing import Dict, List

class ResumeEnhancer:
    async def add_projects(self, resume_content: str, projects: List[Dict]) -> str:
        """
        Add selected projects to the resume content.
        """
        # Simple string append for now
        enhanced_resume = resume_content + "\n\n## Relevant Projects\n"
        for project in projects:
            enhanced_resume += f"- **{project['title']}**: {project['description']} (Tech: {', '.join(project['tech_stack'])})\n"
        
        return enhanced_resume

    async def tailor_resume(self, resume_content: str, job_description: Dict) -> str:
        """
        Rewrite resume to match JD keywords.
        """
        # Placeholder for LLM rewriting
        return resume_content + "\n\n(Tailored for " + job_description.get('title', 'Role') + ")"

resume_enhancer_service = ResumeEnhancer()
