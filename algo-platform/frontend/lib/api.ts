import { mockAlerts, mockStrategies, mockSummary } from "@/lib/mock";
import { Alert, DashboardSummary, LiveTickSnapshot, MarketStatus, Strategy, WatchlistQuote } from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

function getToken() {
  if (typeof window === "undefined") return "";
  return localStorage.getItem("access_token") || "";
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getToken();
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options?.headers || {})
    },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

type ApiStrategy = {
  id: number;
  name: string;
  market: string;
  timeframe: string;
  is_active?: boolean;
  isActive?: boolean;
  today_pnl?: number;
  todayPnl?: number;
  win_rate?: number;
  winRate?: number;
  cagr: number;
  max_drawdown?: number;
  maxDrawdown?: number;
  last_signal?: string;
  lastSignal?: string;
  description?: string;
  strategy_type?: string;
  strategyType?: string;
  config_json?: Record<string, unknown>;
  configJson?: Record<string, unknown>;
};

function normalizeStrategy(strategy: ApiStrategy): Strategy {
  return {
    id: strategy.id,
    name: strategy.name,
    market: strategy.market,
    timeframe: strategy.timeframe,
    isActive: strategy.isActive ?? strategy.is_active ?? false,
    todayPnl: strategy.todayPnl ?? strategy.today_pnl ?? 0,
    winRate: strategy.winRate ?? strategy.win_rate ?? 0,
    cagr: strategy.cagr,
    maxDrawdown: strategy.maxDrawdown ?? strategy.max_drawdown ?? 0,
    lastSignal: strategy.lastSignal ?? strategy.last_signal ?? "N/A",
    description: strategy.description,
    strategyType: strategy.strategyType ?? strategy.strategy_type,
    configJson: strategy.configJson ?? strategy.config_json
  };
}

export async function login(email: string, password: string): Promise<{ access_token: string }> {
  return request<{ access_token: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password })
  });
}

export async function register(name: string, email: string, password: string): Promise<{ id: number; email: string }> {
  return request<{ id: number; email: string }>("/auth/register", {
    method: "POST",
    body: JSON.stringify({ name, email, password })
  });
}

export async function getSummary(): Promise<DashboardSummary> {
  try {
    return await request<DashboardSummary>("/dashboard/summary");
  } catch {
    return mockSummary;
  }
}

export async function getTopStrategies(): Promise<Strategy[]> {
  try {
    const data = await request<ApiStrategy[]>("/dashboard/top-strategies");
    return data.map(normalizeStrategy);
  } catch {
    return mockStrategies;
  }
}

export async function getRecentAlerts(): Promise<Alert[]> {
  try {
    return await request<Alert[]>("/dashboard/recent-alerts");
  } catch {
    return mockAlerts;
  }
}

export async function getStrategies(): Promise<Strategy[]> {
  try {
    const data = await request<ApiStrategy[]>("/strategies");
    return data.map(normalizeStrategy);
  } catch {
    return mockStrategies;
  }
}

export async function getStrategyById(id: number): Promise<Strategy> {
  try {
    const data = await request<ApiStrategy>(`/strategies/${id}`);
    return normalizeStrategy(data);
  } catch {
    const match = mockStrategies.find((s) => s.id === id);
    if (!match) throw new Error("Strategy not found");
    return match;
  }
}

export async function startStrategy(id: number): Promise<Strategy> {
  const data = await request<ApiStrategy>(`/strategies/${id}/start`, { method: "POST" });
  return normalizeStrategy(data);
}

export async function pauseStrategy(id: number): Promise<Strategy> {
  const data = await request<ApiStrategy>(`/strategies/${id}/pause`, { method: "POST" });
  return normalizeStrategy(data);
}

export async function fetchMarketStatus(): Promise<MarketStatus> {
  const fallback: MarketStatus = {
    server_time: new Date().toISOString(),
    market_time: new Date().toISOString(),
    timezone: "Asia/Kolkata",
    is_market_open: false,
    status: "closed",
    status_label: "Market Closed",
    color: "red"
  };
  try {
    return await request<MarketStatus>("/market-data/market-status");
  } catch {
    return fallback;
  }
}

export async function fetchLiveSnapshot(): Promise<LiveTickSnapshot> {
  const fallback: LiveTickSnapshot = {
    ticks: [],
    market_status: await fetchMarketStatus()
  };
  try {
    return await request<LiveTickSnapshot>("/market-data/live");
  } catch {
    return fallback;
  }
}

export function connectLiveMarketSocket(token?: string): WebSocket {
  const query = token ? `?token=${encodeURIComponent(token)}` : "";
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const host = window.location.host;
  return new WebSocket(`${protocol}://${host}/api/v1/market-data/ws/live${query}`);
}

export async function fetchWatchlistQuotes(): Promise<WatchlistQuote[]> {
  return request<WatchlistQuote[]>("/market-data/watchlist-quotes");
}
