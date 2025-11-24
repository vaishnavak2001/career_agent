from typing import List, Dict, Any, Optional
try:
    from langchain.agents import AgentExecutor, create_openai_functions_agent
except ImportError:
    # Fallback or mock for environments with incompatible langchain versions
    print("Warning: Could not import AgentExecutor. Agent features will be disabled.")
    AgentExecutor = None
    create_openai_functions_agent = None

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import Tool
from app.core.config import settings


class CareerAgent:
    """LangChain-based career automation agent."""
    
    def __init__(self):
        """Initialize the career agent."""
        self.llm = ChatOpenAI(
            model=settings.LLM_MODEL,
            temperature=settings.LLM_TEMPERATURE,
            openai_api_key=settings.OPENAI_API_KEY
        )
        self.tools = self._create_tools()
        self.agent = self._create_agent()
    
    def _create_tools(self) -> List[Tool]:
        """Create tools for the agent."""
        tools = [
            Tool(
                name="analyze_resume",
                description="Analyze a resume and extract key skills, experience, and qualifications",
                func=self._analyze_resume
            ),
            Tool(
                name="parse_job_description",
                description="Parse a job description and extract requirements, skills, and details",
                func=self._parse_job_description
            ),
            Tool(
                name="calculate_match_score",
                description="Calculate how well a resume matches a job description (0-100)",
                func=self._calculate_match_score
            ),
            Tool(
                name="generate_cover_letter",
                description="Generate a personalized cover letter for a job application",
                func=self._generate_cover_letter
            ),
            Tool(
                name="enhance_resume",
                description="Enhance a resume for a specific job with relevant keywords and improvements",
                func=self._enhance_resume
            ),
        ]
        return tools
    
    def _create_agent(self) -> Optional[AgentExecutor]:
        """Create the agent executor."""
        if not create_openai_functions_agent or not AgentExecutor:
            return None
            
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert career AI assistant specializing in job applications.
            You help users by:
            - Analyzing resumes and job descriptions
            - Calculating match scores
            - Generating cover letters
            - Enhancing resumes for specific jobs
            - Providing career advice
            
            Be professional, accurate, and helpful."""),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
        
        agent = create_openai_functions_agent(self.llm, self.tools, prompt)
        return AgentExecutor(agent=agent, tools=self.tools, verbose=True)
    
    def _analyze_resume(self, resume_text: str) -> str:
        """Analyze resume using LLM."""
        prompt = f"""Analyze this resume and extract:
        1. Key skills
        2. Years of experience
        3. Education
        4. Notable achievements
        5. Tech stack/tools
        
        Resume:
        {resume_text}
        
        Return as JSON format."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def _parse_job_description(self, jd_text: str) -> str:
        """Parse job description using LLM."""
        prompt = f"""Parse this job description and extract:
        1. Required skills
        2. Preferred skills
        3. Experience level (entry/mid/senior)
        4. Responsibilities
        5. Company culture indicators
        6. Salary range (if mentioned)
        
        Job Description:
        {jd_text}
        
        Return as JSON format."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def _calculate_match_score(self, resume_analysis: str, jd_analysis: str) -> str:
        """Calculate match score between resume and JD."""
        prompt = f"""Calculate a match score (0-100) between this resume and job description.
        Consider:
        - Skills overlap
        - Experience level match
        - Education requirements
        - Cultural fit indicators
        
        Resume Analysis:
        {resume_analysis}
        
        Job Requirements:
        {jd_analysis}
        
        Return:
        - Overall score (0-100)
        - Skills match percentage
        - Experience match percentage
        - Top matching points
        - Missing requirements
        
        Format as JSON."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def _generate_cover_letter(self, params: str) -> str:
        """Generate personalized cover letter."""
        # params should be a dict-like string with job_title, company, resume_summary
        prompt = f"""Generate a professional, personalized cover letter.
        
        Parameters:
        {params}
        
        The cover letter should:
        - Be 3-4 paragraphs
        - Highlight relevant experience
        - Show enthusiasm for the role
        - Be ATS-friendly
        - Sound professional but personable
        
        Return only the cover letter text."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def _enhance_resume(self, params: str) -> str:
        """Enhance resume for specific job."""
        prompt = f"""Enhance this resume for the target job.
        
        {params}
        
        Improvements to make:
        - Add relevant keywords from JD
        - Reframe achievements to match job requirements
        - Optimize for ATS
        - Fix formatting issues
        - Strengthen impact statements
        
        Return the enhanced resume section."""
        
        response = self.llm.invoke(prompt)
        return response.content
    
    def run(self, task: str) -> str:
        """Run the agent with a task."""
        if not self.agent:
            return "Agent features are currently disabled due to missing dependencies."
            
        try:
            result = self.agent.invoke({"input": task})
            return result["output"]
        except Exception as e:
            return f"Error executing agent: {str(e)}"
    
    async def arun(self, task: str) -> str:
        """Run the agent asynchronously."""
        if not self.agent:
            return "Agent features are currently disabled due to missing dependencies."

        try:
            result = await self.agent.ainvoke({"input": task})
            return result["output"]
        except Exception as e:
            return f"Error executing agent: {str(e)}"


# Global agent instance
career_agent = CareerAgent()


def analyze_resume_with_ai(resume_text: str) -> Dict[str, Any]:
    """Analyze resume using AI."""
    result = career_agent.run(f"Analyze this resume: {resume_text}")
    return {"analysis": result}


def generate_cover_letter_ai(
    job_title: str,
    company: str,
    resume_summary: str
) -> str:
    """Generate cover letter using AI."""
    params = f"Job: {job_title} at {company}. Resume: {resume_summary}"
    result = career_agent.run(f"Generate a cover letter for: {params}")
    return result


def calculate_match_with_ai(resume_text: str, jd_text: str) -> float:
    """Calculate match score using AI."""
    task = f"Calculate match score between resume and job description. Resume: {resume_text[:500]}... JD: {jd_text[:500]}..."
    result = career_agent.run(task)
    # Extract score from result (simplified)
    try:
        import json
        data = json.loads(result)
        return float(data.get("score", 0))
    except:
        return 0.0
