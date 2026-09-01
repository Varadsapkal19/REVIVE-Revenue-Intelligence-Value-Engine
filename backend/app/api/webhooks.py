from fastapi import APIRouter, Request, Header, HTTPException
from typing import Dict, Any
from app.agents.orchestrator import Orchestrator

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])
orchestrator = Orchestrator()

@router.post("/razorpay")
async def razorpay_webhook(request: Request, x_razorpay_signature: str = Header(None)):
    payload = await request.json()
    event_type = payload.get("event", "payment.failed")
    
    # Process webhook event
    payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
    amount = float(payment_entity.get("amount", 450000)) / 100.0  # Razorpay amounts in paise
    
    event_data = {
        "event_id": payment_entity.get("id", "pay_rzp_test_123"),
        "event_type": event_type,
        "amount": amount,
        "customer_id": payment_entity.get("email", "cust@example.com"),
        "failure_reason": payment_entity.get("error_description", "Payment failed via Razorpay"),
        "root_cause_type": "ISSUER_DEGRADATION" if "issuer" in payment_entity.get("error_description", "").lower() else "INSUFFICIENT_FUNDS"
    }
    
    result = orchestrator.process(event_data)
    return {"status": "success", "event_processed": event_type, "case_id": result["case_id"]}
