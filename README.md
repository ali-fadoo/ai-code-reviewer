# AI Code Reviewer

A GitHub App that automatically reviews pull requests using a **multi-agent AI pipeline**. Three specialized agents (Security, Logic, Style) analyze every PR in parallel and post a synthesized review comment directly on GitHub.

**Live Demo** → [Dashboard](https://dist-delta-one-72.vercel.app) | [GitHub App](https://github.com/settings/apps/ali-code-reviewer)

---

## How it works

```
PR opened / updated
        │
        ▼
 GitHub Webhook
        │
        ▼
 FastAPI Backend (Railway)
        │
        ├──► Security Agent ─┐
        ├──► Logic Agent    ─┼──► Synthesizer ──► GitHub PR Comment
        └──► Style Agent    ─┘
        │
        ▼
 SQLite  ──►  React Dashboard (Vercel)
```

All three agents run **in parallel** using `asyncio.gather`, keeping review time under ~5 seconds.

---

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI, Python 3.11, SQLAlchemy (async) |
| AI | Groq API — Llama 3.3 70B (free tier) |
| Database | SQLite + aiosqlite |
| Frontend | React 18, TypeScript, Tailwind CSS, Vite |
| Deployment | Railway (backend) + Vercel (frontend) |

---

## What each agent does

| Agent | Looks for |
|---|---|
| **Security** | Hardcoded secrets, SQL injection, XSS, path traversal, SSRF, insecure auth |
| **Logic** | Edge cases, race conditions, off-by-one errors, resource leaks, wrong types |
| **Style** | Complexity, duplication, poor naming, missing docs, single-responsibility violations |
| **Synthesizer** | Merges all three into one clean GitHub comment with a final verdict |

---

## Local setup

### 1. Clone & configure

```bash
git clone https://github.com/ali-fadoo/ai-code-reviewer
cd ai-code-reviewer
cp .env.example backend/.env
```

Fill in `backend/.env`:

```env
GROQ_API_KEY=        # free at console.groq.com
GITHUB_APP_ID=       # from your GitHub App settings
GITHUB_WEBHOOK_SECRET=
GITHUB_PRIVATE_KEY=  # contents of .pem file, newlines as \n
```

### 2. Create a GitHub App

1. Go to **GitHub → Settings → Developer Settings → GitHub Apps → New GitHub App**
2. Set **Webhook URL** → your backend URL + `/webhook`
3. Permissions: **Pull requests** (Read & Write), **Contents** (Read-only)
4. Subscribe to: `Pull request` events
5. Generate and download a **private key** (.pem)
6. Click **Install App** on the repos you want reviewed

### 3. Run locally

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Expose for webhooks (new terminal)
cloudflared tunnel --url http://localhost:8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## Deploy

### Backend → Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway up ./backend --path-as-root
railway variables set GROQ_API_KEY=... GITHUB_APP_ID=... GITHUB_WEBHOOK_SECRET=... GITHUB_PRIVATE_KEY=...
railway domain
```

### Frontend → Vercel

```bash
npm install -g vercel
cd frontend
VITE_API_URL=https://your-railway-url.up.railway.app npm run build
vercel deploy dist --prod
```

Update your GitHub App webhook URL to the Railway domain.

---

## Example review

> When a PR adds a vulnerable `charge_user()` function, the bot posts:
>
> **Critical Issues 🔴** — Hardcoded Stripe API key (`sk_live_...`), SQL injection via string concatenation
>
> **Warnings ⚠️** — Missing error handling on HTTP call, no return value on failure
>
> **Suggestions 💡** — O(n²) loop in `get_all_transactions` can be replaced with a single query
>
> **Verdict: REQUEST CHANGES ❌**
