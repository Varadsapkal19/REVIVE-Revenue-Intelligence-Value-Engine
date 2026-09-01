"use client";
import React from 'react';
import { ArrowUpRight, TrendingUp, AlertCircle, CheckCircle2, IndianRupee } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, PieChart, Pie, Cell } from 'recharts';
import { formatLakhs, formatCurrency } from '@/lib/utils';
import Link from 'next/link';

const trendData = [
  { day: 'Mon', recovery: 2.1 },
  { day: 'Tue', recovery: 2.4 },
  { day: 'Wed', recovery: 2.8 },
  { day: 'Thu', recovery: 2.3 },
  { day: 'Fri', recovery: 3.1 },
  { day: 'Sat', recovery: 2.9 },
  { day: 'Sun', recovery: 3.4 },
];

const actionData = [
  { name: 'Voice Call', value: 400 },
  { name: 'Payment Link', value: 300 },
  { name: 'WhatsApp', value: 300 },
  { name: 'Retry', value: 200 },
];
const COLORS = ['#F97316', '#16A34A', '#D97706', '#374151'];

export default function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-neutral-900">Revenue War Room</h1>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { label: 'At Risk', value: 4820000, change: '↑12% today', color: 'text-danger', bg: 'bg-danger-light' },
          { label: 'Recoverable', value: 3140000, change: '68% of risk', color: 'text-brand', bg: 'bg-brand-50' },
          { label: 'Recovered', value: 1870000, change: '59.6% rate', color: 'text-success', bg: 'bg-success-light' },
          { label: 'Incremental', value: 1590000, change: 'per case ₹2.8K', color: 'text-success', bg: 'bg-success-light' },
        ].map((kpi, i) => (
          <div key={i} className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
            <p className="text-sm text-neutral-500 font-medium">{kpi.label}</p>
            <div className={`text-3xl font-bold mt-2 ${kpi.color}`}>{formatLakhs(kpi.value)}</div>
            <div className={`mt-2 text-xs inline-block px-2 py-1 rounded ${kpi.bg} ${kpi.color}`}>
              {kpi.change}
            </div>
          </div>
        ))}
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="md:col-span-2 bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
          <h3 className="text-lg font-semibold mb-4 text-neutral-900">Recovery Performance</h3>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="day" axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#6B7280', fontSize: 12}} tickFormatter={(val) => `₹${val}L`} />
                <Tooltip cursor={{stroke: '#F97316', strokeWidth: 1, strokeDasharray: '4 4'}} />
                <Line type="monotone" dataKey="recovery" stroke="#F97316" strokeWidth={3} dot={{r: 4, fill: '#F97316'}} activeDot={{r: 6}} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
          <h3 className="text-lg font-semibold mb-4 text-neutral-900">Action Distribution</h3>
          <div className="h-64 flex items-center justify-center">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={actionData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                  {actionData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <div className="flex flex-wrap gap-2 mt-2 justify-center">
            {actionData.map((a, i) => (
              <div key={i} className="flex items-center text-xs">
                <span className="w-2 h-2 rounded-full mr-1" style={{backgroundColor: COLORS[i]}}></span>
                {a.name}
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Critical Risks Table */}
      <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-neutral-200 bg-neutral-50">
          <h3 className="text-lg font-semibold text-neutral-900">Critical Revenue Risks</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-neutral-500 bg-neutral-50 uppercase border-b border-neutral-200">
              <tr>
                <th className="px-6 py-3">Case ID</th>
                <th className="px-6 py-3">Customer</th>
                <th className="px-6 py-3">Risk Amount</th>
                <th className="px-6 py-3">Root Cause</th>
                <th className="px-6 py-3">Action</th>
                <th className="px-6 py-3">Status</th>
              </tr>
            </thead>
            <tbody>
              {[
                { id: 'RV-82931', cust: 'Acme Corp', amt: 45000, cause: 'Issuer Degradation', action: 'Voice Call', status: 'Authorized', color: 'success' },
                { id: 'RV-82932', cust: 'Stark Ind', amt: 120000, cause: 'Insufficient Funds', action: 'Payment Link', status: 'Pending', color: 'warning' },
                { id: 'RV-82933', cust: 'Wayne Ent', amt: 32000, cause: 'Expired Card', action: 'WhatsApp', status: 'Processing', color: 'warning' },
                { id: 'RV-82934', cust: 'Cyberdyne', amt: 85000, cause: 'Fraud Block', action: 'Human Escalation', status: 'Escalated', color: 'brand' },
              ].map((row, i) => (
                <tr key={i} className="border-b border-neutral-100 hover:bg-neutral-50">
                  <td className="px-6 py-4 font-mono font-medium text-brand"><Link href={`/cases/${row.id}`}>{row.id}</Link></td>
                  <td className="px-6 py-4 font-medium">{row.cust}</td>
                  <td className="px-6 py-4 text-danger font-medium">{formatCurrency(row.amt)}</td>
                  <td className="px-6 py-4 text-neutral-600">{row.cause}</td>
                  <td className="px-6 py-4">
                    <span className="px-2 py-1 bg-neutral-100 rounded text-xs border border-neutral-200">{row.action}</span>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 bg-${row.color}-light text-${row.color}-dark border border-${row.color} rounded text-xs font-semibold`}>
                      {row.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
