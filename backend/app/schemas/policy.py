from pydantic import BaseModel
from typing import List
from uuid import UUID
from datetime import datetime

class MerchantPolicyBase(BaseModel):
    merchant_id: UUID
    max_discount_pct: float = 10.0
    max_outreach_per_day: int = 3
    allowed_channels: List[str]
    max_autonomous_amount: float = 50000.0
    human_approval_threshold: float = 100000.0
    recovery_window_hours: int = 72
    max_retry_attempts: int = 3

class MerchantPolicyCreate(MerchantPolicyBase):
    pass

class MerchantPolicyResponse(MerchantPolicyBase):
    id: UUID
    updated_at: datetime
    class Config:
        orm_mode = True
