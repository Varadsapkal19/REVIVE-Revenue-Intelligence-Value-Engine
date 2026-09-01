from app.models.revenue_event import RevenueEvent
from app.models.customer import Customer
from app.models.payment import Payment
from app.schemas.risk import RiskScore

class RiskService:
    def calculate_risk_score(self, event: RevenueEvent, customer: Customer, payment: Payment) -> RiskScore:
        failure_risk = 0.8
        revenue_exposure = min(event.amount / 100000.0, 1.0)
        historical_failure_risk = 0.5
        time_urgency = 0.9
        cohort_anomaly = 0.2
        customer_behavior = 0.4
        
        score = (
            0.35 * failure_risk +
            0.20 * revenue_exposure +
            0.15 * historical_failure_risk +
            0.10 * time_urgency +
            0.10 * cohort_anomaly +
            0.10 * customer_behavior
        )
        
        priority = "low"
        if score > 0.8: priority = "critical"
        elif score > 0.6: priority = "high"
        elif score > 0.4: priority = "medium"

        return RiskScore(
            score=score,
            priority=priority,
            revenue_exposure=revenue_exposure,
            historical_failure_risk=historical_failure_risk,
            cohort_anomaly=cohort_anomaly
        )
    
    def get_cohort_anomaly_score(self) -> float:
        return 0.2

    def get_historical_failure_risk(self) -> float:
        return 0.5

    def prioritize_cases(self, cases: list) -> list:
        return sorted(cases, key=lambda x: x.risk_score, reverse=True)
