import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
from utils.store import get_store
from utils.data import SERVICES, AREAS, PARTNERS

st.set_page_config(page_title="Analytics – WashGo Admin", page_icon="📊", layout="wide")

ADMIN_DARK = "#0F172A"
CARD_BG    = "#1E293B"
BORDER     = "#334155"
GREEN      = "#10B981"
BLUE       = "#3B82F6"
AMBER      = "#F59E0B"
RED        = "#EF4444"
TEXT       = "#F1F5F9"
MUTED      = "#94A3B8"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0F172A; color: #F1F5F9; }
.stApp { background: #0F172A; }
[data-testid="stSidebar"] { background: #1E293B !important; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
h1,h2,h3,h4 { color: #F1F5F9 !important; }

.metric-card {
    background: #1E293B;
    border-radius: 14px;
    padding: 18px 20px;
    border: 1px solid #334155;
    text-align: center;
    margin-bottom: 12px;
}
.m-lbl { font-size: 0.75rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
.m-val { font-size: 1.5rem; font-weight: 800; color: #F1F5F9; margin-top: 4px; }
.m-val.green { color: #10B981; }
.m-val.blue  { color: #3B82F6; }
.m-val.amber { color: #F59E0B; }
</style>
""", unsafe_allow_html=True)

store = get_store()
if not st.session_state.admin_logged_in:
    st.warning("Please log in from the Admin home page.")
    st.stop()

with st.sidebar:
    st.markdown('<span style="font-size:1.3rem;font-weight:800;color:#3B82F6;">⚙️ WashGo Admin</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                       label="🖥️ Command Center")
    st.page_link("pages/1_🔴_Live_Orders.py",    label="🔴 Live Orders")
    st.page_link("pages/2_🚚_Partners.py",       label="🚚 Partners")
    st.page_link("pages/3_👥_Customers.py",      label="👥 Customers")
    st.page_link("pages/4_📊_Analytics.py",      label="📊 Analytics")
    st.page_link("pages/5_⚙️_Settings.py",      label="⚙️ Settings")

st.title("📊 Analytics Dashboard")

df = st.session_state.orders_df.copy()
df["date"] = df["created_at"].apply(lambda x: x.date() if hasattr(x, "date") else datetime.now().date())
df["hour"] = df["created_at"].apply(lambda x: x.hour if hasattr(x, "hour") else 0)

now = datetime.now().date()

# ── Key Metrics ───────────────────────────────────────────────────────────────
delivered = df[df["status"] == "Delivered"]
total_rev  = int(df["amount"].sum())
avg_order  = round(df["amount"].mean(), 0) if len(df) else 0
total_ord  = len(df)

cust_orders = df.groupby("phone")["order_id"].count()
repeat_custs = (cust_orders > 1).sum()
retention    = round(repeat_custs / len(cust_orders) * 100, 1) if len(cust_orders) else 0

cancelled = df[df["status"] == "Cancelled"]
cancel_rate = round(len(cancelled) / len(df) * 100, 1) if len(df) else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card"><div class="m-lbl">Total Revenue</div><div class="m-val green">₹' + str(total_rev) + '</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><div class="m-lbl">Total Orders</div><div class="m-val blue">' + str(total_ord) + '</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="m-lbl">Avg Order Value</div><div class="m-val amber">₹' + str(int(avg_order)) + '</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><div class="m-lbl">Customer Retention</div><div class="m-val green">' + str(retention) + '%</div></div>', unsafe_allow_html=True)

def dark_chart_layout(fig, height=320):
    fig.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT, family="Inter"),
        xaxis=dict(gridcolor=BORDER, tickfont=dict(color=MUTED)),
        yaxis=dict(gridcolor=BORDER, tickfont=dict(color=MUTED)),
        margin=dict(t=30, b=30, l=20, r=20),
        height=height,
        legend=dict(font=dict(color=TEXT)),
    )
    return fig

# ── Revenue Line Chart ─────────────────────────────────────────────────────────
st.subheader("💰 Daily Revenue (Last 30 Days)")
last_30 = now - timedelta(days=30)
rev_df = df[df["date"] >= last_30].groupby("date")["amount"].sum().reset_index()
rev_df.columns = ["date", "revenue"]
rev_df["date_str"] = rev_df["date"].apply(lambda d: d.strftime("%d %b"))

fig_rev = go.Figure()
fig_rev.add_trace(go.Scatter(
    x=rev_df["date_str"], y=rev_df["revenue"],
    mode="lines+markers",
    line=dict(color=GREEN, width=3),
    marker=dict(color=GREEN, size=6),
    fill="tozeroy",
    fillcolor="rgba(16,185,129,0.1)",
))
fig_rev = dark_chart_layout(fig_rev, 300)
fig_rev.update_layout(yaxis_tickprefix="₹")
st.plotly_chart(fig_rev, use_container_width=True)

# ── Orders by Day (stacked by service) ────────────────────────────────────────
st.subheader("📦 Orders by Day & Service")
ord_df = df[df["date"] >= last_30].copy()
ord_pivot = ord_df.groupby(["date", "service"]).size().reset_index(name="count")
ord_pivot["date_str"] = ord_pivot["date"].apply(lambda d: d.strftime("%d %b"))

service_colors = [GREEN, BLUE, AMBER, RED, "#8B5CF6", "#EC4899"]
fig_ord = go.Figure()
for i, svc in enumerate(list(SERVICES.keys())):
    svc_data = ord_pivot[ord_pivot["service"] == svc]
    if not svc_data.empty:
        fig_ord.add_trace(go.Bar(
            x=svc_data["date_str"], y=svc_data["count"],
            name=svc, marker_color=service_colors[i % len(service_colors)],
        ))
fig_ord.update_layout(barmode="stack")
fig_ord = dark_chart_layout(fig_ord, 320)
st.plotly_chart(fig_ord, use_container_width=True)

# ── Area Heatmap + Service Mix ─────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Orders by Area")
    area_count = df.groupby("area").size().reset_index(name="count").sort_values("count", ascending=True)
    max_count = area_count["count"].max()
    colors_area = [
        BLUE if c < max_count * 0.4 else (AMBER if c < max_count * 0.7 else GREEN)
        for c in area_count["count"]
    ]
    fig_area = go.Figure(go.Bar(
        y=area_count["area"], x=area_count["count"],
        orientation="h",
        marker_color=colors_area,
        text=area_count["count"],
        textposition="outside",
        textfont=dict(color=TEXT),
    ))
    fig_area = dark_chart_layout(fig_area, 380)
    st.plotly_chart(fig_area, use_container_width=True)

with col2:
    st.subheader("🥧 Revenue by Service")
    svc_rev = df.groupby("service")["amount"].sum().reset_index()
    fig_donut = go.Figure(go.Pie(
        labels=svc_rev["service"],
        values=svc_rev["amount"],
        hole=0.5,
        marker_colors=service_colors[:len(svc_rev)],
        textfont=dict(color=TEXT),
    ))
    fig_donut.update_layout(
        paper_bgcolor=CARD_BG,
        plot_bgcolor=CARD_BG,
        font=dict(color=TEXT, family="Inter"),
        margin=dict(t=30, b=30, l=20, r=20),
        height=380,
        legend=dict(font=dict(color=TEXT)),
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ── Partner Performance ────────────────────────────────────────────────────────
st.subheader("🚗 Partner Deliveries")
partner_del = df[df["status"] == "Delivered"].groupby("partner_name").size().reset_index(name="deliveries")
fig_part = go.Figure(go.Bar(
    y=partner_del["partner_name"], x=partner_del["deliveries"],
    orientation="h",
    marker_color=BLUE,
    text=partner_del["deliveries"],
    textposition="outside",
    textfont=dict(color=TEXT),
))
fig_part = dark_chart_layout(fig_part, 280)
st.plotly_chart(fig_part, use_container_width=True)

# ── Peak Hours ─────────────────────────────────────────────────────────────────
st.subheader("🕐 Peak Hours")
hour_count = df.groupby("hour").size().reset_index(name="orders")
all_hours  = pd.DataFrame({"hour": range(24)})
hour_count = all_hours.merge(hour_count, on="hour", how="left").fillna(0)
hour_count["label"] = hour_count["hour"].apply(lambda h: str(h) + ":00")

fig_hrs = go.Figure(go.Bar(
    x=hour_count["label"], y=hour_count["orders"],
    marker_color=[AMBER if h in range(7, 22) else MUTED for h in hour_count["hour"]],
    text=hour_count["orders"].astype(int),
    textposition="outside",
    textfont=dict(color=TEXT),
))
fig_hrs = dark_chart_layout(fig_hrs, 280)
st.plotly_chart(fig_hrs, use_container_width=True)

# ── Additional key metrics ─────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📈 Additional Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Cancellation Rate", str(cancel_rate) + "%")
    st.metric("Repeat Customer Rate", str(retention) + "%")
with col2:
    peak_hour = hour_count.loc[hour_count["orders"].idxmax(), "label"] if len(hour_count) else "N/A"
    st.metric("Peak Hour", str(peak_hour))
    st.metric("Avg Orders/Day", str(round(total_ord / 30, 1)))
with col3:
    top_area = df.groupby("area").size().idxmax() if len(df) else "N/A"
    st.metric("Top Area", str(top_area))
    top_svc  = df.groupby("service")["amount"].sum().idxmax() if len(df) else "N/A"
    st.metric("Top Revenue Service", str(top_svc))
