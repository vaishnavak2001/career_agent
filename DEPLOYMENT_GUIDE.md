# 🚀 Deployment & Verification Guide

## 1. Environment Setup

### Backend (Render)
1. Go to your Render Dashboard.
2. Select your `career-agent` service.
3. Go to **Environment**.
4. Add the following environment variables (values from `.env.production.example`):
   - `DATABASE_URL`: (Automatically set by Render if you use their Postgres)
   - `SECRET_KEY`: Generate a strong random string.
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `10080`
   - `BACKEND_CORS_ORIGINS`: `https://your-frontend.vercel.app,http://localhost:5173`
   - `OPENAI_API_KEY`: Your OpenAI Key.
   - `ADZUNA_API_ID`: Your Adzuna ID.
   - `ADZUNA_API_KEY`: Your Adzuna Key.
   - `GOOGLE_CLIENT_ID`: Your Google OAuth Client ID.
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth Client Secret.
   - `GOOGLE_REDIRECT_URI`: `https://your-backend.onrender.com/api/v1/auth/callback/google`
   - `LINKEDIN_CLIENT_ID`: Your LinkedIn Client ID.
   - `LINKEDIN_CLIENT_SECRET`: Your LinkedIn Client Secret.
   - `LINKEDIN_REDIRECT_URI`: `https://your-backend.onrender.com/api/v1/auth/callback/linkedin`

### Frontend (Vercel)
1. Go to your Vercel Dashboard.
2. Select your project.
3. Go to **Settings > Environment Variables**.
4. Add:
   - `VITE_API_URL`: `https://your-backend.onrender.com/api/v1`

## 2. Verification Steps

### Step 1: Verify Backend Health
Visit `https://your-backend.onrender.com/health`.
- **Expected:** `{"status": "healthy", "service": "Career Agent API"}`

### Step 2: Test Authentication
1. Open your frontend URL.
2. Go to the Login page.
3. Try to **Register** a new user.
4. Try to **Login** with the new user.
5. **Expected:** Successful login and redirection to Dashboard.

### Step 3: Test OAuth (Google/LinkedIn)
1. On the Login page, click "Login with Google".
2. **Expected:** Redirect to Google -> Login -> Redirect back to App -> Logged in.

### Step 4: Test Job Scraper
1. Go to the **Jobs** tab.
2. Click "Scrape Jobs" (or similar button).
3. **Expected:** A toast notification saying scraping started, and jobs appearing after a few seconds.

### Step 5: Test Interview Prep
1. Go to **Interview Prep** (if UI is built) or use Postman.
2. Send a POST to `/api/v1/interview/questions` with job details.
3. **Expected:** JSON response with interview questions.

## 3. Troubleshooting

- **CORS Errors:** Check `BACKEND_CORS_ORIGINS` in Render. Ensure no trailing slashes.
- **Database Errors:** Check `DATABASE_URL` and ensure the database is active.
- **Auth Errors:** Check `SECRET_KEY` and OAuth credentials.
- **Import Errors:** Check build logs in Render for any missing dependencies.

---
**Status:** ✅ Code pushed to GitHub. CI/CD pipeline should be running.
