from app.models.revenue_event import RevenueEvent
import random
import uuid

class SimulationService:
    def generate_synthetic_events(self, num_events=10000) -> list:
        events = []
        for _ in range(num_events):
            event = RevenueEvent(
                id=uuid.uuid4(),
                event_type="payment_failed",
                customer_id=uuid.uuid4(),
                amount=random.uniform(500, 50000),
                currency="INR",
                status="pending",
                raw_payload={}
            )
            events.append(event)
        return events

    def run_batch_recovery(self, num_cases: int, scenario_filter: str = None) -> dict:
        total_events = num_cases
        revenue_at_risk = num_cases * 5000.0
        potentially_recoverable = revenue_at_risk * 0.8
        revive_recovery = potentially_recoverable * 0.6
        incremental_recovery = revive_recovery * 0.3
        recovery_rate = revive_recovery / max(revenue_at_risk, 1)

        return {
            "total_events": total_events,
            "revenue_at_risk": revenue_at_risk,
            "potentially_recoverable": potentially_recoverable,
            "revive_recovery": revive_recovery,
            "incremental_recovery": incremental_recovery,
            "recovery_rate": recovery_rate,
            "interventions_count": int(num_cases * 0.5),
            "blocked_count": int(num_cases * 0.1),
            "human_escalations": int(num_cases * 0.05),
            "by_action": {"payment_link": int(num_cases * 0.3), "retry": int(num_cases * 0.2)},
            "by_root_cause": {"INSUFFICIENT_FUNDS": int(num_cases * 0.4)},
            "funnel_data": []
        }
