from app.models.audit_log import AuditLog
import uuid
from datetime import datetime

class AuditService:
    def record_decision(self, case_id, agent, action, reason, evidence, policy_checks, execution_result) -> AuditLog:
        decision_id = f"RV-{datetime.utcnow().strftime('%Y%md')}-{uuid.uuid4().hex[:8]}"
        log = AuditLog(
            case_id=case_id,
            decision_id=decision_id,
            agent=agent,
            action=action,
            reason=reason,
            evidence=evidence,
            policy_checks=policy_checks,
            execution_result=execution_result
        )
        return log
