# 🎯 Quick Start - Test Real Job APIs Locally

Before deploying, let's test the real job integrations on your local machine!

## Step 1: Get Adzuna API Keys (5 minutes)

1. Go to **https://developer.adzuna.com/**
2. Click **"Sign Up"** (completely free, no credit card)
3. Fill in basic details and verify email
4. Go to your **API Dashboard**
5. Copy these values:
   - **Application ID** (looks like: `12345678`)
   - **API Key** (looks like: `abcdef123456789...`)

## Step 2: Configure Environment (2 minutes)

1. **Copy the example file**:
   ```powershell
   copy .env.example .env
   ```

2. **Edit `.env` file** and add your Adzuna credentials:
   ```env
   ADZUNA_API_ID=YOUR_APP_ID_HERE
   ADZUNA_API_KEY=YOUR_API_KEY_HERE
   ```

3. **Save the file**

## Step 3: Install Dependencies (1 minute)

```powershell
pip install feedparser
```

## Step 4: Test Job APIs (1 minute)

Run the test script:

```powershell
python test_job_apis.py
```

### Expected Output:

```
🧪 🧪 🧪 ... REAL JOB API INTEGRATION TESTS

============================================================
🔍 Testing Adzuna API
============================================================
✅ Found 5 jobs from Adzuna

1. Senior Python Developer at TechCorp
   Location: New York, NY
   URL: https://www.adzuna.com/...

... more jobs ...

============================================================
🌍 Testing RemoteOK API
============================================================
✅ Found 5 remote jobs from RemoteOK

1. Full Stack Engineer at RemoteCompany
   Tags: python, react, remote
   URL: https://remoteok.com/...

============================================================
📰 Testing Indeed RSS Feed
============================================================
✅ Found 5 jobs from Indeed RSS

1. Backend Engineer at StartupXYZ
   URL: https://www.indeed.com/...

============================================================
📊 TEST SUMMARY
============================================================
Adzuna              ✅ PASS
RemoteOK            ✅ PASS
Indeed RSS          ✅ PASS
Aggregator          ✅ PASS

Total: 4/4 tests passed

🎉 All tests passed! Your job APIs are working!
```

## Step 5: Try Job Search via API (2 minutes)

With your server running (`python -m uvicorn app.main:app --reload`):

### Option A: Use the Web UI

1. Open: **http://127.0.0.1:8000**
2. Enter your search criteria (e.g., "Python Developer", "New York")
3. Click **"Search Jobs"**
4. See REAL jobs from multiple sources!

### Option B: Use curl

```powershell
curl -X POST "http://127.0.0.1:8000/jobs/scrape" `
  -H "Content-Type: application/json" `
  -d '{
    "region": "New York",
    "role": "Python Developer",
    "platforms": ["adzuna", "remoteok", "indeed"]
  }'
```

### Option C: Use Swagger UI

1. Open: **http://127.0.0.1:8000/docs**
2. Find `POST /jobs/scrape`
3. Click **"Try it out"**
4. Edit the request body:
   ```json
   {
     "region": "Remote",
     "role": "Backend Engineer",
     "platforms": ["adzuna", "remoteok", "indeed"]
   }
   ```
5. Click **"Execute"**
6. See real job results!

## Troubleshooting

### ❌ "Adzuna API credentials not found"

**Solution**: Make sure you:
1. Created the `.env` file (not `.env.example`)
2. Added `ADZUNA_API_ID` and `ADZUNA_API_KEY`
3. Restarted the server after editing `.env`

### ❌ "No jobs found from Adzuna"

**Check**:
1. Your API credentials are correct
2. You haven't exceeded the free tier limit (5000 calls/month)
3. Try different search terms

**Test manually**:
```powershell
python
>>> from app.tools.real_job_apis import AdzunaAPI
>>> api = AdzunaAPI()
>>> jobs = api.search_jobs(query="developer", location="USA")
>>> print(f"Found {len(jobs)} jobs")
```

### ❌ RemoteOK returns empty

**Reason**: RemoteOK may not have jobs matching your specific search term.

**Solution**: Try broader searches like "developer" or "engineer"

### ❌ Indeed RSS not working

**Check**: Your internet connection and firewall settings.

**Alternative**: Indeed RSS feeds work without authentication, so if it fails, it's likely a network issue.

## What's Next?

Once local testing works:

1. ✅ **Verified**: Real job APIs work
2. 🚀 **Next**: Follow `DEPLOYMENT_GUIDE.md` to deploy to Render
3. 🎯 **Then**: Set up email applications (see `.env.example`)
4. 📊 **Finally**: Monitor and optimize your job search!

## FAQ

**Q: Do I need to pay for Adzuna?**
A: No! The free tier gives 5000 API calls/month, which is plenty for personal job searching.

**Q: What about LinkedIn/Indeed scrapers?**
A: We use Indeed's official RSS feeds (legal). LinkedIn scraping violates their ToS, so we use Adzuna instead (which aggregates from many sources including LinkedIn).

**Q: How many jobs will I find?**
A: Depends on your search. Typical searches return 10-50 jobs across all platforms.

**Q: Can I add more job boards?**
A: Yes! Check `REAL_WORLD_DEPLOYMENT_PLAN.md` for more API options (The Muse, Jooble, etc.)

---

**You're ready to test! Run the command:**

```powershell
python test_job_apis.py
```

**Happy job hunting! 🎯**
