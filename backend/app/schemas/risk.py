from pydantic import BaseModel

class RiskScore(BaseModel):
    score: float
    priority: str
    revenue_exposure: float
    historical_failure_risk: float
    cohort_anomaly: float
