from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models.strategy import Strategy
from app.models.user import User
from app.schemas.strategy import StrategyCreate, StrategyResponse, StrategyUpdate

router = APIRouter(prefix="/strategies", tags=["strategies"])


def _get_user_strategy(db: Session, strategy_id: int, user_id: int) -> Strategy:
    strategy = (
        db.query(Strategy)
        .filter(Strategy.id == strategy_id, Strategy.user_id == user_id)
        .first()
    )
    if not strategy:
        raise HTTPException(status_code=404, detail="Strategy not found")
    return strategy


@router.post("", response_model=StrategyResponse, status_code=status.HTTP_201_CREATED)
def create_strategy(
    payload: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategy = Strategy(user_id=current_user.id, **payload.model_dump())
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy


@router.get("", response_model=list[StrategyResponse])
def list_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Strategy).filter(Strategy.user_id == current_user.id).all()


@router.get("/{strategy_id}", response_model=StrategyResponse)
def get_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return _get_user_strategy(db, strategy_id, current_user.id)


@router.put("/{strategy_id}", response_model=StrategyResponse)
def update_strategy(
    strategy_id: int,
    payload: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategy = _get_user_strategy(db, strategy_id, current_user.id)
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(strategy, field, value)
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy


@router.post("/{strategy_id}/start", response_model=StrategyResponse)
def start_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategy = _get_user_strategy(db, strategy_id, current_user.id)
    strategy.is_active = True
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy


@router.post("/{strategy_id}/pause", response_model=StrategyResponse)
def pause_strategy(
    strategy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    strategy = _get_user_strategy(db, strategy_id, current_user.id)
    strategy.is_active = False
    db.add(strategy)
    db.commit()
    db.refresh(strategy)
    return strategy
