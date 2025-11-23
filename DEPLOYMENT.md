# Deployment Guide

## Free-Tier Deployment Stack

This guide shows how to deploy the Autonomous AI Job Application Agent to free-tier platforms.

### Prerequisites

- GitHub account
- Vercel account (free)
- Railway account (free) OR Render account (free)
- Supabase account (free) OR Neon account (free)
- OpenAI API key (optional, for LLM features)

## Step 1: Database Setup (PostgreSQL)

### Option A: Supabase

1. Go to [supabase.com](https://supabase.com)
2. Create a new project
3. Go to **Settings** → **Database**
4. Copy the **Connection String** (URI mode)
5. Save as `DATABASE_URL`

Example:
```
postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres
```

### Option B: Neon

1. Go to [neon.tech](https://neon.tech)
2. Create a new project
3. Copy the connection string
4. Save as `DATABASE_URL`

Example:
```
postgresql://[user]:[password]@[host].neon.tech/main
```

## Step 2: Backend Deployment (Railway/Render)

### Option A: Railway

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

2. **Connect Railway**
   - Go to [railway.app](https://railway.app)
   - Click **New Project** → **Deploy from GitHub repo**
   - Select your repository
   - Railway will auto-detect the Python project

3. **Set Environment Variables**
   In Railway dashboard, add:
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=<generate-random-string>
   OPENAI_API_KEY=sk-...
   ```

4. **Configure Start Command**
   Railway should auto-detect, but if needed, set:
   ```
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Get Deployment URL**
   - Railway will provide a URL like `https://your-app.railway.app`

### Option B: Render

1. **Push to GitHub** (same as above)

2. **Create Web Service**
   - Go to [render.com](https://render.com)
   - Click **New** → **Web Service**
   - Connect your GitHub repo

3. **Configure Service**
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set Environment Variables**
   ```
   DATABASE_URL=postgresql://...
   SECRET_KEY=<random-string>
   OPENAI_API_KEY=sk-...
   ```

5. **Deploy**
   - Render will build and deploy automatically
   - Get URL like `https://your-app.onrender.com`

## Step 3: Frontend Deployment (Vercel)

1. **Update API URL**
   
   Edit `frontend/src/services/api.js`:
   ```javascript
   const BASE_URL = "https://your-backend.railway.app/api/v1"
   // or const BASE_URL = "https://your-backend.onrender.com/api/v1"
   ```

2. **Deploy to Vercel**
   ```bash
   cd frontend
   npm install -g vercel
   vercel login
   vercel --prod
   ```

   Or use Vercel Dashboard:
   - Go to [vercel.com](https://vercel.com)
   - Click **Add New** → **Project**
   - Import from GitHub
   - Set **Root Directory** to `frontend`
   - Click **Deploy**

3. **Get Frontend URL**
   - Vercel provides URL like `https://your-app.vercel.app`

## Step 4: Initialize Database

Once backend is deployed, initialize the database:

1. **SSH into Railway/Render** (if possible) or run locally with production DATABASE_URL:
   ```bash
   export DATABASE_URL=postgresql://...
   python -m app.init_db
   ```

2. **Or use Migrations** (recommended for production):
   ```bash
   # Install alembic
   pip install alembic
   
   # Initialize
   alembic init migrations
   
   # Create migration
   alembic revision --autogenerate -m "Initial schema"
   
   # Apply
   alembic upgrade head
   ```

## Step 5: Configure CORS

Update `app/core/config.py`:

```python
BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
    "http://localhost:3000",
    "https://your-app.vercel.app",
    "https://your-custom-domain.com"
]
```

Redeploy backend after this change.

## Step 6: Set Up GitHub Actions (Optional)

1. **Add GitHub Secrets**
   - Go to repository **Settings** → **Secrets and variables** → **Actions**
   - Add:
     - `RAILWAY_DEPLOY_HOOK` or `RENDER_DEPLOY_HOOK`
     - `VERCEL_TOKEN`
     - `VERCEL_ORG_ID`
     - `VERCEL_PROJECT_ID`

2. **Enable Actions**
   - Push code to `main` branch
   - GitHub Actions will auto-deploy

## Step 7: Test the Deployment

1. **Test Backend**
   ```bash
   curl https://your-backend.railway.app/
   # Should return: {"message":"Welcome to ..."}
   
   curl https://your-backend.railway.app/api/v1/jobs/
   # Should return: [] or job listings
   ```

2. **Test Frontend**
   - Visit `https://your-app.vercel.app`
   - Should see job listing UI
   - Test job search, filters

## Environment Variables Reference

### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Security
SECRET_KEY=<generate-with-openssl-rand-hex-32>

# LLM (optional)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Email (optional)
SENDGRID_API_KEY=SG....
EMAIL_FROM=noreply@yourapp.com

# App Config
BACKEND_CORS_ORIGINS=https://your-app.vercel.app,http://localhost:3000
```

### Frontend (.env)

```env
VITE_API_URL=https://your-backend.railway.app/api/v1
```

## Deployment Checklist

- [ ] Database created and connection string saved
- [ ] Backend deployed to Railway/Render
- [ ] Backend environment variables set
- [ ] Database initialized (tables created)
- [ ] Frontend API URL updated
- [ ] Frontend deployed to Vercel
- [ ] CORS configured correctly
- [ ] Backend API tested (curl/Postman)
- [ ] Frontend tested in browser
- [ ] GitHub Actions configured (optional)
- [ ] Custom domain configured (optional)

## Troubleshooting

### Database Connection Errors

```bash
# Test connection locally
python -c "from app.db.session import engine; print(engine.connect())"
```

### CORS Errors in Frontend

- Check BACKEND_CORS_ORIGINS includes frontend URL
- Ensure both protocols (http/https) are correct
- Redeploy backend after updating CORS settings

### Build Failures

**Backend**:
- Check Python version (should be 3.10+)
- Verify all dependencies in requirements.txt
- Check build logs for specific errors

**Frontend**:
- Check Node version (should be 18+)
- Run `npm install` to verify dependencies
- Check `vite.config.js` configuration

### Port Issues

Railway/Render provide `$PORT` environment variable.
Ensure uvicorn uses it:
```python
--port $PORT  # not --port 8000
```

## Monitoring & Logs

**Railway**:
- Dashboard → Logs tab shows real-time logs
- Metrics tab shows CPU/Memory usage

**Render**:
- Dashboard → Logs shows deployment and runtime logs
- Events tab shows deployment history

**Vercel**:
- Deployments tab shows build logs
- Analytics tab shows traffic (paid feature)

## Scaling (Beyond Free Tier)

When you outgrow free tier:

1. **Database**: Upgrade Supabase/Neon plan for more storage/connections
2. **Backend**: 
   - Railway: Upgrade to Pro ($5/month + usage)
   - Render: Upgrade to Starter ($7/month)
3. **Frontend**: Vercel Pro ($20/month) for analytics & more bandwidth
4. **Add Redis**: For caching, use Upstash (free tier available)
5. **Add CDN**: Use Cloudflare (free) for static assets

## Backup Strategy

1. **Database Backups**
   - Supabase: Auto-backups included in free plan
   - Neon: Point-in-time restore included

2. **Code Repository**
   - GitHub serves as version control backup
   - Tag releases: `git tag -a v1.0.0 -m "Release v1.0.0"`

3. **User Data**
   - Export user data periodically
   - Store backups in S3/Supabase Storage

## Security Recommendations

1. **Use HTTPS everywhere** (Vercel/Railway/Render provide free SSL)
2. **Rotate secrets** regularly
3. **Enable 2FA** on all service accounts
4. **Monitor logs** for suspicious activity
5. **Set up alerts** for errors/downtime
6. **Keep dependencies updated**: `pip list --outdated`

## Cost Estimate (Free Tier Limits)

| Service | Free Tier | Limit |
|---------|-----------|-------|
| Supabase | Free | 500MB DB, 2GB bandwidth |
| Railway | $5 credit/month | ~500 hours runtime |
| Render | Free | 750 hours/month |
| Vercel | Free | 100GB bandwidth |
| Total | $0-5/month | Sufficient for side project |

## Next Steps

1. Set up custom domain (optional)
2. Configure email notifications
3. Add monitoring (Sentry, LogRocket)
4. Implement user authentication
5. Add payment integration (Stripe)
6. Deploy to production!

---

**Questions?** Open an issue on GitHub or check the docs.
