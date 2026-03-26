"use client";

import { useEffect, useMemo, useState } from "react";
import { MarketStatus } from "@/lib/types";

type MarketClockProps = {
  marketStatus: MarketStatus | null;
};

export function MarketClock({ marketStatus }: MarketClockProps) {
  const [now, setNow] = useState<Date>(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id);
  }, []);

  const indiaTime = useMemo(
    () =>
      new Intl.DateTimeFormat("en-IN", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
        timeZone: "Asia/Kolkata"
      }).format(now),
    [now]
  );

  const statusLabel = marketStatus?.status_label || "Market Status";
  const color =
    marketStatus?.color === "green"
      ? "bg-emerald-400"
      : marketStatus?.color === "amber"
      ? "bg-amber-400"
      : "bg-rose-400";

  return (
    <div className="card flex flex-wrap items-center justify-between gap-3">
      <div className="flex items-center gap-2">
        <span className={`h-2.5 w-2.5 rounded-full ${color}`} />
        <p className="text-sm font-medium text-slate-200">{statusLabel}</p>
      </div>
      <p className="text-sm text-slate-300">India Time: {indiaTime}</p>
    </div>
  );
}
