from typing import Any


def build_financial_snapshot(
    company: Any,
    financials: Any,
    ratios: Any | None = None,
) -> dict[str, Any]:
    """Initial normalization boundary.

    Phase 1 intentionally preserves raw SAHMK payloads. Exact normalized field
    mapping and accounting rules are implemented only after a real Pro payload
    is captured and verified for operating companies, banks and REITs.
    """
    return {
        "company": company,
        "financials": financials,
        "ratios": ratios,
        "normalized": False,
        "warnings": [
            "Financial field mapping is pending validation against real SAHMK Pro payloads."
        ],
    }
