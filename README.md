# Saudi Investment AI — Phase 1

Investment decision-support platform for Saudi listed stocks.

## Architecture

- **Frontend:** Flutter / Dart
- **Backend:** Python / FastAPI
- **Database target:** PostgreSQL
- **Market-data source:** SAHMK Pro
- **Real-time target:** SAHMK REST + WebSocket

## Current status

Phase 1 focuses only on **verified SAHMK data transport**. The repository deliberately does **not** emit BUY/SELL decisions yet.

Implemented SAHMK paths:

```text
/quote/{symbol}/
/company/{symbol}/
/historical/{symbol}/
/financials/{symbol}/
/analytics/ratios/{symbol}/
/market/trades/{symbol}/
```

The historical client uses SAHMK's documented `interval/from/to/limit/offset` parameters. Pro financials request quarterly extended history, and executed trades are available for later liquidity/order-flow work.

## Security

Never put a real API key in GitHub.

Copy:

```text
.env.example -> .env
```

Then set locally:

```env
SAHMK_API_KEY=your_real_key_here
```

`.env` is excluded by `.gitignore`.

## Fastest Windows start

Double-click:

```text
START_BACKEND_WINDOWS.bat
```

On first run it creates the Python virtual environment and installs requirements. If `.env` does not exist it creates one from `.env.example`; add the key, then restart.

## Manual backend start

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/api/v1/health
http://127.0.0.1:8000/api/v1/stocks/2222/diagnostics
```

## Important

The final investment engine will be built only after real Pro payloads are validated. No missing financial value may be silently replaced with zero or demo data.

See `docs/PHASE1_SAHMK.md` and `docs/NEXT_STEPS.md`.
