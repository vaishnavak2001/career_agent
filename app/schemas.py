from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Tool Input Schemas ---

class ScrapeJobsInput(BaseModel):
    region: str = Field(..., description="Geographic region to scrape jobs from (e.g., 'San Francisco', 'Remote').")
    role: str = Field(..., description="Job role to search for (e.g., 'Software Engineer', 'Data Scientist').")
    platforms: List[str] = Field(..., description="List of platforms to scrape (e.g., ['LinkedIn', 'Indeed', 'Glassdoor']).")

class ParseJDInput(BaseModel):
    job_text: str = Field(..., description="The full raw text of the job description.")

class ComputeMatchScoreInput(BaseModel):
    resume_text: str = Field(..., description="The user's current resume text.")
    jd_data: Dict[str, Any] = Field(..., description="Structured data extracted from the job description.")

class SearchProjectsInput(BaseModel):
    keywords: List[str] = Field(..., description="List of technical keywords to search projects for.")
    limit: int = Field(3, description="Number of projects to return.")

class AddProjectsToResumeInput(BaseModel):
    base_resume: str = Field(..., description="The original resume text.")
    projects: List[Dict[str, Any]] = Field(..., description="List of project objects to add.")

class RewriteResumeInput(BaseModel):
    resume: str = Field(..., description="The resume text to rewrite.")
    jd_data: Dict[str, Any] = Field(..., description="Structured job description data.")

class GenerateCoverLetterInput(BaseModel):
    job_data: Dict[str, Any] = Field(..., description="Job details including company name, title, and requirements.")
    resume: str = Field(..., description="The resume text being used for the application.")
    personality: str = Field("professional", description="Tone of the cover letter (e.g., 'professional', 'creative', 'direct').")

class DetectScamInput(BaseModel):
    job_data: Dict[str, Any] = Field(..., description="Job details including description, company, salary, etc.")

class SubmitApplicationInput(BaseModel):
    url: str = Field(..., description="The URL to submit the application to.")
    resume_content: str = Field(..., description="The content of the resume to submit.")
    cover_letter: str = Field(..., description="The content of the cover letter.")

class DeduplicateJobInput(BaseModel):
    job_url: str = Field(..., description="URL of the job.")
    company: str = Field(..., description="Company name.")
    title: str = Field(..., description="Job title.")

# --- JSON Schemas for Tool Calling (for LLM) ---

TOOL_SCHEMAS = [
    {
        "name": "scrape_jobs",
        "description": "Scrapes job listings from specified platforms for a given region and role.",
        "parameters": ScrapeJobsInput.model_json_schema()
    },
    {
        "name": "parse_jd",
        "description": "Parses a raw job description into structured data (skills, seniority, etc.).",
        "parameters": ParseJDInput.model_json_schema()
    },
    {
        "name": "compute_match_score",
        "description": "Calculates a match score (0-100) between a resume and a job description.",
        "parameters": ComputeMatchScoreInput.model_json_schema()
    },
    {
        "name": "search_projects",
        "description": "Searches for relevant projects on GitHub, Arxiv, etc. based on keywords.",
        "parameters": SearchProjectsInput.model_json_schema()
    },
    {
        "name": "add_projects_to_resume",
        "description": "Integrates selected projects into the resume text.",
        "parameters": AddProjectsToResumeInput.model_json_schema()
    },
    {
        "name": "rewrite_resume_to_match_jd",
        "description": "Rewrites the resume to better align with the job description keywords and requirements.",
        "parameters": RewriteResumeInput.model_json_schema()
    },
    {
        "name": "generate_cover_letter",
        "description": "Generates a tailored cover letter based on the job and resume.",
        "parameters": GenerateCoverLetterInput.model_json_schema()
    },
    {
        "name": "detect_scam",
        "description": "Analyzes job data for potential scam signals.",
        "parameters": DetectScamInput.model_json_schema()
    },
    {
        "name": "submit_application",
        "description": "Automates the submission of the job application.",
        "parameters": SubmitApplicationInput.model_json_schema()
    },
    {
        "name": "deduplicate_job",
        "description": "Checks if the job has already been processed or applied to.",
        "parameters": DeduplicateJobInput.model_json_schema()
    }
]
