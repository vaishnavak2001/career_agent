from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings

class CoverLetterGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", openai_api_key=settings.OPENAI_API_KEY)

    async def generate_cover_letter(self, resume_text: str, job_description: dict, personality: str = "professional") -> str:
        """
        Generate a cover letter.
        """
        if not settings.OPENAI_API_KEY:
            return f"Dear Hiring Manager,\n\nI am writing to apply for the {job_description.get('title')} position at {job_description.get('company')}. I believe my skills in {', '.join(job_description.get('skills', []))} make me a great fit.\n\nSincerely,\n[Name]"

        prompt = ChatPromptTemplate.from_template(
            """
            Write a cover letter for the following job application.
            
            Resume:
            {resume}
            
            Job Description:
            {job_description}
            
            Personality: {personality}
            
            The cover letter should be concise, highlighting relevant skills and experience.
            """
        )
        
        messages = prompt.format_messages(
            resume=resume_text,
            job_description=job_description,
            personality=personality
        )
        
        try:
            response = await self.llm.apredict_messages(messages)
            return response.content
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return "Error generating cover letter."

cover_letter_service = CoverLetterGenerator()
