"use client";
import React from 'react';
import RevenueRisk from '../revenue-risk/page';

export default function Cases() {
  return (
    <div>
      <div className="mb-4">
        <h1 className="text-2xl font-bold text-neutral-900">All Recovery Cases</h1>
        <p className="text-neutral-500">View and manage all revenue recovery cases</p>
      </div>
      <RevenueRisk />
    </div>
  )
}
