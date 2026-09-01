from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from uuid import UUID
from datetime import datetime

class RecoveryCaseBase(BaseModel):
    customer_id: UUID
    payment_id: Optional[UUID] = None
    event_id: UUID
    amount: float
    risk_score: float
    root_cause: str
    root_cause_confidence: float
    root_cause_evidence: Dict[str, Any]
    recoverable_amount: float
    selected_action: str
    expected_recovery: float
    natural_recovery_estimate: float
    expected_incremental_recovery: float
    fatigue_score: float
    status: str
    guardrail_checks: List[Dict[str, Any]]
    action_ranking: List[Dict[str, Any]]

class RecoveryCaseCreate(RecoveryCaseBase):
    pass

class RecoveryCaseResponse(RecoveryCaseBase):
    id: UUID
    actual_recovery: Optional[float] = None
    actual_incremental_recovery: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        orm_mode = True
