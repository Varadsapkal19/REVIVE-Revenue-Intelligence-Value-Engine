"use client";
import React, { useState } from 'react';
import { Play, Settings, Database, Server, CreditCard, Activity, ArrowRight, TrendingUp } from 'lucide-react';
import { formatLakhs } from '@/lib/utils';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

export default function Simulator() {
  const [running, setRunning] = useState(false);
  const [complete, setComplete] = useState(false);
  const [progress, setProgress] = useState(0);
  const [cases, setCases] = useState(1000);

  const runSimulation = () => {
    setRunning(true);
    setComplete(false);
    setProgress(0);
    
    let p = 0;
    const interval = setInterval(() => {
      p += 5;
      setProgress(p);
      if (p >= 100) {
        clearInterval(interval);
        setRunning(false);
        setComplete(true);
      }
    }, 150);
  };

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-6">
      {/* Controls */}
      <div className="w-1/3 bg-white rounded-lg border border-neutral-200 shadow-sm flex flex-col">
        <div className="p-4 border-b border-neutral-200 bg-neutral-50 flex items-center gap-2">
          <Settings className="w-5 h-5 text-neutral-600" />
          <h2 className="font-semibold text-neutral-900">RECOVERY SIMULATOR</h2>
        </div>
        
        <div className="p-6 flex-1 overflow-y-auto space-y-6">
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">Scenario</label>
            <select className="w-full border border-neutral-300 rounded-md shadow-sm p-2 text-sm focus:ring-brand focus:border-brand">
              <option>All Scenarios</option>
              <option>High Payment Failures</option>
              <option>Subscription Renewals</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">Number of Cases: {cases.toLocaleString()}</label>
            <input 
              type="range" min="100" max="10000" step="100" value={cases} 
              onChange={(e) => setCases(parseInt(e.target.value))}
              className="w-full accent-brand" 
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">Failure Distribution</label>
            <div className="space-y-2">
              {['Issuer Degradation (15%)', 'Insufficient Funds (20%)', 'Expired Card (12%)', 'Fraud Block (8%)'].map(cause => (
                <label key={cause} className="flex items-center text-sm text-neutral-600">
                  <input type="checkbox" defaultChecked className="rounded text-brand focus:ring-brand mr-2" />
                  {cause}
                </label>
              ))}
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-neutral-700 mb-2">Customer Segments</label>
            <div className="flex gap-4">
              {['All', 'Premium', 'Standard'].map(seg => (
                <label key={seg} className="flex items-center text-sm text-neutral-600">
                  <input type="radio" name="segment" defaultChecked={seg === 'All'} className="text-brand focus:ring-brand mr-2" />
                  {seg}
                </label>
              ))}
            </div>
          </div>
        </div>

        <div className="p-6 border-t border-neutral-200">
          <button 
            onClick={runSimulation}
            disabled={running}
            className={`w-full py-3 rounded-lg flex justify-center items-center gap-2 font-bold text-white transition-colors ${running ? 'bg-neutral-400' : 'bg-brand hover:bg-brand-600'}`}
          >
            {running ? (
              <>Processing... {progress}%</>
            ) : (
              <><Play className="w-5 h-5 fill-current" /> RUN RECOVERY BATCH</>
            )}
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="flex-1 bg-white rounded-lg border border-neutral-200 shadow-sm flex flex-col relative overflow-hidden">
        {(!complete && !running) && (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-neutral-400">
            <Activity className="w-16 h-16 mb-4 opacity-50" />
            <p>Configure parameters and run the simulator to see results.</p>
          </div>
        )}
        
        {running && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-white/90 z-10">
            <div className="w-64 h-2 bg-neutral-200 rounded-full overflow-hidden mb-4">
              <div className="bg-brand h-full transition-all duration-200" style={{width: `${progress}%`}}></div>
            </div>
            <p className="text-neutral-600 font-mono text-sm animate-pulse">
              {progress < 30 ? 'Processing cases...' : progress < 60 ? 'Calculating risk scores...' : progress < 90 ? 'Running decisions...' : 'Finalizing results...'}
            </p>
          </div>
        )}

        {complete && (
          <div className="p-8 overflow-y-auto h-full space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
            <h2 className="text-2xl font-bold text-neutral-900">Simulation Results</h2>
            
            <div className="grid grid-cols-4 gap-4">
              {[
                { label: 'Revenue at Risk', value: formatLakhs(cases * 1840), color: 'text-danger', border: 'border-danger-light' },
                { label: 'REVIVE Recovery', value: formatLakhs(cases * 890), color: 'text-success', border: 'border-success-light' },
                { label: 'Incremental', value: formatLakhs(cases * 670), color: 'text-success', border: 'border-success-light' },
                { label: 'Recovery Rate', value: '59.6%', color: 'text-brand', border: 'border-brand-100' },
              ].map(kpi => (
                <div key={kpi.label} className={`p-4 rounded-lg border bg-white shadow-sm ${kpi.border}`}>
                  <p className="text-xs text-neutral-500 uppercase font-semibold">{kpi.label}</p>
                  <p className={`text-2xl font-bold mt-1 ${kpi.color}`}>{kpi.value}</p>
                </div>
              ))}
            </div>

            <div className="bg-neutral-50 p-6 rounded-lg border border-neutral-200">
              <h3 className="font-semibold mb-4 text-neutral-700">Recovery Funnel</h3>
              <div className="space-y-3 font-mono text-sm">
                {[
                  { label: 'Events', count: cases * 10, w: 100 },
                  { label: 'Revenue Events', count: cases * 8.2, w: 82 },
                  { label: 'At Risk', count: cases * 6.1, w: 61 },
                  { label: 'Recoverable', count: cases * 4.4, w: 44 },
                  { label: 'Interventions', count: cases * 3.2, w: 32 },
                  { label: 'Recovered', count: cases * 2.1, w: 21 },
                ].map(step => (
                  <div key={step.label} className="flex items-center gap-4">
                    <div className="w-32 text-right text-neutral-600">{step.label}</div>
                    <div className="flex-1 bg-neutral-200 h-6 rounded overflow-hidden">
                      <div className="bg-brand h-full" style={{width: `${step.w}%`}}></div>
                    </div>
                    <div className="w-24 font-bold">{step.count.toLocaleString()}</div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-6">
              <div className="border border-neutral-200 p-4 rounded-lg">
                <h3 className="font-semibold text-sm mb-4 text-neutral-600 text-center">Recovery by Action</h3>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={[{name:'Voice',v:45},{name:'Link',v:30},{name:'WhatsApp',v:15},{name:'Retry',v:10}]}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="name" tick={{fontSize: 12}} />
                      <Tooltip />
                      <Bar dataKey="v" fill="#F97316" radius={[4,4,0,0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
              <div className="border border-neutral-200 p-4 rounded-lg">
                <h3 className="font-semibold text-sm mb-4 text-neutral-600 text-center">Recovery by Root Cause</h3>
                <div className="h-48">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={[{name:'Degradation',v:40},{name:'Funds',v:25},{name:'Expired',v:20},{name:'Fraud',v:15}]}>
                      <CartesianGrid strokeDasharray="3 3" vertical={false} />
                      <XAxis dataKey="name" tick={{fontSize: 12}} />
                      <Tooltip />
                      <Bar dataKey="v" fill="#16A34A" radius={[4,4,0,0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
