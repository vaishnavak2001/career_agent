# Folder Structure

```
career_agent/
├── .github/                    # GitHub Actions workflows
│   └── workflows/
│       ├── deploy.yml          # CI/CD pipeline
│       └── test.yml            # Test runner
├── app/                        # Backend Application
│   ├── agent/                  # LangChain Agent logic
│   │   ├── agent.py            # Main agent definition
│   │   └── tools.py            # Tool definitions
│   ├── api/                    # API Endpoints
│   │   └── api.py              # Router configuration
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Settings and env vars
│   │   └── security.py         # Auth and security utils
│   ├── db/                     # Database
│   │   ├── init_db.py          # DB initialization
│   │   └── session.py          # DB session management
│   ├── models/                 # SQLAlchemy Models
│   │   └── models.py           # DB tables definition
│   ├── schemas/                # Pydantic Schemas
│   │   └── schemas.py          # Request/Response models
│   ├── services/               # Business Logic Services
│   │   ├── auto_apply.py       # Application submission logic
│   │   ├── cover_letter.py     # Cover letter generation
│   │   ├── matcher.py          # Job matching logic
│   │   ├── parser.py           # Resume/JD parsing
│   │   ├── project_finder.py   # Project search service
│   │   ├── resume_enhancer.py  # Resume tailoring
│   │   ├── scam_detector.py    # Scam detection logic
│   │   └── scraper.py          # Job scraping service
│   └── main.py                 # App entry point
├── frontend/                   # React Frontend
│   ├── public/                 # Static assets
│   ├── src/
│   │   ├── components/         # Reusable UI components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API client services
│   │   ├── App.jsx             # Main App component
│   │   └── index.css           # Global styles (Tailwind)
│   ├── package.json            # Frontend dependencies
│   └── vite.config.js          # Vite configuration
├── tests/                      # Test Suite
│   ├── test_api.py
│   └── test_services.py
├── .env.example                # Environment variables template
├── alembic.ini                 # DB Migration config
├── docker-compose.yml          # Local dev orchestration
├── requirements.txt            # Python dependencies
├── schema.sql                  # Database schema SQL
└── README.md                   # Project documentation
```
