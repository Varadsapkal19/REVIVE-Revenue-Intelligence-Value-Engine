from typing import Dict, Any
from app.agents.sentinel import SentinelAgent
from app.agents.diagnostician import DiagnosticianAgent
from app.agents.strategist import StrategistAgent
from app.agents.executor import ExecutorAgent
from app.agents.auditor import AuditorAgent
from app.services.policy_service import PolicyService
from app.services.fatigue_service import FatigueService

class Orchestrator:
    """REVIVE Orchestrator: Connects Sentinel → Diagnostician → Strategist → Policy Engine → Executor → Auditor."""
    
    def __init__(self):
        self.sentinel = SentinelAgent()
        self.diagnostician = DiagnosticianAgent()
        self.strategist = StrategistAgent()
        self.executor = ExecutorAgent()
        self.auditor = AuditorAgent()
        self.policy_service = PolicyService()

    def process(self, event: Dict[str, Any], merchant_policy: Dict[str, Any] = None) -> Dict[str, Any]:
        if merchant_policy is None:
            merchant_policy = {
                "max_discount_pct": 10.0,
                "max_outreach_per_day": 3,
                "allowed_channels": ["Retry", "Payment Link", "WhatsApp", "Voice Call", "Human Escalation"],
                "max_autonomous_amount": 50000.0,
                "human_approval_threshold": 100000.0,
            }
            
        # Step 1: Sentinel Risk Assessment
        sentinel_res = self.sentinel.process_event(event)
        
        # Step 2: Diagnostician Root Cause Analysis
        diag_res = self.diagnostician.diagnose(event)
        
        # Step 3: Fatigue calculation
        fatigue_score = FatigueService.calculate_fatigue(
            outreach_last_24h=event.get("outreach_last_24h", 1),
            outreach_last_7d=event.get("outreach_last_7d", 2),
            ignored_count=event.get("ignored_count", 0),
            last_contact_hours_ago=event.get("last_contact_hours_ago", 24.0)
        )
        
        # Step 4: Strategist Action Ranking & EV calculation
        strat_res = self.strategist.evaluate(
            amount=sentinel_res["revenue_at_risk"],
            root_cause=diag_res["root_cause"],
            fatigue_score=fatigue_score
        )
        
        # Step 5: Deterministic Policy Check
        guardrail_res = self.policy_service.check_policy(
            proposed_action=strat_res["selected_action"],
            discount_pct=event.get("requested_discount_pct", 0.0),
            merchant_policy=merchant_policy,
            outreach_today=event.get("outreach_today", 1),
            amount=sentinel_res["revenue_at_risk"],
            fatigue_score=fatigue_score,
            customer_consent=event.get("customer_consent", True)
        )
        
        # Step 6: Executor
        exec_res = self.executor.execute(strat_res["selected_action"], guardrail_res)
        
        # Step 7: Auditor Logging
        audit_res = self.auditor.log(
            case_id=sentinel_res["case_id"],
            agent_name="Strategist",
            action=strat_res["selected_action"],
            reason=f"Highest expected incremental recovery (EV: INR {strat_res['expected_recovery']:,.2f})",
            evidence=diag_res["evidence"],
            policy_checks=[c.dict() for c in guardrail_res.checks],
            execution_result=exec_res["status"]
        )
        
        return {
            "case_id": sentinel_res["case_id"],
            "decision_id": audit_res["decision_id"],
            "risk_score": sentinel_res["risk_score"],
            "priority": sentinel_res["priority"],
            "revenue_at_risk": sentinel_res["revenue_at_risk"],
            "root_cause": diag_res["root_cause"],
            "root_cause_confidence": diag_res["confidence"],
            "root_cause_evidence": diag_res["evidence"],
            "fatigue_score": fatigue_score,
            "selected_action": strat_res["selected_action"],
            "expected_recovery": strat_res["expected_recovery"],
            "natural_recovery_estimate": strat_res["natural_recovery_estimate"],
            "expected_incremental_recovery": strat_res["expected_incremental_recovery"],
            "action_ranking": strat_res["candidate_actions"],
            "guardrail_status": guardrail_res.status,
            "guardrail_approved": guardrail_res.approved,
            "guardrail_checks": [c.dict() for c in guardrail_res.checks],
            "execution": exec_res,
            "audit_log": audit_res
        }

REVIVEOrchestrator = Orchestrator
