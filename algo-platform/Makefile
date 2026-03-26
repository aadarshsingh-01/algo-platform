SHELL := /bin/sh

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend:
	cd frontend && npm run dev

migrate:
	cd backend && alembic upgrade head

seed:
	cd backend && python -m app.seed

sync-instruments:
	cd backend && python -m app.scripts.sync_instruments

import-candles:
	cd backend && python -m app.scripts.import_candles_5m --instrument-token 0 --from-date 2026-01-01T09:15:00 --to-date 2026-01-01T15:30:00
