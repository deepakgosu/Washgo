import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from utils.store import get_store
from utils.data import SERVICES

st.set_page_config(page_title="Earnings – WashGo Partner", page_icon="💰", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0D1117; color: #E6EDF3; }
.stApp { background: #0D1117; }
[data-testid="stSidebar"] { background: #0D1117 !important; border-right: 1px solid #21262D; }
[data-testid="stSidebar"] * { color: #E6EDF3 !important; }
h1,h2,h3,h4 { color: #E6EDF3 !important; }
[data-testid="stMetricValue"] { color: #00C853 !important; }

.earn-card {
    background: #161B22;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #21262D;
    margin-bottom: 16px;
}
.earn-title { font-size: 0.82rem; color: #8B949E; margin-bottom: 4px; }
.earn-val   { font-size: 2rem; font-weight: 800; color: #00C853; }
.earn-sub   { font-size: 0.8rem; color: #8B949E; margin-top: 4px; }

.trip-row {
    display: flex; justify-content: space-between; align-items: center;
    background: #161B22;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    border: 1px solid #21262D;
}
.trip-id   { font-size: 0.82rem; font-weight: 600; color: #E6EDF3; }
.trip-meta { font-size: 0.75rem; color: #8B949E; }
.trip-amt  { font-size: 0.95rem; font-weight: 700; color: #00C853; }
</style>
""", unsafe_allow_html=True)

store = get_store()

if not st.session_state.partner_logged_in:
    st.warning("Please log in from the Partner Dashboard.")
    st.stop()

with st.sidebar:
    st.markdown('<span style="font-size:1.4rem;font-weight:800;color:#00C853;">🚗 WashGo Partner</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                          label="🏠 Dashboard")
    st.page_link("pages/1_📋_My_Jobs.py",           label="📋 My Jobs")
    st.page_link("pages/2_🗺️_Active_Delivery.py",  label="🗺️ Active Delivery")
    st.page_link("pages/3_💰_Earnings.py",          label="💰 Earnings")

partner = st.session_state.partner_logged_in
df = st.session_state.orders_df
my_completed = df[
    (df["partner_id"] == partner["id"]) &
    (df["status"] == "Delivered")
].copy()

my_completed["partner_earn"] = (my_completed["amount"] * 0.25).round(0).astype(int)
my_completed["date"] = my_completed["created_at"].apply(lambda x: x.date() if hasattr(x, "date") else datetime.now().date())

st.title("💰 Earnings")

# ── Period selector ───────────────────────────────────────────────────────────
period = st.radio("Period", ["Today", "This Week", "This Month", "All Time"], horizontal=True)

now = datetime.now().date()
if period == "Today":
    mask = my_completed["date"] == now
elif period == "This Week":
    week_start = now - timedelta(days=now.weekday())
    mask = my_completed["date"] >= week_start
elif period == "This Month":
    mask = (my_completed["date"].apply(lambda d: d.month) == now.month) & \
           (my_completed["date"].apply(lambda d: d.year) == now.year)
else:
    mask = pd.Series([True] * len(my_completed), index=my_completed.index)

subset = my_completed[mask]

total_earned = subset["partner_earn"].sum()
trips_done   = len(subset)
avg_per_trip = round(total_earned / trips_done, 0) if trips_done > 0 else 0
online_hrs   = partner.get("online_hours", 0)

# ── Summary cards ─────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        '<div class="earn-card"><div class="earn-title">TOTAL EARNED</div><div class="earn-val">₹' + str(int(total_earned)) + '</div></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        '<div class="earn-card"><div class="earn-title">TRIPS</div><div class="earn-val">' + str(trips_done) + '</div></div>',
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        '<div class="earn-card"><div class="earn-title">AVG PER TRIP</div><div class="earn-val">₹' + str(int(avg_per_trip)) + '</div></div>',
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        '<div class="earn-card"><div class="earn-title">ONLINE HOURS</div><div class="earn-val">' + str(online_hrs) + 'h</div></div>',
        unsafe_allow_html=True
    )

# ── Earnings chart ─────────────────────────────────────────────────────────────
st.subheader("📊 Daily Earnings")

if not subset.empty:
    daily = subset.groupby("date")["partner_earn"].sum().reset_index()
    daily.columns = ["date", "earnings"]
    daily["date_str"] = daily["date"].apply(lambda d: d.strftime("%d %b"))

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=daily["date_str"],
        y=daily["earnings"],
        marker_color="#00C853",
        text=["₹" + str(int(v)) for v in daily["earnings"]],
        textposition="outside",
        textfont=dict(color="#E6EDF3", size=11),
    ))
    fig.update_layout(
        paper_bgcolor="#161B22",
        plot_bgcolor="#161B22",
        font=dict(color="#E6EDF3", family="Inter"),
        xaxis=dict(gridcolor="#21262D", tickfont=dict(color="#8B949E")),
        yaxis=dict(gridcolor="#21262D", tickfont=dict(color="#8B949E"), tickprefix="₹"),
        margin=dict(t=20, b=20, l=20, r=20),
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No earnings data for this period.")

# ── Trips list ────────────────────────────────────────────────────────────────
st.subheader("🕐 Trips")
if subset.empty:
    st.info("No trips in this period.")
else:
    for _, row in subset.sort_values("created_at", ascending=False).iterrows():
        svc_icon = SERVICES.get(str(row.get("service", "")), {}).get("icon", "🧺")
        created_str = row["created_at"].strftime("%d %b, %I:%M %p") if hasattr(row.get("created_at"), "strftime") else ""
        st.markdown(
            '<div class="trip-row">'
            '<div>'
            '<div class="trip-id">' + svc_icon + ' ' + str(row["order_id"]) + '</div>'
            '<div class="trip-meta">📍 ' + str(row.get("area", "")) + ' · ' + str(row.get("service", "")) + '</div>'
            '<div class="trip-meta">' + created_str + '</div>'
            '</div>'
            '<div class="trip-amt">₹' + str(int(row["partner_earn"])) + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

# ── Payment info ──────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🏦 Payment Info")
col1, col2 = st.columns(2)
with col1:
    st.info("Next payout: **" + (now + timedelta(days=(7 - now.weekday()))).strftime("%d %b %Y") + "** (Weekly)")
with col2:
    st.info("Bank Account: ••••" + str(abs(hash(partner["id"])) % 9000 + 1000))
