from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/policies", tags=["Policies"])

class MerchantPolicySchema(BaseModel):
    max_discount_pct: float = 10.0
    max_outreach_per_day: int = 3
    allowed_channels: List[str] = ["Retry", "Payment Link", "WhatsApp", "Voice Call", "Human Escalation"]
    max_autonomous_amount: float = 50000.0
    human_approval_threshold: float = 100000.0
    recovery_window_hours: int = 72
    max_retry_attempts: int = 3

current_policy = MerchantPolicySchema()

@router.get("")
def get_policy():
    return current_policy

@router.put("")
def update_policy(policy: MerchantPolicySchema):
    global current_policy
    current_policy = policy
    return {"status": "success", "policy": current_policy}
