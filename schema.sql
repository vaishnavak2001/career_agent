-- =====================================================
-- Career Agent - Complete PostgreSQL Schema
-- =====================================================

-- ⚠️ CLEAN SLATE: Drop existing objects to avoid conflicts
DROP VIEW IF EXISTS v_application_funnel CASCADE;
DROP VIEW IF EXISTS v_high_match_jobs CASCADE;
DROP TABLE IF EXISTS 
    webhook_events, 
    notifications, 
    audit_logs, 
    skill_demand, 
    daily_metrics, 
    monitoring_configs, 
    applications, 
    cover_letters, 
    projects, 
    match_scores, 
    jobs, 
    resumes, 
    users 
CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;

-- =====================================================
-- EXTENSIONS
-- =====================================================

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "vector";  -- For embeddings (optional)

-- =====================================================
-- USERS & AUTHENTICATION
-- =====================================================

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    phone VARCHAR(50),
    linkedin_url VARCHAR(500),
    github_url VARCHAR(500),
    portfolio_url VARCHAR(500),
    
    -- Settings
    settings JSONB DEFAULT '{}'::jsonb,  -- UI preferences, thresholds, etc.
    
    -- OAuth
    oauth_provider VARCHAR(50),  -- google, linkedin, github
    oauth_id VARCHAR(255),
    
    -- Status
    is_active BOOLEAN DEFAULT true,
    is_verified BOOLEAN DEFAULT false,
    email_verified_at TIMESTAMP,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_uuid ON users(uuid);
CREATE INDEX idx_users_oauth ON users(oauth_provider, oauth_id);

-- =====================================================
-- RESUMES
-- =====================================================

CREATE TABLE resumes (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Version control
    version_name VARCHAR(255),
    is_base BOOLEAN DEFAULT false,  -- Base resume vs tailored
    parent_resume_id INTEGER REFERENCES resumes(id),  -- For version tracking
    
    -- Content
    content TEXT NOT NULL,  -- Markdown or structured JSON
    format VARCHAR(20) DEFAULT 'markdown',  -- markdown, json, html
    
    -- Metadata
    skills JSONB DEFAULT '[]'::jsonb,  -- Extracted skills
    experience_years DECIMAL(4,1),
    education_level VARCHAR(100),
    certifications JSONB DEFAULT '[]'::jsonb,
    
    -- ATS optimization
    ats_score INTEGER CHECK (ats_score >= 0 AND ats_score <= 100),
    ats_keywords JSONB DEFAULT '[]'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_resumes_user ON resumes(user_id);
CREATE INDEX idx_resumes_is_base ON resumes(is_base);
CREATE INDEX idx_resumes_parent ON resumes(parent_resume_id);

-- =====================================================
-- JOBS
-- =====================================================

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    
    -- Source
    source VARCHAR(100) NOT NULL,  -- linkedin, indeed, glassdoor, etc.
    url TEXT UNIQUE NOT NULL,
    external_id VARCHAR(255),  -- Job ID from source platform
    
    -- Basic info
    title VARCHAR(500) NOT NULL,
    company VARCHAR(255) NOT NULL,
    company_url VARCHAR(500),
    location VARCHAR(255),
    is_remote BOOLEAN DEFAULT false,
    employment_type VARCHAR(50),  -- full-time, contract, part-time
    seniority_level VARCHAR(50),  -- entry, mid, senior, lead, principal
    
    -- Dates
    posted_date TIMESTAMP,
    deadline_date TIMESTAMP,
    first_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Content
    raw_text TEXT,
    description TEXT,
    requirements TEXT,
    responsibilities TEXT,
    benefits TEXT,
    
    -- Parsed data (structured)
    parsed_json JSONB DEFAULT '{}'::jsonb,
    -- {
    --   "required_skills": [],
    --   "preferred_skills": [],
    --   "tech_stack": [],
    --   "salary_min": 0,
    --   "salary_max": 0,
    --   "salary_currency": "USD",
    --   "experience_min_years": 0,
    --   "experience_max_years": 0,
    --   "education_required": "",
    --   "visa_sponsorship": false
    -- }
    
    -- Analysis
    is_scam BOOLEAN DEFAULT false,
    scam_score INTEGER CHECK (scam_score >= 0 AND scam_score <= 100),
    scam_flags JSONB DEFAULT '[]'::jsonb,
    -- [
    --   "suspicious_email", "payment_request", "unrealistic_salary",
    --   "missing_company_info", "free_email_domain"
    -- ]
    
    -- Content hashing for deduplication
    content_hash VARCHAR(64),  -- SHA256 of normalized content
    fingerprint VARCHAR(64),   -- Perceptual hash
    
    -- Status
    status VARCHAR(50) DEFAULT 'scraped',
    -- scraped, matched, applying, applied, rejected, offer, ignored
    
    -- Timestamps
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_jobs_source ON jobs(source);
CREATE INDEX idx_jobs_url ON jobs(url);
CREATE INDEX idx_jobs_company ON jobs(company);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_posted_date ON jobs(posted_date);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_is_scam ON jobs(is_scam);
CREATE INDEX idx_jobs_content_hash ON jobs(content_hash);
CREATE INDEX idx_jobs_scraped_at ON jobs(scraped_at DESC);

-- GIN index for JSONB queries
CREATE INDEX idx_jobs_parsed_json ON jobs USING GIN (parsed_json);

-- =====================================================
-- MATCH SCORES
-- =====================================================

CREATE TABLE match_scores (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    resume_id INTEGER NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Overall score
    total_score INTEGER NOT NULL CHECK (total_score >= 0 AND total_score <= 100),
    
    -- Breakdown
    required_skills_score INTEGER CHECK (required_skills_score >= 0 AND required_skills_score <= 100),
    preferred_skills_score INTEGER CHECK (preferred_skills_score >= 0 AND preferred_skills_score <= 100),
    project_alignment_score INTEGER CHECK (project_alignment_score >= 0 AND project_alignment_score <= 100),
    experience_score INTEGER CHECK (experience_score >= 0 AND experience_score <= 100),
    education_score INTEGER CHECK (education_score >= 0 AND education_score <= 100),
    keyword_density_score INTEGER CHECK (keyword_density_score >= 0 AND keyword_density_score <= 100),
    ats_simulation_score INTEGER CHECK (ats_simulation_score >= 0 AND ats_simulation_score <= 100),
    
    -- Details
    matched_skills JSONB DEFAULT '[]'::jsonb,
    missing_skills JSONB DEFAULT '[]'::jsonb,
    match_breakdown JSONB DEFAULT '{}'::jsonb,
    
    -- Timestamps
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(job_id, resume_id)
);

CREATE INDEX idx_match_scores_job ON match_scores(job_id);
CREATE INDEX idx_match_scores_resume ON match_scores(resume_id);
CREATE INDEX idx_match_scores_user ON match_scores(user_id);
CREATE INDEX idx_match_scores_total ON match_scores(total_score DESC);

-- =====================================================
-- PROJECTS
-- =====================================================

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER REFERENCES jobs(id) ON DELETE SET NULL,  -- Associated job
    
    -- Project info
    title VARCHAR(500) NOT NULL,
    description TEXT,
    detailed_description TEXT,
    tech_stack JSONB DEFAULT '[]'::jsonb,  -- ["Python", "React", "PostgreSQL"]
    
    -- Links
    link VARCHAR(1000),  -- GitHub, live demo, etc.
    github_url VARCHAR(500),
    demo_url VARCHAR(500),
    
    -- Source
    source VARCHAR(100),  -- github, huggingface, kaggle, arxiv, custom
    external_id VARCHAR(255),
    
    -- Classification
    is_autogenerated BOOLEAN DEFAULT false,
    is_verified BOOLEAN DEFAULT false,
    confidence_score DECIMAL(5,2),  -- How confident we are this matches
    
    -- Metadata
    metadata_json JSONB DEFAULT '{}'::jsonb,
    -- {
    --   "stars": 0,
    --   "forks": 0,
    --   "language": "",
    --   "topics": [],
    --   "reason_matched": "",
    --   "jd_keywords_matched": []
    -- }
    
    -- Timestamps
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_job ON projects(job_id);
CREATE INDEX idx_projects_source ON projects(source);
CREATE INDEX idx_projects_autogenerated ON projects(is_autogenerated);
CREATE INDEX idx_projects_tech_stack ON projects USING GIN (tech_stack);

-- =====================================================
-- COVER LETTERS
-- =====================================================

CREATE TABLE cover_letters (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    resume_id INTEGER NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    
    -- Content
    content TEXT NOT NULL,
    format VARCHAR(20) DEFAULT 'text',  -- text, html, markdown
    
    -- Generation params
    personality VARCHAR(50) NOT NULL,
    -- professional, friendly, technical, direct, creative, relocation_friendly
    
    template_used VARCHAR(100),
    llm_model VARCHAR(100),  -- gpt-4, claude-3, gemini-pro
    
    -- Quality metrics
    word_count INTEGER,
    readability_score DECIMAL(5,2),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_cover_letters_user ON cover_letters(user_id);
CREATE INDEX idx_cover_letters_job ON cover_letters(job_id);
CREATE INDEX idx_cover_letters_personality ON cover_letters(personality);

-- =====================================================
-- APPLICATIONS
-- =====================================================

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    resume_id INTEGER NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    cover_letter_id INTEGER REFERENCES cover_letters(id) ON DELETE SET NULL,
    
    -- Application mode
    is_sandbox BOOLEAN DEFAULT true,  -- Sandbox vs live application
    requires_approval BOOLEAN DEFAULT true,
    approved_by_user BOOLEAN DEFAULT false,
    approved_at TIMESTAMP,
    
    -- Submission
    status VARCHAR(50) DEFAULT 'draft',
    -- draft, pending_approval, approved, submitted, interview_scheduled,
    -- interview_completed, offer_received, offer_accepted, offer_declined,
    -- rejected, withdrawn
    
    status_history JSONB DEFAULT '[]'::jsonb,
    -- [
    --   {"status": "draft", "timestamp": "2024-01-01T00:00:00Z"},
    --   {"status": "submitted", "timestamp": "2024-01-02T00:00:00Z"}
    -- ]
    
    -- Form data
    form_data JSONB DEFAULT '{}'::jsonb,
    -- Captured form fields for this application
    
    additional_documents JSONB DEFAULT '[]'::jsonb,
    -- [{"name": "portfolio.pdf", "url": "...", "type": "pdf"}]
    
    -- Response & confirmation
    confirmation_number VARCHAR(255),
    confirmation_email TEXT,
    response_content TEXT,
    response_received_at TIMESTAMP,
    
    -- Screenshots & evidence
    screenshot_urls JSONB DEFAULT '[]'::jsonb,
    -- ["s3://bucket/screenshot1.png", "s3://bucket/screenshot2.png"]
    
    -- Metadata
    metadata_json JSONB DEFAULT '{}'::jsonb,
    -- {
    --   "user_agent": "",
    --   "ip_address": "",
    --   "referrer": "",
    --   "captcha_encountered": false,
    --   "manual_intervention_required": false,
    --   "error_logs": []
    -- }
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_applications_user ON applications(user_id);
CREATE INDEX idx_applications_job ON applications(job_id);
CREATE INDEX idx_applications_status ON applications(status);
CREATE INDEX idx_applications_submitted_at ON applications(submitted_at DESC);
CREATE INDEX idx_applications_is_sandbox ON applications(is_sandbox);

-- =====================================================
-- USER MONITORING PREFERENCES
-- =====================================================

CREATE TABLE monitoring_configs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Search criteria
    regions JSONB DEFAULT '[]'::jsonb,  -- ["Remote", "New York", "San Francisco"]
    roles JSONB DEFAULT '[]'::jsonb,    -- ["Software Engineer", "Backend Engineer"]
    platforms JSONB DEFAULT '[]'::jsonb, -- ["linkedin", "indeed", "glassdoor"]
    
    -- Filters
    min_salary INTEGER,
    max_salary INTEGER,
    employment_types JSONB DEFAULT '[]'::jsonb,  -- ["full-time", "contract"]
    remote_only BOOLEAN DEFAULT false,
    
    -- Scoring thresholds
    min_match_score INTEGER DEFAULT 70,
    auto_apply_threshold INTEGER DEFAULT 85,
    
    -- Schedule
    scrape_interval_minutes INTEGER DEFAULT 60,
    is_active BOOLEAN DEFAULT true,
    
    -- Cover letter preference
    default_personality VARCHAR(50) DEFAULT 'professional',
    
    -- Notifications
    email_notifications BOOLEAN DEFAULT true,
    webhook_url VARCHAR(500),
    slack_webhook_url VARCHAR(500),
    discord_webhook_url VARCHAR(500),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_run_at TIMESTAMP,
    
    UNIQUE(user_id)
);

CREATE INDEX idx_monitoring_configs_user ON monitoring_configs(user_id);
CREATE INDEX idx_monitoring_configs_active ON monitoring_configs(is_active);

-- =====================================================
-- ANALYTICS & METRICS
-- =====================================================

CREATE TABLE daily_metrics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    
    -- Counts
    jobs_scraped INTEGER DEFAULT 0,
    jobs_matched INTEGER DEFAULT 0,
    jobs_high_match INTEGER DEFAULT 0,  -- score >= 80
    applications_submitted INTEGER DEFAULT 0,
    interviews_scheduled INTEGER DEFAULT 0,
    offers_received INTEGER DEFAULT 0,
    
    -- Quality
    scams_detected INTEGER DEFAULT 0,
    duplicates_avoided INTEGER DEFAULT 0,
    
    -- Response rates
    response_rate DECIMAL(5,2),  -- % of applications that got response
    interview_rate DECIMAL(5,2), -- % of applications that led to interview
    offer_rate DECIMAL(5,2),     -- % of applications that led to offer
    
    -- Average scores
    avg_match_score DECIMAL(5,2),
    avg_ats_score DECIMAL(5,2),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(user_id, date)
);

CREATE INDEX idx_daily_metrics_user ON daily_metrics(user_id);
CREATE INDEX idx_daily_metrics_date ON daily_metrics(date DESC);

-- =====================================================
-- SKILL ANALYTICS
-- =====================================================

CREATE TABLE skill_demand (
    id SERIAL PRIMARY KEY,
    skill_name VARCHAR(255) NOT NULL,
    period_start DATE NOT NULL,
    period_end DATE NOT NULL,
    
    -- Counts
    total_jobs INTEGER DEFAULT 0,
    as_required INTEGER DEFAULT 0,
    as_preferred INTEGER DEFAULT 0,
    
    -- Salary correlation
    avg_salary_usd INTEGER,
    median_salary_usd INTEGER,
    
    -- Trends
    trend VARCHAR(20),  -- growing, stable, declining
    trend_percentage DECIMAL(5,2),
    
    -- Top companies
    top_companies JSONB DEFAULT '[]'::jsonb,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(skill_name, period_start, period_end)
);

CREATE INDEX idx_skill_demand_name ON skill_demand(skill_name);
CREATE INDEX idx_skill_demand_period ON skill_demand(period_start, period_end);
CREATE INDEX idx_skill_demand_total_jobs ON skill_demand(total_jobs DESC);

-- =====================================================
-- AUDIT LOG
-- =====================================================

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- Event
    event_type VARCHAR(100) NOT NULL,
    -- user_login, job_scraped, application_submitted, manual_override, etc.
    
    event_category VARCHAR(50),  -- auth, scraping, application, system
    severity VARCHAR(20) DEFAULT 'info',  -- debug, info, warning, error, critical
    
    -- Details
    description TEXT,
    entity_type VARCHAR(100),  -- job, application, resume, etc.
    entity_id INTEGER,
    
    -- Context
    metadata JSONB DEFAULT '{}'::jsonb,
    -- {
    --   "ip_address": "",
    --   "user_agent": "",
    --   "request_id": "",
    --   "session_id": ""
    -- }
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);
CREATE INDEX idx_audit_logs_severity ON audit_logs(severity);

-- =====================================================
-- NOTIFICATIONS
-- =====================================================

CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Notification details
    type VARCHAR(50) NOT NULL,
    -- new_match, high_match, application_submitted, interview_scheduled,
    -- offer_received, scam_detected, system_alert
    
    priority VARCHAR(20) DEFAULT 'normal',  -- low, normal, high, urgent
    
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    
    -- Links
    link_url VARCHAR(500),
    link_text VARCHAR(100),
    
    -- References
    job_id INTEGER REFERENCES jobs(id) ON DELETE SET NULL,
    application_id INTEGER REFERENCES applications(id) ON DELETE SET NULL,
    
    -- Status
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP,
    
    -- Delivery
    sent_via_email BOOLEAN DEFAULT false,
    sent_via_webhook BOOLEAN DEFAULT false,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_is_read ON notifications(is_read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at DESC);

-- =====================================================
-- WEBHOOK EVENTS
-- =====================================================

CREATE TABLE webhook_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    
    -- Event
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL,
    
    -- Delivery status
    delivery_status VARCHAR(50) DEFAULT 'pending',
    -- pending, sent, failed, retry
    
    delivery_attempts INTEGER DEFAULT 0,
    last_attempt_at TIMESTAMP,
    next_retry_at TIMESTAMP,
    
    -- Response
    response_status_code INTEGER,
    response_body TEXT,
    error_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    delivered_at TIMESTAMP
);

CREATE INDEX idx_webhook_events_user ON webhook_events(user_id);
CREATE INDEX idx_webhook_events_status ON webhook_events(delivery_status);
CREATE INDEX idx_webhook_events_next_retry ON webhook_events(next_retry_at);

-- =====================================================
-- TRIGGERS FOR UPDATED_AT
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_resumes_updated_at BEFORE UPDATE ON resumes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_applications_updated_at BEFORE UPDATE ON applications
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_monitoring_configs_updated_at BEFORE UPDATE ON monitoring_configs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VIEWS FOR COMMON QUERIES
-- =====================================================

-- Active high-match jobs
CREATE VIEW v_high_match_jobs AS
SELECT 
    j.*,
    ms.total_score as match_score,
    ms.matched_skills,
    ms.missing_skills,
    u.id as user_id
FROM jobs j
JOIN match_scores ms ON j.id = ms.job_id
JOIN users u ON ms.user_id = u.id
WHERE 
    j.is_scam = false 
    AND ms.total_score >= 80
    AND j.status NOT IN ('applied', 'rejected', 'ignored')
ORDER BY ms.total_score DESC, j.posted_date DESC;

-- Application funnel
CREATE VIEW v_application_funnel AS
SELECT 
    u.id as user_id,
    u.email,
    COUNT(DISTINCT CASE WHEN j.status = 'scraped' THEN j.id END) as total_jobs,
    COUNT(DISTINCT CASE WHEN ms.total_score >= 70 THEN j.id END) as matched_jobs,
    COUNT(DISTINCT a.id) as total_applications,
    COUNT(DISTINCT CASE WHEN a.status = 'interview_scheduled' THEN a.id END) as interviews,
    COUNT(DISTINCT CASE WHEN a.status = 'offer_received' THEN a.id END) as offers,
    ROUND(
        COUNT(DISTINCT CASE WHEN a.status = 'interview_scheduled' THEN a.id END)::DECIMAL / 
        NULLIF(COUNT(DISTINCT a.id), 0) * 100, 
        2
    ) as interview_rate,
    ROUND(
        COUNT(DISTINCT CASE WHEN a.status = 'offer_received' THEN a.id END)::DECIMAL / 
        NULLIF(COUNT(DISTINCT a.id), 0) * 100, 
        2
    ) as offer_rate
FROM users u
LEFT JOIN jobs j ON true
LEFT JOIN match_scores ms ON j.id = ms.job_id AND u.id = ms.user_id
LEFT JOIN applications a ON u.id = a.user_id
GROUP BY u.id, u.email;

-- =====================================================
-- SAMPLE DATA SEEDING (for development)
-- =====================================================

-- Insert a test user
INSERT INTO users (email, hashed_password, full_name)
VALUES ('demo@careerAgent.com', '$2b$12$example_hash', 'Demo User')
ON CONFLICT DO NOTHING;
