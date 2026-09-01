from fastapi import APIRouter

router = APIRouter(prefix="/api/experiments", tags=["Experiments"])

@router.get("")
def list_experiments():
    return {
        "experiments": [
            {
                "id": "EXP-101",
                "name": "Intervention Channel Benchmark",
                "status": "Completed",
                "sample_size": 1000,
                "winner": "Payment Link",
                "results": [
                    {"group": "A", "action": "Delayed Retry", "recovery_rate": "45.2%", "incremental": 210000, "cost_per_recovery": 180},
                    {"group": "B", "action": "Payment Link", "recovery_rate": "61.8%", "incremental": 340000, "cost_per_recovery": 290},
                    {"group": "C", "action": "WhatsApp", "recovery_rate": "52.3%", "incremental": 280000, "cost_per_recovery": 145},
                    {"group": "D", "action": "Human Escalation", "recovery_rate": "78.1%", "incremental": 420000, "cost_per_recovery": 890},
                ]
            }
        ]
    }
