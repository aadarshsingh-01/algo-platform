# Algo Platform V1

Production-style V1 monorepo foundation for an algo trading web platform with a Next.js frontend, FastAPI backend, and Dockerized infrastructure.

## Stack

- Frontend: Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui-style components, `lucide-react`, `recharts`
- Backend: FastAPI, SQLAlchemy, Pydantic, Alembic, JWT auth, Passlib bcrypt
- Infra: PostgreSQL, Redis, Nginx reverse proxy, Docker Compose

## Folder Structure

```text
algo-platform/
  frontend/
  backend/
  infra/
  .env.example
  .gitignore
  docker-compose.yml
  Makefile
  README.md
```

## Features Included in V1

- Authentication: register, login, current user endpoint
- Dashboard: summary, top strategies, recent alerts
- Strategies: create, list, detail, update, start, pause
- Frontend pages:
  - `/login`
  - `/register`
  - `/dashboard`
  - `/strategies`
  - `/strategies/[id]`
  - `/scanner` (Coming Soon)
- Seeded demo data:
  - 1 demo user (`demo@algo.com` / `demo1234`)
  - 3 demo strategies
  - sample dashboard + alerts

## Environment Setup

1. Copy env file:

```bash
cp .env.example .env
```

2. Adjust values in `.env` as needed.

## Run Locally (Without Docker)

### Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`, backend on `http://localhost:8000`.

## Run Full Stack with Docker

```bash
cp .env.example .env
docker compose up --build -d
docker compose logs -f
```

App is available at `http://localhost` via Nginx.

## Makefile Commands

- `make up` - start full stack with Docker
- `make down` - stop stack
- `make logs` - follow Docker logs
- `make backend` - run backend dev server
- `make frontend` - run frontend dev server
- `make migrate` - run Alembic migrations
- `make seed` - seed demo data

## API Prefixes

- `/api/v1/auth/*`
- `/api/v1/dashboard/*`
- `/api/v1/strategies/*`
- `/api/v1/health`

## Product Boundaries (V1)

This foundation intentionally excludes:
- real-money order execution
- scanner engine implementation
- options chain engine
- optimizer
- billing
- websocket live feed
- multi-broker workflows
- full Kite auth flow
- full backtesting engine

## Next Steps

1. Add Kite API connector service layer (paper-only first).
2. Add structured backtesting module with historical data adapters.
3. Add strategy run-state persistence and execution logs.
4. Add role-based auth and audit logging.
