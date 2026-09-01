from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.agents.orchestrator import Orchestrator

router = APIRouter(prefix="/api/cases", tags=["Cases"])
orchestrator = Orchestrator()

# Mock seed case for Judge Mode and Case Detail
SAMPLE_EVENT = {
    "event_id": "82931-demo",
    "event_type": "issuer_degradation",
    "customer_id": "CUST-82931",
    "customer_name": "Priya Sharma",
    "customer_segment": "premium",
    "amount": 45000.0,
    "currency": "INR",
    "payment_method": "card",
    "root_cause_type": "ISSUER_DEGRADATION",
    "failure_reason": "31 failures from HDFC Bank within 12 minutes",
    "recent_failures_count": 3
}

@router.get("")
def list_cases(status: Optional[str] = None, priority: Optional[str] = None):
    # Process sample cases dynamically
    case1 = orchestrator.process(SAMPLE_EVENT)
    case2 = orchestrator.process({**SAMPLE_EVENT, "event_id": "82932-demo", "amount": 120000.0, "root_cause_type": "INSUFFICIENT_FUNDS", "customer_name": "Stark Ind"})
    case3 = orchestrator.process({**SAMPLE_EVENT, "event_id": "82933-demo", "amount": 32000.0, "root_cause_type": "EXPIRED_CARD", "customer_name": "Wayne Ent"})
    case4 = orchestrator.process({**SAMPLE_EVENT, "event_id": "82934-demo", "amount": 85000.0, "root_cause_type": "INVOICE_OVERDUE", "customer_name": "Cyberdyne"})

    cases = [case1, case2, case3, case4]
    
    if priority:
        cases = [c for c in cases if c["priority"] == priority]
        
    return {"cases": cases, "total": len(cases)}

@router.get("/{case_id}")
def get_case(case_id: str):
    # Generate case trace dynamically
    case = orchestrator.process({**SAMPLE_EVENT, "event_id": case_id})
    return case
