"""
REVIVE Model Trainer
=====================
Trains Recovery Prediction and Root Cause Classification models.

Usage:
    python train_models.py --data-dir ../datasets --model-dir ../models
"""

import argparse
import json
import os
import pickle
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    brier_score_loss,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier


# ── Feature Engineering ───────────────────────────────────────────────────────

ROOT_CAUSE_ENCODER = LabelEncoder()
SEGMENT_ENCODER = LabelEncoder()
PM_ENCODER = LabelEncoder()
ACTION_ENCODER = LabelEncoder()

SEGMENTS = ["budget", "premium", "standard"]
PAYMENT_METHODS = ["card", "emi", "netbanking", "upi", "wallet"]
ROOT_CAUSES = [
    "CHECKOUT_ABANDONMENT", "EXPIRED_CARD", "INSUFFICIENT_FUNDS",
    "INVOICE_OVERDUE", "ISSUER_DEGRADATION", "MANDATE_FAILURE",
    "NETWORK_FAILURE", "REPEATED_FAILURE", "SUBSCRIPTION_RENEWAL_FAILURE",
]
ACTIONS = ["human", "no_action", "payment_link", "retry", "voice", "whatsapp"]


def encode_categorical(df: pd.DataFrame) -> pd.DataFrame:
    """One-hot encode categorical features."""
    df = df.copy()

    # Normalize strings
    df["customer_segment"] = df["customer_segment"].str.lower().fillna("standard")
    df["payment_method"] = df["payment_method"].str.lower().fillna("card")
    df["subscription_status"] = df["subscription_status"].str.lower().fillna("none")

    # Encode segments
    for seg in SEGMENTS:
        df[f"seg_{seg}"] = (df["customer_segment"] == seg).astype(int)

    # Encode payment methods
    for pm in PAYMENT_METHODS:
        df[f"pm_{pm}"] = (df["payment_method"] == pm).astype(int)

    # Subscription
    df["is_subscription"] = (df["subscription_status"] == "active").astype(int)

    # Log transform amount
    df["amount_log"] = np.log1p(df["amount"])
    df["amount_norm"] = df["amount"] / 500000

    return df


ROOT_CAUSE_FEATURES = [
    "amount_log", "amount_norm",
    "previous_failures", "previous_successes",
    "historical_recovery_rate", "time_since_failure_hours",
    "fatigue_score", "invoice_age_days", "risk_score",
    "is_subscription",
] + [f"seg_{s}" for s in SEGMENTS] + [f"pm_{p}" for p in PAYMENT_METHODS]

RECOVERY_FEATURES = [
    "amount_log", "amount_norm",
    "previous_failures", "previous_successes",
    "historical_recovery_rate", "time_since_failure_hours",
    "fatigue_score", "invoice_age_days", "risk_score",
    "is_subscription",
] + [f"seg_{s}" for s in SEGMENTS] + [f"pm_{p}" for p in PAYMENT_METHODS]


def prepare_root_cause_data(df: pd.DataFrame):
    df_enc = encode_categorical(df)
    X = df_enc[ROOT_CAUSE_FEATURES].fillna(0).values
    y = df["root_cause"].values
    return X, y


def prepare_recovery_data(df: pd.DataFrame, action: str):
    """Prepare data for recovery prediction for a specific action."""
    action_key = f"prob_{action}"
    if action_key not in df.columns:
        return None, None

    df_enc = encode_categorical(df)
    X = df_enc[RECOVERY_FEATURES].fillna(0).values

    # Binary outcome: did recovery happen with this action?
    # Use simulated probabilities thresholded for training labels
    y = (df[action_key] > 0.5).astype(int).values
    return X, y


# ── Root Cause Classifier ─────────────────────────────────────────────────────

def train_root_cause_model(train_df: pd.DataFrame, val_df: pd.DataFrame):
    print("\n── Training Root Cause Classifier ─────────────────────────────")

    X_train, y_train = prepare_root_cause_data(train_df)
    X_val, y_val = prepare_root_cause_data(val_df)

    label_enc = LabelEncoder()
    label_enc.fit(ROOT_CAUSES)
    y_train_enc = label_enc.transform(y_train)
    y_val_enc = label_enc.transform(y_val)

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X_train, y_train_enc,
        eval_set=[(X_val, y_val_enc)],
        verbose=50,
    )

    y_pred = model.predict(X_val)
    acc = accuracy_score(y_val_enc, y_pred)
    f1 = f1_score(y_val_enc, y_pred, average="weighted")
    prec = precision_score(y_val_enc, y_pred, average="weighted", zero_division=0)
    rec = recall_score(y_val_enc, y_pred, average="weighted", zero_division=0)

    print(f"  Accuracy:  {acc:.4f}")
    print(f"  F1 (weighted): {f1:.4f}")
    print(f"  Precision: {prec:.4f}")
    print(f"  Recall:    {rec:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_val_enc, y_pred, target_names=label_enc.classes_))

    metrics = {
        "accuracy": float(acc),
        "f1_weighted": float(f1),
        "precision_weighted": float(prec),
        "recall_weighted": float(rec),
    }

    return model, label_enc, metrics


# ── Recovery Predictor ────────────────────────────────────────────────────────

def train_recovery_models(train_df: pd.DataFrame, val_df: pd.DataFrame):
    print("\n── Training Recovery Prediction Models ─────────────────────────")

    actions = ["retry", "payment_link", "whatsapp", "voice", "human", "no_action"]
    models = {}
    all_metrics = {}

    for action in actions:
        X_train, y_train = prepare_recovery_data(train_df, action)
        X_val, y_val = prepare_recovery_data(val_df, action)

        if X_train is None or len(np.unique(y_train)) < 2:
            print(f"  Skipping {action} — insufficient data")
            continue

        base_model = XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.8,
            use_label_encoder=False,
            eval_metric="logloss",
            random_state=42,
            n_jobs=-1,
        )

        # Calibrated for probability output
        model = CalibratedClassifierCV(base_model, method="isotonic", cv=3)
        model.fit(X_train, y_train)

        y_prob = model.predict_proba(X_val)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)

        try:
            auc = roc_auc_score(y_val, y_prob)
        except ValueError:
            auc = 0.5

        brier = brier_score_loss(y_val, y_prob)
        acc = accuracy_score(y_val, y_pred)

        print(f"  {action:<15} ROC-AUC: {auc:.4f}  Brier: {brier:.4f}  Acc: {acc:.4f}")

        models[action] = model
        all_metrics[action] = {
            "roc_auc": float(auc),
            "brier_score": float(brier),
            "accuracy": float(acc),
        }

    return models, all_metrics


# ── Save / Load ───────────────────────────────────────────────────────────────

def save_models(
    root_cause_model, root_cause_encoder,
    recovery_models,
    model_dir: Path,
    metrics: dict,
):
    model_dir.mkdir(parents=True, exist_ok=True)

    with open(model_dir / "root_cause_model.pkl", "wb") as f:
        pickle.dump(root_cause_model, f)

    with open(model_dir / "root_cause_encoder.pkl", "wb") as f:
        pickle.dump(root_cause_encoder, f)

    with open(model_dir / "recovery_models.pkl", "wb") as f:
        pickle.dump(recovery_models, f)

    meta = {
        "trained_at": datetime.now().isoformat(),
        "features": {
            "root_cause": ROOT_CAUSE_FEATURES,
            "recovery": RECOVERY_FEATURES,
        },
        "classes": ROOT_CAUSES,
        "actions": list(recovery_models.keys()),
        "metrics": metrics,
    }
    with open(model_dir / "model_metadata.json", "w") as f:
        json.dump(meta, f, indent=2)

    print(f"\n✓ Models saved to {model_dir}/")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Train REVIVE ML models")
    parser.add_argument("--data-dir", type=str, default="../datasets")
    parser.add_argument("--model-dir", type=str, default="../models")
    args = parser.parse_args()

    data_dir = Path(args.data_dir)
    model_dir = Path(args.model_dir)

    # Load datasets
    train_path = data_dir / "train.csv"
    val_path = data_dir / "val.csv"

    if not train_path.exists():
        print("Dataset not found. Generating...")
        import subprocess
        subprocess.run(
            ["python", "generate_dataset.py", "--output-dir", str(data_dir)],
            cwd=data_dir.parent,
            check=True,
        )

    print("Loading datasets...")
    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    print(f"  Train: {len(train_df):,} | Val: {len(val_df):,}")

    # Train models
    rc_model, rc_encoder, rc_metrics = train_root_cause_model(train_df, val_df)
    rec_models, rec_metrics = train_recovery_models(train_df, val_df)

    all_metrics = {
        "root_cause": rc_metrics,
        "recovery": rec_metrics,
    }

    # Save
    save_models(rc_model, rc_encoder, rec_models, model_dir, all_metrics)

    print("\n── Training Complete ────────────────────────────────────────────")
    print(f"Root Cause Accuracy: {rc_metrics['accuracy']:.4f}")
    print("Recovery Models:")
    for action, m in rec_metrics.items():
        print(f"  {action:<15} ROC-AUC: {m['roc_auc']:.4f}")


if __name__ == "__main__":
    main()
