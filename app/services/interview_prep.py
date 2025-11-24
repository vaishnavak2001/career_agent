"""Interview preparation service using LLM."""
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from app.core.config import settings

class InterviewPrepService:
    """Service for generating interview preparation materials."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
    
    async def generate_questions(self, job_title: str, company: str, job_description: str) -> Dict[str, Any]:
        """Generate interview questions based on job details."""
        prompt = f"""Generate a list of interview questions for the following role:
        Role: {job_title}
        Company: {company}
        
        Job Description Summary:
        {job_description[:1000]}...
        
        Provide:
        1. 5 Technical questions specific to the role/stack
        2. 3 Behavioral questions (STAR method)
        3. 2 Company-specific questions based on general knowledge or the description
        4. Key topics to review
        
        Return as a structured JSON object with keys: technical, behavioral, company, review_topics.
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            # In a real app, we'd use an OutputParser to ensure JSON
            # For now, we'll assume the LLM follows instructions or return raw text if parsing fails
            return {"content": response.content}
        except Exception as e:
            return {"error": str(e)}

    async def simulate_interview(self, job_title: str, user_answer: str, question: str) -> Dict[str, Any]:
        """Provide feedback on a user's answer."""
        prompt = f"""Act as an interviewer for a {job_title} role.
        
        Question: {question}
        Candidate Answer: {user_answer}
        
        Provide feedback on the answer:
        1. Strengths
        2. Weaknesses
        3. Suggested improvements
        4. Rating (1-10)
        
        Be constructive and professional.
        """
        
        try:
            response = await self.llm.ainvoke(prompt)
            return {"feedback": response.content}
        except Exception as e:
            return {"error": str(e)}

interview_service = InterviewPrepService()
