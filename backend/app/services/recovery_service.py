from app.models.merchant_policy import MerchantPolicy

class RecoveryService:
    def calculate_expected_value(self, action: str, probability: float, amount: float, fatigue: float, policy: MerchantPolicy) -> float:
        intervention_costs = {
            'retry': 0,
            'payment_link': 50,
            'whatsapp': 30,
            'voice': 100,
            'human': 500,
            'no_action': 0
        }
        cost = intervention_costs.get(action, 50)
        fatigue_penalty = fatigue * 10
        return max(0.0, (probability * amount) - cost - fatigue_penalty)

    def select_best_action(self, case, probabilities: dict, policy: MerchantPolicy) -> dict:
        best_action = "no_action"
        best_ev = self.calculate_expected_value("no_action", 0.1, case.amount, case.fatigue_score, policy)
        
        for action, prob in probabilities.items():
            ev = self.calculate_expected_value(action, prob, case.amount, case.fatigue_score, policy)
            if ev > best_ev:
                best_ev = ev
                best_action = action
                
        return {"action": best_action, "ev": best_ev}

    def get_action_ranking(self, case, probabilities: dict, policy: MerchantPolicy) -> list:
        ranking = []
        for action, prob in probabilities.items():
            ev = self.calculate_expected_value(action, prob, case.amount, case.fatigue_score, policy)
            ranking.append({"action": action, "ev": ev})
        return sorted(ranking, key=lambda x: x["ev"], reverse=True)
