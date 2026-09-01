from app.models.revenue_event import RevenueEvent
from app.services.risk_service import RiskService

class SentinelAgent:
    async def process_event(self, event: RevenueEvent) -> dict:
        risk_service = RiskService()
        risk = risk_service.calculate_risk_score(event, None, None)
        return {
            "case_id": event.id,
            "risk_score": risk.score,
            "revenue_at_risk": event.amount,
            "priority": risk.priority,
            "anomaly_detected": False
        }
