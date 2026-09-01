from app.models.merchant_policy import MerchantPolicy

class PolicyService:
    def validate_action(self, proposed_action: str, policy: MerchantPolicy, customer, fatigue_score: float) -> dict:
        checks = []
        approved = True
        
        if fatigue_score >= 90:
            checks.append({"name": "FATIGUE", "passed": False, "reason": "Fatigue score too high"})
            approved = False
        else:
            checks.append({"name": "FATIGUE", "passed": True, "reason": "Fatigue acceptable"})
            
        return {
            "approved": approved,
            "status": "AUTHORIZED" if approved else "BLOCKED",
            "checks": checks
        }
