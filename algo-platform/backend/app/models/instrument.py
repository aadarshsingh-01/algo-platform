from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Instrument(Base):
    __tablename__ = "instruments"

    instrument_token: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    exchange_token: Mapped[int | None] = mapped_column(Integer, nullable=True)
    tradingsymbol: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    name: Mapped[str | None] = mapped_column(String(150), nullable=True)
    last_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    expiry: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    strike: Mapped[float | None] = mapped_column(Float, nullable=True)
    tick_size: Mapped[float] = mapped_column(Float, nullable=False, default=0.05)
    lot_size: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    instrument_type: Mapped[str] = mapped_column(String(40), nullable=False, default="EQ")
    segment: Mapped[str] = mapped_column(String(50), nullable=False, default="NSE")
    exchange: Mapped[str] = mapped_column(String(20), nullable=False, default="NSE")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
