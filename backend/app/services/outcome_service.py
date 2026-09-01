class OutcomeService:
    def record_outcome(self, case_id, actual_recovery: float) -> dict:
        # update case actual_recovery
        return {"case_id": case_id, "status": "recorded"}

    def calculate_incremental_recovery(self, actual: float, natural_baseline: float) -> float:
        return actual - natural_baseline
