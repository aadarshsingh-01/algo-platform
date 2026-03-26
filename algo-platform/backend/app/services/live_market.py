import asyncio
import logging
import random
import threading
from datetime import UTC, datetime, time
from zoneinfo import ZoneInfo

from fastapi import WebSocket
from kiteconnect import KiteTicker

from app.config import settings
from app.database import SessionLocal
from app.models.instrument import Instrument

logger = logging.getLogger(__name__)


class LiveMarketService:
    def __init__(self) -> None:
        self._clients: set[WebSocket] = set()
        self._latest_ticks: dict[int, dict] = {}
        self._loop: asyncio.AbstractEventLoop | None = None
        self._ws: KiteTicker | None = None
        self._ws_thread: threading.Thread | None = None
        self._mock_task: asyncio.Task | None = None
        self._running = False
        self._symbols = self._parse_symbols()
        self._tokens = self._parse_tokens()
        self._tz = ZoneInfo(settings.market_timezone)

    def _parse_tokens(self) -> list[int]:
        return [int(x.strip()) for x in settings.live_watchlist_tokens.split(",") if x.strip()]

    def _parse_symbols(self) -> list[str]:
        return [x.strip() for x in settings.live_watchlist_symbols.split(",") if x.strip()]

    def _resolved_symbol(self, token: int) -> str | None:
        if not self._symbols:
            return None
        idx = self._tokens.index(token) if token in self._tokens else -1
        if idx >= 0 and idx < len(self._symbols):
            return self._symbols[idx]
        return None

    def _hydrate_symbols_from_db(self) -> None:
        if self._symbols or not self._tokens:
            return
        db = SessionLocal()
        try:
            rows = db.query(Instrument).filter(Instrument.instrument_token.in_(self._tokens)).all()
            by_token = {row.instrument_token: row.tradingsymbol for row in rows}
            self._symbols = [by_token.get(token, f"TOKEN-{token}") for token in self._tokens]
        finally:
            db.close()

    def _calc_change_percent(self, last_price: float | None, close: float | None) -> float | None:
        if not last_price or not close:
            return None
        if close == 0:
            return None
        return round(((last_price - close) / close) * 100, 4)

    def market_status(self) -> dict:
        now_utc = datetime.now(UTC)
        market_time = now_utc.astimezone(self._tz)
        current = market_time.time()

        pre_open_start = time(0, 0, 0)
        live_start = time(9, 15, 0)
        live_end = time(15, 30, 0)

        if pre_open_start <= current < live_start:
            status = "pre_open"
            label = "Pre-open"
            color = "amber"
            is_open = False
        elif live_start <= current <= live_end:
            status = "live"
            label = "Market Live"
            color = "green"
            is_open = True
        else:
            status = "closed"
            label = "Market Closed"
            color = "red"
            is_open = False

        return {
            "server_time": now_utc,
            "market_time": market_time,
            "timezone": settings.market_timezone,
            "is_market_open": is_open,
            "status": status,
            "status_label": label,
            "color": color,
        }

    def get_latest_ticks(self) -> list[dict]:
        return list(self._latest_ticks.values())

    def add_client(self, ws: WebSocket) -> None:
        self._clients.add(ws)

    def remove_client(self, ws: WebSocket) -> None:
        self._clients.discard(ws)

    async def broadcast_tick(self, payload: dict) -> None:
        stale_clients: list[WebSocket] = []
        for client in self._clients:
            try:
                await client.send_json(payload)
            except Exception:
                stale_clients.append(client)
        for client in stale_clients:
            self._clients.discard(client)

    def _schedule_broadcast(self, payload: dict) -> None:
        if self._loop and self._loop.is_running():
            asyncio.run_coroutine_threadsafe(self.broadcast_tick(payload), self._loop)

    def _normalize_tick(self, tick: dict) -> dict:
        token = int(tick.get("instrument_token"))
        ohlc = tick.get("ohlc") or {}
        last_price = tick.get("last_price")
        close_price = ohlc.get("close")
        normalized = {
            "instrument_token": token,
            "tradingsymbol": self._resolved_symbol(token),
            "exchange": None,
            "last_price": float(last_price) if last_price is not None else None,
            "last_quantity": tick.get("last_quantity"),
            "average_price": float(tick["average_price"]) if tick.get("average_price") is not None else None,
            "volume": tick.get("volume"),
            "buy_quantity": tick.get("buy_quantity"),
            "sell_quantity": tick.get("sell_quantity"),
            "open": float(ohlc["open"]) if ohlc.get("open") is not None else None,
            "high": float(ohlc["high"]) if ohlc.get("high") is not None else None,
            "low": float(ohlc["low"]) if ohlc.get("low") is not None else None,
            "close": float(close_price) if close_price is not None else None,
            "change_percent": self._calc_change_percent(
                float(last_price) if last_price is not None else None,
                float(close_price) if close_price is not None else None,
            ),
            "last_trade_time": tick.get("last_trade_time"),
            "tick_timestamp": tick.get("timestamp") or datetime.now(UTC),
        }
        self._latest_ticks[token] = normalized
        return normalized

    def _start_kite_ticker(self) -> None:
        if not settings.kite_api_key or not settings.kite_access_token:
            logger.warning("Live market: Kite credentials missing, skipping real ticker startup.")
            return
        if not self._tokens:
            logger.warning("Live market: no watchlist tokens configured, skipping real ticker startup.")
            return

        self._ws = KiteTicker(settings.kite_api_key, settings.kite_access_token)

        def on_ticks(ws, ticks):
            for tick in ticks:
                data = self._normalize_tick(tick)
                self._schedule_broadcast({"type": "tick", "data": data})

        def on_connect(ws, response):
            logger.info("Live market: KiteTicker connected.")
            ws.subscribe(self._tokens)
            ws.set_mode(ws.MODE_FULL, self._tokens)

        def on_close(ws, code, reason):
            logger.warning("Live market: KiteTicker closed code=%s reason=%s", code, reason)
            if self._running:
                try:
                    ws.connect(threaded=True, disable_ssl_verification=False)
                except Exception as exc:
                    logger.exception("Live market reconnect failed: %s", exc)

        def on_error(ws, code, reason):
            logger.error("Live market: KiteTicker error code=%s reason=%s", code, reason)

        self._ws.on_ticks = on_ticks
        self._ws.on_connect = on_connect
        self._ws.on_close = on_close
        self._ws.on_error = on_error

        self._ws_thread = threading.Thread(
            target=lambda: self._ws.connect(threaded=False, disable_ssl_verification=False),
            daemon=True,
            name="kite-live-market-thread",
        )
        self._ws_thread.start()
        logger.info("Live market: started KiteTicker thread.")

    async def _mock_loop(self) -> None:
        if not self._tokens:
            self._tokens = [256265, 260105]
        for token in self._tokens:
            base = 100 + random.uniform(0, 1000)
            self._latest_ticks[token] = {
                "instrument_token": token,
                "tradingsymbol": self._resolved_symbol(token) or f"TOKEN-{token}",
                "exchange": "NSE",
                "last_price": round(base, 2),
                "last_quantity": 0,
                "average_price": round(base, 2),
                "volume": 0,
                "buy_quantity": 0,
                "sell_quantity": 0,
                "open": round(base * 0.99, 2),
                "high": round(base * 1.01, 2),
                "low": round(base * 0.98, 2),
                "close": round(base * 0.995, 2),
                "change_percent": round(((base - (base * 0.995)) / (base * 0.995)) * 100, 4),
                "last_trade_time": None,
                "tick_timestamp": datetime.now(UTC),
            }

        while self._running:
            for token in self._tokens:
                row = self._latest_ticks[token]
                current = float(row["last_price"] or 100.0)
                delta = random.uniform(-1.2, 1.2)
                next_price = round(max(1.0, current + delta), 2)
                row["last_price"] = next_price
                row["high"] = max(float(row["high"] or next_price), next_price)
                row["low"] = min(float(row["low"] or next_price), next_price)
                close = float(row["close"] or next_price)
                row["change_percent"] = self._calc_change_percent(next_price, close)
                row["volume"] = int(row["volume"] or 0) + random.randint(20, 300)
                row["tick_timestamp"] = datetime.now(UTC)
                self._schedule_broadcast({"type": "tick", "data": row})
            self._schedule_broadcast({"type": "status", "data": self.market_status()})
            await asyncio.sleep(1.5)

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._loop = asyncio.get_running_loop()
        self._hydrate_symbols_from_db()
        logger.info("Live market service starting. mock=%s", settings.live_market_mock)
        if settings.live_market_mock:
            self._mock_task = asyncio.create_task(self._mock_loop())
        else:
            try:
                self._start_kite_ticker()
            except Exception as exc:
                logger.exception("Live market startup failed, continuing app boot: %s", exc)

    async def stop(self) -> None:
        self._running = False
        if self._mock_task:
            self._mock_task.cancel()
            self._mock_task = None
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
        self._clients.clear()
        logger.info("Live market service stopped.")
