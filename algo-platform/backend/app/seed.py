from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.strategy import Strategy
from app.models.user import User
from app.security import hash_password


def seed(db: Session) -> None:
    user = db.query(User).filter(User.email == "demo@algo.com").first()
    if not user:
        user = User(
            name="Demo User",
            email="demo@algo.com",
            password_hash=hash_password("demo1234"),
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    if db.query(Strategy).filter(Strategy.user_id == user.id).count() == 0:
        records = [
            Strategy(
                user_id=user.id,
                name="BankNifty Momentum",
                slug="banknifty-momentum",
                description="Momentum breakout strategy",
                strategy_type="momentum",
                timeframe="5m",
                market="NSE",
                config_json={"riskPerTrade": 1.2, "stopLossPct": 0.8},
                is_active=True,
                today_pnl=4250.75,
                win_rate=61.2,
                cagr=28.4,
                max_drawdown=9.8,
                last_signal="BUY 10:15",
            ),
            Strategy(
                user_id=user.id,
                name="Nifty Mean Reversion",
                slug="nifty-mean-reversion",
                description="Mean reversion setup",
                strategy_type="mean_reversion",
                timeframe="15m",
                market="NSE",
                config_json={"entryZScore": 2.0, "exitZScore": 0.7},
                is_active=False,
                today_pnl=-550.20,
                win_rate=55.1,
                cagr=19.2,
                max_drawdown=11.5,
                last_signal="SELL 09:45",
            ),
            Strategy(
                user_id=user.id,
                name="FinNifty Trend Ride",
                slug="finnifty-trend-ride",
                description="Trend-following strategy",
                strategy_type="trend",
                timeframe="30m",
                market="NSE",
                config_json={"atrMultiplier": 2.2, "trailStop": True},
                is_active=True,
                today_pnl=1800.40,
                win_rate=58.9,
                cagr=24.9,
                max_drawdown=10.2,
                last_signal="BUY 11:00",
            ),
        ]
        db.add_all(records)
        db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
