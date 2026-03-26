from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.strategy import Strategy
from app.models.user import User
from app.schemas.dashboard import AlertResponse, DashboardSummaryResponse, TopStrategyResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategies = db.query(Strategy).filter(Strategy.user_id == current_user.id).all()
    total_pnl = sum(s.today_pnl for s in strategies)
    signals_today = len([s for s in strategies if s.last_signal != "N/A"])
    live_positions = len([s for s in strategies if s.is_active])
    best = max(strategies, key=lambda s: s.today_pnl).name if strategies else "N/A"
    return DashboardSummaryResponse(
        totalPaperPnl=total_pnl,
        signalsToday=signals_today,
        livePositions=live_positions,
        bestStrategy=best,
    )


@router.get("/top-strategies", response_model=list[TopStrategyResponse])
def top_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    records = (
        db.query(Strategy)
        .filter(Strategy.user_id == current_user.id)
        .order_by(Strategy.today_pnl.desc())
        .limit(5)
        .all()
    )
    return [
        TopStrategyResponse(
            id=s.id,
            name=s.name,
            market=s.market,
            timeframe=s.timeframe,
            isActive=s.is_active,
            todayPnl=s.today_pnl,
            winRate=s.win_rate,
            cagr=s.cagr,
            maxDrawdown=s.max_drawdown,
            lastSignal=s.last_signal,
        )
        for s in records
    ]


@router.get("/recent-alerts", response_model=list[AlertResponse])
def recent_alerts(
    current_user: User = Depends(get_current_user),
):
    # V1: return static alerts; later this can be backed by Redis/DB event stream.
    return [
        AlertResponse(
            id=1,
            level="warning",
            message=f"{current_user.name}, drawdown threshold reached on one strategy",
            createdAt="2026-03-26T09:20:00Z",
        ),
        AlertResponse(
            id=2,
            level="info",
            message="Momentum strategy generated BUY signal",
            createdAt="2026-03-26T10:15:00Z",
        ),
        AlertResponse(
            id=3,
            level="critical",
            message="Slippage alert triggered in paper trade logs",
            createdAt="2026-03-26T11:05:00Z",
        ),
    ]
