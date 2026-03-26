from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import SessionLocal
from app.routers import auth, dashboard, health, market_data, strategies
from app.seed import seed

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup() -> None:
    # Seed only; schema is expected to be managed by Alembic.
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()


api_prefix = "/api/v1"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(dashboard.router, prefix=api_prefix)
app.include_router(strategies.router, prefix=api_prefix)
app.include_router(market_data.router, prefix=api_prefix)
app.include_router(health.router, prefix=api_prefix)
