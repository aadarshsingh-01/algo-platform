"""add market data tables

Revision ID: 0002_market_data
Revises: 0001_init
Create Date: 2026-03-26 00:30:00
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0002_market_data"
down_revision: Union[str, None] = "0001_init"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "instruments",
        sa.Column("instrument_token", sa.Integer(), primary_key=True),
        sa.Column("exchange_token", sa.Integer(), nullable=True),
        sa.Column("tradingsymbol", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=True),
        sa.Column("last_price", sa.Float(), nullable=True),
        sa.Column("expiry", sa.DateTime(), nullable=True),
        sa.Column("strike", sa.Float(), nullable=True),
        sa.Column("tick_size", sa.Float(), nullable=False),
        sa.Column("lot_size", sa.Integer(), nullable=False),
        sa.Column("instrument_type", sa.String(length=40), nullable=False),
        sa.Column("segment", sa.String(length=50), nullable=False),
        sa.Column("exchange", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_instruments_instrument_token", "instruments", ["instrument_token"], unique=False)
    op.create_index("ix_instruments_tradingsymbol", "instruments", ["tradingsymbol"], unique=False)

    op.create_table(
        "candles_5m",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("instrument_token", sa.Integer(), nullable=False),
        sa.Column("candle_time", sa.DateTime(), nullable=False),
        sa.Column("open", sa.Float(), nullable=False),
        sa.Column("high", sa.Float(), nullable=False),
        sa.Column("low", sa.Float(), nullable=False),
        sa.Column("close", sa.Float(), nullable=False),
        sa.Column("volume", sa.Integer(), nullable=False),
        sa.Column("oi", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["instrument_token"], ["instruments.instrument_token"]),
        sa.UniqueConstraint("instrument_token", "candle_time", name="uq_candles_5m_token_time"),
    )
    op.create_index("ix_candles_5m_id", "candles_5m", ["id"], unique=False)
    op.create_index("ix_candles_5m_instrument_token", "candles_5m", ["instrument_token"], unique=False)
    op.create_index("ix_candles_5m_candle_time", "candles_5m", ["candle_time"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_candles_5m_candle_time", table_name="candles_5m")
    op.drop_index("ix_candles_5m_instrument_token", table_name="candles_5m")
    op.drop_index("ix_candles_5m_id", table_name="candles_5m")
    op.drop_table("candles_5m")
    op.drop_index("ix_instruments_tradingsymbol", table_name="instruments")
    op.drop_index("ix_instruments_instrument_token", table_name="instruments")
    op.drop_table("instruments")
