from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.candle_5m import Candle5m
from app.models.instrument import Instrument
from app.models.user import User
from app.schemas.market_data import (
    Candle5mResponse,
    HistoricalSyncRequest,
    HistoricalSyncResponse,
    InstrumentResponse,
)
from app.scripts.import_candles_5m import import_candles

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/instruments", response_model=list[InstrumentResponse])
def list_instruments(
    search: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=2000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    stmt = select(Instrument).limit(limit)
    if search:
        stmt = stmt.where(Instrument.tradingsymbol.ilike(f"%{search}%"))
    return db.execute(stmt).scalars().all()


@router.post("/historical-sync", response_model=HistoricalSyncResponse)
def trigger_historical_sync(
    payload: HistoricalSyncRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    requested, inserted, skipped = import_candles(
        db=db,
        instrument_token=payload.instrument_token,
        from_date=payload.from_date,
        to_date=payload.to_date,
    )
    return HistoricalSyncResponse(
        instrument_token=payload.instrument_token,
        requested=requested,
        inserted=inserted,
        skipped_duplicates=skipped,
    )


@router.get("/instruments/{instrument_token}/candles", response_model=list[Candle5mResponse])
def get_candles(
    instrument_token: int,
    from_date: datetime,
    to_date: datetime,
    limit: int = Query(default=2000, ge=1, le=10000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    stmt = (
        select(Candle5m)
        .where(
            and_(
                Candle5m.instrument_token == instrument_token,
                Candle5m.candle_time >= from_date,
                Candle5m.candle_time <= to_date,
            )
        )
        .order_by(Candle5m.candle_time.asc())
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()
