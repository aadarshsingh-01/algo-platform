from datetime import datetime

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
