from fastapi import APIRouter

router = APIRouter(prefix="/api/risk", tags=["Risk"])

@router.get("")
def list_risk_scores():
    return {
        "risks": [
            {"case_id": "RV-82931", "customer": "Acme Corp", "amount": 45000, "risk_score": 0.92, "priority": "critical", "root_cause": "Issuer Degradation"},
            {"case_id": "RV-82932", "customer": "Stark Ind", "amount": 120000, "risk_score": 0.85, "priority": "critical", "root_cause": "Insufficient Funds"},
            {"case_id": "RV-82933", "customer": "Wayne Ent", "amount": 32000, "risk_score": 0.68, "priority": "high", "root_cause": "Expired Card"},
            {"case_id": "RV-82934", "customer": "Cyberdyne", "amount": 85000, "risk_score": 0.74, "priority": "high", "root_cause": "Invoice Overdue"},
        ]
    }
