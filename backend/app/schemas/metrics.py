from pydantic import BaseModel
from typing import List, Dict, Any

class DashboardMetrics(BaseModel):
    total_recovered: float
    incremental_recovery: float
    recovery_rate: float
    active_cases: int
    cases_resolved: int
    top_root_causes: List[Dict[str, Any]]
    recovery_by_channel: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
