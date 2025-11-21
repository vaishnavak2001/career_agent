# 🚀 Free Deployment Guide - Career Agent

## Get Your Career Agent Live in 15 Minutes! 🌐

This guide will help you deploy your Career Agent application **completely free** using Render.com with real job search capabilities.

---

## 📋 Prerequisites

Before deploying, you'll need:

1. **GitHub Account** (free)
2. **Render Account** (free) - Sign up at [render.com](https://render.com)
3. **Adzuna API Keys** (free) - Get at [developer.adzuna.com](https://developer.adzuna.com)
4. **Gmail Account** (for sending applications)

---

## ⚡ Quick Start (15 Minutes)

### Step 1: Get Adzuna API Keys (5 min)

1. Go to https://developer.adzuna.com/
2. Click "Sign Up" (free, no credit card)
3. Create an account
4. Navigate to "API Dashboard"
5. Copy your:
   - **Application ID**
   - **API Key**
6. Keep these handy for Step 3

**Note**: Free tier gives you 5,000 API calls/month (plenty for job searching!)

---

### Step 2: Prepare Gmail for Applications (3 min)

To send job applications via email:

1. **Enable 2-Factor Authentication** on your Gmail:
   - Go to https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Create App Password**:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Other (Custom name)"
   - Name it "Career Agent"
   - Click "Generate"
   - **Copy the 16-character password** (no spaces)

**Important**: Use this app password, NOT your regular Gmail password!

---

### Step 3: Push to GitHub (3 min)

Open your terminal in the career_agent directory:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create a new repository on GitHub (via website)
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/career-agent.git
git branch -M main
git push -u origin main
```

**⚠️ SECURITY CHECK**: Make sure your `.env` file is in `.gitignore`!

```powershell
# Verify .env is ignored
git status

# If .env appears in the list, add it to .gitignore:
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ensure .env is ignored"
git push
```

---

### Step 4: Deploy to Render (4 min)

1. **Sign in to Render**:
   - Go to https://render.com
   - Click "Get Started" or "Sign In"
   - Use GitHub to sign in

2. **Create New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `career-agent` repository
   - Click "Connect"

3. **Configure the Service**:
   - **Name**: `career-agent-api`
   - **Environment**: `Python 3`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: `Free`

4. **Add Environment Variables**:
   Click "Advanced" → "Add Environment Variable"
   
   Add these one by one:

   ```
   DATABASE_URL=sqlite:///./career_agent.db
   ADZUNA_API_ID=your_adzuna_app_id
   ADZUNA_API_KEY=your_adzuna_api_key
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your_email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   DRY_RUN=true
   MAX_APPLICATIONS_PER_DAY=5
   ```

5. **Create Service**:
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - You'll get a URL like: `https://career-agent-api.onrender.com`

---

## ✅ Verify Deployment

Once deployed, test your application:

### 1. Check Health Endpoint

Visit: `https://YOUR-APP-URL.onrender.com/`

You should see:
```json
{
  "status": "active",
  "version": "2.0.0",
  "message": "Autonomous Career Agent API is running"
}
```

### 2. View API Documentation

Visit: `https://YOUR-APP-URL.onrender.com/docs`

This shows all available API endpoints with interactive testing.

### 3. Test Real Job Search

Use the Swagger UI or curl:

```powershell
curl -X POST "https://YOUR-APP-URL.onrender.com/jobs/scrape" `
  -H "Content-Type: application/json" `
  -d '{
    "region": "New York",
    "role": "Python Developer",
    "platforms": ["adzuna", "remoteok", "indeed"]
  }'
```

You should get **real job listings** from Adzuna, RemoteOK, and Indeed!

### 4. Test Email Application (Dry Run)

```powershell
# First, get a job ID from the search results
curl "https://YOUR-APP-URL.onrender.com/jobs?limit=1"

# Then test application (won't actually send in dry run mode)
# Use the web interface or API to trigger applications
```

---

## 🎯 Using Your Deployed Application

### Web Interface

Visit your deployment URL to access the beautiful Indeed-inspired interface:

```
https://YOUR-APP-URL.onrender.com
```

Features:
- 🔍 Search real jobs from multiple platforms
- 📊 View match scores and analytics
- 📧 Auto-apply to high-matching positions
- 📈 Track application history

### API Integration

Use the REST API from any application:

```python
import requests

API_URL = "https://YOUR-APP-URL.onrender.com"

# Search for jobs
response = requests.post(f"{API_URL}/jobs/scrape", json={
    "region": "Remote",
    "role": "Backend Engineer",
    "platforms": ["adzuna", "remoteok"]
})

jobs = response.json()
print(f"Found {len(jobs)} jobs!")
```

---

## 🔧 Configuration

### Environment Variables

Update these in Render Dashboard → Settings → Environment:

| Variable | Description | Example |
|----------|-------------|---------|
| `ADZUNA_API_ID` | Your Adzuna App ID | `12345678` |
| `ADZUNA_API_KEY` | Your Adzuna API Key | `abcdef123456` |
| `SMTP_USER` | Your Gmail address | `you@gmail.com` |
| `SMTP_PASSWORD` | Gmail App Password | `abcdefghijklmnop` |
| `DRY_RUN` | Simulate applications | `true` or `false` |
| `MAX_APPLICATIONS_PER_DAY` | Limit daily applications | `5` |

### Enable Real Applications

**⚠️ IMPORTANT**: By default, applications are simulated (`DRY_RUN=true`)

To actually send applications:
1. Go to Render Dashboard → Your Service → Environment
2. Change `DRY_RUN` to `false`
3. Click "Save Changes"
4. **Review each application before it's sent!**

---

## 💾 Database Options

### Option A: SQLite (Current - Simple)

**Pros**: Simple, no setup
**Cons**: Resets on每次 deployment

Already configured! No changes needed.

### Option B: PostgreSQL (Recommended for Production)

**Free for 90 days**, then $7/month

1. In Render Dashboard:
   - Click "New +" → "PostgreSQL"
   - Name: `career-agent-db`
   - Plan: "Free"
   - Click "Create Database"

2. Copy the "Internal Database URL"

3. Update environment variable:
   - `DATABASE_URL` = (paste the PostgreSQL URL)

4. Redeploy your service

---

## 📊 Monitoring & Logs

### View Logs

Render Dashboard → Your Service → Logs

Watch real-time logs to see:
- Job searches
- Match score calculations
- Application submissions
- API errors

### Metrics

Render Dashboard → Your Service → Metrics

Monitor:
- CPU usage
- Memory usage
- Request count
- Response times

---

## 🔒 Security Best Practices

### ✅ DO:

- ✅ Keep `DRY_RUN=true` until you've tested thoroughly
- ✅ Use Gmail App Passwords (never your real password)
- ✅ Review API usage to stay within free limits
- ✅ Regularly check application logs
- ✅ Set `MAX_APPLICATIONS_PER_DAY` to a reasonable number

### ❌ DON'T:

- ❌ Commit `.env` files to GitHub
- ❌ Share your API keys publicly
- ❌ Send applications without reviewing them
- ❌ Exceed API rate limits
- ❌ Spam applications to inappropriate jobs

---

## 🚨 Troubleshooting

### Deployment Failed

**Error**: "Build failed"
- Check requirements.txt is up to date
- View build logs in Render dashboard
- Ensure Python version is compatible

**Solution**:
```powershell
# Test build locally first
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### No Jobs Found

**Issue**: API returns empty results

**Check**:
1. Verify `ADZUNA_API_ID` and `ADZUNA_API_KEY` are set correctly
2. Check Adzuna dashboard for remaining API calls
3. Try different search terms

**Test**:
```powershell
# Check environment variables
curl "https://YOUR-APP-URL.onrender.com/api/info"
```

### Can't Send Emails

**Issue**: SMTP authentication failed

**Check**:
1. Gmail 2FA is enabled
2. Using App Password (not regular password)
3. `SMTP_USER` and `SMTP_PASSWORD` are correct
4. No spaces in app password

### Database Resets

**Issue**: Jobs disappear after redeployment

**Solution**: Switch to PostgreSQL (see "Database Options" above)

---

## 📈 Scaling & Upgrades

### Free Tier Limitations

- **Render Free**: 750 hours/month (enough for 1 service)
- **Adzuna Free**: 5,000 API calls/month
- **PostgreSQL Free**: 90 days, then $7/month

### When to Upgrade

Upgrade when you:
- Need 24/7 uptime (free tier sleeps after inactivity)
- Exceed 5,000 job searches/month
- Want persistent database
- Need faster response times

### Paid Plans (Optional)

- **Render Starter**: $7/month (always on, better performance)
- **Adzuna Paid**: Contact for higher limits
- **PostgreSQL**: $7/month on Render

---

## 🎉 Success Checklist

After deployment, verify:

- [ ] Application is accessible via HTTPS URL
- [ ] API documentation loads at `/docs`
- [ ] Real job search works (using Adzuna)
- [ ] RemoteOK jobs are fetched
- [ ] Indeed RSS jobs appear
- [ ] Match scores are calculated
- [ ] Cover letters generate successfully
- [ ] Email configuration is correct (in DRY_RUN mode)
- [ ] Logs show API activity
- [ ] No errors in console

---

## 🌟 Next Steps

### Week 1: Test & Validate

1. Search for jobs in your field
2. Review match scores
3. Generate cover letters
4. Test application flow (DRY_RUN=true)

### Week 2: Go Live (Carefully!)

1. Set `DRY_RUN=false`
2. Start with `MAX_APPLICATIONS_PER_DAY=1`
3. Monitor results
4. Gradually increase if successful

### Week 3+: Optimize

1. Track which platforms give best results
2. Refine match score algorithm
3. Improve cover letter templates
4. Add more job sources

---

## 📞 Get Help

- **Render Docs**: https://render.com/docs
- **Adzuna API Docs**: https://developer.adzuna.com/docs
- **Application Logs**: Check Render dashboard
- **GitHub Issues**: Report bugs in your repository

---

## 🎊 You're Live!

**Congratulations!** Your Career Agent is now:

✅ Deployed to the cloud (free!)
✅ Searching real job boards
✅ Calculating match scores
✅ Ready to automate applications

**Share your deployment URL**:
```
https://YOUR-APP-URL.onrender.com
```

---

**Pro Tip**: Bookmark your deployed app and check it daily for new high-match jobs! 📱

**Happy Job Hunting! 🎯**
