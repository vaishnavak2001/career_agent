# Quick Start Guide

## 🚀 Get Up and Running in 5 Minutes

### What You Have

A complete **Autonomous AI Job Application Agent** with:
- ✅ FastAPI backend (running on port 8000)
- ✅ React frontend (Tailwind CSS UI like Indeed.com)
- ✅ Job scraping with Playwright
- ✅ AI-powered match scoring
- ✅ Scam detection
- ✅ Auto-apply capability (sandbox mode)
- ✅ Database with sample jobs

### Current Status

**Backend**: ✅ Running at http://127.0.0.1:8000
```
The server is already running!
Access the API at: http://127.0.0.1:8000
API Documentation: http://127.0.0.1:8000/docs
```

**Frontend**: Ready to start
**Database**: Initialized with schema

---

## Step 1: Start the Frontend

Open a **new terminal**:

```bash
cd frontend
npm run dev
```

Frontend will be at: http://localhost:3000

## Step 2: View the System

### Option A: Browser
1. Open http://localhost:3000 in your browser
2. You'll see an Indeed-like job listing interface
3. Browse jobs with match scores

### Option B: API Testing
```bash
# Get all jobs
curl http://127.0.0.1:8000/api/v1/jobs/

# Or open in browser:
http://127.0.0.1:8000/docs  # Interactive API docs
```

## Step 3: Add Sample Data (if needed)

```bash
python seed_jobs.py
```

This adds 3 sample jobs with match scores to the database.

## Step 4: Test Features

### Test Job Scraping
```python
# In Python shell or script
import requests

response = requests.post(
    "http://127.0.0.1:8000/api/v1/jobs/scrape",
    params={"region": "San Francisco", "role": "Software Engineer"}
)
print(response.json())
```

### Test Match Scoring
The match scorer automatically runs when jobs are added. Check the `match_score` field in job records.

### Test Scam Detection
```python
from app.services.scam_detector import scam_detector_service

job = {
    "company": "Test Corp",
    "raw_text": "Great opportunity! Just pay a $500 processing fee..."
}

result = scam_detector_service.detect_scam(job)
print(result)  # Shows scam flags and score
```

---

## 📚 Key URLs

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://127.0.0.1:8000 | Main API endpoint |
| API Docs | http://127.0.0.1:8000/docs | Swagger UI |
| Frontend | http://localhost:3000 | React UI |

## 🗂️ Main Files to Know

### Backend Logic
- `app/main.py` - FastAPI entry point
- `app/services/scraper.py` - Job scraping
- `app/services/matcher.py` - Match scoring
- `app/services/scam_detector.py` - Scam detection
- `app/services/auto_apply.py` - Application automation

### Frontend
- `frontend/src/pages/JobListing.jsx` - Main UI
- `frontend/src/components/JobCard.jsx` - Job cards
- `frontend/src/services/api.js` - API client

### Database
- `career_agent.db` - SQLite database
- `app/db/models.py` - Schema definitions

## 🎯 Common Tasks

### Add More Sample Jobs
```bash
python seed_jobs.py
```

### Reset Database
```bash
# Delete database
rm career_agent.db

# Recreate
python -m app.init_db

# Add sample data
python seed_jobs.py
```

### Check API Status
```bash
curl http://127.0.0.1:8000/
# Returns: {"message":"Welcome to the Autonomous AI Job Application Agent API"}
```

### View Database
```bash
# Install DB browser
pip install sqlite-web

# Open database in browser
sqlite_web career_agent.db
```

## 🔧 Configuration

### Environment Variables (.env)
```env
DATABASE_URL=sqlite:///./career_agent.db
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...  # Optional for LLM features
```

### Enable LLM Features
1. Get OpenAI API key from https://platform.openai.com
2. Add to `.env`:
   ```env
   OPENAI_API_KEY=sk-...
   ```
3. Restart backend
4. LLM-powered parsing and cover letters will work

## 📊 What Each Service Does

### 1. Job Scraper (`scraper.py`)
- Scrapes jobs from Indeed, LinkedIn, etc.
- Uses Playwright for browser automation
- Respects robots.txt
- Returns structured job data

### 2. Match Scorer (`matcher.py`)
- Compares resume skills with job requirements
- Returns score 0-100
- Simple keyword matching (can be enhanced with embeddings)

### 3. Scam Detector (`scam_detector.py`)
- Checks for suspicious patterns
- Flags payment requests, free email domains
- Returns scam score and flags

### 4. Auto-Apply (`auto_apply.py`)
- Fills application forms automatically
- Takes screenshots for verification
- **Sandbox mode by default** (doesn't actually submit)
- Can be enabled for live applications

### 5. Resume Enhancer (`resume_enhancer.py`)
- Adds relevant projects to resume
- Tailors content to match job description
- Maintains version history

### 6. Cover Letter Generator (`cover_letter_generator.py`)
- Creates personalized cover letters
- Multiple personality styles
- LLM-powered when API key is provided

## 🎨 Frontend Features

- **Job Cards**: Indeed-style listings with match scores
- **Search & Filters**: By location, role, company
- **Responsive Design**: Works on mobile and desktop
- **Loading States**: Smooth user experience
- **Match Score Badges**: Visual indicators (color-coded)

## 🐛 Troubleshooting

### Frontend Won't Start
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Backend Port Already in Use
```bash
# Kill process on port 8000
# Windows:
taskkill /F /IM python.exe

# Then restart:
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Database Locked
```bash
# Close all connections, then:
rm career_agent.db
python -m app.init_db
```

## 🚀 Next Steps

1. **Add Your Resume**
   - Create resume upload endpoint
   - Parse and store in database

2. **Connect Real Job Boards**
   - Get Indeed API access
   - Configure LinkedIn OAuth

3. **Deploy to Production**
   - Follow DEPLOYMENT.md guide
   - Use free tiers: Railway + Vercel + Supabase

4. **Enable Auto-Apply**
   - Test in sandbox mode
   - Set `sandbox_mode = False` when ready
   - Monitor applications carefully

5. **Add Email Notifications**
   - Configure SendGrid API
   - Set up daily digests

## 📖 Documentation

- `README.md` - Project overview
- `ARCHITECTURE.md` - Technical design
- `DEPLOYMENT.md` - Deployment guide
- `IMPLEMENTATION_SUMMARY.md` - What's implemented

## 🎓 Learning the Codebase

**Start Here:**
1. Read `README.md` for overview
2. Check `ARCHITECTURE.md` for design
3. Explore `app/main.py` to see API structure
4. Look at `frontend/src/App.jsx` for UI

**Key Concepts:**
- FastAPI for async REST API
- SQLAlchemy ORM for database
- Playwright for browser automation
- LangChain for AI orchestration
- React + Tailwind for UI

## ✨ Features You Can Use Right Now

- ✅ View sample jobs in UI
- ✅ Browse with filters
- ✅ See match scores
- ✅ Test API endpoints
- ✅ Add jobs to database
- ✅ Detect job scams
- ✅ Generate cover letters (with API key)
- ✅ Track applications

## 🔒 Security Notes

- Sandbox mode is **ON by default** for auto-apply
- Never stores plain passwords (hashing ready)
- Scam detection runs on all jobs
- Rate limiting ready for production
- CORS configured for security

---

## Need Help?

1. Check `TROUBLESHOOTING.md` (if exists)
2. Review API docs: http://127.0.0.1:8000/docs
3. Open GitHub issue
4. Check implementation files for comments

**Happy Job Hunting! 🎯**
