export interface DashboardMetrics {
  revenue_at_risk: number
  potentially_recoverable: number
  recovered: number
  incremental_recovery: number
  recovery_rate: number
  total_interventions: number
  successful_interventions: number
  blocked_interventions: number
  human_escalations: number
  incremental_per_intervention: number
}

export interface ActionRanking {
  action: string
  expected_value: number
  probability: number
  is_selected: boolean
}

export interface GuardrailCheck {
  name: string
  passed: boolean
  reason: string
}

export interface RecoveryCase {
  id: string
  customer_id: string
  amount: number
  risk_score: number
  priority: 'critical' | 'high' | 'medium' | 'low'
  root_cause: string
  root_cause_confidence: number
  root_cause_evidence: string[]
  recoverable_amount: number
  selected_action: string
  expected_recovery: number
  natural_recovery_estimate: number
  expected_incremental_recovery: number
  actual_recovery?: number
  actual_incremental_recovery?: number
  fatigue_score: number
  status: string
  guardrail_checks: GuardrailCheck[]
  action_ranking: ActionRanking[]
  created_at: string
}

export interface FunnelStep {
  label: string
  count: number
  w: number
}

export interface SimulatorResult {
  total_events: number
  revenue_at_risk: number
  potentially_recoverable: number
  revive_recovery: number
  incremental_recovery: number
  recovery_rate: number
  interventions_count: number
  blocked_count: number
  human_escalations: number
  by_action: Record<string, number>
  by_root_cause: Record<string, number>
  funnel: FunnelStep[]
}

export interface MerchantPolicy {
  max_discount_pct: number
  max_outreach_per_day: number
  allowed_channels: string[]
  max_autonomous_amount: number
  human_approval_threshold: number
  recovery_window_hours: number
  max_retry_attempts: number
}

export interface AuditLog {
  id: string
  case_id: string
  decision_id: string
  agent: string
  action: string
  reason: string
  evidence: Record<string, unknown>
  policy_checks: GuardrailCheck[]
  execution_result: string
  outcome?: string
  created_at: string
}
