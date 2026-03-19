import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from datetime import datetime
from utils.store import get_store, get_customer_orders
from utils.data import AREAS

st.set_page_config(page_title="Profile – WashGo", page_icon="👤", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F5F5F5; }
[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E0E0E0; }
[data-testid="stSidebar"] * { color: #1A1A1A !important; }

.page-title { font-size: 1.6rem; font-weight: 800; color: #1A1A1A; margin-bottom: 4px; }

.profile-header {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    margin-bottom: 24px;
    border: 1px solid #F0F0F0;
}
.avatar {
    width: 72px; height: 72px;
    border-radius: 50%;
    background: #00C853;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem; font-weight: 700; color: #fff;
    flex-shrink: 0;
}
.profile-name   { font-size: 1.3rem; font-weight: 800; color: #1A1A1A; }
.profile-phone  { font-size: 0.9rem; color: #888; margin-top: 2px; }
.profile-since  { font-size: 0.8rem; color: #BBBBBB; margin-top: 4px; }

.section-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border: 1px solid #F0F0F0;
}
.section-heading { font-size: 0.95rem; font-weight: 700; color: #1A1A1A; margin-bottom: 14px; }

.stat-row {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
}
.stat-box {
    background: #F8F8F8;
    border-radius: 12px;
    padding: 14px 18px;
    flex: 1;
    text-align: center;
}
.stat-val { font-size: 1.4rem; font-weight: 800; color: #1A1A1A; }
.stat-lbl { font-size: 0.75rem; color: #888; margin-top: 2px; }

.danger-btn button {
    background: #FFF3F3 !important;
    color: #E53935 !important;
    border: 1px solid #FFCDD2 !important;
}
</style>
""", unsafe_allow_html=True)

store = get_store()

if not st.session_state.customer_logged_in:
    st.warning("Please log in from the Home page.")
    st.stop()

with st.sidebar:
    st.markdown('<span style="font-size:1.4rem;font-weight:800;color:#00C853;">🧺 WashGo</span>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                       label="🏠 Home")
    st.page_link("pages/1_📦_Book_Order.py",     label="📦 Book Order")
    st.page_link("pages/2_📍_Track_Order.py",    label="📍 Track Order")
    st.page_link("pages/3_📋_My_Orders.py",      label="📋 My Orders")
    st.page_link("pages/4_💳_Subscription.py",   label="💳 Subscription")
    st.page_link("pages/5_👤_Profile.py",        label="👤 Profile")

st.markdown('<div class="page-title">👤 My Profile</div>', unsafe_allow_html=True)

cust = st.session_state.customer
name = cust.get("name", "User")
phone = cust.get("phone", "")
initials = "".join([w[0].upper() for w in name.split()[:2]]) if name else "U"
member_since = cust.get("member_since", datetime.now())
member_str = member_since.strftime("%B %Y") if hasattr(member_since, "strftime") else "Recently"

st.markdown(
    '<div class="profile-header">'
    '<div class="avatar">' + initials + '</div>'
    '<div>'
    '<div class="profile-name">' + name + '</div>'
    '<div class="profile-phone">📞 ' + phone + '</div>'
    '<div class="profile-since">Member since ' + member_str + '</div>'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Order stats ────────────────────────────────────────────────────────────────
orders = get_customer_orders(phone) if phone else st.session_state.orders_df.iloc[0:0]
total_orders = len(orders)
total_spent  = orders["amount"].sum() if total_orders else 0
rated = orders[orders["rating"].notna()]
avg_rating = rated["rating"].mean() if not rated.empty else 0

st.markdown(
    '<div class="stat-row">'
    '<div class="stat-box"><div class="stat-val">' + str(total_orders) + '</div><div class="stat-lbl">Orders</div></div>'
    '<div class="stat-box"><div class="stat-val">₹' + str(int(total_spent)) + '</div><div class="stat-lbl">Total Spent</div></div>'
    '<div class="stat-box"><div class="stat-val">' + (str(round(avg_rating, 1)) + " ⭐" if avg_rating else "—") + '</div><div class="stat-lbl">Avg Rating</div></div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Edit name ─────────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-heading">Edit Profile</div>', unsafe_allow_html=True)
new_name = st.text_input("Display Name", value=name)
new_area = st.selectbox("Preferred Area", AREAS, index=AREAS.index(cust.get("area", AREAS[0])) if cust.get("area") in AREAS else 0)
new_email = st.text_input("Email Address (optional)", value=cust.get("email", ""))
if st.button("Save Changes", type="primary"):
    st.session_state.customer["name"]  = new_name.strip()
    st.session_state.customer["area"]  = new_area
    st.session_state.customer["email"] = new_email.strip()
    st.success("Profile updated!")
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# ── Addresses ─────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📍 Saved Addresses")
addresses = cust.get("addresses", [])
if addresses:
    for i, addr in enumerate(addresses):
        col1, col2 = st.columns([5, 1])
        with col1:
            st.text_input("Address " + str(i + 1), value=addr, key="addr_" + str(i))
        with col2:
            if st.button("🗑️", key="del_addr_" + str(i)):
                addresses.pop(i)
                st.session_state.customer["addresses"] = addresses
                st.rerun()
else:
    st.info("No saved addresses.")

new_addr = st.text_input("Add new address", placeholder="Flat 12, Green Valley, Gachibowli")
if st.button("Add Address"):
    if new_addr.strip():
        addresses.append(new_addr.strip())
        st.session_state.customer["addresses"] = addresses
        st.success("Address added!")
        st.rerun()

# ── Notification prefs ────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🔔 Notification Preferences")
if "notif_prefs" not in st.session_state:
    st.session_state.notif_prefs = {
        "order_updates": True,
        "promotions": True,
        "sms_alerts": True,
        "email_updates": False,
    }

st.session_state.notif_prefs["order_updates"] = st.toggle("Order Status Updates", value=st.session_state.notif_prefs["order_updates"])
st.session_state.notif_prefs["promotions"]    = st.toggle("Promotions & Offers",  value=st.session_state.notif_prefs["promotions"])
st.session_state.notif_prefs["sms_alerts"]    = st.toggle("SMS Alerts",           value=st.session_state.notif_prefs["sms_alerts"])
st.session_state.notif_prefs["email_updates"] = st.toggle("Email Updates",        value=st.session_state.notif_prefs["email_updates"])

# ── Subscription status ────────────────────────────────────────────────────────
st.markdown("---")
plan = cust.get("subscription")
if plan:
    st.success("Current Plan: **" + plan.title() + "**")
    if st.button("Manage Subscription"):
        st.switch_page("pages/4_💳_Subscription.py")
else:
    st.info("You're on the **Free** plan.")
    if st.button("Upgrade to Premium →", type="primary"):
        st.switch_page("pages/4_💳_Subscription.py")

# ── Danger zone ───────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("⚠️ Danger Zone")
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = False

if not st.session_state.confirm_delete:
    st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
    if st.button("🗑️ Delete Account", use_container_width=True):
        st.session_state.confirm_delete = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("Are you sure? This action cannot be undone.")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes, Delete", type="primary", use_container_width=True):
            st.session_state.customer_logged_in = False
            st.session_state.customer = {
                "name": "", "phone": "", "email": "", "area": AREAS[0],
                "subscription": None, "addresses": [], "member_since": datetime.now(),
            }
            st.session_state.confirm_delete = False
            st.success("Account deleted.")
            st.rerun()
    with col2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.confirm_delete = False
            st.rerun()
