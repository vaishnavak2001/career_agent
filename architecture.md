# 🏗️ Career Agent - Complete Architecture

## Folder Structure

```
career_agent/
├── .github/
│   └── workflows/
│       ├── ci.yml                    # Continuous Integration
│       ├── deploy-backend.yml        # Backend deployment
│       └── deploy-frontend.yml       # Frontend deployment
├── backend/
│   ├── alembic/                      # Database migrations
│   │   ├── versions/
│   │   └── env.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry
│   │   ├── config.py                 # Configuration management
│   │   ├── database.py               # DB connection
│   │   ├── dependencies.py           # Shared dependencies
│   │   ├── models/                   # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── resume.py
│   │   │   ├── project.py
│   │   │   ├── application.py
│   │   │   └── analytics.py
│   │   ├── schemas/                  # Pydantic schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── resume.py
│   │   │   ├── project.py
│   │   │   ├── application.py
│   │   │   └── tool_schemas.py       # Tool calling schemas
│   │   ├── api/                      # API routes
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── jobs.py
│   │   │   ├── resumes.py
│   │   │   ├── applications.py
│   │   │   ├── analytics.py
│   │   │   ├── agent.py
│   │   │   └── websocket.py
│   │   ├── core/                     # Core business logic
│   │   │   ├── __init__.py
│   │   │   ├── security.py           # Auth & encryption
│   │   │   ├── logging.py            # Logging config
│   │   │   └── rate_limiter.py       # Rate limiting
│   │   ├── agent/                    # LangChain agent
│   │   │   ├── __init__.py
│   │   │   ├── executor.py           # Agent executor
│   │   │   ├── prompts.py            # System prompts
│   │   │   ├── chains.py             # LangChain chains
│   │   │   └── memory.py             # Conversation memory
│   │   ├── tools/                    # LangChain tools
│   │   │   ├── __init__.py
│   │   │   ├── scraping/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── scraper.py        # scrape_jobs
│   │   │   │   ├── linkedin.py
│   │   │   │   ├── indeed.py
│   │   │   │   ├── glassdoor.py
│   │   │   │   └── robots_checker.py
│   │   │   ├── deduplication.py      # deduplicate_job
│   │   │   ├── scam_detection.py     # detect_scam
│   │   │   ├── jd_parser.py          # parse_jd
│   │   │   ├── match_scorer.py       # compute_match_score
│   │   │   ├── project_search.py     # search_projects
│   │   │   ├── resume_builder.py     # add_projects_to_resume
│   │   │   ├── resume_rewriter.py    # rewrite_resume_to_match_jd
│   │   │   ├── cover_letter.py       # generate_cover_letter
│   │   │   ├── form_filler.py        # submit_application
│   │   │   ├── storage.py            # store_* tools
│   │   │   └── analytics.py          # dashboard_metrics
│   │   ├── services/                 # External services
│   │   │   ├── __init__.py
│   │   │   ├── email.py              # Email service
│   │   │   ├── storage.py            # S3-compatible storage
│   │   │   ├── webhooks.py           # Webhook delivery
│   │   │   ├── github_api.py         # GitHub integration
│   │   │   ├── linkedin_api.py       # LinkedIn OAuth
│   │   │   └── captcha_handler.py    # CAPTCHA prompt
│   │   ├── scheduler/                # Background jobs
│   │   │   ├── __init__.py
│   │   │   ├── jobs.py               # APScheduler jobs
│   │   │   └── tasks.py              # Celery tasks (optional)
│   │   └── utils/                    # Utilities
│   │       ├── __init__.py
│   │       ├── embeddings.py         # Vector embeddings
│   │       ├── ats_simulator.py      # ATS scoring
│   │       ├── content_hashing.py    # Fingerprinting
│   │       └── validators.py         # Input validation
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_tools/
│   │   ├── test_api/
│   │   └── test_agent/
│   ├── scripts/
│   │   ├── setup.sh                  # Initial setup
│   │   ├── migrate.sh                # Run migrations
│   │   └── seed.py                   # Seed database
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── alembic.ini
├── frontend/
│   ├── public/
│   │   ├── index.html
│   │   ├── robots.txt
│   │   └── favicon.ico
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── index.css
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── Footer.jsx
│   │   │   ├── jobs/
│   │   │   │   ├── JobCard.jsx       # Indeed-style card
│   │   │   │   ├── JobList.jsx       # Infinite scroll
│   │   │   │   ├── JobDetail.jsx     # Detail modal
│   │   │   │   ├── JobFilters.jsx    # Search filters
│   │   │   │   └── MatchScoreBadge.jsx
│   │   │   ├── dashboard/
│   │   │   │   ├── Dashboard.jsx
│   │   │   │   ├── MetricCard.jsx
│   │   │   │   ├── Charts.jsx
│   │   │   │   └── Timeline.jsx
│   │   │   ├── resume/
│   │   │   │   ├── ResumeEditor.jsx
│   │   │   │   ├── ResumePreview.jsx
│   │   │   │   ├── ATSPreview.jsx
│   │   │   │   └── VersionHistory.jsx
│   │   │   ├── projects/
│   │   │   │   ├── ProjectSearch.jsx
│   │   │   │   ├── ProjectCard.jsx
│   │   │   │   └── ProjectSelector.jsx
│   │   │   ├── applications/
│   │   │   │   ├── ApplicationList.jsx
│   │   │   │   ├── ApplicationDetail.jsx
│   │   │   │   └── StatusTracker.jsx
│   │   │   ├── settings/
│   │   │   │   ├── Settings.jsx
│   │   │   │   ├── Preferences.jsx
│   │   │   │   ├── Integrations.jsx
│   │   │   │   └── Security.jsx
│   │   │   └── common/
│   │   │       ├── Button.jsx
│   │   │       ├── Modal.jsx
│   │   │       ├── Input.jsx
│   │   │       ├── Dropdown.jsx
│   │   │       └── Notification.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useJobs.js
│   │   │   ├── useWebSocket.js
│   │   │   └── useInfiniteScroll.js
│   │   ├── services/
│   │   │   ├── api.js               # Axios instance
│   │   │   ├── auth.js              # Auth service
│   │   │   ├── jobs.js              # Jobs API
│   │   │   └── websocket.js         # WebSocket client
│   │   ├── utils/
│   │   │   ├── formatters.js
│   │   │   ├── validators.js
│   │   │   └── constants.js
│   │   └── store/                   # State management (optional)
│   │       └── index.js
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   └── Dockerfile
├── infrastructure/
│   ├── terraform/                   # Infrastructure as Code
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── docker-compose.yml           # Local development
│   ├── docker-compose.prod.yml      # Production
│   └── k8s/                         # Kubernetes (optional)
│       ├── deployment.yaml
│       └── service.yaml
├── docs/
│   ├── API.md                       # API documentation
│   ├── ARCHITECTURE.md              # This file
│   ├── DEPLOYMENT.md                # Deployment guide
│   ├── DEVELOPMENT.md               # Dev setup guide
│   ├── TOOLS.md                     # Tool calling reference
│   └── LEGAL.md                     # Legal & ethics
├── .gitignore
├── .env.example
├── README.md
├── LICENSE
└── CONTRIBUTING.md
```

## Technology Stack

### Backend
- **Framework**: FastAPI 0.109+
- **Agent**: LangChain 0.1+
- **Database**: PostgreSQL 15+ (Neon/Supabase free tier)
- **ORM**: SQLAlchemy 2.0+ (async)
- **Migrations**: Alembic
- **LLM**: OpenAI GPT-4 / Anthropic Claude / Google Gemini
- **Browser Automation**: Playwright 1.40+
- **Task Queue**: APScheduler (or Celery for production)
- **Authentication**: OAuth2 + JWT
- **Email**: SendGrid / Mailgun (free tier)
- **Storage**: Supabase Storage / S3-compatible

### Frontend
- **Framework**: React 18+ with Vite
- **Styling**: Tailwind CSS 3+
- **State**: React Context / Zustand
- **HTTP Client**: Axios
- **WebSocket**: Socket.io-client
- **Charts**: Recharts / Chart.js
- **Forms**: React Hook Form
- **Routing**: React Router v6

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Backend Hosting**: Railway / Render / Fly.io (free tier)
- **Frontend Hosting**: Vercel / Netlify (free tier)
- **Monitoring**: Sentry (free tier)
- **Analytics**: PostHog (free tier, optional)

## Core Principles

1. **Ethics First**: Never fabricate, always transparent, user consent
2. **Legal Compliance**: robots.txt, ToS, rate limiting, CAPTCHA respect
3. **Privacy**: PII encrypted, user data deletion, GDPR-ready
4. **Scalability**: Async operations, queue-based processing
5. **Observability**: Comprehensive logging, metrics, alerts
6. **User Control**: Sandbox mode, manual approval, opt-in/out
