from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class SimulatorRequest(BaseModel):
    num_cases: int
    scenario_filter: Optional[str] = None
    failure_distribution: Optional[Dict[str, float]] = None

class SimulatorResponse(BaseModel):
    total_events: int
    revenue_at_risk: float
    potentially_recoverable: float
    revive_recovery: float
    incremental_recovery: float
    recovery_rate: float
    interventions_count: int
    blocked_count: int
    human_escalations: int
    by_action: Dict[str, int]
    by_root_cause: Dict[str, int]
    funnel_data: List[Dict[str, Any]]
