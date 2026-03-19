"""
PostgreSQL database utilities for WashGo.

Connection is configured via the DATABASE_URL environment variable:
    DATABASE_URL=postgresql://user:password@host:5432/washgo

If DATABASE_URL is not set the module returns None from get_engine() and
all public helpers become no-ops, so the app gracefully falls back to the
in-memory sample data.
"""

import os
import pandas as pd
from datetime import datetime

try:
    from sqlalchemy import (
        create_engine, text, MetaData, Table, Column,
        String, Float, Integer, DateTime, Text, inspect,
    )
    from sqlalchemy.exc import SQLAlchemyError
    _SQLALCHEMY_AVAILABLE = True
except ImportError:
    _SQLALCHEMY_AVAILABLE = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


# ── Engine ─────────────────────────────────────────────────────────────────────

_engine = None


def get_engine():
    """Return a cached SQLAlchemy engine, or None if not configured."""
    global _engine
    if not _SQLALCHEMY_AVAILABLE:
        return None
    if _engine is not None:
        return _engine

    url = os.environ.get("DATABASE_URL", "")
    if not url:
        return None

    # Heroku / Railway use postgres:// but SQLAlchemy 2.x requires postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    try:
        _engine = create_engine(url, pool_pre_ping=True)
        return _engine
    except Exception:
        return None


# ── Schema ─────────────────────────────────────────────────────────────────────

ORDERS_DDL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id            VARCHAR(20)  PRIMARY KEY,
    customer_name       VARCHAR(100),
    phone               VARCHAR(20),
    area                VARCHAR(100),
    address             TEXT,
    service             VARCHAR(50),
    weight_kg           FLOAT,
    pieces              INTEGER,
    delivery_type       VARCHAR(50),
    time_slot           VARCHAR(50),
    status              VARCHAR(50),
    status_idx          INTEGER,
    partner_id          VARCHAR(20),
    partner_name        VARCHAR(100),
    facility            VARCHAR(100),
    amount              FLOAT,
    payment_method      VARCHAR(30),
    payment_status      VARCHAR(30),
    created_at          TIMESTAMP,
    rating              FLOAT,
    special_instructions TEXT
);
"""

PARTNERS_DDL = """
CREATE TABLE IF NOT EXISTS partners (
    id          VARCHAR(20)  PRIMARY KEY,
    name        VARCHAR(100),
    rating      FLOAT,
    deliveries  INTEGER,
    phone       VARCHAR(20),
    area        VARCHAR(100)
);
"""


def create_tables():
    """Create database tables if they don't exist. Returns True on success."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text(ORDERS_DDL))
            conn.execute(text(PARTNERS_DDL))
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


# ── Seed helpers ───────────────────────────────────────────────────────────────

def is_orders_empty() -> bool:
    """Return True if the orders table has zero rows."""
    engine = get_engine()
    if engine is None:
        return True
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM orders"))
            return result.scalar() == 0
    except SQLAlchemyError:
        return True


def seed_orders(df: pd.DataFrame) -> bool:
    """Insert sample orders into an empty orders table."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        df.to_sql("orders", engine, if_exists="append", index=False, method="multi")
        return True
    except SQLAlchemyError:
        return False


def seed_partners(partners: list) -> bool:
    """Insert partner records if the table is empty."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            count = conn.execute(text("SELECT COUNT(*) FROM partners")).scalar()
            if count > 0:
                return True
            for p in partners:
                conn.execute(
                    text(
                        "INSERT INTO partners (id, name, rating, deliveries, phone, area) "
                        "VALUES (:id, :name, :rating, :deliveries, :phone, :area) "
                        "ON CONFLICT (id) DO NOTHING"
                    ),
                    p,
                )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


# ── CRUD ───────────────────────────────────────────────────────────────────────

def load_orders() -> pd.DataFrame | None:
    """Load all orders from PostgreSQL. Returns None if DB not available."""
    engine = get_engine()
    if engine is None:
        return None
    try:
        df = pd.read_sql("SELECT * FROM orders ORDER BY created_at DESC", engine)
        return df
    except SQLAlchemyError:
        return None


def save_order(order: dict) -> bool:
    """Insert a new order row. Returns True on success."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        df = pd.DataFrame([order])
        df.to_sql("orders", engine, if_exists="append", index=False, method="multi")
        return True
    except SQLAlchemyError:
        return False


def update_order_status(order_id: str, status: str, status_idx: int) -> bool:
    """Update status and status_idx for a given order. Returns True on success."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(
                text(
                    "UPDATE orders SET status = :status, status_idx = :idx "
                    "WHERE order_id = :oid"
                ),
                {"status": status, "idx": status_idx, "oid": order_id},
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def save_rating(order_id: str, rating: float) -> bool:
    """Persist a customer rating for a delivered order. Returns True on success."""
    engine = get_engine()
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(
                text("UPDATE orders SET rating = :rating WHERE order_id = :oid"),
                {"rating": rating, "oid": order_id},
            )
            conn.commit()
        return True
    except SQLAlchemyError:
        return False


def is_available() -> bool:
    """Return True if the database connection is working."""
    return get_engine() is not None
