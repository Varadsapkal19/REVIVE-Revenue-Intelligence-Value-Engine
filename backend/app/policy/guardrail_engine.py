from pydantic import BaseModel
from typing import List, Optional

class CheckResult(BaseModel):
    name: str
    passed: bool
    reason: str

class GuardrailResult(BaseModel):
    approved: bool
    status: str  # AUTHORIZED | BLOCKED | HUMAN_REVIEW
    checks: List[CheckResult]

class GuardrailEngine:
    """100% Deterministic Guardrail Policy Gate — No LLM bypass permitted."""
    
    def validate(
        self,
        proposed_action: str,
        discount_pct: float,
        policy_max_discount: float,
        max_outreach_per_day: int,
        outreach_today: int,
        allowed_channels: List[str],
        max_autonomous_amount: float,
        human_approval_threshold: float,
        amount: float,
        fatigue_score: float,
        customer_consent: bool = True
    ) -> GuardrailResult:
        checks = []
        approved = True
        status = "AUTHORIZED"

        # Check 1: Consent
        if not customer_consent:
            checks.append(CheckResult(name="CONSENT", passed=False, reason="Customer consent not given"))
            approved = False

        # Check 2: Fatigue (Stop outreach at 90+)
        if fatigue_score >= 90:
            checks.append(CheckResult(name="FATIGUE", passed=False, reason=f"Fatigue score {fatigue_score:.1f}/100 exceeds threshold 90"))
            approved = False
        else:
            checks.append(CheckResult(name="FATIGUE", passed=True, reason=f"Fatigue score {fatigue_score:.1f}/100 within safe limits"))

        # Check 3: Frequency
        if outreach_today >= max_outreach_per_day:
            checks.append(CheckResult(name="FREQUENCY", passed=False, reason=f"Daily outreach limit {max_outreach_per_day} reached ({outreach_today} today)"))
            approved = False
        else:
            checks.append(CheckResult(name="FREQUENCY", passed=True, reason=f"Outreach count {outreach_today}/{max_outreach_per_day} allowed"))

        # Check 4: Amount
        if amount > human_approval_threshold:
            checks.append(CheckResult(name="AMOUNT", passed=False, reason=f"Amount ₹{amount:,.0f} exceeds human approval threshold ₹{human_approval_threshold:,.0f}"))
            status = "HUMAN_REVIEW"
            approved = False
        elif amount > max_autonomous_amount:
            checks.append(CheckResult(name="AMOUNT", passed=False, reason=f"Amount ₹{amount:,.0f} exceeds autonomous limit ₹{max_autonomous_amount:,.0f}"))
            status = "HUMAN_REVIEW"
            approved = False
        else:
            checks.append(CheckResult(name="AMOUNT", passed=True, reason=f"Amount ₹{amount:,.0f} within autonomous limit ₹{max_autonomous_amount:,.0f}"))

        # Check 5: Discount limit
        if discount_pct > policy_max_discount:
            checks.append(CheckResult(name="DISCOUNT", passed=False, reason=f"Requested discount {discount_pct}% exceeds merchant max {policy_max_discount}%"))
            approved = False
        else:
            checks.append(CheckResult(name="DISCOUNT", passed=True, reason=f"Discount {discount_pct}% within policy max {policy_max_discount}%"))

        # Check 6: Channel permission
        channel_name = proposed_action.lower()
        if channel_name != "no_action" and channel_name not in [c.lower() for c in allowed_channels]:
            checks.append(CheckResult(name="CHANNEL", passed=False, reason=f"Channel {proposed_action} not in merchant allowed list"))
            approved = False
        else:
            checks.append(CheckResult(name="CHANNEL", passed=True, reason=f"Channel {proposed_action} permitted"))

        if not approved and status != "HUMAN_REVIEW":
            status = "BLOCKED"

        return GuardrailResult(approved=approved, status=status, checks=checks)
