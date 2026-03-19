import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime
from utils.store import get_store
from utils.data import SERVICES, AREAS

st.set_page_config(
    page_title="WashGo – Customer",
    page_icon="🧺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F5F5F5; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E0E0E0;
}
[data-testid="stSidebar"] * { color: #1A1A1A !important; }

/* Hide default header */
header[data-testid="stHeader"] { background: transparent; }

.washgo-logo {
    font-size: 1.6rem;
    font-weight: 800;
    color: #00C853;
    letter-spacing: -0.5px;
}

.greeting-bar {
    background: #1A1A1A;
    color: #FFFFFF;
    padding: 20px 28px;
    border-radius: 16px;
    margin-bottom: 24px;
}
.greeting-name { font-size: 1.5rem; font-weight: 700; }
.greeting-sub  { font-size: 0.9rem; color: #AAAAAA; margin-top: 4px; }

.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1A1A1A;
    margin: 24px 0 12px;
}

.service-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 16px;
    text-align: center;
    border: 2px solid #F0F0F0;
    cursor: pointer;
    transition: all 0.2s;
    min-height: 130px;
}
.service-card:hover { border-color: #00C853; box-shadow: 0 4px 16px rgba(0,200,83,0.12); }
.service-icon { font-size: 2.2rem; }
.service-name { font-size: 0.85rem; font-weight: 600; color: #1A1A1A; margin-top: 8px; }
.service-price { font-size: 0.8rem; color: #00C853; font-weight: 600; margin-top: 2px; }

.active-banner {
    background: linear-gradient(135deg, #00C853, #00A846);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.active-banner-left h3 { margin: 0; font-size: 1rem; font-weight: 700; }
.active-banner-left p  { margin: 4px 0 0; font-size: 0.85rem; opacity: 0.9; }

.order-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border: 1px solid #F0F0F0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.order-id   { font-size: 0.85rem; font-weight: 700; color: #1A1A1A; }
.order-meta { font-size: 0.78rem; color: #888; margin-top: 2px; }
.order-amt  { font-size: 1rem; font-weight: 700; color: #1A1A1A; }

.status-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 4px;
}

.upsell-card {
    background: linear-gradient(135deg, #FF6D00, #FF8F00);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 22px 24px;
    margin-top: 24px;
}
.upsell-card h3 { margin: 0 0 6px; font-size: 1.1rem; }
.upsell-card p  { margin: 0; font-size: 0.88rem; opacity: 0.9; }

.login-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 40px;
    max-width: 420px;
    margin: 80px auto;
    box-shadow: 0 8px 40px rgba(0,0,0,0.08);
}
.login-logo { font-size: 2rem; font-weight: 800; color: #00C853; text-align: center; margin-bottom: 8px; }
.login-sub  { text-align: center; color: #888; margin-bottom: 28px; font-size: 0.9rem; }

div[data-testid="stButton"] button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    transition: all 0.2s !important;
}
</style>
""", unsafe_allow_html=True)

# ── Store & Auth ─────────────────────────────────────────────────────────────
store = get_store()

def show_login():
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">🧺 WashGo</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Enter your details to continue</div>', unsafe_allow_html=True)
    name  = st.text_input("Your Name", placeholder="e.g. Priya Reddy")
    phone = st.text_input("Phone Number", placeholder="10-digit mobile number")
    if st.button("Continue →", use_container_width=True, type="primary"):
        if name.strip() and len(phone.strip()) == 10 and phone.strip().isdigit():
            st.session_state.customer["name"]  = name.strip()
            st.session_state.customer["phone"] = phone.strip()
            st.session_state.customer_logged_in = True
            st.rerun()
        else:
            st.error("Please enter a valid name and 10-digit phone number.")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.customer_logged_in:
    show_login()
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="washgo-logo">🧺 WashGo</div>', unsafe_allow_html=True)
    st.markdown("---")
    cust = st.session_state.customer
    st.markdown("**" + cust["name"] + "**")
    st.caption(cust["phone"])
    st.markdown("---")
    st.page_link("app.py",                       label="🏠 Home")
    st.page_link("pages/1_📦_Book_Order.py",     label="📦 Book Order")
    st.page_link("pages/2_📍_Track_Order.py",    label="📍 Track Order")
    st.page_link("pages/3_📋_My_Orders.py",      label="📋 My Orders")
    st.page_link("pages/4_💳_Subscription.py",   label="💳 Subscription")
    st.page_link("pages/5_👤_Profile.py",        label="👤 Profile")
    st.markdown("---")
    if st.button("📦 Schedule Pickup", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📦_Book_Order.py")
    if st.button("Logout", use_container_width=True):
        st.session_state.customer_logged_in = False
        st.session_state.customer = {
            "name": "", "phone": "", "email": "", "area": AREAS[0],
            "subscription": None, "addresses": [],
            "member_since": st.session_state.customer.get("member_since"),
        }
        st.rerun()

# ── Main content ──────────────────────────────────────────────────────────────
hour = datetime.now().hour
greeting = "Good morning" if hour < 12 else ("Good afternoon" if hour < 17 else "Good evening")

cust = st.session_state.customer
st.markdown(
    '<div class="greeting-bar">'
    '<div class="greeting-name">' + greeting + ', ' + cust["name"] + ' 👋</div>'
    '<div class="greeting-sub">What can we wash for you today?</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Active order banner ───────────────────────────────────────────────────────
df = st.session_state.orders_df
active_orders = df[
    (df["phone"] == cust["phone"]) &
    (~df["status"].isin(["Delivered"]))
] if cust["phone"] else df.iloc[0:0]

if not active_orders.empty:
    latest = active_orders.iloc[-1]
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            '<div class="active-banner">'
            '<div class="active-banner-left">'
            '<h3>🚗 Order in Progress</h3>'
            '<p>' + str(latest["order_id"]) + ' · ' + str(latest["status"]) + '</p>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )
    with col2:
        if st.button("Track →", type="primary"):
            st.switch_page("pages/2_📍_Track_Order.py")

# ── Service cards ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">What do you need washed today?</div>', unsafe_allow_html=True)

service_names = list(SERVICES.keys())
cols = st.columns(3)
for i, svc_name in enumerate(service_names):
    svc = SERVICES[svc_name]
    with cols[i % 3]:
        st.markdown(
            '<div class="service-card">'
            '<div class="service-icon">' + svc["icon"] + '</div>'
            '<div class="service-name">' + svc_name + '</div>'
            '<div class="service-price">₹' + str(svc["price"]) + '/' + svc["unit"] + '</div>'
            '<div style="font-size:0.72rem;color:#888;margin-top:2px;">' + svc["turnaround"] + '</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Book", key="svc_" + svc_name, use_container_width=True):
            st.session_state.booking_data = {"service": svc_name}
            st.session_state.booking_step = 1
            st.switch_page("pages/1_📦_Book_Order.py")

# ── Recent orders ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Recent Orders</div>', unsafe_allow_html=True)

if cust["phone"]:
    from utils.store import get_customer_orders
    recent = get_customer_orders(cust["phone"]).sort_values("created_at", ascending=False).head(3)
else:
    recent = df.sort_values("created_at", ascending=False).head(3)

STATUS_COLORS_LOCAL = {
    "Order Placed": "#FFA000", "Picked Up": "#1E88E5",
    "At Facility": "#8E24AA", "Processing": "#039BE5",
    "Out for Delivery": "#F4511E", "Delivered": "#43A047",
}

if recent.empty:
    st.info("No orders yet. Book your first wash!")
else:
    for _, row in recent.iterrows():
        color = STATUS_COLORS_LOCAL.get(row["status"], "#888")
        svc_icon = SERVICES.get(row["service"], {}).get("icon", "🧺")
        created_str = row["created_at"].strftime("%d %b %Y") if hasattr(row["created_at"], "strftime") else str(row["created_at"])[:10]
        st.markdown(
            '<div class="order-card">'
            '<div>'
            '<div class="order-id">' + svc_icon + ' ' + str(row["order_id"]) + '</div>'
            '<div class="order-meta">' + str(row["service"]) + ' · ' + created_str + '</div>'
            '<div class="status-badge" style="background:' + color + '22;color:' + color + ';">' + str(row["status"]) + '</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div class="order-amt">₹' + str(int(row["amount"])) + '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

# ── Subscription upsell ────────────────────────────────────────────────────────
if not cust.get("subscription"):
    st.markdown(
        '<div class="upsell-card">'
        '<h3>💎 Save ₹500/month with WashGo Premium</h3>'
        '<p>Get 20% off every order + free delivery always + express processing guaranteed.</p>'
        '</div>',
        unsafe_allow_html=True
    )
    if st.button("View Plans →", type="secondary"):
        st.switch_page("pages/4_💳_Subscription.py")
