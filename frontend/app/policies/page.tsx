"use client";
import React from 'react';
import { Save, AlertTriangle, CheckCircle } from 'lucide-react';

export default function Policies() {
  return (
    <div className="flex gap-6 h-[calc(100vh-8rem)]">
      <div className="flex-1 overflow-y-auto pr-2 space-y-6">
        <div className="flex justify-between items-center">
          <h1 className="text-2xl font-bold text-neutral-900">Policy Center</h1>
          <button className="flex items-center gap-2 px-4 py-2 bg-brand text-white rounded font-medium text-sm">
            <Save className="w-4 h-4" /> Save Changes
          </button>
        </div>

        <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm space-y-6">
          <h2 className="text-lg font-bold border-b pb-2">Financial Controls</h2>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-1">Maximum Discount Percentage</label>
              <div className="flex items-center gap-2">
                <input type="number" defaultValue="10" className="border border-neutral-300 rounded p-2 w-24" />
                <span className="text-neutral-500">%</span>
              </div>
              <p className="text-xs text-danger mt-1 flex items-center gap-1"><AlertTriangle className="w-3 h-3"/> Actions requesting &gt;10% will be BLOCKED</p>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Max Autonomous Action Amount</label>
              <div className="flex items-center gap-2">
                <span className="text-neutral-500">₹</span>
                <input type="number" defaultValue="50000" className="border border-neutral-300 rounded p-2 w-32" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Human Approval Threshold</label>
              <div className="flex items-center gap-2">
                <span className="text-neutral-500">₹</span>
                <input type="number" defaultValue="100000" className="border border-neutral-300 rounded p-2 w-32" />
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm space-y-6">
          <h2 className="text-lg font-bold border-b pb-2">Outreach Controls</h2>
          <div className="grid grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-1">Max Outreach per Day (per customer)</label>
              <input type="number" defaultValue="3" className="border border-neutral-300 rounded p-2 w-24" /> contacts
            </div>
            <div>
              <label className="block text-sm font-medium mb-1">Recovery Time Window</label>
              <input type="number" defaultValue="72" className="border border-neutral-300 rounded p-2 w-24" /> hours
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg border border-neutral-200 shadow-sm space-y-4">
          <h2 className="text-lg font-bold border-b pb-2">Allowed Channels</h2>
          <div className="grid grid-cols-3 gap-4">
            {['Retry', 'Payment Link', 'WhatsApp', 'SMS', 'Email', 'Voice', 'Human Escalation'].map(ch => (
              <label key={ch} className="flex items-center gap-2">
                <input type="checkbox" defaultChecked className="rounded text-brand focus:ring-brand" /> {ch}
              </label>
            ))}
          </div>
        </div>
      </div>

      <div className="w-80 bg-neutral-900 rounded-lg p-6 text-neutral-300 font-mono text-sm space-y-4 h-fit sticky top-0 shadow-lg border border-neutral-800">
        <h3 className="font-bold text-white border-b border-neutral-700 pb-2 mb-4">Guardrail Preview</h3>
        <ul className="space-y-3">
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-success mt-0.5 shrink-0" />
            <span>Discounts up to 10% authorized</span>
          </li>
          <li className="flex items-start gap-2 text-danger">
            <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
            <span>Discounts &gt; 10% BLOCKED</span>
          </li>
          <li className="flex items-start gap-2">
            <CheckCircle className="w-4 h-4 text-success mt-0.5 shrink-0" />
            <span>Autonomous actions up to ₹50,000</span>
          </li>
          <li className="flex items-start gap-2 text-warning">
            <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
            <span>₹50,001 - ₹1,00,000 requires human approval</span>
          </li>
          <li className="flex items-start gap-2 text-danger">
            <AlertTriangle className="w-4 h-4 mt-0.5 shrink-0" />
            <span>Actions &gt; ₹1,00,000 blocked</span>
          </li>
        </ul>
      </div>
    </div>
  )
}
