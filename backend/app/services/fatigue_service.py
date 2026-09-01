class FatigueService:
    def calculate_fatigue(self, customer_id, recent_interventions, engagement_history) -> float:
        num_interventions_last_24h = len(recent_interventions)
        score = min(100.0, num_interventions_last_24h * 20.0)
        return score
