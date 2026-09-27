from fastapi import APIRouter, HTTPException
from app.core.config import get_settings
from app.services.sahmk.client import sahmk_client, SahmkError
from app.services.financial.engine import build_financial_snapshot
from app.services.fundamental.engine import calculate_fundamental_score
from app.services.valuation.engine import calculate_valuation
from app.services.liquidity.engine import analyze_liquidity
from app.services.risk.engine import calculate_risk
from app.services.decision.engine import build_decision

router = APIRouter()
settings = get_settings()


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "sahmk_configured": sahmk_client.configured,
        "sahmk_plan": settings.sahmk_plan,
    }


@router.get("/stocks/{symbol}/raw")
async def stock_raw(symbol: str) -> dict:
    symbol = symbol.strip()
    try:
        company = await sahmk_client.get_company(symbol)
        quote = await sahmk_client.get_quote(symbol)
        financials = await sahmk_client.get_financials(symbol)
        return {"symbol": symbol, "company": company, "quote": quote, "financials": financials}
    except SahmkError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get("/stocks/{symbol}/analyze")
async def analyze_stock(symbol: str) -> dict:
    symbol = symbol.strip()
    try:
        company = await sahmk_client.get_company(symbol)
        quote = await sahmk_client.get_quote(symbol)
        financials = await sahmk_client.get_financials(symbol)
    except SahmkError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    # Exact price extraction will be finalized after validating the real quote payload.
    price = None
    snapshot = build_financial_snapshot(company, financials)
    fundamentals = calculate_fundamental_score(snapshot)
    valuation = calculate_valuation(snapshot, price)
    liquidity = analyze_liquidity()
    risk = calculate_risk(snapshot)
    decision = build_decision(fundamentals, valuation, liquidity, risk)

    return {
        "symbol": symbol,
        "raw_quote": quote,
        "analysis": decision,
    }
