from typing import Any


def build_decision(
    fundamentals: dict[str, Any],
    valuation: dict[str, Any],
    liquidity: dict[str, Any],
    risk: dict[str, Any],
) -> dict[str, Any]:
    """Final decision is intentionally conservative in v0.1.0.

    No BUY/SELL label is emitted before the validated scoring, veto rules,
    MOS logic and backtesting phase are implemented.
    """
    return {
        "decision": "insufficient_data",
        "reason": "Decision rules are not finalized in v0.1.0.",
        "components": {
            "fundamentals": fundamentals,
            "valuation": valuation,
            "liquidity": liquidity,
            "risk": risk,
        },
    }
