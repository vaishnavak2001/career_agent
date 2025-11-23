# Frontend Deployment Guide - Vercel

## Quick Deploy Steps

### 1. Go to Vercel
Visit: https://vercel.com/dashboard

### 2. Import Project
- Click "Add New Project"
- Import your `career_agent` GitHub repository
- **IMPORTANT**: Set Root Directory to `frontend`

### 3. Configure Settings
- Framework: Vite (auto-detected)
- Build Command: `npm run build`
- Output Directory: `dist`

### 4. Add Environment Variable
In "Environment Variables" section, add:
- Key: `VITE_API_URL`
- Value: `https://career-agent-api.onrender.com/api/v1`

### 5. Deploy
Click "Deploy" and wait 2-3 minutes!

## View Your Live Application

After deployment, Vercel provides a URL like:
```
https://career-agent-[random].vercel.app
```

Find it in: Vercel Dashboard → Your Project → Domains

## What You'll See

Your live application will show:
- **15 test jobs** from your backend API
- **Dashboard statistics**: 15 jobs scraped, 20 applications sent
- Job search and filtering
- Application tracking
- Resume management

## Test the Deployment

1. Visit your Vercel URL
2. Open DevTools (F12) → Network tab
3. Should see API calls to `career-agent-api.onrender.com`
4. Jobs should load and display

## Continuous Deployment

Every push to GitHub automatically redeploys:
```bash
git add .
git commit -m "Update"
git push origin master
# Vercel auto-deploys in ~2 minutes!
```

## Troubleshooting

**Blank page?**
- Check environment variable is set correctly
- Verify backend API is running: https://career-agent-api.onrender.com/api/v1/jobs/

**Build fails?**
- Ensure Root Directory = `frontend` in Vercel settings

**API errors?**
- Verify `VITE_API_URL` = `https://career-agent-api.onrender.com/api/v1` (no trailing slash)

## Your Full Stack App

Once deployed, you have:
- ✅ Frontend: Vercel (your-app.vercel.app)
- ✅ Backend: Render (career-agent-api.onrender.com)
- ✅ Database: Supabase
- ✅ Full production system ready!
