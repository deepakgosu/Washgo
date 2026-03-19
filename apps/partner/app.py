import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from utils.store import get_store
from utils.data import PARTNERS

st.set_page_config(
    page_title="WashGo Partner",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #0D1117;
    color: #E6EDF3;
}
.stApp { background: #0D1117; }
[data-testid="stSidebar"] { background: #0D1117 !important; border-right: 1px solid #21262D; }
[data-testid="stSidebar"] * { color: #E6EDF3 !important; }
[data-testid="stSidebar"] .stButton button { background: #161B22; color: #E6EDF3; border: 1px solid #30363D; }

h1, h2, h3, h4, h5 { color: #E6EDF3 !important; }
p, span, label, div { color: #E6EDF3; }
.stTextInput input, .stSelectbox select {
    background: #161B22 !important; color: #E6EDF3 !important;
    border: 1px solid #30363D !important;
}
.stButton button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

.login-wrap {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 80vh;
}
.login-card {
    background: #161B22;
    border-radius: 20px;
    padding: 48px 40px;
    max-width: 440px;
    width: 100%;
    border: 1px solid #30363D;
    text-align: center;
}
.login-logo { font-size: 2rem; font-weight: 800; color: #00C853; margin-bottom: 8px; }
.login-sub  { color: #8B949E; font-size: 0.9rem; margin-bottom: 28px; }

.online-toggle-on {
    background: linear-gradient(135deg, #00C853, #00A846);
    color: #fff;
    border-radius: 16px;
    padding: 18px 24px;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 0 24px rgba(0,200,83,0.3);
    margin-bottom: 20px;
}
.online-toggle-off {
    background: #21262D;
    color: #8B949E;
    border-radius: 16px;
    padding: 18px 24px;
    text-align: center;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 20px;
}

.stat-card {
    background: #161B22;
    border-radius: 14px;
    padding: 18px;
    border: 1px solid #21262D;
    text-align: center;
}
.stat-val { font-size: 1.6rem; font-weight: 800; color: #E6EDF3; }
.stat-lbl { font-size: 0.78rem; color: #8B949E; margin-top: 2px; }
.stat-green { color: #00C853 !important; }

.job-card {
    background: #161B22;
    border-radius: 16px;
    padding: 20px 24px;
    border: 2px solid #F59E0B;
    margin-top: 16px;
}
.job-customer { font-size: 1rem; font-weight: 700; color: #E6EDF3; }
.job-detail   { font-size: 0.85rem; color: #8B949E; margin-top: 4px; }
.job-earning  { font-size: 1.2rem; font-weight: 800; color: #00C853; margin-top: 8px; }

.trip-row {
    display: flex; justify-content: space-between; align-items: center;
    background: #161B22;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    border: 1px solid #21262D;
}
.trip-id   { font-size: 0.82rem; font-weight: 600; color: #E6EDF3; }
.trip-meta { font-size: 0.78rem; color: #8B949E; }
.trip-amt  { font-size: 0.95rem; font-weight: 700; color: #00C853; }

.washgo-logo { font-size: 1.4rem; font-weight: 800; color: #00C853; }
</style>
""", unsafe_allow_html=True)

store = get_store()

# ── Login gate ────────────────────────────────────────────────────────────────
def show_login():
    st.markdown(
        '<div style="display:flex;flex-direction:column;align-items:center;margin-top:80px;">'
        '<div class="login-card">'
        '<div class="login-logo">🚗 WashGo Partner</div>'
        '<div class="login-sub">Log in to start accepting deliveries</div>',
        unsafe_allow_html=True
    )
    partner_id = st.text_input("Partner ID", placeholder="e.g. P001")
    partner_nm = st.text_input("Your Name",  placeholder="e.g. Ravi Kumar")
    if st.button("Go Online 🟢", use_container_width=True, type="primary"):
        matched = next(
            (p for p in PARTNERS if p["id"] == partner_id.strip() and p["name"].lower() == partner_nm.strip().lower()),
            None
        )
        if matched:
            enriched = next((p for p in st.session_state.partners if p["id"] == matched["id"]), None)
            if enriched:
                st.session_state.partner_logged_in = enriched
            else:
                ep = dict(matched)
                ep.update({"online": True, "current_order": None, "today_earnings": 0.0, "today_trips": 0, "online_hours": 0.0, "vehicle_number": "TS-09-AB-0000"})
                st.session_state.partner_logged_in = ep
            st.rerun()
        else:
            st.error("Partner ID and Name don't match. Check your credentials.")
    st.markdown('</div></div>', unsafe_allow_html=True)

if not st.session_state.partner_logged_in:
    show_login()
    st.stop()

partner = st.session_state.partner_logged_in

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="washgo-logo">🚗 WashGo Partner</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**" + partner["name"] + "**")
    st.caption(partner.get("area", ""))
    st.markdown("---")
    st.page_link("app.py",                          label="🏠 Dashboard")
    st.page_link("pages/1_📋_My_Jobs.py",           label="📋 My Jobs")
    st.page_link("pages/2_🗺️_Active_Delivery.py",  label="🗺️ Active Delivery")
    st.page_link("pages/3_💰_Earnings.py",          label="💰 Earnings")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.partner_logged_in = None
        st.rerun()

# ── Online / Offline toggle ───────────────────────────────────────────────────
is_online = partner.get("online", False)
if is_online:
    st.markdown('<div class="online-toggle-on">🟢 You\'re Online — Accepting Orders</div>', unsafe_allow_html=True)
    if st.button("Go Offline", use_container_width=True):
        for p in st.session_state.partners:
            if p["id"] == partner["id"]:
                p["online"] = False
        st.session_state.partner_logged_in["online"] = False
        st.rerun()
else:
    st.markdown('<div class="online-toggle-off">⚫ You\'re Offline</div>', unsafe_allow_html=True)
    if st.button("Go Online 🟢", use_container_width=True, type="primary"):
        for p in st.session_state.partners:
            if p["id"] == partner["id"]:
                p["online"] = True
        st.session_state.partner_logged_in["online"] = True
        st.rerun()

st.markdown("---")

# ── Today stats ───────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(
        '<div class="stat-card"><div class="stat-val stat-green">₹' + str(int(partner.get("today_earnings", 0))) + '</div><div class="stat-lbl">Earnings Today</div></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        '<div class="stat-card"><div class="stat-val">' + str(partner.get("today_trips", 0)) + '</div><div class="stat-lbl">Trips Today</div></div>',
        unsafe_allow_html=True
    )
with col3:
    st.markdown(
        '<div class="stat-card"><div class="stat-val">' + str(partner.get("rating", 4.5)) + ' ⭐</div><div class="stat-lbl">Rating</div></div>',
        unsafe_allow_html=True
    )
with col4:
    st.markdown(
        '<div class="stat-card"><div class="stat-val">' + str(partner.get("online_hours", 0)) + 'h</div><div class="stat-lbl">Online Hours</div></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Next Job ──────────────────────────────────────────────────────────────────
df = st.session_state.orders_df
pending = df[
    (df["partner_id"] == partner["id"]) &
    (df["status"] == "Order Placed")
]

if is_online and not pending.empty:
    next_job = pending.iloc[0]
    svc = next_job.get("service", "Regular Wash")
    est_earn = int(next_job.get("amount", 0) * 0.25)

    st.subheader("📥 Next Job")
    st.markdown(
        '<div class="job-card">'
        '<div class="job-customer">👤 ' + str(next_job.get("customer_name", "")) + '</div>'
        '<div class="job-detail">📍 ' + str(next_job.get("area", "")) + ' · ' + svc + '</div>'
        '<div class="job-detail">🏠 ' + str(next_job.get("address", ""))[:60] + '</div>'
        '<div class="job-earning">₹' + str(est_earn) + ' estimated earnings</div>'
        '</div>',
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Accept", use_container_width=True, type="primary"):
            from utils.store import update_order_status
            update_order_status(next_job["order_id"], "Picked Up")
            for p in st.session_state.partners:
                if p["id"] == partner["id"]:
                    p["current_order"] = next_job["order_id"]
                    p["today_trips"] += 1
            st.session_state.partner_logged_in["current_order"] = next_job["order_id"]
            st.success("Job accepted! Navigate to Active Delivery.")
            st.rerun()
    with col2:
        if st.button("✗ Decline", use_container_width=True):
            st.info("Job declined.")
elif is_online:
    st.subheader("📥 Next Job")
    with st.spinner("Waiting for orders..."):
        st.markdown(
            '<div style="background:#161B22;border-radius:14px;padding:28px;text-align:center;color:#8B949E;border:1px dashed #30363D;">'
            '🔍 Looking for nearby orders...'
            '</div>',
            unsafe_allow_html=True
        )

# ── Recent trips ──────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🕐 Recent Trips")
completed = df[
    (df["partner_id"] == partner["id"]) &
    (df["status"] == "Delivered")
].sort_values("created_at", ascending=False).head(5)

if completed.empty:
    st.info("No completed trips yet.")
else:
    for _, row in completed.iterrows():
        earned = int(row.get("amount", 0) * 0.25)
        created_str = row["created_at"].strftime("%d %b, %I:%M %p") if hasattr(row.get("created_at"), "strftime") else ""
        st.markdown(
            '<div class="trip-row">'
            '<div>'
            '<div class="trip-id">' + str(row["order_id"]) + '</div>'
            '<div class="trip-meta">' + str(row.get("area", "")) + ' · ' + str(row.get("service", "")) + '</div>'
            '<div class="trip-meta">' + created_str + '</div>'
            '</div>'
            '<div class="trip-amt">₹' + str(earned) + '</div>'
            '</div>',
            unsafe_allow_html=True
        )
