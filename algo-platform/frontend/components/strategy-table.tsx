import Link from "next/link";
import { Strategy } from "@/lib/types";
import { StatusBadge } from "@/components/status-badge";

type StrategyTableProps = {
  strategies: Strategy[];
};

export function StrategyTable({ strategies }: StrategyTableProps) {
  return (
    <div className="card overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="border-b border-border text-left text-slate-400">
            <th className="pb-3">Name</th>
            <th className="pb-3">Market</th>
            <th className="pb-3">Timeframe</th>
            <th className="pb-3">Status</th>
            <th className="pb-3">Today P&L</th>
            <th className="pb-3">Win Rate</th>
            <th className="pb-3">CAGR</th>
            <th className="pb-3">Max DD</th>
            <th className="pb-3">Last Signal</th>
            <th className="pb-3">Action</th>
          </tr>
        </thead>
        <tbody>
          {strategies.map((strategy) => (
            <tr key={strategy.id} className="border-b border-border/60">
              <td className="py-3 font-medium">{strategy.name}</td>
              <td>{strategy.market}</td>
              <td>{strategy.timeframe}</td>
              <td><StatusBadge active={strategy.isActive} /></td>
              <td className={strategy.todayPnl >= 0 ? "text-emerald-300" : "text-rose-300"}>
                {strategy.todayPnl.toFixed(2)}
              </td>
              <td>{strategy.winRate.toFixed(1)}%</td>
              <td>{strategy.cagr.toFixed(1)}%</td>
              <td>{strategy.maxDrawdown.toFixed(1)}%</td>
              <td>{strategy.lastSignal}</td>
              <td>
                <Link href={`/strategies/${strategy.id}`} className="text-cyan-300 hover:text-cyan-200">
                  Details
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
