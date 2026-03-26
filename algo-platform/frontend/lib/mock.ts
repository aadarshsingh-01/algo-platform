import { Alert, DashboardSummary, Strategy } from "@/lib/types";

export const mockSummary: DashboardSummary = {
  totalPaperPnl: 12450.33,
  signalsToday: 18,
  livePositions: 5,
  bestStrategy: "BankNifty Momentum"
};

export const mockStrategies: Strategy[] = [
  {
    id: 1,
    name: "BankNifty Momentum",
    market: "NSE",
    timeframe: "5m",
    isActive: true,
    todayPnl: 4250.75,
    winRate: 61.2,
    cagr: 28.4,
    maxDrawdown: 9.8,
    lastSignal: "BUY 10:15",
    strategyType: "momentum",
    description: "Momentum breakout strategy",
    configJson: { riskPerTrade: 1.2, stopLossPct: 0.8 }
  },
  {
    id: 2,
    name: "Nifty Mean Reversion",
    market: "NSE",
    timeframe: "15m",
    isActive: false,
    todayPnl: -550.2,
    winRate: 55.1,
    cagr: 19.2,
    maxDrawdown: 11.5,
    lastSignal: "SELL 09:45"
  },
  {
    id: 3,
    name: "FinNifty Trend Ride",
    market: "NSE",
    timeframe: "30m",
    isActive: true,
    todayPnl: 1800.4,
    winRate: 58.9,
    cagr: 24.9,
    maxDrawdown: 10.2,
    lastSignal: "BUY 11:00"
  }
];

export const mockAlerts: Alert[] = [
  { id: 1, level: "warning", message: "Nifty Mean Reversion hit drawdown threshold", createdAt: "2026-03-26T09:20:00Z" },
  { id: 2, level: "info", message: "BankNifty Momentum generated BUY signal", createdAt: "2026-03-26T10:15:00Z" },
  { id: 3, level: "critical", message: "FinNifty Trend Ride max slippage exceeded", createdAt: "2026-03-26T11:05:00Z" }
];
