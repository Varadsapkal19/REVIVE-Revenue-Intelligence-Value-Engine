"use client";
import React from 'react';
import { Search, Info, CheckCircle, XCircle, Shield, AlertTriangle } from 'lucide-react';
import { formatCurrency } from '@/lib/utils';

export default function JudgeMode() {
  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-neutral-900">Judge Mode</h1>
          <p className="text-neutral-500">Explainable AI decisions</p>
        </div>
        <div className="flex gap-4">
          <button className="px-4 py-2 bg-neutral-200 hover:bg-neutral-300 text-neutral-800 rounded-md text-sm font-medium transition-colors flex items-center gap-2">
            <XCircle className="w-4 h-4 text-danger" />
            DEMO: Show Blocked Action
          </button>
          <button className="px-4 py-2 bg-brand hover:bg-brand-600 text-white rounded-md text-sm font-medium transition-colors">
            View Random Critical Case
          </button>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-lg border border-neutral-200 overflow-hidden font-mono text-sm">
        {/* Header */}
        <div className="bg-neutral-900 text-neutral-100 p-6 flex justify-between items-center border-b-4 border-brand">
          <div>
            <div className="flex items-center gap-3">
              <h2 className="text-xl font-bold">CASE #RV-82931</h2>
              <span className="px-3 py-1 bg-success-dark text-success-light border border-success rounded-full text-xs font-bold tracking-wider">
                ● AUTHORIZED
              </span>
            </div>
            <p className="text-neutral-400 mt-1 font-sans">Revenue Recovery Intelligence Report</p>
          </div>
          <button className="bg-brand hover:bg-brand-600 text-white px-4 py-2 rounded flex items-center gap-2 font-sans font-medium transition-all transform hover:scale-105 shadow-md shadow-brand/20">
            <Info className="w-4 h-4" />
            WHY THIS ACTION?
          </button>
        </div>

        {/* Content */}
        <div className="p-8 space-y-8 bg-neutral-50 text-neutral-800">
          
          <div className="flex gap-12 pb-6 border-b border-neutral-200">
            <div>
              <p className="text-neutral-500 uppercase tracking-widest text-xs mb-1">Revenue at Risk</p>
              <p className="text-3xl font-bold text-danger">{formatCurrency(45000)}</p>
            </div>
            <div>
              <p className="text-neutral-500 uppercase tracking-widest text-xs mb-1">Customer</p>
              <p className="text-lg font-bold">Priya Sharma <span className="text-brand text-sm ml-2 bg-brand-50 px-2 py-0.5 rounded border border-brand-100">[PREMIUM]</span></p>
              <p className="text-neutral-600 text-xs mt-1">Fatigue: 23/100 <span className="text-success">[LOW]</span></p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-bold text-neutral-900 mb-4 flex items-center gap-2 border-b-2 border-neutral-200 pb-2">
              <Search className="w-5 h-5 text-brand" /> ROOT CAUSE ANALYSIS
            </h3>
            <div className="flex items-center gap-4 mb-4">
              <div className="font-bold text-xl text-neutral-800 bg-neutral-200 px-4 py-2 rounded">
                ISSUER DEGRADATION
              </div>
              <div className="flex-1 bg-neutral-200 h-2 rounded-full overflow-hidden">
                <div className="bg-success h-full w-[91%]"></div>
              </div>
              <span className="font-bold">91% Confidence</span>
            </div>
            <div className="bg-white p-4 rounded border border-neutral-200 shadow-inner">
              <p className="font-bold mb-2 text-neutral-700">Evidence:</p>
              <ul className="space-y-2 font-sans">
                {['31 failures from HDFC Bank within 12 minutes', 'Merchant baseline failure rate: 3%', 'Current cohort failure rate: 27%', 'No customer-side issues detected'].map((ev, i) => (
                  <li key={i} className="flex gap-2 items-start text-neutral-600">
                    <span className="text-brand mt-1">•</span> {ev}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-bold text-neutral-900 mb-4 flex items-center gap-2 border-b-2 border-neutral-200 pb-2">
              <TrendingUp className="w-5 h-5 text-brand" /> RECOVERY OPTIONS EVALUATED
            </h3>
            <div className="space-y-3 mb-6 bg-white p-4 border border-neutral-200 rounded">
              {[
                { name: 'Voice Call', val: 13400, pct: 100, selected: true },
                { name: 'Payment Link', val: 11200, pct: 83 },
                { name: 'Human Escl.', val: 10200, pct: 76 },
                { name: 'Retry', val: 8100, pct: 60 },
                { name: 'WhatsApp', val: 7800, pct: 58 },
                { name: 'Do Nothing', val: 4900, pct: 36 },
              ].map(opt => (
                <div key={opt.name} className="flex items-center gap-4">
                  <div className={`w-32 font-bold ${opt.selected ? 'text-brand' : 'text-neutral-600'}`}>{opt.name}</div>
                  <div className="flex-1 bg-neutral-100 h-4 rounded overflow-hidden flex">
                    <div className={`${opt.selected ? 'bg-brand' : 'bg-neutral-300'} h-full transition-all`} style={{ width: `${opt.pct}%` }}></div>
                  </div>
                  <div className={`w-24 text-right font-bold ${opt.selected ? 'text-brand' : ''}`}>{formatCurrency(opt.val)}</div>
                  <div className="w-24 text-xs font-bold text-brand">{opt.selected && '← SELECTED'}</div>
                </div>
              ))}
            </div>
            
            <div className="bg-brand-50 border-l-4 border-brand p-4 rounded-r font-sans text-neutral-800">
              <h4 className="font-bold mb-1">Why Voice Call?</h4>
              <p className="text-sm">Voice Call selected as it offers the highest expected incremental recovery (₹8,500 above natural baseline). Given issuer degradation as root cause (high issuer recovery probability), direct voice outreach maximizes P(recovery) = 0.73 × ₹45,000 = ₹32,850 gross.</p>
            </div>
          </div>

          <div>
            <h3 className="text-lg font-bold text-neutral-900 mb-4 flex items-center gap-2 border-b-2 border-neutral-200 pb-2">
              <Shield className="w-5 h-5 text-brand" /> GUARDRAIL VERIFICATION
            </h3>
            <div className="bg-white p-4 border border-neutral-200 rounded">
              <ul className="space-y-2">
                {[
                  { name: 'CONSENT', desc: 'Customer opted in to recovery outreach' },
                  { name: 'MERCHANT POLICY', desc: 'Voice permitted in merchant policy' },
                  { name: 'FREQUENCY', desc: '1 of 3 allowed contacts today' },
                  { name: 'AMOUNT', desc: '₹45,000 within autonomous limit (₹50,000)' },
                  { name: 'DISCOUNT', desc: 'No incentive applied' },
                ].map(check => (
                  <li key={check.name} className="flex gap-4">
                    <CheckCircle className="w-5 h-5 text-success shrink-0" />
                    <span className="w-36 font-bold">{check.name}</span>
                    <span className="text-neutral-600">{check.desc}</span>
                  </li>
                ))}
              </ul>
              <div className="mt-4 pt-4 border-t border-neutral-100 font-bold text-success text-lg flex items-center gap-2">
                Final Decision: AUTHORIZED <CheckCircle className="w-5 h-5" />
              </div>
            </div>
          </div>

          <div className="flex gap-6">
            <div className="flex-1">
              <h3 className="text-lg font-bold text-neutral-900 mb-4 flex items-center gap-2 border-b-2 border-neutral-200 pb-2">
                COUNTERFACTUAL
              </h3>
              <div className="bg-white p-4 border border-neutral-200 rounded space-y-2">
                <div className="flex justify-between text-neutral-600">
                  <span>Without REVIVE:</span>
                  <span className="font-bold">{formatCurrency(4900)}</span>
                </div>
                <div className="flex justify-between font-bold">
                  <span>With REVIVE:</span>
                  <span>{formatCurrency(13400)}</span>
                </div>
                <div className="pt-2 border-t border-neutral-100 flex justify-between font-bold text-success text-lg">
                  <span>Incremental:</span>
                  <span>{formatCurrency(8500)}</span>
                </div>
              </div>
            </div>
            
            <div className="flex-1">
              <h3 className="text-lg font-bold text-neutral-900 mb-4 flex items-center gap-2 border-b-2 border-neutral-200 pb-2">
                AUDIT REFERENCE
              </h3>
              <div className="bg-neutral-900 text-neutral-300 p-4 rounded text-xs space-y-2 h-full">
                <p><span className="text-neutral-500">Decision ID:</span> RV-20260901-F7K2P8A1</p>
                <p><span className="text-neutral-500">Timestamp:</span> 2026-09-01 20:15:23 IST</p>
                <p><span className="text-neutral-500">Agents:</span> Sentinel → Diagnostician → Strategist → Executor</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  )
}
// placeholder for TrendingUp
function TrendingUp(props: any) {
  return <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline></svg>
}
