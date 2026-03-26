from datetime import datetime

from kiteconnect import KiteConnect

from app.config import settings


class KiteService:
    def __init__(self) -> None:
        if not settings.kite_api_key or not settings.kite_access_token:
            raise ValueError("Kite API credentials are missing in environment variables.")
        self.client = KiteConnect(api_key=settings.kite_api_key)
        self.client.set_access_token(settings.kite_access_token)

    def fetch_instruments(self, exchange: str | None = None) -> list[dict]:
        instruments = self.client.instruments(exchange=exchange) if exchange else self.client.instruments()
        return instruments

    def fetch_historical_candles(
        self,
        instrument_token: int,
        from_date: datetime,
        to_date: datetime,
        interval: str = "5minute",
    ) -> list[dict]:
        return self.client.historical_data(
            instrument_token=instrument_token,
            from_date=from_date,
            to_date=to_date,
            interval=interval,
            continuous=False,
            oi=True,
        )
