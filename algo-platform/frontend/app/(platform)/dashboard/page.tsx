 "use client";

import { useEffect, useState } from "react";
import { SummaryCard } from "@/components/summary-card";
import { StrategyTable } from "@/components/strategy-table";
import { getRecentAlerts, getSummary, getTopStrategies } from "@/lib/api";
import { mockAlerts, mockStrategies, mockSummary } from "@/lib/mock";
import { Alert, DashboardSummary, Strategy } from "@/lib/types";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary>(mockSummary);
  const [strategies, setStrategies] = useState<Strategy[]>(mockStrategies);
  const [alerts, setAlerts] = useState<Alert[]>(mockAlerts);

  useEffect(() => {
    getSummary().then(setSummary).catch(() => setSummary(mockSummary));
    getTopStrategies().then(setStrategies).catch(() => setStrategies(mockStrategies));
    getRecentAlerts().then(setAlerts).catch(() => setAlerts(mockAlerts));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <SummaryCard title="Total Paper P&L" value={`${summary.totalPaperPnl.toFixed(2)}`} />
        <SummaryCard title="Signals Today" value={`${summary.signalsToday}`} />
        <SummaryCard title="Live Positions" value={`${summary.livePositions}`} />
        <SummaryCard title="Best Strategy" value={summary.bestStrategy} />
      </section>

      <section>
        <h2 className="mb-3 text-lg font-semibold">Top Performing Strategies</h2>
        <StrategyTable strategies={strategies} />
      </section>

      <section className="card">
        <h2 className="mb-4 text-lg font-semibold">Recent Alerts</h2>
        <div className="space-y-3">
          {alerts.map((alert) => (
            <div key={alert.id} className="rounded-xl border border-border bg-slate-900 p-3">
              <p className="text-sm font-medium capitalize text-cyan-300">{alert.level}</p>
              <p className="text-sm text-slate-200">{alert.message}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
