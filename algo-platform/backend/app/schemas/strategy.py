from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StrategyCreate(BaseModel):
    name: str
    slug: str
    description: str = ""
    strategy_type: str = "momentum"
    timeframe: str = "5m"
    market: str = "NSE"
    config_json: dict[str, Any] = Field(default_factory=dict)


class StrategyUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    strategy_type: str | None = None
    timeframe: str | None = None
    market: str | None = None
    config_json: dict[str, Any] | None = None


class StrategyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    slug: str
    description: str
    strategy_type: str
    timeframe: str
    market: str
    config_json: dict[str, Any]
    is_active: bool
    today_pnl: float
    win_rate: float
    cagr: float
    max_drawdown: float
    last_signal: str
    created_at: datetime
    updated_at: datetime
