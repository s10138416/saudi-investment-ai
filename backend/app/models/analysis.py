from pydantic import BaseModel, Field


class DataConfidence(BaseModel):
    score: float = Field(ge=0, le=100)
    missing_fields: list[str] = []
    warnings: list[str] = []


class InvestmentSnapshot(BaseModel):
    symbol: str
    company_name: str | None = None
    sector: str | None = None
    price: float | None = None
    fundamental_score: float | None = None
    valuation_score: float | None = None
    liquidity_score: float | None = None
    risk_score: float | None = None
    margin_of_safety: float | None = None
    accumulation_signal: str = "not_evaluated"
    final_decision: str = "insufficient_data"
    confidence: DataConfidence
