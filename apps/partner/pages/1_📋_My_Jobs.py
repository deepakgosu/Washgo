import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from utils.store import get_store, update_order_status
from utils.data import STATUSES, STATUS_COLORS, SERVICES

st.set_page_config(page_title="My Jobs – WashGo Partner", page_icon="📋", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0D1117; color: #E6EDF3; }
.stApp { background: #0D1117; }
[data-testid="stSidebar"] { background: #0D1117 !important; border-right: 1px solid #21262D; }
[data-testid="stSidebar"] * { color: #E6EDF3 !important; }
h1,h2,h3,h4 { color: #E6EDF3 !important; }

.job-card {
    background: #161B22;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border: 1px solid #21262D;
}
.job-header { display: flex; justify-content: space-between; align-items: flex-start; }
.job-id     { font-size: 0.9rem; font-weight: 700; color: #E6EDF3; }
.job-area   { font-size: 0.8rem; color: #8B949E; margin-top: 2px; }
.job-svc    { font-size: 0.8rem; color: #8B949E; }
.job-amt    { font-size: 1rem; font-weight: 700; color: #00C853; }

.status-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
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
df = st.session_state.orders_df
my_orders = df[df["partner_id"] == partner["id"]].copy()

st.title("📋 My Jobs")

STATUS_NEXT = {
    "Order Placed":    "Picked Up",
    "Picked Up":       "At Facility",
    "At Facility":     "Out for Delivery",
    "Out for Delivery": "Delivered",
}

BUTTON_LABELS = {
    "Order Placed":    "🚗 Start Pickup",
    "Picked Up":       "🏭 Arrived at Facility",
    "At Facility":     "🚚 Out for Delivery",
    "Out for Delivery": "✅ Mark Delivered",
}

PENDING_STATUSES   = ["Order Placed"]
ACTIVE_STATUSES    = ["Picked Up", "At Facility", "Processing", "Out for Delivery"]
COMPLETED_STATUSES = ["Delivered"]

def render_jobs(subset):
    if subset.empty:
        st.markdown(
            '<div style="background:#161B22;border-radius:14px;padding:28px;text-align:center;color:#8B949E;border:1px dashed #30363D;">No jobs here.</div>',
            unsafe_allow_html=True
        )
        return
    for _, row in subset.sort_values("created_at", ascending=False).iterrows():
        color = STATUS_COLORS.get(str(row.get("status", "")), "#888")
        svc_icon = SERVICES.get(str(row.get("service", "")), {}).get("icon", "🧺")
        earned = int(row.get("amount", 0) * 0.25)
        created_str = row["created_at"].strftime("%d %b, %I:%M %p") if hasattr(row.get("created_at"), "strftime") else ""
        status_str = str(row.get("status", ""))

        st.markdown(
            '<div class="job-card">'
            '<div class="job-header">'
            '<div>'
            '<div class="job-id">' + svc_icon + ' ' + str(row["order_id"]) + '</div>'
            '<div class="job-area">📍 ' + str(row.get("area", "")) + ' · ' + str(row.get("customer_name", "")) + '</div>'
            '<div class="job-svc">' + str(row.get("service", "")) + ' · ' + created_str + '</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div class="status-badge" style="background:' + color + '22;color:' + color + ';">' + status_str + '</div>'
            '<div class="job-amt" style="margin-top:6px;">₹' + str(earned) + '</div>'
            '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        if status_str in STATUS_NEXT:
            btn_lbl = BUTTON_LABELS.get(status_str, "Update Status")
            next_status = STATUS_NEXT[status_str]
            if st.button(btn_lbl, key="job_act_" + str(row["order_id"]), use_container_width=True):
                update_order_status(str(row["order_id"]), next_status)
                if next_status == "Picked Up":
                    for p in st.session_state.partners:
                        if p["id"] == partner["id"]:
                            p["current_order"] = str(row["order_id"])
                    st.session_state.partner_logged_in["current_order"] = str(row["order_id"])
                elif next_status == "Delivered":
                    earn = int(row.get("amount", 0) * 0.25)
                    for p in st.session_state.partners:
                        if p["id"] == partner["id"]:
                            p["today_earnings"] = p.get("today_earnings", 0) + earn
                            p["current_order"] = None
                    st.session_state.partner_logged_in["today_earnings"] = st.session_state.partner_logged_in.get("today_earnings", 0) + earn
                    st.session_state.partner_logged_in["current_order"] = None
                st.success("Status updated to: " + next_status)
                st.rerun()

tab_pending, tab_active, tab_done, tab_all = st.tabs(["Pending", "Active", "Completed", "All"])

with tab_pending:
    render_jobs(my_orders[my_orders["status"].isin(PENDING_STATUSES)])
with tab_active:
    render_jobs(my_orders[my_orders["status"].isin(ACTIVE_STATUSES)])
with tab_done:
    render_jobs(my_orders[my_orders["status"].isin(COMPLETED_STATUSES)])
with tab_all:
    render_jobs(my_orders)
