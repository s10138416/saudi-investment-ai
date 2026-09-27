# Saudi Investment AI v0.1.0

Starter architecture for a Saudi-market investment decision engine.

## Stack
- Frontend: Flutter / Dart
- Backend: Python 3.12 + FastAPI
- Database: PostgreSQL
- Market data: SAHMK Pro (server-side only)
- Realtime-ready: WebSocket architecture

## What this version includes
- FastAPI backend skeleton
- Health endpoint
- SAHMK client service with secure env-based API key handling
- Placeholder endpoints for stock profile and unified analysis
- PostgreSQL-ready configuration
- Flutter starter UI connected to backend health endpoint
- Docker Compose for backend + PostgreSQL
- Investment-engine module structure for financial, fundamental, valuation, liquidity, risk, and decision layers

## What is intentionally NOT finalized in v0.1.0
- Hero Card investment logic
- MOS-based final decision rules
- Institutional accumulation classification
- Sector-specific scoring weights
- Backtesting / walk-forward engine

These should be added only after confirming the exact SAHMK Pro payloads and historical depth.

## Quick start with Docker
1. Copy `.env.example` to `.env`.
2. Put your SAHMK key in `.env` locally. Never commit `.env`.
3. Run:

```bash
docker compose up --build
```

Backend:
- http://localhost:8000
- API docs: http://localhost:8000/docs
- Health: http://localhost:8000/api/v1/health

## Local backend start without Docker

```bash
cd backend
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Flutter

```bash
cd frontend
flutter pub get
flutter run
```

By default Flutter expects backend at `http://127.0.0.1:8000`.
For Android emulator you may need `http://10.0.2.2:8000`.
