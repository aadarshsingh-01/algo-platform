from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class InstrumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instrument_token: int
    tradingsymbol: str
    exchange: str
    segment: str
    instrument_type: str
    tick_size: float
    lot_size: int


class Candle5mResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    instrument_token: int
    candle_time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    oi: int | None


class HistoricalSyncRequest(BaseModel):
    instrument_token: int
    from_date: datetime
    to_date: datetime


class HistoricalSyncResponse(BaseModel):
    instrument_token: int
    requested: int
    inserted: int
    skipped_duplicates: int


class LiveTick(BaseModel):
    instrument_token: int
    tradingsymbol: str | None
    exchange: str | None
    last_price: float | None
    last_quantity: int | None
    average_price: float | None
    volume: int | None
    buy_quantity: int | None
    sell_quantity: int | None
    open: float | None
    high: float | None
    low: float | None
    close: float | None
    change_percent: float | None
    last_trade_time: datetime | None
    tick_timestamp: datetime


class MarketStatus(BaseModel):
    server_time: datetime
    market_time: datetime
    timezone: str
    is_market_open: bool
    status: Literal["pre_open", "live", "closed"]
    status_label: str
    color: Literal["green", "amber", "red"]


class LiveTickSnapshot(BaseModel):
    ticks: list[LiveTick]
    market_status: MarketStatus
