# REVIVE — Architecture Documentation

## System Overview

REVIVE is a closed-loop autonomous revenue recovery intelligence system. Every revenue-risk event passes through a 7-stage pipeline:

```
Detect → Diagnose → Predict → Choose → Govern → Execute → Verify → Learn
```

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    REVIVE System                                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Next.js Frontend (Port 3000)                            │   │
│  │  Revenue War Room · Risk Radar · Simulator · Judge Mode  │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                              │ REST API (HTTP/JSON)              │
│  ┌──────────────────────────▼───────────────────────────────┐   │
│  │  FastAPI Backend (Port 8000)                              │   │
│  │                                                           │   │
│  │  ┌───────────┐  ┌───────────────┐  ┌──────────────────┐ │   │
│  │  │ Sentinel   │  │ Diagnostician │  │   Strategist      │ │   │
│  │  │ (Risk)     │  │ (Root Cause)  │  │ (Expected Value)  │ │   │
│  │  └─────┬──────┘  └──────┬────────┘  └────────┬─────────┘ │   │
│  │        │                │                     │            │   │
│  │  ┌─────▼────────────────▼─────────────────────▼─────────┐ │   │
│  │  │              REVIVE Orchestrator                       │ │   │
│  │  └──────────────────────┬──────────────────────────────┘ │   │
│  │                          │                                 │   │
│  │  ┌───────────────────────▼──────────────────────────────┐ │   │
│  │  │  Guardrail Engine (DETERMINISTIC — zero LLM)         │ │   │
│  │  │  Consent · Policy · Amount · Discount · Frequency    │ │   │
│  │  └───────────────────────┬──────────────────────────────┘ │   │
│  │                          │                                 │   │
│  │  ┌───────────────────────▼──────────────────────────────┐ │   │
│  │  │  Executor (only runs if guardrail APPROVED)          │ │   │
│  │  └───────────────────────┬──────────────────────────────┘ │   │
│  │                          │                                 │   │
│  │  ┌───────────────────────▼──────────────────────────────┐ │   │
│  │  │  Auditor (immutable decision log)                    │ │   │
│  │  └──────────────────────────────────────────────────────┘ │   │
│  └──────────┬────────────────────────────────────────────────┘   │
│             │                                                     │
│  ┌──────────▼──────────────────────────────────────────────┐     │
│  │  PostgreSQL (Port 5432) │ Redis (Port 6379)              │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────┐     │
│  │  Ollama / Qwen2.5 (Port 11434) — LLM for explanations   │     │
│  │  ⚠ LLM NEVER makes recovery decisions                    │     │
│  └──────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

---

## AI vs Deterministic Split

### Deterministic (zero LLM involvement)

| Component | Function |
|-----------|----------|
| GuardrailEngine | All policy validation and authorization |
| RecoveryService | Expected value calculations |
| FatigueService | Customer fatigue scoring |
| RiskService | Risk score calculation |
| OutcomeService | Incremental recovery measurement |
| AuditService | Immutable decision logging |
| PolicyService | Policy rule enforcement |

### AI/ML Components

| Component | Function |
|-----------|----------|
| RootCauseClassifier | XGBoost multi-class root cause prediction |
| RecoveryPredictor | XGBoost calibrated P(recovery\|action, context) |
| DiagnosticianAgent | LLM-enhanced explanation generation (Ollama) |
| StrategistAgent | LLM contextual reasoning (Ollama) — explanation only |

> ⚠ **LLM output never directly authorizes or executes financial actions.**

---

## Recovery Decision Formula

```
Expected Recovery Value(action) =
    P(recovery | action, customer_context)
    × Recoverable Amount
    − Intervention Cost
    − Incentive Cost
    − Customer Fatigue Penalty
    − Risk Penalty

Best Action = argmax(Expected Recovery Value)

Subject to:
    merchant_policy.allowed_channels
    merchant_policy.max_discount_pct
    merchant_policy.max_autonomous_amount
    merchant_policy.max_outreach_per_day
    customer.consent == True
    fatigue_score < 90
```

---

## Database Schema

### Key Tables

```sql
revenue_events
  id UUID PK
  event_type   -- payment_failed | checkout_abandoned | subscription_failed | ...
  customer_id  -- FK to customers
  payment_id   -- FK to payments (nullable)
  amount       -- Revenue at risk
  status       -- pending | processing | resolved | escalated
  raw_payload  -- JSONB (full event data for audit)
  created_at

recovery_cases
  id UUID PK
  event_id            -- FK to revenue_events
  customer_id         -- FK to customers
  amount              -- Revenue at risk
  risk_score          -- 0.0–1.0
  root_cause          -- Classified failure type
  root_cause_confidence -- 0.0–1.0
  root_cause_evidence -- JSONB array of evidence strings
  recoverable_amount
  selected_action     -- The chosen intervention
  expected_recovery   -- Predicted EV of selected action
  natural_recovery_estimate -- What would happen without REVIVE
  expected_incremental_recovery -- expected_recovery - natural_recovery_estimate
  actual_recovery     -- Populated after outcome
  actual_incremental_recovery  -- actual_recovery - natural_recovery_estimate
  fatigue_score       -- Customer fatigue 0–100
  status              -- pending | processing | executed | recovered | failed | escalated | no_action
  guardrail_checks    -- JSONB array of check results
  action_ranking      -- JSONB array of all evaluated actions with EVs
  created_at
  updated_at

audit_logs
  id UUID PK
  case_id        -- FK to recovery_cases
  decision_id    -- Unique RV-YYYYMMDD-XXXXXXXX (immutable)
  agent          -- Which agent made the decision
  action         -- What action was decided/taken
  reason         -- Text explanation
  evidence       -- JSONB
  policy_checks  -- JSONB array of guardrail results
  execution_result -- AUTHORIZED | BLOCKED | HUMAN_REVIEW | EXECUTION_FAILED
  outcome        -- Populated after observation
  created_at     -- Never updated after insert
```

---

## Guardrail Engine Flow

```
AI Decision Proposed
        │
        ▼
   Consent Check ──── FAIL ──► BLOCKED
        │
        ▼
  Fatigue Check ────── FAIL ──► BLOCKED (score ≥ 90: STOP OUTREACH)
        │
        ▼
 Frequency Check ───── FAIL ──► BLOCKED
        │
        ▼
  Amount Check ──────── > human_threshold ──► HUMAN_REVIEW
        │
        ▼
 Discount Check ─────── FAIL ──► BLOCKED
        │
        ▼
  Channel Check ──────── FAIL ──► BLOCKED
        │
        ▼
     AUTHORIZED ──────────────► Executor runs
```

---

## Security Model

1. **No secrets in source code** — All credentials from `.env`
2. **Frontend only sees public config** — `NEXT_PUBLIC_*` vars only
3. **Razorpay secrets backend-only** — Never passed to frontend
4. **Webhook signature verification** — Before processing any webhook
5. **Idempotent processing** — Duplicate events detected and skipped
6. **LLM output sandboxed** — Never passed to guardrail or executor
7. **Audit logs immutable** — No UPDATE on audit_logs after INSERT

---

## Failure Recovery

```
External Action Fails
        │
        ▼
  Log EXECUTION_FAILED in audit
        │
        ▼
  Is retry permitted by policy?
        │
    YES │                   NO │
        ▼                       ▼
  Schedule Retry         Create HUMAN_REVIEW case
        │
   Retry Fails?
        │
        ▼
  HUMAN_REVIEW
```
