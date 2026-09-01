from app.models.recovery_case import RecoveryCase
from app.models.merchant_policy import MerchantPolicy
from app.services.recovery_service import RecoveryService

class StrategistAgent:
    async def strategize(self, case: RecoveryCase, diagnosis: dict, policy: MerchantPolicy, fatigue: float) -> dict:
        service = RecoveryService()
        probs = {"retry": 0.6, "payment_link": 0.8, "whatsapp": 0.5, "no_action": 0.2}
        best = service.select_best_action(case, probs, policy)
        ranking = service.get_action_ranking(case, probs, policy)
        return {
            "selected_action": best["action"],
            "expected_value": best["ev"],
            "action_ranking": ranking,
            "natural_baseline": case.amount * 0.1,
            "incremental_recovery": best["ev"] - (case.amount * 0.1)
        }
