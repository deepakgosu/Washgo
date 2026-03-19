import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from utils.store import get_store
from utils.data import SERVICES, AREAS, DELIVERY_FEE, TIME_SLOTS

st.set_page_config(page_title="Settings – WashGo Admin", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0F172A; color: #F1F5F9; }
.stApp { background: #0F172A; }
[data-testid="stSidebar"] { background: #1E293B !important; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
h1,h2,h3,h4 { color: #F1F5F9 !important; }
.stTextInput input, .stSelectbox select, .stNumberInput input, .stTextArea textarea {
    background: #1E293B !important; color: #F1F5F9 !important; border: 1px solid #334155 !important;
}
.section-card {
    background: #1E293B;
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 20px;
    border: 1px solid #334155;
}
.section-title { font-size: 1rem; font-weight: 700; color: #F1F5F9; margin-bottom: 14px; }
.danger-zone { border-color: #EF4444 !important; }
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

st.title("⚙️ Settings")

# ── Init settings state ────────────────────────────────────────────────────────
if "settings" not in st.session_state:
    st.session_state.settings = {
        "pricing": {k: {"price": v["price"], "unit": v["unit"]} for k, v in SERVICES.items()},
        "delivery_fee": DELIVERY_FEE,
        "active_areas": {a: True for a in AREAS},
        "operating_start": "7:00 AM",
        "operating_end": "10:00 PM",
        "plans": {
            "plus":    {"name": "WashGo Plus",    "price": 999,  "benefits": "10% off orders\nFree delivery ₹300+\nPriority support"},
            "premium": {"name": "WashGo Premium", "price": 1799, "benefits": "20% off orders\nFree delivery always\nExpress processing\nDedicated support"},
        },
        "sms_templates": {
            "confirmed": "Hi {name}! Your WashGo order {order_id} is confirmed. Pickup scheduled for {slot}.",
            "picked_up": "Hi {name}! Your laundry has been picked up. Order ID: {order_id}.",
            "delivered": "Hi {name}! Your laundry has been delivered. Hope you love it! Order: {order_id}.",
        },
    }

settings = st.session_state.settings

# ── Pricing Config ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">💰 Service Pricing</div>', unsafe_allow_html=True)
pricing_changed = {}
for svc_name, svc_cfg in SERVICES.items():
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        svc_icon = svc_cfg.get("icon", "🧺")
        st.markdown("**" + svc_icon + " " + svc_name + "**")
    with col2:
        new_price = st.number_input(
            "Price (₹)", value=settings["pricing"].get(svc_name, {}).get("price", svc_cfg["price"]),
            step=5, key="price_" + svc_name, min_value=0
        )
        pricing_changed[svc_name] = new_price
    with col3:
        st.text_input("Unit", value=svc_cfg["unit"], disabled=True, key="unit_" + svc_name)

if st.button("💾 Save Pricing", type="primary"):
    for svc_name, price in pricing_changed.items():
        settings["pricing"][svc_name]["price"] = price
    st.success("Pricing saved!")
st.markdown('</div>', unsafe_allow_html=True)

# ── Area Management ────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📍 Area Management</div>', unsafe_allow_html=True)
st.markdown("Toggle areas to enable or disable service in those zones.")
area_cols = st.columns(4)
for i, area in enumerate(AREAS):
    with area_cols[i % 4]:
        enabled = st.toggle(area, value=settings["active_areas"].get(area, True), key="area_" + area)
        settings["active_areas"][area] = enabled
st.markdown('</div>', unsafe_allow_html=True)

# ── Delivery Fee ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">🚗 Delivery Fee</div>', unsafe_allow_html=True)
new_fee = st.number_input("Delivery Fee (₹)", value=settings["delivery_fee"], step=5, min_value=0)
if st.button("Save Delivery Fee"):
    settings["delivery_fee"] = new_fee
    st.success("Delivery fee updated to ₹" + str(new_fee))
st.markdown('</div>', unsafe_allow_html=True)

# ── Operating Hours ────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">🕐 Operating Hours</div>', unsafe_allow_html=True)
hour_options = ["6:00 AM", "7:00 AM", "8:00 AM", "9:00 AM", "10:00 AM", "9:00 PM", "10:00 PM", "11:00 PM"]
col1, col2 = st.columns(2)
with col1:
    op_start = st.selectbox("Start Time", hour_options, index=hour_options.index(settings.get("operating_start", "7:00 AM")) if settings.get("operating_start") in hour_options else 1)
with col2:
    op_end = st.selectbox("End Time", hour_options, index=hour_options.index(settings.get("operating_end", "10:00 PM")) if settings.get("operating_end") in hour_options else 6)
if st.button("Save Hours"):
    settings["operating_start"] = op_start
    settings["operating_end"]   = op_end
    st.success("Operating hours updated: " + op_start + " – " + op_end)
st.markdown('</div>', unsafe_allow_html=True)

# ── Subscription Plans ─────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">💎 Subscription Plans</div>', unsafe_allow_html=True)
for plan_id, plan_cfg in settings["plans"].items():
    st.markdown("**" + plan_cfg["name"] + "**")
    col1, col2 = st.columns([1, 3])
    with col1:
        new_plan_price = st.number_input("Price ₹/mo", value=plan_cfg["price"], step=50, key="plan_price_" + plan_id)
        plan_cfg["price"] = new_plan_price
    with col2:
        new_benefits = st.text_area("Benefits (one per line)", value=plan_cfg["benefits"], key="plan_ben_" + plan_id, height=80)
        plan_cfg["benefits"] = new_benefits
    st.markdown("---")
if st.button("💾 Save Plans"):
    st.success("Plan settings saved!")
st.markdown('</div>', unsafe_allow_html=True)

# ── SMS Templates ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📱 SMS Notification Templates</div>', unsafe_allow_html=True)
st.caption("Variables: {name}, {order_id}, {slot}")
for tmpl_key, tmpl_label in [("confirmed", "Order Confirmed"), ("picked_up", "Picked Up"), ("delivered", "Delivered")]:
    new_tmpl = st.text_area(tmpl_label, value=settings["sms_templates"][tmpl_key], key="tmpl_" + tmpl_key)
    settings["sms_templates"][tmpl_key] = new_tmpl
if st.button("💾 Save Templates"):
    st.success("SMS templates saved!")
st.markdown('</div>', unsafe_allow_html=True)

# ── System / Danger Zone ──────────────────────────────────────────────────────
st.markdown('<div class="section-card danger-zone">', unsafe_allow_html=True)
st.markdown("**⚠️ System Actions**")
col1, col2 = st.columns(2)

with col1:
    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear = False
    if not st.session_state.confirm_clear:
        if st.button("🗑️ Clear All Orders", type="secondary", use_container_width=True):
            st.session_state.confirm_clear = True
            st.rerun()
    else:
        st.error("Are you sure? This will delete ALL order data.")
        cc1, cc2 = st.columns(2)
        with cc1:
            if st.button("Yes, Clear", type="primary", use_container_width=True):
                import pandas as pd
                st.session_state.orders_df = pd.DataFrame(columns=st.session_state.orders_df.columns)
                st.session_state.confirm_clear = False
                st.success("All orders cleared.")
                st.rerun()
        with cc2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()

with col2:
    if st.button("🔄 Generate Test Orders (10)", use_container_width=True):
        from utils.data import generate_sample_orders
        import pandas as pd
        new_orders = generate_sample_orders(10)
        import random
        new_orders["order_id"] = ["WG" + str(random.randint(80000, 99999)) for _ in range(10)]
        st.session_state.orders_df = pd.concat([st.session_state.orders_df, new_orders], ignore_index=True)
        st.success("10 test orders generated!")
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── App info ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("WashGo Admin v1.0 · Built with Streamlit · © 2024 WashGo Technologies")
