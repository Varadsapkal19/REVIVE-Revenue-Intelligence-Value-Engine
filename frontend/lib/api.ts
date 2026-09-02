import axios from 'axios';
import { DashboardMetrics, RecoveryCase, SimulatorResult, MerchantPolicy, AuditLog } from './types';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getDashboardMetrics = async (): Promise<DashboardMetrics> => {
  try {
    const res = await api.get('/api/v1/dashboard/metrics');
    return res.data;
  } catch (err) {
    // Return mock if API fails
    return {
      revenue_at_risk: 4820000,
      potentially_recoverable: 3140000,
      recovered: 1870000,
      incremental_recovery: 1590000,
      recovery_rate: 59.6,
      total_interventions: 642,
      successful_interventions: 451,
      blocked_interventions: 87,
      human_escalations: 34,
      incremental_per_intervention: 2800
    };
  }
};

// other api functions would go here...
export default api;
