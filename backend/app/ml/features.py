import numpy as np

def extract_features(event, customer, payment) -> np.ndarray:
    amount_log = np.log1p(event.amount if event else 0)
    return np.array([amount_log, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

ROOT_CAUSE_FEATURES = ["amount_log", "failure_reason_encoded", "payment_method_encoded"]
RECOVERY_FEATURES = ["amount_log", "fatigue_score", "historical_recovery_rate"]
