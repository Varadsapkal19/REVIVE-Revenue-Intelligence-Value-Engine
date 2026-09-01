"use client";
import React from 'react';
import Link from 'next/link';
import { Filter, Search } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';

export default function RevenueRisk() {
  const cases = [
    { id: 'RV-82931', cust: 'Acme Corp', seg: 'Premium', amt: 45000, score: 85, cause: 'Issuer Degradation', action: 'Voice Call', status: 'Pending', p: 'critical' },
    { id: 'RV-82932', cust: 'Stark Ind', seg: 'Standard', amt: 120000, score: 92, cause: 'Insufficient Funds', action: 'Payment Link', status: 'Pending', p: 'critical' },
    { id: 'RV-82933', cust: 'Wayne Ent', seg: 'Premium', amt: 32000, score: 78, cause: 'Expired Card', action: 'WhatsApp', status: 'Processing', p: 'high' },
    { id: 'RV-82934', cust: 'Cyberdyne', seg: 'Standard', amt: 85000, score: 65, cause: 'Fraud Block', action: 'Human Escalation', status: 'Escalated', p: 'medium' },
    { id: 'RV-82935', cust: 'Umbrella Corp', seg: 'Standard', amt: 12000, score: 42, cause: 'Network Error', action: 'Retry', status: 'Pending', p: 'low' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900">Risk Radar</h1>
          <p className="text-neutral-500">2 Critical Cases — ₹1.65L at risk</p>
        </div>
        
        <div className="flex gap-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
            <input type="text" placeholder="Search..." className="pl-9 pr-4 py-2 border border-neutral-300 rounded-md text-sm w-64" />
          </div>
          <button className="flex items-center gap-2 px-4 py-2 border border-neutral-300 rounded-md text-sm font-medium hover:bg-neutral-50 bg-white">
            <Filter className="w-4 h-4" /> Filter
          </button>
        </div>
      </div>

      <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-neutral-500 bg-neutral-50 uppercase border-b border-neutral-200">
            <tr>
              <th className="px-6 py-4">Case ID</th>
              <th className="px-6 py-4">Customer</th>
              <th className="px-6 py-4">Revenue at Risk</th>
              <th className="px-6 py-4 w-48">Risk Score</th>
              <th className="px-6 py-4">Root Cause</th>
              <th className="px-6 py-4">Action</th>
              <th className="px-6 py-4"></th>
            </tr>
          </thead>
          <tbody>
            {cases.map((row, i) => (
              <tr key={i} className="border-b border-neutral-100 hover:bg-neutral-50">
                <td className="px-6 py-4 font-mono font-medium text-brand"><Link href={`/cases/${row.id}`}>{row.id}</Link></td>
                <td className="px-6 py-4">
                  <div className="font-medium">{row.cust}</div>
                  <div className="text-xs text-neutral-500">{row.seg}</div>
                </td>
                <td className="px-6 py-4 font-bold text-danger">{formatCurrency(row.amt)}</td>
                <td className="px-6 py-4">
                  <div className="flex items-center gap-2">
                    <div className="flex-1 bg-neutral-200 h-2 rounded-full overflow-hidden">
                      <div className={`h-full ${row.score > 80 ? 'bg-danger' : row.score > 60 ? 'bg-brand' : 'bg-success'}`} style={{width: `${row.score}%`}}></div>
                    </div>
                    <span className="text-xs font-bold w-6">{row.score}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-neutral-700">{row.cause}</td>
                <td className="px-6 py-4">
                  <span className="px-2 py-1 bg-neutral-100 rounded text-xs border border-neutral-200">{row.action}</span>
                </td>
                <td className="px-6 py-4 text-right">
                  <Link href={`/cases/${row.id}`} className="text-brand hover:text-brand-700 font-medium text-sm">View Case</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        <div className="p-4 border-t border-neutral-200 text-sm text-neutral-500 flex justify-between items-center bg-neutral-50">
          <span>Showing 1 to 5 of 5 entries</span>
          <div className="flex gap-1">
            <button className="px-3 py-1 border border-neutral-300 rounded bg-white text-neutral-400" disabled>Previous</button>
            <button className="px-3 py-1 border border-neutral-300 rounded bg-brand text-white">1</button>
            <button className="px-3 py-1 border border-neutral-300 rounded bg-white text-neutral-400" disabled>Next</button>
          </div>
        </div>
      </div>
    </div>
  )
}
