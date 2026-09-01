from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from app.agents.orchestrator import Orchestrator

router = APIRouter(prefix="/api/events", tags=["Events"])
orchestrator = Orchestrator()

class RevenueEventIngest(BaseModel):
    event_type: str
    amount: float
    customer_id: str
    failure_reason: str = "Payment processing failed"

@router.post("")
def ingest_event(event: RevenueEventIngest):
    result = orchestrator.process(event.dict())
    return {"status": "processed", "case": result}
