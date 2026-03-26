from datetime import datetime
import asyncio

from fastapi import APIRouter, Depends, Query, Request, WebSocket, WebSocketDisconnect, status
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
    LiveTickSnapshot,
    MarketStatus,
)
from app.security import decode_access_token
from app.scripts.import_candles_5m import import_candles
from app.services.live_market import LiveMarketService

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


def _live_service(request: Request) -> LiveMarketService:
    return request.app.state.live_market_service


@router.get("/live", response_model=LiveTickSnapshot)
def get_live_snapshot(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    service = _live_service(request)
    return LiveTickSnapshot(ticks=service.get_latest_ticks(), market_status=service.market_status())


@router.get("/market-status", response_model=MarketStatus)
def get_market_status(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    _ = current_user
    service = _live_service(request)
    return MarketStatus(**service.market_status())


@router.websocket("/ws/live")
async def ws_live_market(websocket: WebSocket):
    # Minimal WS auth: optional bearer token in query. If provided and invalid, reject.
    token = websocket.query_params.get("token")
    if token:
        try:
            decode_access_token(token)
        except Exception:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

    await websocket.accept()
    service: LiveMarketService = websocket.app.state.live_market_service
    service.add_client(websocket)
    await websocket.send_json({"type": "status", "data": service.market_status()})
    try:
        while True:
            await asyncio.sleep(5)
            await websocket.send_json({"type": "status", "data": service.market_status()})
    except WebSocketDisconnect:
        service.remove_client(websocket)
    except Exception:
        service.remove_client(websocket)
