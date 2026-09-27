from __future__ import annotations

from typing import Any, Awaitable, Callable

from fastapi import APIRouter, HTTPException, Query

from app.core.config import get_settings
from app.services.decision.engine import build_decision
from app.services.financial.engine import build_financial_snapshot
from app.services.fundamental.engine import calculate_fundamental_score
from app.services.liquidity.engine import analyze_liquidity
from app.services.risk.engine import calculate_risk
from app.services.sahmk.client import SahmkError, sahmk_client
from app.services.sahmk.parsers import extract_quote_price, summarize_payload
from app.services.valuation.engine import calculate_valuation

router = APIRouter()
settings = get_settings()


def _clean_symbol(symbol: str) -> str:
    cleaned = symbol.strip()
    if not cleaned:
        raise HTTPException(status_code=400, detail="Symbol is required")
    return cleaned


def _http_status_for_sahmk_error(exc: SahmkError) -> int:
    if exc.code == "NO_KEY":
        return 503
    if exc.status_code in {400, 401, 403, 404, 429}:
        return exc.status_code
    return 502


async def _diagnostic_call(
    name: str,
    call: Callable[[], Awaitable[Any]],
) -> tuple[str, dict[str, Any]]:
    try:
        payload = await call()
        return name, {"ok": True, "summary": summarize_payload(payload)}
    except SahmkError as exc:
        return name, {
            "ok": False,
            "error": str(exc),
            "code": exc.code,
            "upstream_status": exc.status_code,
        }


@router.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.app_env,
        "sahmk_configured": sahmk_client.configured,
        "sahmk_plan": settings.sahmk_plan,
        "phase": "phase-1-sahmk-integration",
    }


@router.get("/stocks/{symbol}/diagnostics")
async def stock_diagnostics(symbol: str) -> dict:
    """Validate the real SAHMK Pro payloads before we hard-code financial mappings."""
    symbol = _clean_symbol(symbol)

    checks = [
        await _diagnostic_call("quote", lambda: sahmk_client.get_quote(symbol)),
        await _diagnostic_call("company", lambda: sahmk_client.get_company(symbol)),
        await _diagnostic_call(
            "historical",
            lambda: sahmk_client.get_historical(symbol, interval="1d", limit=5),
        ),
        await _diagnostic_call(
            "financials",
            lambda: sahmk_client.get_financials(
                symbol,
                period="quarterly",
                history="5y",
                metrics="extended",
                limit=4,
            ),
        ),
        await _diagnostic_call(
            "ratios",
            lambda: sahmk_client.get_ratios(
                symbol,
                history="5y",
                period="quarterly",
                metrics="extended",
            ),
        ),
        await _diagnostic_call("trades", lambda: sahmk_client.get_trades(symbol, limit=5)),
    ]

    result = dict(checks)
    passed = sum(1 for item in result.values() if item["ok"])
    return {
        "symbol": symbol,
        "configured": sahmk_client.configured,
        "plan_config": settings.sahmk_plan,
        "passed": passed,
        "total": len(result),
        "checks": result,
    }


@router.get("/stocks/{symbol}/raw")
async def stock_raw(
    symbol: str,
    include_history: bool = Query(default=False),
    include_trades: bool = Query(default=False),
) -> dict:
    symbol = _clean_symbol(symbol)
    try:
        company = await sahmk_client.get_company(symbol)
        quote = await sahmk_client.get_quote(symbol)
        financials = await sahmk_client.get_financials(symbol)
        ratios = await sahmk_client.get_ratios(symbol)
        payload: dict[str, Any] = {
            "symbol": symbol,
            "price": extract_quote_price(quote),
            "company": company,
            "quote": quote,
            "financials": financials,
            "ratios": ratios,
        }
        if include_history:
            payload["historical"] = await sahmk_client.get_historical(symbol, interval="1d", limit=500)
        if include_trades:
            payload["trades"] = await sahmk_client.get_trades(symbol, limit=100)
        return payload
    except SahmkError as exc:
        raise HTTPException(status_code=_http_status_for_sahmk_error(exc), detail=str(exc)) from exc


@router.get("/stocks/{symbol}/analyze")
async def analyze_stock(symbol: str) -> dict:
    symbol = _clean_symbol(symbol)
    try:
        company = await sahmk_client.get_company(symbol)
        quote = await sahmk_client.get_quote(symbol)
        financials = await sahmk_client.get_financials(symbol)
        ratios = await sahmk_client.get_ratios(symbol)
        history = await sahmk_client.get_historical(symbol, interval="1d", limit=500)
        trades = await sahmk_client.get_trades(symbol, limit=100)
    except SahmkError as exc:
        raise HTTPException(status_code=_http_status_for_sahmk_error(exc), detail=str(exc)) from exc

    price = extract_quote_price(quote)
    snapshot = build_financial_snapshot(company, financials, ratios)
    fundamentals = calculate_fundamental_score(snapshot)
    valuation = calculate_valuation(snapshot, price)
    liquidity = analyze_liquidity(history=history, trades=trades)
    risk = calculate_risk(snapshot, history=history)
    decision = build_decision(fundamentals, valuation, liquidity, risk)

    return {
        "symbol": symbol,
        "price": price,
        "quote_is_delayed": quote.get("is_delayed") if isinstance(quote, dict) else None,
        "analysis": decision,
        "phase_note": (
            "Phase 1 validates data transport only. Final financial normalization, "
            "scoring and investment decisions remain intentionally disabled."
        ),
    }
