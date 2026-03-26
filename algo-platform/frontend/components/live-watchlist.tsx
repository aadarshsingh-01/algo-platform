"use client";

import { WatchlistQuote } from "@/lib/types";

type LiveWatchlistProps = {
  ticks: WatchlistQuote[];
  loading: boolean;
  error?: string;
};

export function LiveWatchlist({ ticks, loading, error }: LiveWatchlistProps) {
  if (loading) {
    return <div className="card text-sm text-slate-300">Loading live watchlist...</div>;
  }
  if (error) {
    return <div className="card text-sm text-rose-300">{error}</div>;
  }
  if (!ticks.length) {
    return <div className="card text-sm text-slate-300">No watchlist quotes available.</div>;
  }

  return (
    <div className="card overflow-x-auto">
      <h2 className="mb-3 text-lg font-semibold">Watchlist Prices</h2>
      <table className="min-w-full text-sm">
        <thead>
          <tr className="border-b border-border text-left text-slate-400">
            <th className="pb-2">Symbol</th>
            <th className="pb-2">LTP</th>
            <th className="pb-2">Open</th>
            <th className="pb-2">High</th>
            <th className="pb-2">Low</th>
            <th className="pb-2">Close</th>
            <th className="pb-2">% Chg</th>
            <th className="pb-2">Updated</th>
          </tr>
        </thead>
        <tbody>
          {ticks.map((tick) => (
            <tr key={tick.instrument_token} className="border-b border-border/50">
              <td className="py-2 font-medium">{tick.tradingsymbol || tick.instrument_token}</td>
              <td>{tick.last_price?.toFixed(2) ?? "-"}</td>
              <td>{tick.open?.toFixed(2) ?? "-"}</td>
              <td>{tick.high?.toFixed(2) ?? "-"}</td>
              <td>{tick.low?.toFixed(2) ?? "-"}</td>
              <td>{tick.close?.toFixed(2) ?? "-"}</td>
              <td className={(tick.change_percent || 0) >= 0 ? "text-emerald-300" : "text-rose-300"}>
                {tick.change_percent !== null ? `${tick.change_percent.toFixed(2)}%` : "-"}
              </td>
              <td>{new Date(tick.timestamp).toLocaleTimeString("en-IN", { hour12: false, timeZone: "Asia/Kolkata" })}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
