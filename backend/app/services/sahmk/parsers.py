from __future__ import annotations

from typing import Any


def extract_quote_price(quote: Any) -> float | None:
    """Extract a numeric market price without fabricating a fallback value."""
    if not isinstance(quote, dict):
        return None

    candidates: list[Any] = [
        quote.get("price"),
        quote.get("last_price"),
        quote.get("close"),
    ]

    data = quote.get("data")
    if isinstance(data, dict):
        candidates.extend([data.get("price"), data.get("last_price"), data.get("close")])

    for value in candidates:
        if isinstance(value, bool) or value is None:
            continue
        try:
            numeric = float(value)
        except (TypeError, ValueError):
            continue
        if numeric > 0:
            return numeric

    return None


def summarize_payload(payload: Any) -> dict[str, Any]:
    """Small diagnostics summary; never exposes credentials and avoids dumping huge payloads."""
    if isinstance(payload, dict):
        return {
            "type": "object",
            "keys": sorted(str(key) for key in payload.keys())[:40],
            "symbol": payload.get("symbol"),
            "count": payload.get("count"),
            "is_delayed": payload.get("is_delayed"),
        }
    if isinstance(payload, list):
        return {"type": "array", "count": len(payload)}
    return {"type": type(payload).__name__}
