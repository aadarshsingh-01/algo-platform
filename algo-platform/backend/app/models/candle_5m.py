from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Candle5m(Base):
    __tablename__ = "candles_5m"
    __table_args__ = (
        UniqueConstraint("instrument_token", "candle_time", name="uq_candles_5m_token_time"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    instrument_token: Mapped[int] = mapped_column(ForeignKey("instruments.instrument_token"), index=True, nullable=False)
    candle_time: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    open: Mapped[float] = mapped_column(Float, nullable=False)
    high: Mapped[float] = mapped_column(Float, nullable=False)
    low: Mapped[float] = mapped_column(Float, nullable=False)
    close: Mapped[float] = mapped_column(Float, nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    oi: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
