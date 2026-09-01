"use client";
import React from 'react';
import { ResponsiveContainer, BarChart, Bar, XAxis, Tooltip, CartesianGrid } from 'recharts';

export default function Experiments() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-neutral-900">Recovery Experiments</h1>
        <button className="px-4 py-2 bg-brand text-white rounded font-medium text-sm">New Experiment</button>
      </div>

      <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
        <div className="p-6 border-b border-neutral-200">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-bold text-neutral-900">Exp-24: High-Value Retries vs Payment Links</h2>
              <p className="text-sm text-neutral-500">Testing delayed retries against immediate payment links for amounts &gt; ₹10,000</p>
            </div>
            <span className="px-3 py-1 bg-success-light text-success-dark border border-success rounded-full text-xs font-bold">
              COMPLETED
            </span>
          </div>

          <div className="grid grid-cols-2 gap-8 mt-6">
            <div>
              <table className="w-full text-sm">
                <thead>
                  <tr className="text-left text-neutral-500 border-b border-neutral-200">
                    <th className="pb-2">Group</th>
                    <th className="pb-2">Action</th>
                    <th className="pb-2 text-right">Recovery Rate</th>
                    <th className="pb-2 text-right">Incremental</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-neutral-100">
                    <td className="py-3 font-bold">A</td>
                    <td className="py-3">Delayed Retry</td>
                    <td className="py-3 text-right">45.2%</td>
                    <td className="py-3 text-right font-medium">₹2.1L</td>
                  </tr>
                  <tr className="border-b border-neutral-100 bg-brand-50">
                    <td className="py-3 font-bold text-brand">B (Winner)</td>
                    <td className="py-3">Payment Link</td>
                    <td className="py-3 text-right font-bold">61.8%</td>
                    <td className="py-3 text-right font-bold text-success">₹3.4L</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div className="h-40">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={[{name:'A (Retry)',v:45.2},{name:'B (Link)',v:61.8}]}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="name" />
                  <Tooltip />
                  <Bar dataKey="v" fill="#F97316" radius={[4,4,0,0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
