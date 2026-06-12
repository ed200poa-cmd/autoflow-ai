# AutoFlow AI Demo

**n8n Workflow Automation + Claude AI Lead Scoring Pipeline**

Built by **Edward Kim** — AI Automation Developer

---

## Overview

AutoFlow AI Demo is a complete lead qualification automation system that:

1. Accepts lead submissions via a web form or n8n webhook
2. Sends lead data to a FastAPI backend
3. Uses **Claude AI (Haiku)** to score leads as **Hot / Warm / Cold**
4. Returns a personalized email draft and follow-up date
5. Simulates Slack notification, Google Sheets logging, and Gmail send

---

## Architecture

```
Lead Form / n8n Webhook
        ↓
  FastAPI Backend (/analyze-lead or /webhook/n8n)
        ↓
  Claude AI (claude-haiku-4-5) — Lead Scoring
        ↓
  SQLite — Persist result
        ↓
  Simulated: Slack / Google Sheets / Gmail
```

---

## Scoring Logic

| Score | Budget     | Follow-up  |
|-------|------------|------------|
| 🔥 Hot  | > $1,000   | Within 24h |
| ✨ Warm | $300–$1,000 | Within 1 week |
| ❄️ Cold | < $300     | Nurture sequence |

---

## Quick Start

### 1. Install dependencies

```bash
cd autoflow_demo
pip install -r requirements.txt
```

### 2. Set up environment

```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 3. Run the server

```bash
uvicorn main:app --reload
```

Open [http://localhost:8000](http://localhost:8000)

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET`  | `/` | Demo frontend |
| `GET`  | `/health` | Health check |
| `POST` | `/analyze-lead` | Analyze a lead with Claude AI |
| `POST` | `/webhook/n8n` | n8n webhook receiver |
| `GET`  | `/dashboard` | All leads + stats (JSON) |

### Example request

```bash
curl -X POST http://localhost:8000/analyze-lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Chen",
    "email": "sarah@techcorp.com",
    "company": "TechCorp Inc",
    "budget": 5000,
    "message": "We need enterprise AI automation ASAP."
  }'
```

---

## n8n Workflow

Import `n8n_workflow.json` into your n8n instance.

**Setup:**
1. Import the JSON file via n8n → Workflows → Import
2. Update the HTTP Request node URL to your deployed FastAPI URL
3. Enable and configure credentials for Slack, Gmail, Google Sheets
4. Activate the workflow — the webhook URL is `POST /webhook/lead-intake`

---

## File Structure

```
autoflow_demo/
├── main.py              # FastAPI app + all endpoints
├── claude_analyzer.py   # Claude AI lead scoring
├── database.py          # SQLite async operations
├── static/
│   └── index.html       # Demo frontend (Tailwind CSS)
├── n8n_workflow.json    # Importable n8n workflow
├── requirements.txt
├── Procfile             # For Heroku/Railway deployment
├── .env.example
└── README.md
```

---

## Tech Stack

- **FastAPI** — async Python web framework
- **Claude AI** (claude-haiku-4-5) — lead scoring & email drafting
- **SQLite + aiosqlite** — async local database
- **n8n** — workflow automation orchestration
- **Tailwind CSS** — frontend styling

---

*Built by Edward Kim — AI Automation Developer*
