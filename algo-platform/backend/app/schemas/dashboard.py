from pydantic import BaseModel


class DashboardSummaryResponse(BaseModel):
    totalPaperPnl: float
    signalsToday: int
    livePositions: int
    bestStrategy: str


class TopStrategyResponse(BaseModel):
    id: int
    name: str
    market: str
    timeframe: str
    isActive: bool
    todayPnl: float
    winRate: float
    cagr: float
    maxDrawdown: float
    lastSignal: str


class AlertResponse(BaseModel):
    id: int
    level: str
    message: str
    createdAt: str
