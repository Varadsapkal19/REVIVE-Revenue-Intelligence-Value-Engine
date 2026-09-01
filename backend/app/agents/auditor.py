from app.services.audit_service import AuditService

class AuditorAgent:
    async def record(self, case, sentinel_out, diagnosis_out, strategy_out, guardrail_result, execution_out) -> dict:
        service = AuditService()
        log = service.record_decision(
            case_id=case.id,
            agent="REVIVE Orchestrator",
            action=strategy_out["selected_action"],
            reason=diagnosis_out["reasoning"],
            evidence=diagnosis_out["evidence"],
            policy_checks=guardrail_result["checks"],
            execution_result=execution_out["status"]
        )
        return {"audit_id": str(log.id), "decision_id": log.decision_id}
