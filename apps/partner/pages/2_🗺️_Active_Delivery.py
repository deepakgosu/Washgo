import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from utils.store import get_store, update_order_status
from utils.data import SERVICES, STATUS_COLORS

st.set_page_config(page_title="Active Delivery – WashGo Partner", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0D1117; color: #E6EDF3; }
.stApp { background: #0D1117; }
[data-testid="stSidebar"] { background: #0D1117 !important; border-right: 1px solid #21262D; }
[data-testid="stSidebar"] * { color: #E6EDF3 !important; }
h1,h2,h3,h4 { color: #E6EDF3 !important; }

.order-card {
    background: #161B22;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #21262D;
    margin-bottom: 16px;
}
.cust-name { font-size: 1.2rem; font-weight: 700; color: #E6EDF3; }
.cust-detail { font-size: 0.85rem; color: #8B949E; margin-top: 4px; }

.status-panel {
    background: #0D1117;
    border-radius: 14px;
    padding: 20px 24px;
    border: 2px solid #00C853;
    text-align: center;
    margin-bottom: 16px;
}
.current-status-label { font-size: 0.82rem; color: #8B949E; margin-bottom: 6px; }
.current-status-val   { font-size: 1.5rem; font-weight: 800; color: #00C853; }

.map-container {
    background: #161B22;
    border-radius: 16px;
    padding: 28px 24px;
    border: 1px solid #21262D;
    text-align: center;
    margin: 16px 0;
    font-family: monospace;
    font-size: 1rem;
    color: #8B949E;
    letter-spacing: 2px;
}
.map-route { font-size: 0.95rem; color: #E6EDF3; letter-spacing: 3px; margin-top: 12px; }

.earning-preview {
    background: #161B22;
    border-radius: 12px;
    padding: 16px 20px;
    border: 1px solid #21262D;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
}
.earn-lbl { font-size: 0.88rem; color: #8B949E; }
.earn-val  { font-size: 1.2rem; font-weight: 800; color: #00C853; }

.instructions-box {
    background: #1C2333;
    border-radius: 10px;
    padding: 14px 18px;
    border-left: 4px solid #F59E0B;
    color: #E6EDF3;
    font-size: 0.88rem;
}
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
current_order_id = partner.get("current_order")

st.title("🗺️ Active Delivery")

if not current_order_id:
    st.markdown(
        '<div style="background:#161B22;border-radius:16px;padding:48px;text-align:center;border:1px dashed #30363D;margin-top:24px;">'
        '<div style="font-size:2rem;margin-bottom:12px;">🏁</div>'
        '<div style="font-size:1.1rem;font-weight:600;color:#8B949E;">No active delivery</div>'
        '<div style="font-size:0.88rem;color:#8B949E;margin-top:6px;">Go to My Jobs to accept an order.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("Go to My Jobs →", type="primary"):
        st.switch_page("pages/1_📋_My_Jobs.py")
    st.stop()

df = st.session_state.orders_df
order_rows = df[df["order_id"] == current_order_id]
if order_rows.empty:
    st.error("Order not found. It may have been completed.")
    st.session_state.partner_logged_in["current_order"] = None
    st.stop()

order = order_rows.iloc[0]
status = str(order.get("status", "Order Placed"))
svc_icon = SERVICES.get(str(order.get("service", "")), {}).get("icon", "🧺")
color = STATUS_COLORS.get(status, "#888")

# ── Order card ─────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="order-card">'
    '<div class="cust-name">👤 ' + str(order.get("customer_name", "")) + '</div>'
    '<div class="cust-detail">📍 ' + str(order.get("address", "")) + '</div>'
    '<div class="cust-detail">' + svc_icon + ' ' + str(order.get("service", "")) + ' · ' + str(order["order_id"]) + '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Status panel ──────────────────────────────────────────────────────────────
STATUS_NEXT = {
    "Order Placed":    ("Picked Up",       "🚗 Arrive at Customer"),
    "Picked Up":       ("At Facility",     "🏭 Drop at Facility"),
    "At Facility":     ("Out for Delivery","📦 Pick from Facility"),
    "Out for Delivery": ("Delivered",      "✅ Mark Delivered"),
}

st.markdown(
    '<div class="status-panel">'
    '<div class="current-status-label">Current Status</div>'
    '<div class="current-status-val">' + status + '</div>'
    '</div>',
    unsafe_allow_html=True
)

if status in STATUS_NEXT:
    next_status, btn_label = STATUS_NEXT[status]
    if st.button(btn_label, use_container_width=True, type="primary"):
        update_order_status(current_order_id, next_status)
        if next_status == "Delivered":
            earn = int(order.get("amount", 0) * 0.25)
            for p in st.session_state.partners:
                if p["id"] == partner["id"]:
                    p["today_earnings"] = p.get("today_earnings", 0) + earn
                    p["current_order"] = None
            st.session_state.partner_logged_in["today_earnings"] = st.session_state.partner_logged_in.get("today_earnings", 0) + earn
            st.session_state.partner_logged_in["current_order"] = None
            st.success("Order delivered! Great job.")
        else:
            st.success("Status updated to: " + next_status)
        st.rerun()
else:
    st.success("This order is complete!")

# ── Simulated map ─────────────────────────────────────────────────────────────
area = str(order.get("area", "Customer"))
facility = str(order.get("facility", "Facility"))

st.markdown(
    '<div class="map-container">'
    '<div style="font-size:0.78rem;color:#8B949E;margin-bottom:8px;">ROUTE</div>'
    '<div class="map-route">📍 ' + area + '  ————  🚗 You  ————  🏭 ' + facility + '</div>'
    '<div style="margin-top:12px;font-size:0.78rem;color:#8B949E;">Simulated route · Live maps coming soon</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Customer contact ──────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    with st.expander("📞 Customer Contact"):
        st.write("**" + str(order.get("customer_name", "")) + "**")
        st.write("Phone: " + str(order.get("phone", "")))
with col2:
    instructions = str(order.get("special_instructions", ""))
    if instructions and instructions not in ("", "nan"):
        with st.expander("📌 Special Instructions", expanded=True):
            st.markdown(
                '<div class="instructions-box">⚠️ ' + instructions + '</div>',
                unsafe_allow_html=True
            )

# ── Earnings preview ──────────────────────────────────────────────────────────
base_earn = int(order.get("amount", 0) * 0.22)
dist_earn = int(order.get("amount", 0) * 0.03)
total_earn = base_earn + dist_earn

st.markdown(
    '<div class="earning-preview">'
    '<div>'
    '<div class="earn-lbl">Base Earning</div>'
    '<div style="font-size:0.95rem;color:#E6EDF3;">₹' + str(base_earn) + '</div>'
    '</div>'
    '<div>'
    '<div class="earn-lbl">Distance Bonus</div>'
    '<div style="font-size:0.95rem;color:#E6EDF3;">₹' + str(dist_earn) + '</div>'
    '</div>'
    '<div>'
    '<div class="earn-lbl">Total Earnings</div>'
    '<div class="earn-val">₹' + str(total_earn) + '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)
