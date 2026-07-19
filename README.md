# ⚡ Planner — Personal Command Center

A single-user personal command center for managing tasks, timetable, career roadmap, and daily planning. Built for a grad student running a demanding M.Tech AI schedule alongside a 14-month ML/AI career roadmap.

## Features

### Core
- **Task CRUD** with priorities (P0/P1/P2) — tasks stay open until YOU close them
- **Auto-rollover** — incomplete past-due tasks move to today at midnight, never lost
- **Today / Backlog / Done views** — aging indicators for neglected tasks (≥3 rollovers)
- **Daily Morning Brief** — emailed to all your configured addresses at 7am

### Notifications (Firebase + Email)
- **Class reminder** — push notification 10 minutes before every class
- **P0 backlog alerts** — hourly push during 7am-10pm if critical tasks are overdue
- **Daily backlog summary** — full backlog status at 8:30am
- **Morning brief** — sent to Gmail + university email (no spam — sends from your own account)

### Multi-user
- **Registration endpoint** — other people can create accounts
- **Per-user notification emails** — configure Gmail + university + any other addresses
- **FCM token** — each user registers their device for push notifications

### Roadmap & Planning
- **14 milestones** seeded from real career plan (MS AI Engineer ✓, Claude ✓, Andrew Ng, Karpathy, 3B1B, AWS SAA, NeetCode, RAG project, ML pipeline)
- **41 tasks** planned through September 2026 with realistic scheduling
- **22 class slots** from M.Tech AI Sem 1 timetable

## Architecture

```
┌─────────────────────────────────────────────────┐
│                React Frontend                    │
│        (Vite + TypeScript + Tailwind)            │
└──────────────────────┬──────────────────────────┘
                       │ REST API
┌──────────────────────┴──────────────────────────┐
│              FastAPI Backend                      │
│  ┌──────────┐  ┌───────────┐  ┌──────────────┐  │
│  │ API Layer│  │ Services  │  │ Jobs         │  │
│  │ (routes) │  │ (logic)   │  │ (APScheduler)│  │
│  └──────────┘  └───────────┘  └──────────────┘  │
│                       │                          │
│  ┌───────────────┐ ┌─────────────────────────┐   │
│  │ Email (SMTP)  │ │ Push (Firebase FCM)     │   │
│  └───────────────┘ └─────────────────────────┘   │
│                       │                          │
│  ┌──────────────────────────────────────────┐    │
│  │         SQLAlchemy (sync) + Alembic      │    │
│  └──────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────┘
                       │
              ┌────────┴────────┐
              │  PostgreSQL 16  │
              └─────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, SQLAlchemy (sync), Alembic |
| Scheduler | APScheduler (BackgroundScheduler, in-process) |
| Database | PostgreSQL 16 (Docker) |
| Email | Gmail SMTP (App Password) — no spam |
| Push | Firebase Cloud Messaging (FCM) |
| Frontend | React 18, Vite, TypeScript, Tailwind CSS |
| Auth | JWT (python-jose + passlib/bcrypt) |

## Quick Start

### 1. Clone & configure

```bash
git clone <repo-url>
cd Planner
cp .env.example .env
```

Edit `.env` — at minimum set:
- `SECRET_KEY` (any random string)
- `SMTP_USER` + `SMTP_PASSWORD` (Gmail + App Password for real emails)

### 2. Start PostgreSQL

```bash
docker compose up -d
```

### 3. Backend setup

```bash
cd backend
python -m venv .venv

# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -e ".[dev]"
```

### 4. Run migrations & seed

```bash
alembic upgrade head
python -m seeds.seed_data
```

### 5. Start the backend

```bash
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 6. Frontend (new terminal)

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### 7. Login

- **Email:** `neharsha@planner.local`
- **Password:** `planner123`

## Gmail SMTP Setup (for real daily briefs)

1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Generate an App Password for "Mail"
4. Put in `.env`:
   ```
   SMTP_USER=your.email@gmail.com
   SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
   ```
5. Briefs arrive in your inbox (not spam — it's from your own account)

## Firebase Push Setup (optional)

1. Create a project at https://console.firebase.google.com
2. Download service account JSON from Project Settings > Service Accounts
3. Set `FIREBASE_CREDENTIALS_PATH=/path/to/serviceAccount.json` in `.env`
4. Without Firebase config, push notifications are logged to console

## Scheduled Jobs

| Job | Schedule | What it does |
|-----|----------|-------------|
| Daily rollover | 00:01 | Moves past-due tasks to today, increments rollover count |
| Morning brief | 07:00 | Emails today's plan to all configured addresses |
| Class reminder | Every 1 min | Push notification 10 min before each class |
| P0 backlog alert | Hourly (7-22) | Push if critical tasks are overdue |
| Daily backlog summary | 08:30 | Push with full backlog stats |

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | No | Create account |
| POST | /auth/login | No | Get JWT token |
| POST | /auth/fcm-token | Yes | Register device push token |
| GET | /tasks?view=today\|backlog\|done | Yes | List tasks by view |
| POST | /tasks | Yes | Create task |
| GET | /tasks/{id} | Yes | Task detail |
| PUT | /tasks/{id} | Yes | Update task |
| DELETE | /tasks/{id} | Yes | Delete task |
| POST | /tasks/{id}/complete | Yes | Mark done |
| GET | /health | No | DB health check |

## Dev Scripts

```powershell
# Windows
.\dev.ps1 dev      # Docker + backend + frontend
.\dev.ps1 migrate  # Alembic upgrade head
.\dev.ps1 seed     # Seed database
.\dev.ps1 test     # Pytest
```

```bash
# macOS/Linux
make dev && make migrate && make seed && make test
```

## Upcoming

- **Phase 1:** Timetable UI, class-aware day planner, M365 calendar sync
- **Phase 2:** Claude AI agent (chief-of-staff, task decomposition, NL commands)
- **Phase 3:** Full notification suite, public website, contacts/watchers
- **Later:** Finance module, analytics, habits, Pomodoro, voice capture
