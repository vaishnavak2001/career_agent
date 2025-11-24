# 🚀 **QUICK START GUIDE - Testing Your Fixed System**

**Career Agent - Getting Started After Phase 1 Fixes**

---

## ✅ **Prerequisites Verified**

You already have:
- ✅ Python 3.14.0 installed
- ✅ Node.js 24.11.1 installed
- ✅ PostgreSQL database (Supabase) connected
- ✅ All dependencies in requirements.txt
- ✅ Core infrastructure fixed and working

---

## 🎯 **Step 1: Start the Backend API** (2 minutes)

### **Option A: Standard Start**
```bash
cd c:\Users\AK\Documents\anti gravity test1\career_agent
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### **Option B: With Detailed Logs**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --log-level debug
```

**Expected Output:**
```
[DB] Resolved 13.239.87.90 -> 13.239.87.90 (IPv4)
[DB] Database: postgresql://postgres.crloioefsqqqlthbnrka:...
[DB] Engine: PostgreSQL
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### **Test It:**
Open browser: http://127.0.0.1:8000

You should see:
```json
{
  "message": "Welcome to the Autonomous AI Job Application Agent API"
}
```

---

## 🧪 **Step 2: Test API Endpoints** (5 minutes)

### **Quick Test with Browser:**
1. **Root:** http://127.0.0.1:8000
2. **Health:** http://127.0.0.1:8000/health
3. **Docs:** http://127.0.0.1:8000/docs (Interactive API docs)
4. **Jobs:** http://127.0.0.1:8000/api/v1/jobs/
5. **Dashboard:** http://127.0.0.1:8000/api/v1/dashboard/stats

### **Full Test with Script:**
```bash
python test_api.py
```

**Expected:**
```
[TEST] Testing root endpoint...
[SUCCESS] Root endpoint working

[TEST] Testing jobs endpoint...
[SUCCESS] Jobs endpoint working (0 jobs found - database is empty)

[TEST] Testing dashboard stats...
[SUCCESS] Dashboard endpoint working
{
  "jobs_scraped": 0,
  "applications_sent": 0,
  "interviews": 0,
  "scams_blocked": 0
}
```

---

## 🎨 **Step 3: Start the Frontend** (3 minutes)

### **Navigate to Frontend:**
```bash
cd frontend
```

### **Install Dependencies (if needed):**
```bash
npm install
```

### **Start Development Server:**
```bash
npm run dev
```

**Expected Output:**
```
VITE v5.1.0  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

### **Open in Browser:**
http://localhost:5173

You should see the Job Listing page (currently empty as no jobs in database).

---

## 📊 **Step 4: Add Test Data** (5 minutes)

### **Option A: Use Seed Script**
```bash
cd c:\Users\AK\Documents\anti gravity test1\career_agent
python seed_jobs.py
```

### **Option B: Via API (using /docs page)**
1. Go to: http://127.0.0.1:8000/docs
2. Find `POST /api/v1/jobs/scrape`
3. Click "Try it out"
4. Set parameters:
   - `region`: "Remote"
   - `role`: "Software Engineer"
5. Click "Execute"

**This will:**
- Call Adzuna API
- Scrape real jobs
- Save to database
- Calculate match scores

---

## 🔍 **Step 5: Verify Everything Works** (5 minutes)

### **Check 1: Jobs in Database**
```bash
# Option 1: Via API
curl http://127.0.0.1:8000/api/v1/jobs/

# Option 2: Via browser
http://127.0.0.1:8000/api/v1/jobs/
```

Should return JSON array of jobs.

### **Check 2: Frontend Displays Jobs**
1. Refresh: http://localhost:5173
2. You should see job cards
3. Click on a job to see details

### **Check 3: Dashboard Stats Updated**
```bash
curl http://127.0.0.1:8000/api/v1/dashboard/stats
```

Should show:
```json
{
  "jobs_scraped": 5,  // or however many were scraped
  "applications_sent": 0,
  "interviews": 0,
  "scams_blocked": 0
}
```

---

## 🚧 **Common Issues & Fixes**

### **Issue: Port Already in Use**
```
ERROR: [Errno 10048] error while attempting to bind on address
```

**Fix:**
```bash
# Use different port
uvicorn app.main:app --reload --port 8001
```

### **Issue: Frontend Can't Connect to API**
**Check:**
1. Backend is running on http://127.0.0.1:8000
2. CORS is configured correctly (check `.env`)
3. Frontend `.env.local` has correct API URL

**Fix Frontend API URL:**
Edit `frontend/.env.local`:
```
VITE_API_URL=http://127.0.0.1:8000/api/v1
```

Restart frontend:
```bash
npm run dev
```

### **Issue: Database Connection Error**
**Check `.env` file:**
```
DATABASE_URL=postgresql://postgres.crloioefsqqqlthbnrka:%40Vaishnav321@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
```

Make sure password is URL-encoded (`@` → `%40`).

---

## 📝 **What You Should See**

### **Backend (Terminal 1):**
```
INFO:     127.0.0.1:xxxxx - "GET /api/v1/jobs/ HTTP/1.1" 200 OK
INFO:     127.0.0.1:xxxxx - "GET /api/v1/dashboard/stats HTTP/1.1" 200 OK
```

### **Frontend (Terminal 2):**
```
  ➜  Local:   http://localhost:5173/
  VITE ready in 100 ms
```

### **Browser (localhost:5173):**
- Job listing page with search bar
- Job cards showing: title, company, location, match score
- Filters sidebar
- Navigation: Jobs, Dashboard, Resumes, Settings

---

## 🎯 **Next Actions**

After verifying everything works:

1. **Test Resume Upload:**
   - Go to http://localhost:5173/resumes
   - Upload a test resume
   - Verify it appears in database

2. **Test Application Flow:**
   - Click on a job
   - Click "Apply"
   - Check applications endpoint: http://127.0.0.1:8000/api/v1/applications/

3. **Test Scraping:**
   - Trigger scrape via API docs
   - Watch terminal for logs
   - Verify new jobs appear

4. **Explore API Docs:**
   - http://127.0.0.1:8000/docs
   - Try different endpoints
   - Test POST/PUT operations

---

## 🆘 **Need Help?**

### **Check Logs:**
- Backend: Terminal where uvicorn is running
- Frontend: Browser console (F12)
- Database: `[DB]` prefixed messages

### **Verify Imports:**
```bash
python -c "from app.models import Job; print('[OK] Models working')"
python -c "from app.database import engine; print('[OK] Database working')"
python -c "from app.core.config import settings; print('[OK] Config working')"
```

### **Check Database Tables:**
```bash
python -c "from app.database import engine; from sqlalchemy import inspect; print('Tables:', inspect(engine).get_table_names())"
```

Should output:
```
Tables: ['daily_metrics', 'jobs', 'users', 'cover_letters', 'projects', 'resumes', 'applications']
```

---

## ✅ **Success Checklist**

Before moving to Phase 2, verify:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Root endpoint returns welcome message
- [ ] /docs page loads (Swagger UI)
- [ ] Jobs endpoint returns empty array or jobs
- [ ] Dashboard stats return valid JSON
- [ ] Frontend displays without errors
- [ ] Can trigger job scraping
- [ ] Jobs appear in UI after scraping
- [ ] Database has correct tables

**If all checked ✅ → You're ready for Phase 2!**

---

## 🚀 **Quick Commands Reference**

```bash
# Start Backend
uvicorn app.main:app --reload

# Start Frontend
cd frontend && npm run dev

# Test API
python test_api.py

# Reset Database
echo yes | python reset_database.py

# Fix Imports (if needed)
python fix_imports.py

# Check Python Setup
python --version
python -c "from app.models import Job; print('OK')"

# Check Node Setup
node --version
cd frontend && npm --version
```

---

**Ready to start testing!** 🎉

Run this:
```bash
uvicorn app.main:app --reload
```

Then open: http://127.0.0.1:8000/docs
