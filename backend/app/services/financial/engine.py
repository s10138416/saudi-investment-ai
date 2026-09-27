from typing import Any


def build_financial_snapshot(company: Any, financials: Any) -> dict[str, Any]:
    """Initial normalization layer. Exact field mapping must be finalized after inspecting real SAHMK Pro payloads."""
    return {
        "company": company,
        "financials": financials,
        "normalized": False,
        "warnings": [
            "Financial field mapping is intentionally pending until real SAHMK Pro payloads are validated."
        ],
    }
