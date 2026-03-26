import argparse
from datetime import datetime

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.instrument import Instrument
from app.services.kite_service import KiteService


def sync_instruments(db: Session, exchange: str | None = None) -> tuple[int, int]:
    service = KiteService()
    records = service.fetch_instruments(exchange=exchange)

    inserted = 0
    updated = 0

    for item in records:
        token = int(item["instrument_token"])
        instrument = db.get(Instrument, token)
        if not instrument:
            instrument = Instrument(instrument_token=token)
            inserted += 1
        else:
            updated += 1

        instrument.exchange_token = int(item["exchange_token"]) if item.get("exchange_token") is not None else None
        instrument.tradingsymbol = str(item["tradingsymbol"])
        instrument.name = item.get("name")
        instrument.last_price = float(item["last_price"]) if item.get("last_price") is not None else None
        instrument.expiry = item.get("expiry")
        instrument.strike = float(item["strike"]) if item.get("strike") is not None else None
        instrument.tick_size = float(item.get("tick_size", 0.05))
        instrument.lot_size = int(item.get("lot_size", 1))
        instrument.instrument_type = str(item.get("instrument_type", "EQ"))
        instrument.segment = str(item.get("segment", "NSE"))
        instrument.exchange = str(item.get("exchange", "NSE"))
        instrument.updated_at = datetime.utcnow()
        db.add(instrument)

    db.commit()
    return inserted, updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync instruments from Kite into DB.")
    parser.add_argument("--exchange", type=str, default=None, help="Optional exchange filter, e.g. NSE")
    args = parser.parse_args()

    db = SessionLocal()
    try:
        inserted, updated = sync_instruments(db, exchange=args.exchange)
        print(f"Instrument sync completed. inserted={inserted} updated={updated}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
