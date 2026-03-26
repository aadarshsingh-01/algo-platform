"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { ChartCard } from "@/components/chart-card";
import { EmptyState } from "@/components/empty-state";
import { StatusBadge } from "@/components/status-badge";
import { SummaryCard } from "@/components/summary-card";
import { getStrategyById, pauseStrategy, startStrategy } from "@/lib/api";
import { Strategy } from "@/lib/types";

export default function StrategyDetailPage() {
  const params = useParams<{ id: string }>();
  const [strategy, setStrategy] = useState<Strategy | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    const id = Number(params.id);
    getStrategyById(id).then(setStrategy).catch(() => setError("Unable to load strategy"));
  }, [params.id]);

  async function handleStart() {
    if (!strategy) return;
    try {
      const updated = await startStrategy(strategy.id);
      setStrategy(updated);
    } catch {
      setStrategy({ ...strategy, isActive: true });
    }
  }

  async function handlePause() {
    if (!strategy) return;
    try {
      const updated = await pauseStrategy(strategy.id);
      setStrategy(updated);
    } catch {
      setStrategy({ ...strategy, isActive: false });
    }
  }

  if (error) return <EmptyState title="Strategy Error" description={error} />;
  if (!strategy) return <EmptyState title="Loading Strategy" description="Fetching strategy details..." />;

  return (
    <div className="space-y-6">
      <div className="card flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold">{strategy.name}</h1>
          <p className="mt-1 text-sm text-slate-400">{strategy.description || "No description available"}</p>
        </div>
        <div className="flex items-center gap-3">
          <StatusBadge active={strategy.isActive} />
          <button onClick={handleStart} className="rounded-xl bg-emerald-500 px-4 py-2 text-sm font-medium text-slate-950">Start</button>
          <button onClick={handlePause} className="rounded-xl bg-amber-500 px-4 py-2 text-sm font-medium text-slate-950">Pause</button>
        </div>
      </div>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <SummaryCard title="Today P&L" value={strategy.todayPnl.toFixed(2)} />
        <SummaryCard title="Win Rate" value={`${strategy.winRate.toFixed(1)}%`} />
        <SummaryCard title="CAGR" value={`${strategy.cagr.toFixed(1)}%`} />
        <SummaryCard title="Max Drawdown" value={`${strategy.maxDrawdown.toFixed(1)}%`} />
      </section>

      <div className="card">
        <h3 className="mb-3 text-lg font-semibold">Signals Today</h3>
        <p className="text-sm text-slate-300">{strategy.lastSignal}</p>
      </div>

      <ChartCard />

      <div className="card">
        <h3 className="mb-3 text-lg font-semibold">Trade Log (Placeholder)</h3>
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border text-left text-slate-400">
              <th className="pb-2">Time</th><th className="pb-2">Symbol</th><th className="pb-2">Side</th><th className="pb-2">Qty</th><th className="pb-2">PnL</th>
            </tr>
          </thead>
          <tbody>
            <tr><td className="py-2">10:15</td><td>BANKNIFTY</td><td>BUY</td><td>25</td><td className="text-emerald-300">+420.50</td></tr>
            <tr><td className="py-2">11:05</td><td>BANKNIFTY</td><td>SELL</td><td>25</td><td className="text-rose-300">-120.20</td></tr>
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3 className="mb-3 text-lg font-semibold">Config Preview</h3>
        <pre className="overflow-x-auto rounded-xl bg-slate-900 p-4 text-xs text-slate-300">
          {JSON.stringify(strategy.configJson || { riskPerTrade: 1, stopLossPct: 1 }, null, 2)}
        </pre>
      </div>
    </div>
  );
}
