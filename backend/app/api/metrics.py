from fastapi import APIRouter
from app.simulation.batch_processor import BatchProcessor

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])

@router.get("/dashboard")
def get_dashboard_metrics():
    # Return realistic initial dashboard metrics
    return {
        "revenue_at_risk": 4820000.0,
        "potentially_recoverable": 3140000.0,
        "recovered": 1870000.0,
        "incremental_recovery": 1590000.0,
        "recovery_rate": 59.6,
        "total_interventions": 642,
        "successful_interventions": 451,
        "blocked_interventions": 87,
        "human_escalations": 34,
        "incremental_per_intervention": 2476.0
    }
