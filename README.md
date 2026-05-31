# AI Code Reviewer

A GitHub App that automatically reviews pull requests using a multi-agent AI pipeline built on Claude. Three specialized agents (Security, Logic, Style) analyze every PR in parallel and post a synthesized review comment directly on GitHub.

![Dashboard preview](https://raw.githubusercontent.com/ali-fadoo/ai-code-reviewer/main/docs/preview.png)

## How it works

```
PR opened/updated
      │
      ▼
 GitHub Webhook
      │
      ▼
 FastAPI Backend
      │
      ├──► Security Agent  ─┐
      ├──► Logic Agent     ─┼──► Synthesizer Agent ──► GitHub PR Comment
      └──► Style Agent     ─┘
      │
      ▼
 SQLite (review stored)
      │
      ▼
 React Dashboard
```

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Python 3.12 |
| AI | Google Gemini 1.5 Flash (free tier) |
| Database | SQLite + SQLAlchemy (async) |
| Frontend | React 18, TypeScript, Tailwind CSS |
| Deployment | Docker Compose / Railway |

## Setup

### 1. Create a GitHub App

1. Go to **GitHub → Settings → Developer Settings → GitHub Apps → New GitHub App**
2. Set:
   - **Webhook URL**: `https://your-backend-url/webhook`
   - **Webhook secret**: any random string (save it)
3. Permissions:
   - **Pull requests**: Read & Write
   - **Contents**: Read-only
4. Subscribe to events: `Pull request`
5. Generate a **private key** (.pem file) and download it

### 2. Configure environment

```bash
cp .env.example .env
```

Fill in `.env`:
- `GOOGLE_API_KEY` — get one free at [aistudio.google.com](https://aistudio.google.com/app/apikey)
- `GITHUB_APP_ID` — shown on your GitHub App's settings page
- `GITHUB_WEBHOOK_SECRET` — the random string you set above
- `GITHUB_PRIVATE_KEY` — contents of the .pem file, with newlines replaced by `\n`

### 3. Run locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Or with Docker:

```bash
docker compose up --build
```

### 4. Expose your local server (for webhook testing)

```bash
# Using ngrok
ngrok http 8000
# Copy the https URL → set as webhook URL in your GitHub App
```

### 5. Install the App

On your GitHub App settings page, click **Install App** and choose which repos to install it on. Any PR opened in those repos will trigger a review.

## Deploy to Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app)

1. Push this repo to GitHub
2. New project on Railway → Deploy from GitHub repo
3. Add a service for `backend/` with the env vars from `.env.example`
4. Add a service for `frontend/` 
5. Set your Railway backend URL as the GitHub App webhook URL

## Dashboard

Visit `http://localhost:5173` (dev) or your deployed frontend URL to see all reviews, severity stats, and drill into individual agent reports.

<!-- test -->
 
.
