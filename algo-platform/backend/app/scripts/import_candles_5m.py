import argparse
from datetime import datetime

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.candle_5m import Candle5m
from app.models.instrument import Instrument
from app.services.kite_service import KiteService


def _resolve_instrument_token(db: Session, instrument_token: int | None, symbol: str | None) -> int:
    if instrument_token is not None:
        return instrument_token
    if not symbol:
        raise ValueError("Provide either --instrument-token or --symbol.")

    instrument = db.execute(
        select(Instrument).where(Instrument.tradingsymbol == symbol)
    ).scalar_one_or_none()
    if not instrument:
        raise ValueError(f"Symbol not found in DB: {symbol}. Run instrument sync first.")
    return instrument.instrument_token


def import_candles(
    db: Session,
    instrument_token: int,
    from_date: datetime,
    to_date: datetime,
) -> tuple[int, int, int]:
    service = KiteService()
    raw_candles = service.fetch_historical_candles(
        instrument_token=instrument_token,
        from_date=from_date,
        to_date=to_date,
        interval="5minute",
    )

    existing_times = set(
        db.execute(
            select(Candle5m.candle_time).where(
                and_(
                    Candle5m.instrument_token == instrument_token,
                    Candle5m.candle_time >= from_date,
                    Candle5m.candle_time <= to_date,
                )
            )
        ).scalars()
    )

    inserted = 0
    skipped = 0

    for row in raw_candles:
        candle_time = row["date"]
        if candle_time in existing_times:
            skipped += 1
            continue

        db.add(
            Candle5m(
                instrument_token=instrument_token,
                candle_time=candle_time,
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=int(row.get("volume", 0)),
                oi=int(row["oi"]) if row.get("oi") is not None else None,
            )
        )
        inserted += 1

    db.commit()
    return len(raw_candles), inserted, skipped


def main() -> None:
    parser = argparse.ArgumentParser(description="Import 5-minute candles from Kite into DB.")
    parser.add_argument("--instrument-token", type=int, default=None)
    parser.add_argument("--symbol", type=str, default=None)
    parser.add_argument("--from-date", type=str, required=True, help="ISO datetime, e.g. 2026-03-01T09:15:00")
    parser.add_argument("--to-date", type=str, required=True, help="ISO datetime, e.g. 2026-03-10T15:30:00")
    args = parser.parse_args()

    from_date = datetime.fromisoformat(args.from_date)
    to_date = datetime.fromisoformat(args.to_date)

    db = SessionLocal()
    try:
        token = _resolve_instrument_token(db, args.instrument_token, args.symbol)
        requested, inserted, skipped = import_candles(
            db=db,
            instrument_token=token,
            from_date=from_date,
            to_date=to_date,
        )
        print(
            f"Candle import completed. instrument_token={token} requested={requested} "
            f"inserted={inserted} skipped_duplicates={skipped}"
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
