"use client";
import React from 'react';
import { ArrowLeft, Download, ShieldAlert, Zap, User, Clock, FileText, CheckCircle2, AlertTriangle, ListChecks } from 'lucide-react';
import Link from 'next/link';
import { formatCurrency } from '@/lib/utils';

export default function CaseDetail({ params }: { params: { id: string } }) {
  const id = params.id || 'RV-82931';
  
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/cases" className="text-neutral-500 hover:text-neutral-900 transition-colors">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <h1 className="text-2xl font-bold text-neutral-900 font-mono">{id}</h1>
          <span className="px-3 py-1 bg-success-light text-success-dark border border-success rounded-full text-xs font-bold uppercase tracking-wide">
            Authorized
          </span>
        </div>
        <div className="flex gap-3">
          <div className="text-sm text-neutral-500 flex items-center gap-1">
            <Clock className="w-4 h-4" /> Created 2 hours ago
          </div>
          <button className="px-3 py-1.5 border border-neutral-300 rounded text-sm hover:bg-neutral-50 font-medium flex items-center gap-2">
            <Download className="w-4 h-4" /> Export
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Left Column 60% */}
        <div className="lg:col-span-3 space-y-6">
          
          {/* Risk Card */}
          <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm flex items-center justify-between">
            <div>
              <p className="text-sm text-neutral-500 font-medium mb-1 uppercase tracking-wider">Revenue at Risk</p>
              <h2 className="text-4xl font-bold text-danger">{formatCurrency(45000)}</h2>
              <div className="flex gap-2 mt-3">
                <span className="px-2 py-1 bg-neutral-100 text-neutral-600 rounded text-xs">Premium Segment</span>
                <span className="px-2 py-1 bg-neutral-100 text-neutral-600 rounded text-xs">Credit Card</span>
              </div>
            </div>
            <div className="relative w-24 h-24 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#FEE2E2" strokeWidth="3" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#DC2626" strokeWidth="3" strokeDasharray="85, 100" />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-xl font-bold text-danger">85</span>
                <span className="text-[10px] text-neutral-500">Risk</span>
              </div>
            </div>
          </div>

          {/* Root Cause Card */}
          <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
            <div className="bg-neutral-50 px-6 py-4 border-b border-neutral-200 flex items-center gap-2">
              <ShieldAlert className="w-5 h-5 text-brand" />
              <h3 className="font-semibold text-neutral-900">Root Cause Diagnosis</h3>
            </div>
            <div className="p-6">
              <div className="flex items-center gap-4 mb-6">
                <span className="px-3 py-1 bg-brand text-white rounded font-bold">Issuer Degradation</span>
                <div className="flex-1 bg-neutral-100 h-2 rounded-full">
                  <div className="bg-brand h-full w-[91%] rounded-full"></div>
                </div>
                <span className="text-sm font-bold text-neutral-600">91% Confidence</span>
              </div>
              <ul className="space-y-3">
                {[
                  '31 failures from HDFC Bank within 12 minutes',
                  'Merchant baseline failure rate: 3%',
                  'Current cohort failure rate: 27%',
                  'No customer-side issues detected'
                ].map((ev, i) => (
                  <li key={i} className="flex gap-3 text-sm text-neutral-700">
                    <CheckCircle2 className="w-5 h-5 text-brand shrink-0" />
                    {ev}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Action Evaluation */}
          <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden border-l-4 border-l-brand">
            <div className="bg-neutral-50 px-6 py-4 border-b border-neutral-200 flex items-center gap-2">
              <Zap className="w-5 h-5 text-brand" />
              <h3 className="font-semibold text-neutral-900">Action Evaluation</h3>
            </div>
            <div className="p-6">
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-neutral-500 border-b border-neutral-200">
                    <th className="pb-3 font-medium">Action</th>
                    <th className="pb-3 font-medium text-center">Probability</th>
                    <th className="pb-3 font-medium text-right">Expected Value</th>
                  </tr>
                </thead>
                <tbody>
                  {[
                    { action: 'Voice Call', p: '73%', v: 13400, selected: true },
                    { action: 'Payment Link', p: '82%', v: 11200 },
                    { action: 'Human Escl.', p: '85%', v: 10200 },
                    { action: 'WhatsApp', p: '57%', v: 7800 },
                    { action: 'Retry', p: '61%', v: 8100 },
                    { action: 'Do Nothing', p: '15%', v: 4900 },
                  ].map((row, i) => (
                    <tr key={i} className={`border-b border-neutral-100 last:border-0 ${row.selected ? 'bg-brand-50 text-brand-700 font-medium' : 'text-neutral-700'}`}>
                      <td className="py-3 flex items-center gap-2">
                        {row.selected && <span className="w-2 h-2 rounded-full bg-brand"></span>}
                        {row.action} {row.selected && <span className="ml-2 text-[10px] bg-brand text-white px-2 py-0.5 rounded font-bold">SELECTED</span>}
                      </td>
                      <td className="py-3 text-center">{row.p}</td>
                      <td className="py-3 text-right">{formatCurrency(row.v)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          
          {/* Counterfactual */}
          <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
            <h3 className="font-semibold text-neutral-900 mb-4">Counterfactual Recovery</h3>
            <div className="space-y-3 font-mono text-sm">
              <div className="flex justify-between p-3 bg-neutral-50 rounded">
                <span className="text-neutral-600">Without REVIVE (Natural)</span>
                <span className="font-bold">{formatCurrency(4900)}</span>
              </div>
              <div className="flex justify-between p-3 bg-neutral-50 rounded">
                <span className="text-neutral-600">With REVIVE Action</span>
                <span className="font-bold">{formatCurrency(13400)}</span>
              </div>
              <div className="flex justify-between p-4 bg-success-light border border-success rounded text-success-dark font-bold text-lg">
                <span>Incremental Recovery</span>
                <span>{formatCurrency(8500)}</span>
              </div>
            </div>
          </div>

        </div>

        {/* Right Column 40% */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Guardrails */}
          <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
            <div className="bg-neutral-50 px-6 py-4 border-b border-neutral-200 flex items-center gap-2">
              <ListChecks className="w-5 h-5 text-neutral-500" />
              <h3 className="font-semibold text-neutral-900">Guardrail Checks</h3>
            </div>
            <div className="p-6">
              <ul className="space-y-4">
                {[
                  { n: 'CONSENT', d: 'Customer consent verified' },
                  { n: 'FREQUENCY', d: '1/3 outreach today' },
                  { n: 'AMOUNT', d: '₹45K < ₹50K auto limit' },
                  { n: 'DISCOUNT', d: 'No discount applied' },
                  { n: 'CHANNEL', d: 'Voice channel permitted' },
                ].map(g => (
                  <li key={g.n} className="flex gap-3 text-sm">
                    <CheckCircle2 className="w-5 h-5 text-success shrink-0" />
                    <div>
                      <p className="font-bold text-neutral-800">{g.n}</p>
                      <p className="text-neutral-500">{g.d}</p>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Fatigue */}
          <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm flex flex-col items-center">
            <h3 className="font-semibold text-neutral-900 w-full mb-4">Customer Fatigue</h3>
            <div className="relative w-32 h-32 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#E5E7EB" strokeWidth="4" />
                <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#16A34A" strokeWidth="4" strokeDasharray="23, 100" />
              </svg>
              <div className="absolute flex flex-col items-center">
                <span className="text-2xl font-bold text-success">23</span>
                <span className="text-xs font-bold text-success">LOW</span>
              </div>
            </div>
            <p className="text-xs text-neutral-500 mt-4 text-center">Score is low. Outreach permitted.</p>
          </div>

          {/* Status Timeline */}
          <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm">
            <h3 className="font-semibold text-neutral-900 mb-4">Execution Status</h3>
            <div className="space-y-4 relative before:absolute before:inset-0 before:ml-2 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-neutral-200">
              {['Created', 'Diagnosed', 'Action Selected', 'Guardrail Passed', 'Executed'].map((step, i) => (
                <div key={step} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                  <div className="flex items-center justify-center w-5 h-5 rounded-full border-2 border-white bg-brand text-neutral-500 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow"></div>
                  <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.25rem)] text-sm font-medium p-2 text-neutral-700">
                    {step}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
