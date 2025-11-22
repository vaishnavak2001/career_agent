# 🚀 Deployment Guide - Career Agent

Complete guide for deploying the Autonomous Career Agent on free-tier platforms.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Database Setup (Neon/Supabase)](#database-setup)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Environment Variables](#environment-variables)
6. [CI/CD Setup](#cicd-setup)
7. [Post-Deployment](#post-deployment)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Accounts (All Free Tier)
- [ ] GitHub account
- [ ] Neon or Supabase account (PostgreSQL)
- [ ] Railway or Render account (Backend hosting)
- [ ] Vercel or Netlify account (Frontend hosting)
- [ ] OpenAI/Anthropic/Google account (LLM API)
- [ ] SendGrid or Mailgun account (Email)

### Local Development Tools
```bash
# Required
- Python 3.11+
- Node.js 18+
- Git
- Docker (optional, for local testing)

# Install CLIs
npm install -g vercel railway @netlify/cli
```

---

## Database Setup

### Option 1: Neon (Recommended)

1. **Create Account**
   ```
   Visit: https://neon.tech
   Sign up with GitHub
   ```

2. **Create Database**
   ```bash
   # Via Neon Console
   - Click "Create Project"
   - Name: career-agent-prod
   - Region: Choose closest to your backend
   - PostgreSQL version: 15
   ```

3. **Get Connection String**
   ```bash
   # Example format:
   postgresql://user:password@ep-cool-name-123456.us-east-2.aws.neon.tech/main?sslmode=require
   ```

4. **Run Migrations**
   ```bash
   # Clone your repo
   git clone https://github.com/yourusername/career-agent.git
   cd career-agent/backend
   
   # Set environment variable
   export DATABASE_URL="your-neon-connection-string"
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run schema
   psql $DATABASE_URL < ../schema.sql
   
   # OR use Alembic
   alembic upgrade head
   ```

### Option 2: Supabase

1. **Create Project**
   ```
   Visit: https://supabase.com
   - New Project → career-agent
   - Set database password
   - Choose region
   ```

2. **Get Connection String**
   ```
   Settings → Database → Connection String (URI)
   ```

3. **Enable Extensions**
   ```sql
   -- In Supabase SQL Editor
   CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
   CREATE EXTENSION IF NOT EXISTS "pgcrypto";
   CREATE EXTENSION IF NOT EXISTS "vector";
   ```

4. **Run Schema**
   ```bash
   # Upload and run schema.sql via Supabase SQL Editor
   # OR connect via psql
   psql "your-supabase-connection-string" < schema.sql
   ```

---

## Backend Deployment

### Option 1: Railway (Recommended)

1. **Install CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Create Project**
   ```bash
   cd backend
   railway init
   # Select: Create new project
   # Name: career-agent-backend
   ```

3. **Set Environment Variables**
   ```bash
   railway variables set DATABASE_URL="your-database-url"
   railway variables set OPENAI_API_KEY="your-openai-key"
   railway variables set SECRET_KEY="$(openssl rand -hex 32)"
   railway variables set FRONTEND_URL="https://your-frontend.vercel.app"
   
   # All variables (see below for complete list)
   railway variables set SMTP_HOST="smtp.sendgrid.net"
   railway variables set SMTP_PORT="587"
   railway variables set SMTP_USER="apikey"
   railway variables set SMTP_PASSWORD="your-sendgrid-key"
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Generate Domain**
   ```bash
   railway domain
   # Note the generated URL: career-agent-backend.up.railway.app
   ```

6. **Run Migrations**
   ```bash
   railway run alembic upgrade head
   ```

### Option 2: Render

1. **Create Account**
   ```
   Visit: https://render.com
   Connect GitHub
   ```

2. **New Web Service**
   ```
   - Click "New +" → Web Service
   - Connect repository: yourusername/career-agent
   - Name: career-agent-backend
   - Root Directory: backend
   - Build Command: pip install -r requirements.txt
   - Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**
   ```
   Add in Render dashboard:
   - DATABASE_URL
   - OPENAI_API_KEY
   - SECRET_KEY
   - etc. (see complete list below)
   ```

4. **Deploy**
   ```
   Click "Create Web Service"
   Wait for deployment (~3-5 minutes)
   ```

### Option 3: Fly.io

1. **Install CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Launch App**
   ```bash
   cd backend
   fly launch
   # Follow prompts
   # Name: career-agent-backend
   # Region: Choose closest
   ```

3. **Set Secrets**
   ```bash
   fly secrets set DATABASE_URL="your-db-url"
   fly secrets set OPENAI_API_KEY="your-key"
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

---

## Frontend Deployment

### Option 1: Vercel (Recommended)

1. **Install CLI**
   ```bash
   npm install -g vercel
   vercel login
   ```

2. **Deploy**
   ```bash
   cd frontend
   
   # Set environment variable
   echo "VITE_API_URL=https://your-backend.railway.app" > .env.production
   
   # Deploy
   vercel --prod
   ```

3. **Configure via Dashboard**
   ```
   - Visit vercel.com/dashboard
   - Select project
   - Settings → Environment Variables
   - Add: VITE_API_URL=https://your-backend-url.com
   - Redeploy
   ```

### Option 2: Netlify

1. **Install CLI**
   ```bash
   npm install -g netlify-cli
   netlify login
   ```

2. **Build**
   ```bash
   cd frontend
   npm run build
   ```

3. **Deploy**
   ```bash
   netlify deploy --prod --dir=dist
   ```

4. **Environment Variables**
   ```bash
   # Via CLI
   netlify env:set VITE_API_URL "https://your-backend-url.com"
   
   # OR via dashboard
   Site settings → Build & deploy → Environment
   ```

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname?sslmode=require

# Security
SECRET_KEY=your-secret-key-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# LLM
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=AIza...
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo-preview

# CORS
FRONTEND_URL=https://your-frontend.vercel.app
ALLOWED_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173

# Email
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-api-key
FROM_EMAIL=noreply@yourapp.com
FROM_NAME=Career Agent

# Storage
STORAGE_TYPE=supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_BUCKET=career-agent-files

# OAuth (Optional)
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-secret
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-secret

# Webhooks
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Monitoring
SENTRY_DSN=https://...@sentry.io/...
ENVIRONMENT=production
```

### Frontend (.env.production)

```bash
VITE_API_URL=https://your-backend.railway.app
VITE_APP_NAME=Career Agent
VITE_ENABLE_ANALYTICS=true
VITE_SENTRY_DSN=https://...@sentry.io/...
```

---

## CI/CD Setup

### GitHub Actions (Already configured in `.github/workflows/`)

1. **Add GitHub Secrets**
   ```
   Repository → Settings → Secrets and variables → Actions
   
   Add:
   - RAILWAY_TOKEN (from railway.app/account/tokens)
   - VERCEL_TOKEN (from vercel.com/account/tokens)
   - RAILWAY_PROJECT_ID (from railway project settings)
   - VERCEL_ORG_ID (from vercel.com/teams)
   - VERCEL_PROJECT_ID (from vercel project settings)
   - All sensitive env vars (DATABASE_URL, API_KEYS, etc.)
   ```

2. **Push to Main**
   ```bash
   git add .
   git commit -m "Initial deployment setup"
   git push origin main
   ```

3. **Automatic Deployment**
   ```
   ✅ Tests run on push
   ✅ Security scans execute
   ✅ Docker images built
   ✅ Backend deploys to Railway
   ✅ Frontend deploys to Vercel
   ✅ Notifications sent to Slack
   ```

---

## Post-Deployment

### 1. Verify Backend

```bash
# Health check
curl https://your-backend.railway.app/api/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### 2. Verify Frontend

```
Visit: https://your-frontend.vercel.app
Should load the React UI
```

### 3. Run Database Migrations

```bash
# Via Railway
railway run alembic upgrade head

# Via Render
# SSH into instance or use Render Shell
alembic upgrade head
```

### 4. Create Admin User

```bash
# Via Railway
railway run python scripts/create_admin.py \
  --email admin@example.com \
  --password secure-password

# OR via API
curl -X POST https://your-backend/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "secure-password",
    "full_name": "Admin User"
  }'
```

### 5. Test Full Workflow

```bash
# Login
curl -X POST https://your-backend/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "your-password"}'

# Get token from response, then:
export TOKEN="your-jwt-token"

# Test agent
curl -X POST https://your-backend/api/agent/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"instruction": "Find 5 remote Python jobs and show me the top match"}'
```

---

## Free Tier Limits

### Neon PostgreSQL
- ✅ 1 project
- ✅ 0.5 GB storage
- ✅ Unlimited queries
- ❌ Auto-pause after 5min inactivity

### Railway
- ✅ $5 free credit/month
- ✅ ~500 hours runtime
- ❌ Hibernates if not used

### Vercel
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth
- ✅ Custom domains

### SendGrid
- ✅ 100 emails/day free

### OpenAI
- ❌ Pay-as-you-go
- Typical cost: $0.10-0.50 per application

---

## Monitoring & Alerts

### Sentry (Error Tracking)

1. **Create Account**
   ```
   Visit: https://sentry.io
   Free tier: 5,000 errors/month
   ```

2. **Create Project**
   ```
   - Platform: Python (backend) / React (frontend)
   - Copy DSN
   ```

3. **Add to Environment**
   ```bash
   # Backend
   railway variables set SENTRY_DSN="your-sentry-dsn"
   
   # Frontend
   vercel env add VITE_SENTRY_DSN
   ```

### Uptime Monitoring

```
Use: https://uptimerobot.com (Free tier: 50 monitors)

Add monitors for:
- https://your-backend/api/health (every 5 min)
- https://your-frontend.vercel.app (every 5 min)

Alert via: Email, Slack, Discord
```

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
railway logs

# Common issues:
1. DATABASE_URL not set → Set via `railway variables`
2. Missing dependencies → Check requirements.txt
3. Port binding → Railway auto-assigns PORT env var
```

### Frontend can't connect to backend

```bash
# Check CORS settings in backend
# Ensure ALLOWED_ORIGINS includes frontend URL

# Verify frontend env
vercel env ls
# Should show VITE_API_URL

# Check browser console for errors
```

### Database connection fails

```bash
# Test connection
psql "$DATABASE_URL"

# Common issues:
1. SSL required → Add ?sslmode=require to URL
2. IP whitelist → Neon/Supabase usually allow all IPs
3. Max connections → Free tier has limits
```

### Playwright installation issues

```bash
# On Railway/Render
# Add to requirements.txt:
playwright==1.40.0

# Add build command:
playwright install chromium

# OR use Dockerfile with pre-installed browsers
```

---

## Cost Estimate (Monthly)

```
FREE TIER:
✅ Database (Neon): $0
✅ Backend (Railway): $0 (with $5 credit)
✅ Frontend (Vercel): $0
✅ Email (SendGrid): $0 (100/day)
✅ Storage (Supabase): $0 (1GB)
✅ Monitoring (Sentry): $0

PAID USAGE:
⚠️  LLM API (OpenAI): ~$10-50/month
   (Depends on jobs processed)
⚠️  Extra email (SendGrid): $15/month (40k emails)

TOTAL: $10-50/month (mostly LLM costs)
```

---

## Scaling Beyond Free Tier

When you outgrow free tier:

1. **Database**: Upgrade Neon to Pro ($19/mo) or migrate to AWS RDS
2. **Backend**: Railway Pro ($20/mo) or AWS ECS/Fargate
3. **Frontend**: Vercel stays free or Pro ($20/mo)
4. **Email**: SendGrid Essentials ($15/mo)
5. **Storage**: S3 ($3-10/mo)
6. **Monitoring**: Sentry Team ($26/mo)

**Est. production cost**: $80-120/month at scale

---

## Quick Deploy Script

```bash
#!/bin/bash
# deploy.sh - One-command deployment

set -e

echo "🚀 Deploying Career Agent..."

# 1. Database
echo "📊 Setting up database..."
psql "$DATABASE_URL" < schema.sql

# 2. Backend
echo "⚙️  Deploying backend..."
cd backend
railway up
railway run alembic upgrade head
BACKEND_URL=$(railway status --json | jq -r '.deployments[0].url')
cd ..

# 3. Frontend
echo "🎨 Deploying frontend..."
cd frontend
echo "VITE_API_URL=$BACKEND_URL" > .env.production
vercel --prod
cd ..

echo "✅ Deployment complete!"
echo "Backend: $BACKEND_URL"
echo "Frontend: $(vercel inspect --json | jq -r '.url')"
```

**Usage**:
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## Support

- **GitHub Issues**: https://github.com/yourusername/career-agent/issues
- **Documentation**: https://career-agent.gitbook.io
- **Discord**: https://discord.gg/career-agent

---

✅ **Your Career Agent is now live and ready to help you land your dream job!**
