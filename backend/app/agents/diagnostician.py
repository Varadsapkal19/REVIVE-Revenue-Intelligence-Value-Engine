from app.models.recovery_case import RecoveryCase
from app.services.diagnosis_service import DiagnosisService

class DiagnosticianAgent:
    async def diagnose(self, case: RecoveryCase, context: dict) -> dict:
        service = DiagnosisService()
        root_cause, confidence, evidence = service.classify_root_cause(None, None, [])
        reasoning = await self._get_llm_reasoning(context)
        return {
            "root_cause": root_cause,
            "confidence": confidence,
            "evidence": evidence,
            "reasoning": reasoning
        }
        
    async def _get_llm_reasoning(self, context) -> str:
        return "Rule-based analysis applied."
