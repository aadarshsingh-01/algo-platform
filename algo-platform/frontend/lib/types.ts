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
