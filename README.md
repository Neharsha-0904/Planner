<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" />
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" />
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" />
  <img src="https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" />
</p>

<h1 align="center">⚡ Planner</h1>
<p align="center"><strong>Personal Command Center for Grad Students</strong></p>
<p align="center">
  <em>Plan your day. Track your roadmap. Never let a task slip.</em>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-features">Features</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-scheduled-jobs">Scheduled Jobs</a> •
  <a href="#-api">API</a> •
  <a href="#-roadmap">Roadmap</a>
</p>

---

## 🎯 What is this?

A single-app personal command center for grad students managing academics, career prep, and daily planning. One shared database — tasks, timetable, milestones, contacts, and finance all live together. New modules plug into the same spine; never a separate mini-app.

**Built for daily use:** open it every morning, see what matters, get nudged when things slip.

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 📋 Task Engine
- P0 / P1 / P2 priorities (heat scale)
- Tasks **never auto-complete** — only you close them
- Auto-rollover at midnight (never lost)
- Aging indicators at 3+ rollovers
- Tags, subtasks, milestone linking

</td>
<td width="50%">

### 🔔 Smart Notifications
- **Morning brief** — email + WhatsApp on startup
- **Class reminder** — WhatsApp 10 min before
- **9 PM nightly** — tomorrow's classes + tasks + backlog
- **P0 alerts** — hourly during waking hours
- **Daily backlog summary** — 8:30am
- Channels: Gmail SMTP + WhatsApp Cloud API + Firebase Push
- Gmail SMTP (no spam — from your own account)

</td>
</tr>
<tr>
<td width="50%">

### 🗺️ Roadmap Tracking
- Milestone-based progress tracking
- Courses, certifications, projects
- Visual skill dependency map (SVG)
- Link tasks to milestones for auto-progress
- Customizable per user

</td>
<td width="50%">

### 👥 Multi-User Ready
- Registration endpoint
- Per-user notification emails
- Per-user FCM push tokens
- Per-user timetable & milestones
- JWT auth with configurable expiry

</td>
</tr>
</table>

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│              React + Vite + Tailwind                 │
│          (dark theme, design-system tokens)          │
└──────────────────────┬──────────────────────────────┘
                       │ REST
┌──────────────────────┴──────────────────────────────┐
│                  FastAPI Backend                      │
│                                                      │
│   ┌─────────┐  ┌──────────┐  ┌──────────────────┐   │
│   │  Routes │  │ Services │  │  APScheduler     │   │
│   │  (API)  │  │ (Logic)  │  │  (5 cron jobs)   │   │
│   └─────────┘  └──────────┘  └──────────────────┘   │
│                                                      │
│   ┌─────────────────┐  ┌────────────────────────┐   │
│   │  Gmail SMTP     │  │  Firebase FCM (push)   │   │
│   └─────────────────┘  └────────────────────────┘   │
│   ┌──────────────────────────────────────────────┐   │
│   │       WhatsApp Cloud API (free 1K/mo)        │   │
│   └──────────────────────────────────────────────┘   │
│                                                      │
│   ┌──────────────────────────────────────────────┐   │
│   │       SQLAlchemy (sync) + Alembic            │   │
│   └──────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────┘
                       │
              ┌────────┴────────┐
              │  PostgreSQL 16  │
              │    (Docker)     │
              └─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version |
|------|---------|
| Docker | 20+ |
| Python | 3.11+ |
| Node.js | 18+ |

### Setup

```bash
# 1. Clone
git clone https://github.com/Neharsha-0904/Planner.git
cd Planner

# 2. Configure
cp .env.example .env
# Edit .env → set SECRET_KEY, optionally SMTP_USER + SMTP_PASSWORD

# 3. Database
docker compose up -d

# 4. Backend
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1    # Windows
# source .venv/bin/activate     # macOS/Linux
pip install -e ".[dev]"
alembic upgrade head
python -m seeds.seed_data

# 5. Run
uvicorn app.main:app --reload --port 8000

# 6. Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Login

| Field | Value |
|-------|-------|
| Email | `neharsha@planner.local` |
| Password | `planner123` |

---

## 📧 Email Setup (Gmail)

> Briefs land in your inbox, not spam — they're sent from your own account.

1. Enable **2-Factor Auth** on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate one for "Mail"
4. Add to `.env`:
```env
SMTP_USER=you@gmail.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
```

---

## ⏰ Scheduled Jobs

| Job | When | Channels | What |
|-----|------|----------|------|
| 🔄 Auto-rollover | 00:01 | DB | Past-due → today, `rolled_over_count++` |
| ☀️ Morning brief | On startup (after 7am) | Email + WhatsApp | Today's classes + tasks |
| 📚 Class reminder | Every 1 min | WhatsApp + Push | 10 min before each class |
| 🔴 P0 alert | Hourly (7–22) | Push | Critical tasks overdue |
| 📋 Backlog summary | 08:30 | Push | Full backlog stats |
| 🌙 Nightly schedule | 21:00 | Email + WhatsApp | Tomorrow's classes + tasks + backlog |

---

## 🔌 API

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `POST` | `/auth/register` | — | Create account |
| `POST` | `/auth/login` | — | Get JWT |
| `POST` | `/auth/fcm-token` | 🔒 | Register push token |
| `GET` | `/tasks?view=today\|backlog\|done` | 🔒 | List tasks |
| `POST` | `/tasks` | 🔒 | Create task |
| `GET` | `/tasks/{id}` | 🔒 | Detail |
| `PUT` | `/tasks/{id}` | 🔒 | Update |
| `DELETE` | `/tasks/{id}` | 🔒 | Delete |
| `POST` | `/tasks/{id}/complete` | 🔒 | Mark done |
| `GET` | `/health` | — | Status check |

Full interactive docs at **http://localhost:8000/docs**

---

## 🎨 Design System

Dark-first, color-for-meaning-only. See [`design-notes.md`](design-notes.md).

| Surface | Priority | Status |
|---------|----------|--------|
| `#0F1117` app bg | 🔴 `#EF4E52` P0 | 🟣 `#7C6BF0` in-progress |
| `#1A2130` cards | 🟡 `#F5A524` P1 | 🟢 `#34D399` done |
| `#2A3346` borders | ⚪ `#6B7486` P2 | ⚪ `#6B7486` backlog |

---

## 🗂️ Project Structure

```
Planner/
├── backend/
│   ├── app/
│   │   ├── api/           # Routes (auth, tasks, health)
│   │   ├── models/        # 7 SQLAlchemy models
│   │   ├── schemas/       # Pydantic validation
│   │   ├── services/      # Email, notifications, task logic
│   │   ├── jobs/          # 5 APScheduler jobs
│   │   ├── agent/         # [Phase 2] Claude AI
│   │   └── integrations/  # [Phase 1] M365, GitHub
│   ├── alembic/           # Migrations
│   ├── seeds/             # Seed data (real roadmap)
│   └── tests/             # Pytest suite
├── frontend/
│   └── src/
│       ├── pages/         # Today, Backlog, Done, Login
│       ├── components/    # TaskCard, Form, Layout
│       ├── hooks/         # React Query
│       └── types/         # TypeScript interfaces
├── docker-compose.yml
├── design-notes.md
└── README.md
```

---

## 🛣️ Roadmap

| Phase | Status | What |
|-------|--------|------|
| **0** | ✅ Done | Task CRUD, auto-rollover, views, auth, email, push, seed data |
| **1** | 🔜 Next | Timetable UI, class-aware day planner, M365 sync |
| **2** | 📋 Planned | Claude AI agent (chief-of-staff, NL commands, task decomposition) |
| **3** | 📋 Planned | Full notification suite, public website, contacts/watchers |
| **∞** | 💭 Ideas | Finance, analytics, habits, Pomodoro, voice capture |

---

## 🛠️ Dev Commands

```powershell
# Windows
.\dev.ps1 dev       # Docker + backend + frontend
.\dev.ps1 migrate   # Alembic upgrade head
.\dev.ps1 seed      # Seed database
.\dev.ps1 test      # Pytest
```

```bash
# macOS / Linux
make dev && make migrate && make seed && make test
```

---

<p align="center">
  <sub>Built with 🧠 by <a href="https://github.com/Neharsha-0904">Neharsha Vishnu</a> — M.Tech AI, Amrita Vishwa Vidyapeetham</sub>
</p>
