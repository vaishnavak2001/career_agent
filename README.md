# Autonomous AI Job Application Agent

A full-stack AI-powered career agent that automatically finds, scores, and applies to relevant job listings.

## 🚀 Features

- **Continuous Job Monitoring**: Scrapes jobs from Indeed, LinkedIn, Glassdoor
- **Smart Matching**: AI-powered match scoring (0-100) based on skills, experience, projects
- **Resume Enhancement**: Auto-tailors resumes for each job with relevant projects
- **Cover Letter Generation**: Creates personalized cover letters with multiple personalities
- **Scam Detection**: Identifies suspicious job postings
- **Auto-Apply**: Browser automation for application submission (sandbox mode included)
- **Real-time Dashboard**: Analytics, metrics, application tracking
- **Indeed-like UI**: Clean, responsive React interface

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
│  Tailwind CSS   │
└────────┬────────┘
         │ REST API
┌────────▼────────┐
│  FastAPI Backend│  (Port 8000)
│  + LangChain    │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬─────────┐
    ▼         ▼          ▼         ▼
 SQLite   Playwright  LLM API  Services
  (DB)    (Browser)  (OpenAI)  (Scraper)
```

## 📦 Tech Stack

- **Backend**: FastAPI, Python 3.10+
- **Frontend**: React 19, Vite, Tailwind CSS
- **Database**: SQLite (development), PostgreSQL (production)
- **AI/ML**: LangChain, OpenAI/Anthropic
- **Browser Automation**: Playwright
- **Deployment**: Railway/Render (backend), Vercel (frontend)

## 🛠️ Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd career_agent
```

2. **Backend Setup**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium

# Initialize database
python -m app.init_db

# Seed with sample data (optional)
python seed_jobs.py

# Start backend server
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

3. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

4. **Environment Variables**

Create `.env` file in root:
```env
DATABASE_URL=sqlite:///./career_agent.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=your-openai-key-here  # Optional
```

## 🎯 Usage

1. **Access the UI**: Open `http://localhost:3000`
2. **View Jobs**: Browse scraped jobs with match scores
3. **Upload Resume**: Add your base resume
4. **Configure Settings**: Set preferences (region, roles, thresholds)
5. **Auto-Apply**: Enable/disable auto-application feature
6. **Monitor Progress**: Check dashboard for analytics

## 📚 API Endpoints

- `GET /api/v1/jobs/` - List all jobs
- `POST /api/v1/jobs/scrape` - Trigger job scraping
- `GET /api/v1/resumes/` - List resumes
- `POST /api/v1/resumes/upload` - Upload new resume
- `GET /api/v1/applications/` - List applications
- `POST /api/v1/applications/apply/{job_id}` - Apply to job

## 🗂️ Project Structure

```
career_agent/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── core/
│   │   └── config.py        # Configuration
│   ├── db/
│   │   ├── models.py        # Database models  
│   │   └── session.py       # DB connection
│   ├── api/
│   │   ├── api.py           # Router config
│   │   └── endpoints/       # API routes
│   ├── services/
│   │   ├── scraper.py       # Job scraping
│   │   ├── parser.py        # JD parsing
│   │   ├── matcher.py       # Match scoring
│   │   ├── auto_apply.py    # Application automation
│   │   └── scam_detector.py # Scam detection
│   └── agent/
│       └── tools.py         # LangChain tools
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/      # UI components
│   │   ├── pages/           # Page components
│   │   └── services/        # API client
│   └── package.json
├── requirements.txt
├── .env
└── README.md
```

## 🔒 Security & Ethics

- **User Privacy**: All data encrypted at rest
- **No Fabrication**: Never creates fake employment history
- **Transparent Projects**: Auto-generated projects clearly labeled
- **Rate Limiting**: Respects robots.txt and site ToS
- **CAPTCHA Handling**: Prompts user instead of bypassing
- **Opt-in Features**: User control over auto-apply and data sharing

## 🚢 Deployment

### Free-Tier Deployment

**Database**: Neon or Supabase (PostgreSQL free tier)
```bash
# Update .env with production DATABASE_URL
DATABASE_URL=postgresql://user:pass@host:5432/db
```

**Backend**: Deploy to Railway/Render
```bash
# Push to GitHub, connect to Railway/Render
git push origin main
```

**Frontend**: Deploy to Vercel
```bash
cd frontend
vercel --prod
```

**CI/CD**: GitHub Actions automatically builds and deploys on push to main

## 📊 Database Schema

- **users**: User accounts and settings
- **jobs**: Scraped job listings
- **resumes**: Resume versions
- **projects**: Relevant projects (real + autogenerated)
- **applications**: Application tracking
- **activity_logs**: Audit trail

## 🧪 Testing

```bash
# Backend tests
pytest

# Frontend tests  
cd frontend
npm test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes  
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - See LICENSE file

## 🙋 Support

For issues and questions, please open a GitHub issue.

---

Built with ❤️ using FastAPI, React, and LangChain
