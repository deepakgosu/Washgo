"""
utils/store.py
Shared in-memory state for all three WashGo apps via Streamlit session state.
"""

import streamlit as st
import pandas as pd
import random
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.data import (
    AREAS, SERVICES, STATUSES, STATUS_COLORS, PARTNERS,
    FACILITIES, TIME_SLOTS, CUSTOMERS, DELIVERY_FEE,
    generate_sample_orders,
)


def get_store():
    """Initialize and return the full app state dict from session state."""

    # ── Orders ──────────────────────────────────────────────────────────────
    if "orders_df" not in st.session_state:
        st.session_state.orders_df = generate_sample_orders(60)

    # ── Partners (enriched) ──────────────────────────────────────────────────
    if "partners" not in st.session_state:
        enriched = []
        for p in PARTNERS:
            ep = dict(p)
            ep["online"] = random.choice([True, True, False])
            ep["current_order"] = None
            ep["today_earnings"] = round(random.uniform(200, 1200), 2)
            ep["today_trips"] = random.randint(2, 12)
            ep["online_hours"] = round(random.uniform(1.0, 9.0), 1)
            ep["vehicle_number"] = random.choice([
                "TS-09-AB-1234", "TS-05-HX-5678", "TS-11-CD-9012",
                "AP-28-EF-3456", "TS-07-GH-7890",
            ])
            enriched.append(ep)
        st.session_state.partners = enriched

    # ── Customer profile ─────────────────────────────────────────────────────
    if "customer" not in st.session_state:
        st.session_state.customer = {
            "name": "",
            "phone": "",
            "email": "",
            "area": AREAS[0],
            "subscription": None,
            "addresses": [],
            "member_since": datetime.now() - timedelta(days=random.randint(30, 365)),
        }

    # ── Auth flags ───────────────────────────────────────────────────────────
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if "partner_logged_in" not in st.session_state:
        st.session_state.partner_logged_in = None

    if "customer_logged_in" not in st.session_state:
        st.session_state.customer_logged_in = False

    # ── Booking wizard ───────────────────────────────────────────────────────
    if "booking_step" not in st.session_state:
        st.session_state.booking_step = 1
    if "booking_data" not in st.session_state:
        st.session_state.booking_data = {}
    if "last_order_id" not in st.session_state:
        st.session_state.last_order_id = None

    return {
        "orders_df": st.session_state.orders_df,
        "partners": st.session_state.partners,
        "customer": st.session_state.customer,
        "admin_logged_in": st.session_state.admin_logged_in,
        "partner_logged_in": st.session_state.partner_logged_in,
        "customer_logged_in": st.session_state.customer_logged_in,
    }


def add_order(order_dict):
    """Append a new order dict to orders_df in session state."""
    get_store()
    new_row = pd.DataFrame([order_dict])
    st.session_state.orders_df = pd.concat(
        [st.session_state.orders_df, new_row], ignore_index=True
    )


def update_order_status(order_id, new_status):
    """Update the status of an order by order_id."""
    get_store()
    df = st.session_state.orders_df
    mask = df["order_id"] == order_id
    if mask.any():
        idx = STATUSES.index(new_status) if new_status in STATUSES else 0
        df.loc[mask, "status"] = new_status
        df.loc[mask, "status_idx"] = idx
        st.session_state.orders_df = df


def get_customer_orders(phone):
    """Return orders DataFrame filtered by customer phone number."""
    get_store()
    df = st.session_state.orders_df
    return df[df["phone"] == phone].copy()
