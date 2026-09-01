from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from app.simulation.batch_processor import BatchProcessor

router = APIRouter(prefix="/api/simulator", tags=["Simulator"])

class SimulatorRequest(BaseModel):
    num_cases: int = 1000
    scenario: Optional[str] = "All Scenarios"

@router.post("/run")
def run_simulation(req: SimulatorRequest):
    return BatchProcessor.run_simulation(num_cases=req.num_cases, scenario=req.scenario)
