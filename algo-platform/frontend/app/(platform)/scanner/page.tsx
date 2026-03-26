"use client";

import { EmptyState } from "@/components/empty-state";
import { MarketClock } from "@/components/market-clock";
import { fetchMarketStatus } from "@/lib/api";
import { useEffect, useState } from "react";
import { MarketStatus } from "@/lib/types";

export default function ScannerPage() {
  const [marketStatus, setMarketStatus] = useState<MarketStatus | null>(null);
  useEffect(() => {
    fetchMarketStatus().then(setMarketStatus).catch(() => setMarketStatus(null));
  }, []);

  return (
    <div className="space-y-4">
      <MarketClock marketStatus={marketStatus} />
      <EmptyState title="Scanner" description="Coming Soon - Scanner will build on this live feed next." />
    </div>
  );
}
