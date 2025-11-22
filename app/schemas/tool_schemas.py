"""
Tool Calling Schemas for LangChain Agent
All 13 tools with complete JSON schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

# =====================================================
# ENUMS
# =====================================================

class JobPlatform(str, Enum):
    LINKEDIN = "linkedin"
    INDEED = "indeed"
    GLASSDOOR = "glassdoor"
    ZIPRECRUITER = "ziprecruiter"
    DICE = "dice"
    ANGELLIST = "angellist"
    REMOTECO = "remote.co"
    WEWORKREMOTELY = "weworkremotely"

class CoverLetterPersonality(str, Enum):
    PROFESSIONAL = "professional"
    FRIENDLY = "friendly"
    TECHNICAL = "technical"
    DIRECT = "direct"
    CREATIVE = "creative"
    RELOCATION_FRIENDLY = "relocation_friendly"

class ApplicationStatus(str, Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    INTERVIEW = "interview_scheduled"
    OFFER = "offer_received"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

# =====================================================
# TOOL 1: SCRAPE JOBS
# =====================================================

class ScrapeJobsInput(BaseModel):
    """Input schema for scraping jobs from multiple platforms."""
    
    region: str = Field(
        description="Geographic region or location (e.g., 'Remote', 'New York', 'San Francisco')"
    )
    role: str = Field(
        description="Job role or title to search for (e.g., 'Software Engineer', 'Data Scientist')"
    )
    platforms: List[JobPlatform] = Field(
        default=[JobPlatform.LINKEDIN, JobPlatform.INDEED],
        description="List of job platforms to scrape"
    )
    since_timestamp: Optional[datetime] = Field(
        default=None,
        description="Only scrape jobs posted after this timestamp (UTC). If None, scrape all."
    )
    max_results_per_platform: int = Field(
        default=50,
        description="Maximum number of jobs to scrape per platform",
        ge=1,
        le=500
    )

class JobRecord(BaseModel):
    """Output schema for a scraped job."""
    
    source: str
    url: str
    external_id: Optional[str] = None
    title: str
    company: str
    company_url: Optional[str] = None
    location: str
    is_remote: bool = False
    posted_date: Optional[datetime] = None
    raw_text: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    scraped_at: datetime

class ScrapeJobsOutput(BaseModel):
    """Output schema for scrape_jobs tool."""
    
    jobs: List[JobRecord]
    total_scraped: int
    platform_counts: Dict[str, int]
    errors: List[str] = []

# =====================================================
# TOOL 2: DEDUPLICATE JOB
# =====================================================

class DeduplicateJobInput(BaseModel):
    """Input schema for job deduplication check."""
    
    job_url: str = Field(description="Job posting URL")
    company: str = Field(description="Company name")
    title: str = Field(description="Job title")
    posted_date: Optional[datetime] = Field(default=None, description="Job posted date")
    content_text: str = Field(description="Full job description text for content hashing")

class DeduplicateJobOutput(BaseModel):
    """Output schema for deduplicate_job tool."""
    
    is_duplicate: bool
    duplicate_type: Optional[str] = None  # url, content_hash, company_title_date
    existing_job_id: Optional[int] = None
    match_confidence: float = Field(ge=0.0, le=1.0)
    reason: str

# =====================================================
# TOOL 3: DETECT SCAM
# =====================================================

class DetectScamInput(BaseModel):
    """Input schema for scam detection."""
    
    job_url: str
    company: str
    company_url: Optional[str] = None
    contact_email: Optional[str] = None
    salary_range: Optional[str] = None
    description: str
    requirements: Optional[str] = None

class ScamFlag(BaseModel):
    """Individual scam flag."""
    
    flag_type: str  # suspicious_email, payment_request, unrealistic_salary, etc.
    severity: str  # low, medium, high
    description: str
    evidence: str

class DetectScamOutput(BaseModel):
    """Output schema for detect_scam tool."""
    
    is_scam: bool
    scam_score: int = Field(ge=0, le=100, description="0=legitimate, 100=definite scam")
    flags: List[ScamFlag] = []
    recommendation: str  # apply, caution, avoid
    reasoning: str

# =====================================================
# TOOL 4: PARSE JD
# =====================================================

class ParseJDInput(BaseModel):
    """Input schema for parsing job description."""
    
    job_text: str = Field(description="Full job description text")
    job_title: Optional[str] = None
    company: Optional[str] = None

class ParsedJD(BaseModel):
    """Structured job description output."""
    
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    tech_stack: List[str] = []
    responsibilities: List[str] = []
    qualifications: List[str] = []
    
    experience_min_years: Optional[int] = None
    experience_max_years: Optional[int] = None
    education_required: Optional[str] = None
    
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    salary_currency: str = "USD"
    
    employment_type: Optional[str] = None  # full-time, contract, etc.
    seniority_level: Optional[str] = None  # entry, mid, senior, etc.
    visa_sponsorship: bool = False
    
    benefits: List[str] = []
    perks: List[str] = []
    
    keywords: List[str] = []
    industry: Optional[str] = None

class ParseJDOutput(BaseModel):
    """Output schema for parse_jd tool."""
    
    parsed_data: ParsedJD
    confidence_score: float = Field(ge=0.0, le=1.0)
    extraction_notes: List[str] = []

# =====================================================
# TOOL 5: COMPUTE MATCH SCORE
# =====================================================

class ComputeMatchScoreInput(BaseModel):
    """Input schema for computing match score."""
    
    resume_text: str = Field(description="Candidate's resume content")
    parsed_jd: ParsedJD = Field(description="Structured job description")
    candidate_projects: List[Dict[str, Any]] = Field(
        default=[],
        description="List of candidate projects with title, description, tech_stack"
    )

class MatchBreakdown(BaseModel):
    """Detailed match score breakdown."""
    
    required_skills_score: int = Field(ge=0, le=100)
    required_skills_matched: List[str] = []
    required_skills_missing: List[str] = []
    
    preferred_skills_score: int = Field(ge=0, le=100)
    preferred_skills_matched: List[str] = []
    
    project_alignment_score: int = Field(ge=0, le=100)
    relevant_projects: List[str] = []
    
    experience_score: int = Field(ge=0, le=100)
    experience_gap: Optional[str] = None
    
    education_score: int = Field(ge=0, le=100)
    
    keyword_density_score: int = Field(ge=0, le=100)
    matched_keywords: List[str] = []
    
    ats_simulation_score: int = Field(ge=0, le=100)

class ComputeMatchScoreOutput(BaseModel):
    """Output schema for compute_match_score tool."""
    
    total_score: int = Field(ge=0, le=100)
    breakdown: MatchBreakdown
    recommendation: str  # strong_match, good_match, weak_match, poor_match
    improvement_suggestions: List[str] = []

# =====================================================
# TOOL 6: SEARCH PROJECTS
# =====================================================

class SearchProjectsInput(BaseModel):
    """Input schema for searching relevant projects."""
    
    jd_keywords: List[str] = Field(description="Keywords extracted from job description")
    tech_stack: List[str] = Field(default=[], description="Technologies from JD")
    max_results: int = Field(default=10, ge=1, le=50)
    sources: List[str] = Field(
        default=["github", "huggingface", "kaggle"],
        description="Sources to search: github, huggingface, kaggle, arxiv"
    )
    min_stars: int = Field(default=10, description="Minimum GitHub stars")

class ProjectSearchResult(BaseModel):
    """Individual project search result."""
    
    title: str
    description: str
    url: str
    source: str  # github, huggingface, kaggle, arxiv
    tech_stack: List[str] = []
    
    # GitHub-specific
    stars: Optional[int] = None
    forks: Optional[int] = None
    language: Optional[str] = None
    topics: List[str] = []
    
    # Relevance
    relevance_score: float = Field(ge=0.0, le=1.0)
    matched_keywords: List[str] = []
    reason: str

class SearchProjectsOutput(BaseModel):
    """Output schema for search_projects tool."""
    
    projects: List[ProjectSearchResult]
    total_found: int
    sources_searched: List[str]

# =====================================================
# TOOL 7: ADD PROJECTS TO RESUME
# =====================================================

class AddProjectsToResumeInput(BaseModel):
    """Input schema for adding projects to resume."""
    
    base_resume: str = Field(description="Original resume content (Markdown)")
    selected_projects: List[int] = Field(description="List of project IDs to add")
    placement: str = Field(
        default="after_experience",
        description="Where to place projects: after_experience, after_education, dedicated_section"
    )

class AddProjectsToResumeOutput(BaseModel):
    """Output schema for add_projects_to_resume tool."""
    
    updated_resume: str = Field(description="Resume with projects added")
    project_metadata: List[Dict[str, Any]] = Field(
        description="Metadata for added projects (for DB storage)"
    )
    changes_summary: str

# =====================================================
# TOOL 8: STORE PROJECT METADATA
# =====================================================

class StoreProjectMetadataInput(BaseModel):
    """Input schema for storing project metadata."""
    
    user_id: int
    job_id: Optional[int] = None
    title: str
    description: str
    tech_stack: List[str]
    link: str
    source: str
    is_autogenerated: bool = False
    metadata_json: Dict[str, Any] = {}

class StoreProjectMetadataOutput(BaseModel):
    """Output schema for store_project_metadata tool."""
    
    success: bool
    project_id: Optional[int] = None
    error: Optional[str] = None

# =====================================================
# TOOL 9: REWRITE RESUME TO MATCH JD
# =====================================================

class RewriteResumeInput(BaseModel):
    """Input schema for resume rewriting."""
    
    resume: str = Field(description="Current resume content")
    parsed_jd: ParsedJD = Field(description="Structured job description")
    optimization_level: str = Field(
        default="moderate",
        description="How aggressive to optimize: light, moderate, aggressive"
    )
    preserve_truthfulness: bool = Field(
        default=True,
        description="Never fabricate information"
    )

class RewriteResumeOutput(BaseModel):
    """Output schema for rewrite_resume_to_match_jd tool."""
    
    tailored_resume: str
    changes_made: List[str]
    keyword_improvements: Dict[str, int]  # keyword -> frequency_increase
    ats_score_improvement: int
    version_name: str

# =====================================================
# TOOL 10: GENERATE COVER LETTER
# =====================================================

class GenerateCoverLetterInput(BaseModel):
    """Input schema for cover letter generation."""
    
    job_title: str
    company: str
    job_description: str
    tailored_resume: str
    candidate_name: str
    personality: CoverLetterPersonality = CoverLetterPersonality.PROFESSIONAL
    max_words: int = Field(default=300, ge=100, le=500)
    
    # Optional context
    referral_source: Optional[str] = None
    specific_achievements: List[str] = []
    reasons_for_interest: List[str] = []

class GenerateCoverLetterOutput(BaseModel):
    """Output schema for generate_cover_letter tool."""
    
    cover_letter_text: str
    word_count: int
    personality_used: str
    tone_analysis: Dict[str, float]  # professional: 0.8, enthusiastic: 0.6, etc.
    template_id: Optional[str] = None

# =====================================================
# TOOL 11: SUBMIT APPLICATION
# =====================================================

class SubmitApplicationInput(BaseModel):
    """Input schema for application submission."""
    
    job_url: str
    form_data: Dict[str, Any] = Field(
        description="Form fields to fill: name, email, phone, etc."
    )
    resume_file_path: str = Field(description="Path to resume PDF")
    cover_letter_file_path: Optional[str] = None
    additional_documents: List[str] = Field(
        default=[],
        description="Paths to additional documents"
    )
    
    # Automation settings
    is_sandbox: bool = Field(
        default=True,
        description="If true, simulate but don't actually submit"
    )
    screenshot: bool = Field(default=True)
    wait_for_confirmation: bool = Field(default=True)
    timeout_seconds: int = Field(default=60)

class SubmitApplicationOutput(BaseModel):
    """Output schema for submit_application tool."""
    
    status: str  # success, failed, captcha_required, manual_required
    confirmation_number: Optional[str] = None
    confirmation_email: Optional[str] = None
    screenshot_urls: List[str] = []
    
    # Errors/issues
    error_message: Optional[str] = None
    captcha_encountered: bool = False
    manual_intervention_required: bool = False
    
    # Metadata
    submission_timestamp: datetime
    metadata: Dict[str, Any] = {}

# =====================================================
# TOOL 12: STORE APPLICATION STATUS
# =====================================================

class StoreApplicationStatusInput(BaseModel):
    """Input schema for storing application status."""
    
    user_id: int
    job_id: int
    resume_id: int
    cover_letter_id: Optional[int] = None
    status: ApplicationStatus
    is_sandbox: bool
    form_data: Dict[str, Any] = {}
    confirmation_number: Optional[str] = None
    screenshot_urls: List[str] = []
    metadata_json: Dict[str, Any] = {}

class StoreApplicationStatusOutput(BaseModel):
    """Output schema for store_application_status tool."""
    
    success: bool
    application_id: Optional[int] = None
    error: Optional[str] = None

# =====================================================
# TOOL 13: DASHBOARD METRICS
# =====================================================

class DashboardMetricsInput(BaseModel):
    """Input schema for dashboard metrics."""
    
    user_id: int
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    include_charts: bool = Field(default=True)

class MetricsSummary(BaseModel):
    """Summary metrics for dashboard."""
    
    total_jobs_scraped: int
    total_jobs_matched: int
    total_applications: int
    pending_approval: int
    applications_submitted: int
    interviews_scheduled: int
    offers_received: int
    
    scams_detected: int
    duplicates_avoided: int
    
    avg_match_score: float
    avg_response_time_days: Optional[float] = None
    
    response_rate: float = Field(ge=0.0, le=100.0)
    interview_rate: float = Field(ge=0.0, le=100.0)
    offer_rate: float = Field(ge=0.0, le=100.0)

class DashboardMetricsOutput(BaseModel):
    """Output schema for dashboard_metrics tool."""
    
    summary: MetricsSummary
    top_skills: List[Dict[str, Any]] = []  # skill, count, avg_salary
    top_companies: List[Dict[str, Any]] = []  # company, jobs_count
    match_score_distribution: Dict[str, int] = {}  # range -> count
    timeline_data: List[Dict[str, Any]] = []  # date, jobs, applications
    recent_activity: List[Dict[str, Any]] = []  # Recent jobs/applications

# =====================================================
# EXPORT ALL SCHEMAS
# =====================================================

__all__ = [
    # Tool 1
    "ScrapeJobsInput",
    "JobRecord",
    "ScrapeJobsOutput",
    
    # Tool 2
    "DeduplicateJobInput",
    "DeduplicateJobOutput",
    
    # Tool 3
    "DetectScamInput",
    "ScamFlag",
    "DetectScamOutput",
    
    # Tool 4
    "ParseJDInput",
    "ParsedJD",
    "ParseJDOutput",
    
    # Tool 5
    "ComputeMatchScoreInput",
    "MatchBreakdown",
    "ComputeMatchScoreOutput",
    
    # Tool 6
    "SearchProjectsInput",
    "ProjectSearchResult",
    "SearchProjectsOutput",
    
    # Tool 7
    "AddProjectsToResumeInput",
    "AddProjectsToResumeOutput",
    
    # Tool 8
    "StoreProjectMetadataInput",
    "StoreProjectMetadataOutput",
    
    # Tool 9
    "RewriteResumeInput",
    "RewriteResumeOutput",
    
    # Tool 10
    "GenerateCoverLetterInput",
    "GenerateCoverLetterOutput",
    
    # Tool 11
    "SubmitApplicationInput",
    "SubmitApplicationOutput",
    
    # Tool 12
    "StoreApplicationStatusInput",
    "StoreApplicationStatusOutput",
    
    # Tool 13
    "DashboardMetricsInput",
    "MetricsSummary",
    "DashboardMetricsOutput",
]
