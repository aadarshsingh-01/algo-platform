export type DashboardSummary = {
  totalPaperPnl: number;
  signalsToday: number;
  livePositions: number;
  bestStrategy: string;
};

export type Alert = {
  id: number;
  level: "info" | "warning" | "critical";
  message: string;
  createdAt: string;
};

export type Strategy = {
  id: number;
  name: string;
  market: string;
  timeframe: string;
  isActive: boolean;
  todayPnl: number;
  winRate: number;
  cagr: number;
  maxDrawdown: number;
  lastSignal: string;
  description?: string;
  strategyType?: string;
  configJson?: Record<string, unknown>;
};

export type LiveTick = {
  instrument_token: number;
  tradingsymbol: string | null;
  exchange: string | null;
  last_price: number | null;
  last_quantity: number | null;
  average_price: number | null;
  volume: number | null;
  buy_quantity: number | null;
  sell_quantity: number | null;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  change_percent: number | null;
  last_trade_time: string | null;
  tick_timestamp: string;
};

export type MarketStatus = {
  server_time: string;
  market_time: string;
  timezone: string;
  is_market_open: boolean;
  status: "pre_open" | "live" | "closed";
  status_label: string;
  color: "green" | "amber" | "red";
};

export type LiveTickSnapshot = {
  ticks: LiveTick[];
  market_status: MarketStatus;
};

export type LiveFeedMessage =
  | { type: "tick"; data: LiveTick }
  | { type: "status"; data: MarketStatus };

export type WatchlistQuote = {
  instrument_token: number;
  tradingsymbol: string;
  exchange: string;
  last_price: number | null;
  open: number | null;
  high: number | null;
  low: number | null;
  close: number | null;
  change_percent: number | null;
  timestamp: string;
};
