import random
import uuid
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any

SCENARIO_DISTRIBUTION = {
    "ISSUER_DEGRADATION": 0.15,
    "INSUFFICIENT_FUNDS": 0.20,
    "EXPIRED_CARD": 0.12,
    "NETWORK_FAILURE": 0.08,
    "MANDATE_FAILURE": 0.10,
    "CHECKOUT_ABANDONMENT": 0.18,
    "SUBSCRIPTION_RENEWAL_FAILURE": 0.08,
    "INVOICE_OVERDUE": 0.05,
    "REPEATED_FAILURE": 0.04,
}

PAYMENT_METHODS = ["card", "upi", "netbanking", "wallet", "emi"]
CUSTOMER_SEGMENTS = ["premium", "standard", "budget"]

class EventGenerator:
    """Generates synthetic revenue events for testing and simulation."""
    
    @staticmethod
    def generate_events(n: int = 1000, seed: int = 42) -> List[Dict[str, Any]]:
        random.seed(seed)
        np.random.seed(seed)
        
        events = []
        scenarios = list(SCENARIO_DISTRIBUTION.keys())
        weights = list(SCENARIO_DISTRIBUTION.values())
        
        start_time = datetime.now() - timedelta(days=7)
        
        for _ in range(n):
            scenario = np.random.choice(scenarios, p=weights)
            cust_id = f"CUST-{random.randint(1000, 9999)}"
            segment = np.random.choice(CUSTOMER_SEGMENTS, p=[0.25, 0.55, 0.20])
            pm = np.random.choice(PAYMENT_METHODS, p=[0.40, 0.35, 0.12, 0.08, 0.05])
            
            # Amount based on scenario
            if scenario in ["ISSUER_DEGRADATION", "INVOICE_OVERDUE"]:
                amount = float(round(np.random.uniform(15000, 150000), 2))
            elif scenario == "CHECKOUT_ABANDONMENT":
                amount = float(round(np.random.uniform(800, 12000), 2))
            else:
                amount = float(round(np.random.uniform(1500, 45000), 2))
                
            event_id = str(uuid.uuid4())
            events.append({
                "event_id": event_id,
                "event_type": scenario.lower(),
                "customer_id": cust_id,
                "customer_name": f"Customer {cust_id[-4:]}",
                "customer_segment": segment,
                "amount": amount,
                "currency": "INR",
                "payment_method": pm,
                "root_cause_type": scenario,
                "failure_reason": f"System error: {scenario.lower().replace('_', ' ')}",
                "created_at": (start_time + timedelta(minutes=random.randint(0, 10080))).isoformat()
            })
            
        return events
