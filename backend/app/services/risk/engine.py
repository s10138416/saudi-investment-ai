from typing import Any


def calculate_risk(financial_snapshot: dict[str, Any], history: Any = None) -> dict[str, Any]:
    return {
        "score": None,
        "level": "not_evaluated",
        "status": "pending_data",
    }
