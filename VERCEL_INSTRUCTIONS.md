# ▲ Vercel Deployment Guide

## 1. Import Project
1.  **Log in** to your [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **Add New...** -> **Project**.
3.  Select **Import Git Repository**.
4.  Choose your `career_agent` repository.

## 2. Configure Project
Vercel will try to auto-detect settings, but you must ensure they are correct:

*   **Framework Preset:** `Vite`
*   **Root Directory:** `frontend`
    *   *Important:* Click "Edit" and select the `frontend` folder. Do NOT leave it as `./`.
*   **Build Command:** `npm run build` (Default)
*   **Output Directory:** `dist` (Default)
*   **Install Command:** `npm install` (Default)

## 3. Environment Variables
You need to tell the frontend where your backend API lives.

1.  Expand the **Environment Variables** section.
2.  Add a new variable:
    *   **Key:** `VITE_API_URL`
    *   **Value:** `https://your-render-app-name.onrender.com`
        *   *Replace this with your actual Render Web Service URL.*
        *   *Example:* `https://career-agent-api.onrender.com`

## 4. Deploy
1.  Click **Deploy**.
2.  Wait for the build to complete (approx. 1 minute).
3.  Once finished, you will get a live URL (e.g., `https://career-agent-frontend.vercel.app`).

## 5. Final Connection Check
1.  Open your new Vercel URL.
2.  Go to **Register**.
3.  Create an account.
4.  If it succeeds, your **Frontend (Vercel)** is successfully talking to your **Backend (Render)** which is talking to your **Database (Supabase)**! 🎉
