"""
REVIVE Synthetic Dataset Generator
===================================
Generates 10,000 realistic synthetic payment failure events
for training, evaluation and simulation.

Usage:
    python generate_dataset.py --output datasets/revive_dataset.csv --seed 42
"""

import argparse
import json
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

# ── Reproducibility ────────────────────────────────────────────────────────────
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# ── Failure Scenario Configuration ────────────────────────────────────────────
SCENARIOS = {
    "ISSUER_DEGRADATION": {
        "proportion": 0.15,
        "recovery_base_retry": 0.72,
        "recovery_base_payment_link": 0.78,
        "recovery_base_whatsapp": 0.55,
        "recovery_base_voice": 0.80,
        "recovery_base_human": 0.85,
        "recovery_base_no_action": 0.12,
        "natural_recovery": 0.15,
        "amount_range": (5000, 200000),
    },
    "INSUFFICIENT_FUNDS": {
        "proportion": 0.20,
        "recovery_base_retry": 0.18,
        "recovery_base_payment_link": 0.45,
        "recovery_base_whatsapp": 0.52,
        "recovery_base_voice": 0.60,
        "recovery_base_human": 0.65,
        "recovery_base_no_action": 0.08,
        "natural_recovery": 0.08,
        "amount_range": (1000, 50000),
    },
    "EXPIRED_CARD": {
        "proportion": 0.12,
        "recovery_base_retry": 0.15,
        "recovery_base_payment_link": 0.72,
        "recovery_base_whatsapp": 0.65,
        "recovery_base_voice": 0.70,
        "recovery_base_human": 0.78,
        "recovery_base_no_action": 0.05,
        "natural_recovery": 0.10,
        "amount_range": (2000, 100000),
    },
    "NETWORK_FAILURE": {
        "proportion": 0.08,
        "recovery_base_retry": 0.82,
        "recovery_base_payment_link": 0.70,
        "recovery_base_whatsapp": 0.40,
        "recovery_base_voice": 0.50,
        "recovery_base_human": 0.55,
        "recovery_base_no_action": 0.25,
        "natural_recovery": 0.30,
        "amount_range": (500, 500000),
    },
    "MANDATE_FAILURE": {
        "proportion": 0.10,
        "recovery_base_retry": 0.45,
        "recovery_base_payment_link": 0.60,
        "recovery_base_whatsapp": 0.55,
        "recovery_base_voice": 0.65,
        "recovery_base_human": 0.72,
        "recovery_base_no_action": 0.08,
        "natural_recovery": 0.12,
        "amount_range": (3000, 50000),
    },
    "CHECKOUT_ABANDONMENT": {
        "proportion": 0.18,
        "recovery_base_retry": 0.10,
        "recovery_base_payment_link": 0.38,
        "recovery_base_whatsapp": 0.42,
        "recovery_base_voice": 0.35,
        "recovery_base_human": 0.30,
        "recovery_base_no_action": 0.05,
        "natural_recovery": 0.05,
        "amount_range": (500, 30000),
    },
    "SUBSCRIPTION_RENEWAL_FAILURE": {
        "proportion": 0.08,
        "recovery_base_retry": 0.52,
        "recovery_base_payment_link": 0.65,
        "recovery_base_whatsapp": 0.58,
        "recovery_base_voice": 0.68,
        "recovery_base_human": 0.75,
        "recovery_base_no_action": 0.10,
        "natural_recovery": 0.15,
        "amount_range": (1000, 20000),
    },
    "INVOICE_OVERDUE": {
        "proportion": 0.05,
        "recovery_base_retry": 0.20,
        "recovery_base_payment_link": 0.48,
        "recovery_base_whatsapp": 0.50,
        "recovery_base_voice": 0.55,
        "recovery_base_human": 0.60,
        "recovery_base_no_action": 0.08,
        "natural_recovery": 0.10,
        "amount_range": (10000, 500000),
    },
    "REPEATED_FAILURE": {
        "proportion": 0.04,
        "recovery_base_retry": 0.12,
        "recovery_base_payment_link": 0.30,
        "recovery_base_whatsapp": 0.28,
        "recovery_base_voice": 0.35,
        "recovery_base_human": 0.42,
        "recovery_base_no_action": 0.05,
        "natural_recovery": 0.05,
        "amount_range": (1000, 100000),
    },
}

CUSTOMER_SEGMENTS = ["premium", "standard", "budget"]
SEGMENT_WEIGHTS = [0.20, 0.55, 0.25]

PAYMENT_METHODS = ["card", "upi", "netbanking", "wallet", "emi"]
PM_WEIGHTS = [0.40, 0.35, 0.12, 0.08, 0.05]

CHANNELS = ["retry", "payment_link", "whatsapp", "voice", "human", "no_action"]


def generate_customer_id(n: int = 2000) -> list[str]:
    return [f"CUST-{str(uuid.uuid4())[:8].upper()}" for _ in range(n)]


def generate_amount(scenario: str) -> float:
    lo, hi = SCENARIOS[scenario]["amount_range"]
    # Log-normal distribution for realistic payment amounts
    mean_log = np.log((lo + hi) / 2)
    std_log = 0.8
    amount = np.random.lognormal(mean_log, std_log)
    return float(np.clip(amount, lo, hi))


def get_recovery_probabilities(scenario: str, amount: float, segment: str, fatigue: float) -> dict[str, float]:
    s = SCENARIOS[scenario]
    segment_mult = {"premium": 1.15, "standard": 1.0, "budget": 0.85}[segment]
    fatigue_mult = max(0.3, 1.0 - (fatigue / 100) * 0.5)
    amount_mult = max(0.7, 1.0 - (amount / 500000) * 0.2)

    probs = {}
    for channel in CHANNELS:
        base = s.get(f"recovery_base_{channel}", 0.0)
        noise = np.random.normal(0, 0.05)
        prob = base * segment_mult * fatigue_mult * amount_mult + noise
        probs[channel] = float(np.clip(prob, 0.01, 0.99))

    return probs


def select_best_action(probs: dict[str, float], amount: float) -> str:
    """Simple EV-based action selection (mirrors backend logic)."""
    INTERVENTION_COSTS = {
        "retry": 0,
        "payment_link": 50,
        "whatsapp": 30,
        "voice": 100,
        "human": 500,
        "no_action": 0,
    }
    best_action = "no_action"
    best_ev = -999999

    for action, prob in probs.items():
        ev = prob * amount - INTERVENTION_COSTS.get(action, 0)
        if ev > best_ev:
            best_ev = ev
            best_action = action

    return best_action


def simulate_outcome(selected_action: str, probs: dict[str, float]) -> bool:
    """Simulate whether recovery actually occurred."""
    prob = probs.get(selected_action, 0.1)
    return np.random.random() < prob


def generate_dataset(n: int = 10000, seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)

    # Generate customer pool
    customers = generate_customer_id(2000)
    customer_segments = {
        c: np.random.choice(CUSTOMER_SEGMENTS, p=SEGMENT_WEIGHTS)
        for c in customers
    }

    scenario_names = list(SCENARIOS.keys())
    scenario_proportions = [SCENARIOS[s]["proportion"] for s in scenario_names]

    records = []
    start_time = datetime.now() - timedelta(days=30)

    for i in range(n):
        # Sample scenario
        scenario = np.random.choice(scenario_names, p=scenario_proportions)
        customer_id = np.random.choice(customers)
        segment = customer_segments[customer_id]
        amount = generate_amount(scenario)
        fatigue = np.random.beta(2, 5) * 100  # Most customers have low fatigue
        payment_method = np.random.choice(PAYMENT_METHODS, p=PM_WEIGHTS)

        # Historical data
        prev_failures = np.random.poisson(1.5)
        prev_successes = np.random.poisson(8)
        historical_recovery_rate = np.random.beta(3, 2) if prev_failures > 0 else 0.5

        # Time features
        event_time = start_time + timedelta(
            seconds=random.randint(0, 30 * 24 * 3600)
        )
        time_since_failure_hours = np.random.exponential(4)

        # Recovery probabilities for each action
        probs = get_recovery_probabilities(scenario, amount, segment, fatigue)
        natural_recovery_prob = SCENARIOS[scenario]["natural_recovery"]

        # Select best action
        selected_action = select_best_action(probs, amount)

        # Simulate outcome
        recovered = simulate_outcome(selected_action, probs)
        actual_recovery = amount if recovered else 0.0
        natural_recovery = amount * natural_recovery_prob * np.random.uniform(0.8, 1.2)
        incremental_recovery = actual_recovery - natural_recovery

        # Risk score (mirrors backend formula)
        failure_risk = min(1.0, (prev_failures + 1) / 5)
        revenue_exposure = min(1.0, amount / 500000)
        historical_failure_risk = prev_failures / max(prev_failures + prev_successes, 1)
        time_urgency = max(0, 1 - time_since_failure_hours / 72)
        cohort_anomaly = 0.3 if scenario == "ISSUER_DEGRADATION" else 0.05
        customer_behavior = min(1.0, fatigue / 100)

        risk_score = (
            0.35 * failure_risk
            + 0.20 * revenue_exposure
            + 0.15 * historical_failure_risk
            + 0.10 * time_urgency
            + 0.10 * cohort_anomaly
            + 0.10 * customer_behavior
        )

        records.append({
            "id": str(uuid.uuid4()),
            "customer_id": customer_id,
            "customer_segment": segment,
            "amount": round(amount, 2),
            "payment_method": payment_method,
            "root_cause": scenario,
            "failure_reason": scenario.lower().replace("_", " "),
            "previous_failures": prev_failures,
            "previous_successes": prev_successes,
            "historical_recovery_rate": round(historical_recovery_rate, 4),
            "time_since_failure_hours": round(time_since_failure_hours, 2),
            "fatigue_score": round(fatigue, 2),
            "subscription_status": "active" if scenario == "SUBSCRIPTION_RENEWAL_FAILURE" else "none",
            "invoice_age_days": round(np.random.exponential(15)) if scenario == "INVOICE_OVERDUE" else 0,
            "risk_score": round(risk_score, 4),
            "prob_retry": round(probs["retry"], 4),
            "prob_payment_link": round(probs["payment_link"], 4),
            "prob_whatsapp": round(probs["whatsapp"], 4),
            "prob_voice": round(probs["voice"], 4),
            "prob_human": round(probs["human"], 4),
            "prob_no_action": round(probs["no_action"], 4),
            "selected_action": selected_action,
            "recovered": int(recovered),
            "actual_recovery": round(actual_recovery, 2),
            "natural_recovery": round(natural_recovery, 2),
            "incremental_recovery": round(incremental_recovery, 2),
            "event_timestamp": event_time.isoformat(),
        })

    df = pd.DataFrame(records)
    return df


def split_dataset(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Split into 70/15/15 train/val/test."""
    n = len(df)
    shuffled = df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)
    train_end = int(n * 0.70)
    val_end = int(n * 0.85)

    train = shuffled.iloc[:train_end]
    val = shuffled.iloc[train_end:val_end]
    test = shuffled.iloc[val_end:]

    return train, val, test


def main():
    parser = argparse.ArgumentParser(description="Generate REVIVE synthetic dataset")
    parser.add_argument("--n", type=int, default=10000, help="Number of events")
    parser.add_argument("--output-dir", type=str, default="datasets", help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating {args.n} synthetic events (seed={args.seed})...")
    df = generate_dataset(n=args.n, seed=args.seed)

    # Save full dataset
    df.to_csv(output_dir / "revive_full.csv", index=False)
    print(f"✓ Full dataset: {len(df)} records → {output_dir}/revive_full.csv")

    # Split
    train, val, test = split_dataset(df)
    train.to_csv(output_dir / "train.csv", index=False)
    val.to_csv(output_dir / "val.csv", index=False)
    test.to_csv(output_dir / "test.csv", index=False)

    print(f"✓ Train: {len(train)} | Val: {len(val)} | Test: {len(test)}")

    # Print summary statistics
    print("\n── Dataset Summary ──────────────────────────────────────────")
    print(f"Total events:          {len(df):,}")
    print(f"Unique customers:      {df['customer_id'].nunique():,}")
    print(f"Total revenue at risk: ₹{df['amount'].sum():,.0f}")
    print(f"Total recovered:       ₹{df['actual_recovery'].sum():,.0f}")
    print(f"Overall recovery rate: {df['recovered'].mean()*100:.1f}%")
    print(f"Avg incremental:       ₹{df['incremental_recovery'].mean():,.0f}")
    print("\nBy root cause:")
    for cause, group in df.groupby("root_cause"):
        rate = group["recovered"].mean() * 100
        total = group["amount"].sum()
        print(f"  {cause:<35} {len(group):>5} cases  ₹{total:>12,.0f}  {rate:.1f}% recovery")

    # Save metadata
    meta = {
        "generated_at": datetime.now().isoformat(),
        "seed": args.seed,
        "total_events": len(df),
        "unique_customers": int(df["customer_id"].nunique()),
        "total_revenue_at_risk": float(df["amount"].sum()),
        "total_recovered": float(df["actual_recovery"].sum()),
        "overall_recovery_rate": float(df["recovered"].mean()),
        "splits": {"train": len(train), "val": len(val), "test": len(test)},
    }
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"\n✓ Metadata saved → {output_dir}/metadata.json")
    print("\nDataset generation complete!")


if __name__ == "__main__":
    main()
