# Career Agent - Quick Start Guide 🚀

## ⚡ Super Quick Start (30 seconds)

**Your server is ALREADY RUNNING!** 🎉

Just open your browser and go to:
```
http://127.0.0.1:8000
```

That's it! The application is ready to use right now.

---

## 📖 Complete Setup Guide (First Time Users)

### Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version
   ```
   Should show: `Python 3.8+`

2. **pip** (Python package manager)
   ```bash
   pip --version
   ```

---

## 🔧 Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd "c:\Users\AK\Documents\anti gravity test1\career_agent"
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**What this installs:**
- FastAPI (Web framework)
- SQLAlchemy (Database)
- APScheduler (Background tasks)
- BeautifulSoup4 (Web scraping)
- Pandas (Data processing)
- And more...

**Installation time:** ~2-3 minutes

---

## 🎯 Running the Application

### Method 1: Standard Start (Recommended)

```bash
python -m uvicorn app.main:app --reload
```

**What this does:**
- `app.main:app` - Loads the FastAPI application
- `--reload` - Auto-restarts when code changes
- Runs on: http://127.0.0.1:8000

### Method 2: With Custom Port

```bash
python -m uvicorn app.main:app --reload --port 8001
```

### Method 3: Production Mode (No auto-reload)

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🌐 Accessing the Application

Once the server starts, you'll see:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Access Points:**

1. **Main Web UI:**
   ```
   http://127.0.0.1:8000
   ```
   The beautiful Indeed-style interface

2. **API Documentation (Swagger):**
   ```
   http://127.0.0.1:8000/docs
   ```
   Interactive API testing

3. **Alternative API Docs (ReDoc):**
   ```
   http://127.0.0.1:8000/redoc
   ```
   Clean API documentation

---

## 🎨 Using the Web Interface

### Navigation Tabs

1. **Jobs** 📋
   - Search for jobs
   - View match scores
   - Save favorites
   - Apply to positions

2. **Saved** 💾
   - Your bookmarked jobs
   - Quick access to favorites

3. **Applications** ✅
   - Track submitted applications
   - Filter by status
   - View timeline

4. **Analytics** 📊
   - Dashboard metrics
   - Database statistics
   - Match distribution
   - Top skills & companies

5. **Monitoring** ⏰
   - Start/stop continuous scraping
   - Configure monitoring
   - Email notifications
   - View logs

6. **Resume** 📄
   - Edit your resume
   - Search for projects
   - View version history

---

## 🔍 Quick Feature Tour

### Searching for Jobs

1. Enter job title (e.g., "Python Developer")
2. Enter location (e.g., "Remote" or "New York")
3. Click "Find Jobs"
4. Jobs appear in main area

### Viewing Job Details

1. Click any job card
2. Modal opens with:
   - Full description
   - Required skills
   - Match score
   - Company info
3. Click "Apply Now" to generate cover letter

### Starting Continuous Monitoring

1. Go to **Monitoring** tab
2. Configure:
   - **Region:** Remote
   - **Role:** Software Engineer
   - **Platforms:** Check LinkedIn, Indeed
   - **Interval:** 60 minutes
3. Click "Save Configuration"
4. Click "Start Monitoring"
5. Watch status turn green with pulse animation

### Viewing Analytics

1. Go to **Analytics** tab
2. See:
   - Database connection info (top card)
   - 4 metric cards (Jobs, Matches, Applications, Projects)
   - Match score distribution chart
   - Application timeline
   - Top skills and companies

---

## 🛠️ Configuration (Optional)

### Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example file
cp .env.example .env
```

Edit `.env` with your preferences:

```bash
# Database (default: SQLite)
DATABASE_URL=sqlite:///./career_agent.db

# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/career_agent_db

# OpenAI (optional - for advanced features)
OPENAI_API_KEY=your_key_here

# Email Notifications (optional)
NOTIFICATIONS_ENABLED=false
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECIPIENT_EMAIL=your_email@gmail.com

# Monitoring
DEFAULT_SCRAPE_INTERVAL=60
DEFAULT_REGION=Remote
DEFAULT_ROLE=Software Engineer

# Safety
DRY_RUN=true  # Set to false to actually submit applications
MIN_MATCH_SCORE=70
```

---

## 🧪 Testing the Application

### Run the Test Suite

```bash
python test_api.py
```

**This tests:**
- All API endpoints
- Job scraping
- Match scoring
- Cover letter generation
- Dashboard metrics
- And more...

**Expected output:**
```
============================================================
Career Agent API Tests
============================================================

[1] Testing root endpoint... ✓
[2] Testing job scraping... ✓
[3] Listing scraped jobs... ✓
[4] Getting job details... ✓
[5] Analyzing job... ✓
[6] Calculating match score... ✓
[7] Generating cover letter... ✓
[8] Searching for projects... ✓
[9] Getting dashboard stats... ✓
[10] Getting match distribution... ✓

============================================================
All tests completed!
============================================================
```

---

## 📱 Using the API Directly

### Via cURL

**Scrape Jobs:**
```bash
curl -X POST "http://127.0.0.1:8000/jobs/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "New York",
    "role": "Backend Engineer",
    "platforms": ["LinkedIn", "Indeed"]
  }'
```

**Get Dashboard Stats:**
```bash
curl "http://127.0.0.1:8000/dashboard/stats"
```

**Generate Cover Letter:**
```bash
curl -X POST "http://127.0.0.1:8000/cover-letter/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "resume_text": "Your resume here...",
    "personality": "professional"
  }'
```

### Via Python

```python
import requests

# Scrape jobs
response = requests.post(
    "http://127.0.0.1:8000/jobs/scrape",
    json={
        "region": "San Francisco",
        "role": "Python Developer",
        "platforms": ["LinkedIn"]
    }
)
jobs = response.json()

# Get jobs
response = requests.get("http://127.0.0.1:8000/jobs")
all_jobs = response.json()

# Get dashboard stats
response = requests.get("http://127.0.0.1:8000/dashboard/stats")
stats = response.json()
```

---

## ⚙️ Advanced Features

### Continuous Monitoring

**Via API:**
```bash
# Configure monitoring
curl -X POST "http://127.0.0.1:8000/monitor/configure" \
  -H "Content-Type: application/json" \
  -d '{
    "region": "Remote",
    "role": "Software Engineer",
    "platforms": ["LinkedIn", "Indeed"],
    "interval_minutes": 60
  }'

# Start monitoring
curl -X POST "http://127.0.0.1:8000/monitor/start"

# Check status
curl "http://127.0.0.1:8000/monitor/status"

# Stop monitoring
curl -X POST "http://127.0.0.1:8000/monitor/stop"
```

### Email Notifications

**Test your email setup:**
```bash
curl -X POST "http://127.0.0.1:8000/notifications/test"
```

**Check config:**
```bash
curl "http://127.0.0.1:8000/notifications/config"
```

---

## 🔧 Troubleshooting

### Server Won't Start

**Error: "Address already in use"**
```bash
# Kill existing process
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use a different port:
python -m uvicorn app.main:app --reload --port 8001
```

**Error: "ModuleNotFoundError"**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Error: "No module named 'app'"**
```bash
# Make sure you're in the project directory
cd "c:\Users\AK\Documents\anti gravity test1\career_agent"
```

### Database Issues

**Reset database:**
```bash
# Delete the database file
del career_agent.db

# Restart server (tables auto-create)
python -m uvicorn app.main:app --reload
```

**Switch to PostgreSQL:**
```bash
# Edit .env
DATABASE_URL=postgresql://username:password@localhost/career_agent_db

# Restart server
```

### UI Not Loading

**Clear browser cache:**
- Press `Ctrl + Shift + R` (hard refresh)
- Or clear cache in browser settings

**Check server logs:**
- Look for errors in terminal where server is running

### No Jobs Appearing

**Scrape some jobs first:**
1. Go to http://127.0.0.1:8000
2. Enter job title and location
3. Click "Find Jobs"
4. Or use API: `POST /jobs/scrape`

---

## 🛑 Stopping the Server

**Press:** `CTRL + C` in the terminal

You'll see:
```
INFO:     Shutting down
INFO:     Waiting for application shutdown.
INFO:     Application shutdown complete.
INFO:     Finished server process
```

---

## 📊 Database Management

### Viewing Database Contents

**SQLite:**
```bash
# Install SQLite browser (optional)
# Or use Python:
python
>>> from app.database import SessionLocal
>>> from app.models import Job
>>> db = SessionLocal()
>>> jobs = db.query(Job).all()
>>> print(f"Total jobs: {len(jobs)}")
```

### Backup Database

**SQLite:**
```bash
# Copy the database file
copy career_agent.db career_agent_backup.db
```

**PostgreSQL:**
```bash
pg_dump career_agent_db > backup.sql
```

---

## 🎯 Common Workflows

### Daily Job Hunt Workflow

1. **Start server:** `python -m uvicorn app.main:app --reload`
2. **Open UI:** http://127.0.0.1:8000
3. **Configure monitoring:** Monitoring tab → Set preferences
4. **Start monitoring:** Click "Start Monitoring"
5. **Check Analytics:** View new jobs daily
6. **Apply to jobs:** Click jobs → Apply Now
7. **Track applications:** Applications tab

### One-Time Job Search

1. **Start server**
2. **Go to Jobs tab**
3. **Search:** Enter role + location → Find Jobs
4. **Filter:** Set minimum match score (e.g., 70%)
5. **Review:** Click job cards to see details
6. **Apply:** Generate cover letter → Submit

### Resume Enhancement

1. **Go to Resume tab**
2. **Paste resume:** In text area
3. **Save:** Click "Save Resume"
4. **Search projects:** Enter skills → Search Projects
5. **View versions:** Click "View History"

---

## 📚 Documentation

- **README.md** - Project overview
- **COMPLIANCE_REPORT.md** - 100% requirements verification
- **V2_UPDATE_SUMMARY.md** - Version 2.0 features
- **UI_V3_ENHANCEMENTS.md** - Version 3.0 UI details
- **GAP_ANALYSIS.md** - Feature comparison
- **architecture.md** - System architecture
- **API Docs:** http://127.0.0.1:8000/docs

---

## ✅ Quick Checklist

Before running:
- [ ] Python 3.8+ installed
- [ ] In project directory
- [ ] Dependencies installed (`pip install -r requirements.txt`)

To start:
- [ ] Run: `python -m uvicorn app.main:app --reload`
- [ ] Wait for "Application startup complete"
- [ ] Open: http://127.0.0.1:8000

To use:
- [ ] Search for jobs
- [ ] View analytics
- [ ] Generate cover letters
- [ ] Start monitoring (optional)
- [ ] Configure email notifications (optional)

---

## 🎉 You're All Set!

The Career Agent is now running and ready to help you find your dream job!

**Server Location:** http://127.0.0.1:8000  
**Status:** ✅ RUNNING  
**Features:** All operational  
**UI:** Enhanced Indeed-style v3.0  

**Need help?** Check the documentation or API docs at `/docs`

---

## 🔥 Pro Tips

1. **Keep server running:** Set up continuous monitoring for passive job hunting
2. **Bookmark the UI:** Add http://127.0.0.1:8000 to browser favorites
3. **Use keyboard shortcuts:** Tab navigation with keyboard
4. **Check Analytics daily:** Monitor job market trends
5. **Customize match threshold:** Adjust to your preferences
6. **Enable notifications:** Get alerted for high-match jobs
7. **Use multiple platforms:** Enable LinkedIn, Indeed, and Glassdoor

---

**Happy job hunting! 🚀**
