from fastapi import APIRouter
from app.services.audit_service import AuditService

router = APIRouter(prefix="/api/audit", tags=["Audit"])

@router.get("")
def list_audit_logs():
    return {
        "logs": [
            AuditService.build_audit_log("RV-82931", "Strategist", "Voice Call", "Highest expected incremental recovery (EV: INR 13,400)", ["31 failures from HDFC Bank within 12 minutes"], [{"name": "CONSENT", "passed": True}], "AUTHORIZED"),
            AuditService.build_audit_log("RV-82932", "PolicyEngine", "15% Discount", "Requested discount 15% exceeds merchant policy max 10%", ["Requested discount exceed limit"], [{"name": "DISCOUNT", "passed": False}], "BLOCKED"),
            AuditService.build_audit_log("RV-82933", "Orchestrator", "Payment Link", "Executed recovery link dispatch", ["Card expired"], [{"name": "AMOUNT", "passed": True}], "AUTHORIZED"),
        ]
    }
