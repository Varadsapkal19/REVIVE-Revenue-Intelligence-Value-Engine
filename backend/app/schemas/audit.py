from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class AuditLogBase(BaseModel):
    case_id: UUID
    decision_id: str
    agent: str
    action: str
    reason: str
    evidence: Dict[str, Any]
    policy_checks: Dict[str, Any]
    execution_result: str
    outcome: Optional[str] = None

class AuditLogResponse(AuditLogBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True
