"use client";
import React from 'react';
import { Search, Filter } from 'lucide-react';

export default function Audit() {
  const logs = [
    { did: 'RV-20260901-A1', cid: '82931', agent: 'Strategist', action: 'Voice Call', status: 'AUTHORIZED', time: '2m ago', color: 'success' },
    { did: 'RV-20260901-A2', cid: '82944', agent: 'PolicyEngine', action: '15% Discount', status: 'BLOCKED', time: '5m ago', color: 'danger' },
    { did: 'RV-20260901-A3', cid: '82951', agent: 'Orchestrator', action: 'No Action', status: 'AUTHORIZED', time: '12m ago', color: 'success' },
    { did: 'RV-20260901-A4', cid: '82955', agent: 'Diagnostician', action: 'Classification', status: 'COMPLETED', time: '18m ago', color: 'neutral' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900">Audit Center</h1>
          <p className="text-neutral-500">Immutable log of all AI decisions</p>
        </div>
        <div className="flex gap-3">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-neutral-400" />
            <input type="text" placeholder="Search logs..." className="pl-9 pr-4 py-2 border border-neutral-300 rounded-md text-sm w-64" />
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
              <th className="px-6 py-4">Decision ID</th>
              <th className="px-6 py-4">Case</th>
              <th className="px-6 py-4">Agent</th>
              <th className="px-6 py-4">Action</th>
              <th className="px-6 py-4">Status</th>
              <th className="px-6 py-4 text-right">Time</th>
            </tr>
          </thead>
          <tbody>
            {logs.map((row, i) => (
              <tr key={i} className="border-b border-neutral-100 hover:bg-neutral-50 cursor-pointer">
                <td className="px-6 py-4 font-mono font-medium">{row.did}</td>
                <td className="px-6 py-4 font-mono text-brand">{row.cid}</td>
                <td className="px-6 py-4">{row.agent}</td>
                <td className="px-6 py-4">{row.action}</td>
                <td className="px-6 py-4">
                  <span className={`px-2 py-1 bg-${row.color}-light text-${row.color}-dark border border-${row.color} rounded text-xs font-semibold`}>
                    {row.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-right text-neutral-500">{row.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
