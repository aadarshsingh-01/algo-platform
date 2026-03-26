 "use client";

import { useEffect, useState } from "react";
import { LiveWatchlist } from "@/components/live-watchlist";
import { MarketClock } from "@/components/market-clock";
import { SummaryCard } from "@/components/summary-card";
import { StrategyTable } from "@/components/strategy-table";
import { connectLiveMarketSocket, fetchLiveSnapshot, getRecentAlerts, getSummary, getTopStrategies } from "@/lib/api";
import { mockAlerts, mockStrategies, mockSummary } from "@/lib/mock";
import { Alert, DashboardSummary, LiveFeedMessage, LiveTick, MarketStatus, Strategy } from "@/lib/types";

export default function DashboardPage() {
  const [summary, setSummary] = useState<DashboardSummary>(mockSummary);
  const [strategies, setStrategies] = useState<Strategy[]>(mockStrategies);
  const [alerts, setAlerts] = useState<Alert[]>(mockAlerts);
  const [ticks, setTicks] = useState<LiveTick[]>([]);
  const [marketStatus, setMarketStatus] = useState<MarketStatus | null>(null);
  const [liveLoading, setLiveLoading] = useState(true);
  const [liveError, setLiveError] = useState("");

  useEffect(() => {
    getSummary().then(setSummary).catch(() => setSummary(mockSummary));
    getTopStrategies().then(setStrategies).catch(() => setStrategies(mockStrategies));
    getRecentAlerts().then(setAlerts).catch(() => setAlerts(mockAlerts));
  }, []);

  useEffect(() => {
    let ws: WebSocket | null = null;
    let reconnectTimer: ReturnType<typeof setTimeout> | null = null;

    const bootstrap = async () => {
      try {
        const snapshot = await fetchLiveSnapshot();
        setTicks(snapshot.ticks || []);
        setMarketStatus(snapshot.market_status);
      } catch {
        setLiveError("Unable to load live snapshot.");
      } finally {
        setLiveLoading(false);
      }
    };

    const connect = () => {
      const token = typeof window !== "undefined" ? localStorage.getItem("access_token") || undefined : undefined;
      ws = connectLiveMarketSocket(token);
      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data) as LiveFeedMessage;
          if (message.type === "tick") {
            setTicks((prev) => {
              const next = [...prev];
              const idx = next.findIndex((x) => x.instrument_token === message.data.instrument_token);
              if (idx >= 0) next[idx] = message.data;
              else next.push(message.data);
              return next.sort((a, b) => a.instrument_token - b.instrument_token);
            });
          } else if (message.type === "status") {
            setMarketStatus(message.data);
          }
        } catch {
          // Ignore malformed payloads.
        }
      };
      ws.onerror = () => setLiveError("Live connection error. Reconnecting...");
      ws.onclose = () => {
        reconnectTimer = setTimeout(connect, 3000);
      };
    };

    bootstrap();
    connect();

    return () => {
      if (reconnectTimer) clearTimeout(reconnectTimer);
      if (ws) ws.close();
    };
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold">Dashboard</h1>
      <MarketClock marketStatus={marketStatus} />
      <LiveWatchlist ticks={ticks} loading={liveLoading} error={liveError} />
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
