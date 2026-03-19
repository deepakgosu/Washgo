import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import streamlit as st
from datetime import datetime, timedelta
from utils.store import get_store
from utils.data import STATUS_COLORS, SERVICES

st.set_page_config(
    page_title="WashGo Admin",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0F172A; color: #F1F5F9; }
.stApp { background: #0F172A; }
[data-testid="stSidebar"] {
    background: #1E293B !important;
    border-right: 1px solid #334155;
}
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
[data-testid="stSidebar"] .stButton button {
    background: #0F172A; color: #F1F5F9;
    border: 1px solid #334155;
}
h1,h2,h3,h4,h5 { color: #F1F5F9 !important; }
p, span, label, div { color: #F1F5F9; }

.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background: #1E293B !important;
    color: #F1F5F9 !important;
    border: 1px solid #334155 !important;
}
.stButton button { border-radius: 10px !important; font-weight: 600 !important; }

/* Login */
.login-card {
    background: #1E293B;
    border-radius: 20px;
    padding: 48px 40px;
    max-width: 420px;
    margin: 100px auto;
    border: 1px solid #334155;
    text-align: center;
}
.login-logo { font-size: 2rem; font-weight: 800; color: #3B82F6; margin-bottom: 8px; }
.login-sub  { color: #94A3B8; font-size: 0.9rem; margin-bottom: 24px; }

/* Stats bar */
.stat-bar {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 24px;
}
.stat-tile {
    background: #1E293B;
    border-radius: 12px;
    padding: 14px 18px;
    flex: 1;
    min-width: 130px;
    border: 1px solid #334155;
}
.stat-lbl  { font-size: 0.72rem; color: #94A3B8; margin-bottom: 4px; letter-spacing: 0.5px; }
.stat-val  { font-size: 1.4rem; font-weight: 800; color: #F1F5F9; }
.stat-green { color: #10B981 !important; }
.stat-blue  { color: #3B82F6 !important; }
.stat-amber { color: #F59E0B !important; }
.stat-red   { color: #EF4444 !important; }

/* Orders feed */
.feed-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    margin-bottom: 6px;
    font-size: 0.82rem;
}
.feed-row.delivered { background: rgba(16,185,129,0.08); }
.feed-row.in-progress { background: rgba(245,158,11,0.08); }
.feed-row.pending { background: rgba(239,68,68,0.08); }
.feed-row.default { background: #1E293B; }
.feed-oid  { font-weight: 700; color: #F1F5F9; min-width: 80px; }
.feed-cust { color: #CBD5E1; min-width: 120px; }
.feed-area { color: #94A3B8; min-width: 100px; }
.feed-svc  { color: #CBD5E1; min-width: 110px; }
.feed-amt  { color: #10B981; font-weight: 700; min-width: 60px; }
.feed-time { color: #64748B; font-size: 0.75rem; }
.status-badge {
    display: inline-block; padding: 2px 8px;
    border-radius: 12px; font-size: 0.7rem; font-weight: 600;
}

/* Partner cards */
.partner-mini {
    background: #1E293B;
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 8px;
    border: 1px solid #334155;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.pname  { font-size: 0.9rem; font-weight: 700; color: #F1F5F9; }
.parea  { font-size: 0.75rem; color: #94A3B8; }
.ponline { font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 10px; }
.ponline.on  { background: rgba(16,185,129,0.2); color: #10B981; }
.ponline.off { background: rgba(239,68,68,0.15); color: #EF4444; }

.washgo-logo { font-size: 1.3rem; font-weight: 800; color: #3B82F6; }
</style>
""", unsafe_allow_html=True)

store = get_store()

# ── Login gate ────────────────────────────────────────────────────────────────
if not st.session_state.admin_logged_in:
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-logo">⚙️ WashGo Admin</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Command Center · Restricted Access</div>', unsafe_allow_html=True)
    pwd = st.text_input("Admin Password", type="password", placeholder="Enter password")
    if st.button("Login →", use_container_width=True, type="primary"):
        if pwd == "admin123":
            st.session_state.admin_logged_in = True
            st.rerun()
        else:
            st.error("Incorrect password.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="washgo-logo">⚙️ WashGo Admin</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.page_link("app.py",                       label="🖥️ Command Center")
    st.page_link("pages/1_🔴_Live_Orders.py",    label="🔴 Live Orders")
    st.page_link("pages/2_🚚_Partners.py",       label="🚚 Partners")
    st.page_link("pages/3_👥_Customers.py",      label="👥 Customers")
    st.page_link("pages/4_📊_Analytics.py",      label="📊 Analytics")
    st.page_link("pages/5_⚙️_Settings.py",      label="⚙️ Settings")
    st.markdown("---")
    if st.button("Logout", use_container_width=True):
        st.session_state.admin_logged_in = False
        st.rerun()

# ── Auto-refresh ──────────────────────────────────────────────────────────────
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

elapsed = (datetime.now() - st.session_state.last_refresh).seconds
if elapsed > 30:
    st.session_state.last_refresh = datetime.now()
    st.rerun()

st.title("🖥️ Command Center")
st.caption("Auto-refreshes every 30 seconds · Last refresh: " + datetime.now().strftime("%I:%M:%S %p"))

df = st.session_state.orders_df
partners = st.session_state.partners

now = datetime.now()
today_orders = df[df["created_at"].apply(lambda x: x.date() if hasattr(x, "date") else now.date()) == now.date()]

active_count   = len(df[~df["status"].isin(["Delivered"])])
pending_count  = len(df[df["status"] == "Order Placed"])
otd_count      = len(df[df["status"] == "Out for Delivery"])
delivered_today = len(today_orders[today_orders["status"] == "Delivered"])
revenue_today  = int(today_orders[today_orders["status"] == "Delivered"]["amount"].sum())
online_count   = len([p for p in partners if p.get("online")])
total_partners = len(partners)

st.markdown(
    '<div class="stat-bar">'
    '<div class="stat-tile"><div class="stat-lbl">ACTIVE ORDERS</div><div class="stat-val stat-blue">' + str(active_count) + '</div></div>'
    '<div class="stat-tile"><div class="stat-lbl">PENDING PICKUP</div><div class="stat-val stat-amber">' + str(pending_count) + '</div></div>'
    '<div class="stat-tile"><div class="stat-lbl">OUT FOR DELIVERY</div><div class="stat-val stat-amber">' + str(otd_count) + '</div></div>'
    '<div class="stat-tile"><div class="stat-lbl">DELIVERED TODAY</div><div class="stat-val stat-green">' + str(delivered_today) + '</div></div>'
    '<div class="stat-tile"><div class="stat-lbl">REVENUE TODAY</div><div class="stat-val stat-green">₹' + str(revenue_today) + '</div></div>'
    '<div class="stat-tile"><div class="stat-lbl">PARTNERS ONLINE</div><div class="stat-val">' + str(online_count) + '/' + str(total_partners) + '</div></div>'
    '</div>',
    unsafe_allow_html=True
)

# ── Main content: orders feed + partner status ────────────────────────────────
col_feed, col_partner = st.columns([6, 4])

with col_feed:
    st.subheader("📡 Recent Orders Feed")
    recent = df.sort_values("created_at", ascending=False).head(15)
    for _, row in recent.iterrows():
        status = str(row.get("status", ""))
        color  = STATUS_COLORS.get(status, "#888")
        svc_icon = SERVICES.get(str(row.get("service", "")), {}).get("icon", "🧺")

        if status == "Delivered":
            row_cls = "delivered"
        elif status in ["Picked Up", "At Facility", "Processing", "Out for Delivery"]:
            row_cls = "in-progress"
        elif status == "Order Placed":
            created = row.get("created_at")
            if hasattr(created, "replace"):
                age_hrs = (now - created).seconds / 3600
                row_cls = "pending" if age_hrs > 2 else "in-progress"
            else:
                row_cls = "in-progress"
        else:
            row_cls = "default"

        created_str = row["created_at"].strftime("%I:%M %p") if hasattr(row.get("created_at"), "strftime") else ""
        st.markdown(
            '<div class="feed-row ' + row_cls + '">'
            '<div class="feed-oid">' + str(row["order_id"]) + '</div>'
            '<div class="feed-cust">' + str(row.get("customer_name", ""))[:15] + '</div>'
            '<div class="feed-area">' + str(row.get("area", ""))[:12] + '</div>'
            '<div class="feed-svc">' + svc_icon + ' ' + str(row.get("service", ""))[:12] + '</div>'
            '<div><span class="status-badge" style="background:' + color + '22;color:' + color + ';">' + status + '</span></div>'
            '<div class="feed-amt">₹' + str(int(row.get("amount", 0))) + '</div>'
            '<div class="feed-time">' + created_str + '</div>'
            '</div>',
            unsafe_allow_html=True
        )

with col_partner:
    st.subheader("🚗 Partner Status")
    for p in partners:
        online_cls  = "on" if p.get("online") else "off"
        online_text = "Online" if p.get("online") else "Offline"
        cur_order   = p.get("current_order", "")
        assign_text = "On: " + str(cur_order) if cur_order else "Available"

        st.markdown(
            '<div class="partner-mini">'
            '<div>'
            '<div class="pname">' + p["name"] + '</div>'
            '<div class="parea">📍 ' + p.get("area", "") + ' · ' + assign_text + '</div>'
            '<div class="parea">⭐ ' + str(p.get("rating", "")) + ' · ' + str(p.get("today_trips", 0)) + ' trips · ₹' + str(int(p.get("today_earnings", 0))) + '</div>'
            '</div>'
            '<span class="ponline ' + online_cls + '">' + online_text + '</span>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button(("Go Offline" if p.get("online") else "Go Online"), key="toggle_partner_" + p["id"], use_container_width=True):
            for pp in st.session_state.partners:
                if pp["id"] == p["id"]:
                    pp["online"] = not pp.get("online", False)
            st.rerun()

# ── Quick Actions ─────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("⚡ Quick Actions")
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Assign Order to Partner**")
    unassigned = df[df["status"] == "Order Placed"]
    if not unassigned.empty:
        order_opts = unassigned["order_id"].tolist()
        sel_order  = st.selectbox("Select Order", order_opts, key="qa_order")
        partner_opts = [p["name"] for p in partners]
        sel_partner = st.selectbox("Select Partner", partner_opts, key="qa_partner")
        if st.button("Assign →", type="primary"):
            p_obj = next((p for p in partners if p["name"] == sel_partner), None)
            if p_obj:
                mask = st.session_state.orders_df["order_id"] == sel_order
                st.session_state.orders_df.loc[mask, "partner_id"]   = p_obj["id"]
                st.session_state.orders_df.loc[mask, "partner_name"] = p_obj["name"]
                st.session_state.orders_df.loc[mask, "status"] = "Picked Up"
                st.session_state.orders_df.loc[mask, "status_idx"] = 1
                st.success("Assigned " + sel_order + " to " + sel_partner)
                st.rerun()
    else:
        st.info("No unassigned orders.")

with col2:
    st.markdown("**Send Alert to All Partners**")
    alert_msg = st.text_input("Alert message", placeholder="e.g. High demand in Gachibowli area")
    if st.button("📣 Send Alert", type="primary"):
        if alert_msg.strip():
            st.success("Alert sent to " + str(total_partners) + " partners: \"" + alert_msg + "\"")
        else:
            st.warning("Enter a message first.")
