# 🚀 CareerAgent Deployment Guide

This guide details how to deploy the CareerAgent frontend application to production.

## 📋 Prerequisites

- **Node.js**: Version 20 or higher recommended.
- **Git**: For version control.
- **Backend API**: A running instance of the CareerAgent backend (FastAPI).

## 🏗️ Build Process

The application is built using Vite, which produces a highly optimized static asset bundle.

1.  **Install Dependencies:**
    ```bash
    cd frontend
    npm install
    ```

2.  **Run Production Build:**
    ```bash
    npm run build
    ```

    **Output:**
    The build artifacts will be generated in the `frontend/dist` directory.
    - `index.html`: Entry point.
    - `assets/`: CSS and JavaScript chunks (code-split).
    - `sw.js`: Service Worker for PWA functionality.
    - `manifest.webmanifest`: PWA manifest.

3.  **Preview Build (Optional):**
    To test the production build locally:
    ```bash
    npm run preview
    ```

## 🌍 Environment Variables

You must configure the backend API URL.

**Local Development (`.env`):**
```env
VITE_API_URL=http://localhost:8000
```

**Production:**
Set `VITE_API_URL` in your hosting provider's environment variable settings to point to your live backend (e.g., `https://api.careeragent.com`).

---

## ☁️ Deployment Options

### Option 1: Vercel (Recommended)

Vercel is the creators of Next.js and provides excellent support for Vite apps.

1.  **Install Vercel CLI:**
    ```bash
    npm install -g vercel
    ```

2.  **Deploy:**
    Run the following command from the `frontend` directory:
    ```bash
    vercel --prod
    ```
    Follow the prompts.

3.  **Configure Environment:**
    Go to the Vercel Dashboard -> Settings -> Environment Variables and add `VITE_API_URL`.

### Option 2: Netlify

1.  **Install Netlify CLI:**
    ```bash
    npm install -g netlify-cli
    ```

2.  **Deploy:**
    ```bash
    netlify deploy --prod
    ```
    Set the publish directory to `dist`.

### Option 3: Docker / Nginx

You can serve the static files using Nginx.

**Dockerfile:**
```dockerfile
# Build Stage
FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production Stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Nginx Config (`nginx.conf`):**
```nginx
server {
    listen 80;
    location / {
        root /usr/share/nginx/html;
        index index.html index.htm;
        try_files $uri $uri/ /index.html; # Important for React Router
    }
}
```

## ✅ Post-Deployment Verification

1.  **PWA Check:** Open the site on a mobile device or Chrome. You should see an "Install" icon.
2.  **Offline Mode:** Turn off network and refresh. The app should still load (cached by Service Worker).
3.  **API Connection:** Try logging in. If it fails, check the Network tab to ensure requests are going to the correct `VITE_API_URL`.
