class DiagnosisService:
    def classify_root_cause(self, event, payment, recent_events) -> tuple[str, float, list]:
        if payment and payment.failure_reason:
            reason = payment.failure_reason.lower()
            if 'insufficient' in reason:
                return "INSUFFICIENT_FUNDS", 0.95, [{"type": "failure_reason", "value": payment.failure_reason}]
            elif 'expired' in reason:
                return "EXPIRED_CARD", 0.95, [{"type": "failure_reason", "value": payment.failure_reason}]
        
        if len(recent_events) >= 3:
            return "ISSUER_DEGRADATION", 0.85, [{"type": "recent_failures_count", "value": len(recent_events)}]
        
        return "NETWORK_FAILURE", 0.60, []
