"use client";

import { useEffect, useMemo, useState } from "react";
import { StrategyTable } from "@/components/strategy-table";
import { getStrategies } from "@/lib/api";
import { Strategy } from "@/lib/types";

export default function StrategiesPage() {
  const [strategies, setStrategies] = useState<Strategy[]>([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    getStrategies().then(setStrategies).catch(() => setStrategies([]));
  }, []);

  const filtered = useMemo(
    () => strategies.filter((s) => s.name.toLowerCase().includes(query.toLowerCase())),
    [strategies, query]
  );

  return (
    <div className="space-y-5">
      <h1 className="text-2xl font-semibold">Strategies</h1>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full max-w-md rounded-xl border border-border bg-slate-900 p-3"
        placeholder="Search strategies..."
      />
      <StrategyTable strategies={filtered} />
    </div>
  );
}
