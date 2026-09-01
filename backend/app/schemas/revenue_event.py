from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class RevenueEventBase(BaseModel):
    event_type: str
    customer_id: UUID
    payment_id: Optional[UUID] = None
    subscription_id: Optional[UUID] = None
    amount: float
    currency: str
    status: str
    raw_payload: Dict[str, Any]

class RevenueEventCreate(RevenueEventBase):
    pass

class RevenueEventResponse(RevenueEventBase):
    id: UUID
    created_at: datetime
    class Config:
        orm_mode = True
