# Deployment Guide: Vercel (frontend) + Render (backend)

Vercel hosts the static React build. The FastAPI backend is a long-running Python server, so it is hosted separately on **Render** (any host that runs Python web services works, e.g. Railway or Fly.io). Deploy the **backend first** so you have its URL.

Prerequisite: the project is on GitHub (see GITHUB_SETUP.md).

## Part A: Backend on Render
1. Sign up at https://render.com with GitHub.
2. **New + > Web Service**, select your repository.
3. Settings:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance type**: Free
   - **Environment variables**: `PYTHON_VERSION` = `3.11.9`, and `ALLOWED_ORIGINS` = `http://localhost:5173` for now.
   (Alternatively use **New + > Blueprint**; `render.yaml` in the repo root fills these in.)
4. Create the service. When the deploy finishes, copy the URL, e.g. `https://pathfinder-api.onrender.com`.
5. Test: open `<your-url>/api/health` (should return `{"status":"ok"}`) and `<your-url>/docs`.

## Part B: Frontend on Vercel
1. Sign up at https://vercel.com with GitHub.
2. **Add New > Project**, import the repository.
3. Settings:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite (auto-detected); Build `npm run build`, Output `dist`.
   - **Environment Variables**: `VITE_API_BASE_URL` = your Render URL, **without** a trailing slash.
4. **Deploy**. You get a URL such as `https://pathfinder-xyz.vercel.app`.
`frontend/vercel.json` adds the single-page-app fallback to `index.html`. The code has no hardcoded localhost URL: development uses the Vite proxy, production uses `VITE_API_BASE_URL`.

## Part C: Connect them (CORS)
1. In Render > your service > **Environment**, set
   `ALLOWED_ORIGINS` = `https://pathfinder-xyz.vercel.app,http://localhost:5173`
   (exact origin: scheme + host, no trailing slash, no path). Save; Render redeploys.
2. Open the Vercel URL and run a route. If you change `VITE_API_BASE_URL` later, **redeploy** on Vercel: Vite bakes environment variables in at build time.

## Automatic redeploys
Both services watch the `main` branch. Every `git push` to `main` rebuilds and redeploys them. Branch pushes create Vercel preview URLs (add those origins to `ALLOWED_ORIGINS` if you want to test them).

## Free-tier limitations
- Render free web services **spin down after about 15 minutes without traffic**; the next request can take 30 to 60 seconds. The app shows an error with a retry button if the first call fails; click **Try again**. Before a demo, open `<backend-url>/api/health` a minute early.
- Free instances have limited CPU, RAM and monthly hours; plenty for this project.
- Vercel's Hobby plan is intended for personal, non-commercial use.
- Free-tier terms change; check each provider's pricing page.

## Troubleshooting
| Symptom | Cause / fix |
|---|---|
| "Cannot reach the PATHFINDER backend" | Backend asleep or `VITE_API_BASE_URL` missing/wrong. Test `/api/health`; redeploy Vercel after changing variables. |
| CORS error in browser console | Vercel URL missing from `ALLOWED_ORIGINS`, or it has a trailing slash. |
| Render build fails | Root Directory must be `backend`; check `requirements.txt` is there. |
| Vercel 404 on refresh | Root Directory must be `frontend` so `vercel.json` is picked up. |
