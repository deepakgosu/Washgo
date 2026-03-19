import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from datetime import datetime, date
from utils.store import get_store, get_customer_orders
from utils.data import SERVICES, STATUS_COLORS

st.set_page_config(page_title="My Orders – WashGo", page_icon="📋", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F5F5F5; }
[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E0E0E0; }
[data-testid="stSidebar"] * { color: #1A1A1A !important; }

.page-title { font-size: 1.6rem; font-weight: 800; color: #1A1A1A; margin-bottom: 4px; }
.page-sub   { font-size: 0.9rem; color: #888; margin-bottom: 24px; }

.stat-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 18px 20px;
    border: 1px solid #F0F0F0;
    text-align: center;
}
.stat-val  { font-size: 1.6rem; font-weight: 800; color: #1A1A1A; }
.stat-lbl  { font-size: 0.8rem; color: #888; margin-top: 2px; }

.order-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    border: 1px solid #F0F0F0;
}
.order-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.order-id   { font-size: 0.9rem; font-weight: 700; color: #1A1A1A; }
.order-svc  { font-size: 0.8rem; color: #888; margin-top: 2px; }
.order-amt  { font-size: 1rem; font-weight: 700; color: #1A1A1A; }
.status-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    margin-top: 4px;
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

st.markdown('<div class="page-title">📋 My Orders</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Your complete order history.</div>', unsafe_allow_html=True)

cust = st.session_state.customer
df = get_customer_orders(cust.get("phone", "")) if cust.get("phone") else st.session_state.orders_df.head(20).copy()

# ── Summary stats ─────────────────────────────────────────────────────────────
total_orders = len(df)
total_spent  = df["amount"].sum() if total_orders else 0
rated = df[df["rating"].notna()]
avg_rating = rated["rating"].mean() if not rated.empty else 0

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(
        '<div class="stat-card"><div class="stat-val">' + str(total_orders) + '</div><div class="stat-lbl">Total Orders</div></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        '<div class="stat-card"><div class="stat-val">₹' + str(int(total_spent)) + '</div><div class="stat-lbl">Total Spent</div></div>',
        unsafe_allow_html=True
    )
with col3:
    rating_str = str(round(avg_rating, 1)) + " ⭐" if avg_rating else "—"
    st.markdown(
        '<div class="stat-card"><div class="stat-val">' + rating_str + '</div><div class="stat-lbl">Avg Rating Given</div></div>',
        unsafe_allow_html=True
    )

st.markdown("---")

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("🔍 Filters"):
    fcol1, fcol2, fcol3 = st.columns(3)
    with fcol1:
        svc_filter = st.selectbox("Service", ["All"] + list(SERVICES.keys()))
    with fcol2:
        date_from = st.date_input("From", value=date(2024, 1, 1))
    with fcol3:
        date_to = st.date_input("To", value=date.today())

filtered = df.copy()
if svc_filter != "All":
    filtered = filtered[filtered["service"] == svc_filter]
if not filtered.empty and "created_at" in filtered.columns:
    filtered["_date"] = filtered["created_at"].apply(lambda x: x.date() if hasattr(x, "date") else date.today())
    filtered = filtered[(filtered["_date"] >= date_from) & (filtered["_date"] <= date_to)]

filtered = filtered.sort_values("created_at", ascending=False)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_all, tab_active, tab_done, tab_cancelled = st.tabs(["All", "Active", "Completed", "Cancelled"])

ACTIVE_STATUSES    = ["Order Placed", "Picked Up", "At Facility", "Processing", "Out for Delivery"]
COMPLETED_STATUSES = ["Delivered"]
CANCELLED_STATUSES = ["Cancelled"]

def render_orders(subset):
    if subset.empty:
        st.info("No orders in this category.")
        return
    for _, row in subset.iterrows():
        svc_icon = SERVICES.get(str(row.get("service", "")), {}).get("icon", "🧺")
        color = STATUS_COLORS.get(str(row.get("status", "")), "#888")
        created_str = row["created_at"].strftime("%d %b %Y") if hasattr(row.get("created_at"), "strftime") else str(row.get("created_at", ""))[:10]

        with st.expander(
            svc_icon + " " + str(row["order_id"]) + " · " + str(row["service"]) + " · " + created_str + " · ₹" + str(int(row["amount"]))
        ):
            col_l, col_r = st.columns([3, 1])
            with col_l:
                st.markdown(
                    '<div class="status-badge" style="background:' + color + '22;color:' + color + ';">' + str(row["status"]) + '</div>',
                    unsafe_allow_html=True
                )
                st.write("**Area:** " + str(row.get("area", "")))
                st.write("**Address:** " + str(row.get("address", "")))
                st.write("**Partner:** " + str(row.get("partner_name", "")))
                st.write("**Facility:** " + str(row.get("facility", "")))
                st.write("**Payment:** " + str(row.get("payment_method", "")) + " · " + str(row.get("payment_status", "")))
                if row.get("special_instructions"):
                    st.write("**Instructions:** " + str(row["special_instructions"]))
            with col_r:
                st.metric("Amount", "₹" + str(int(row["amount"])))
                if row.get("delivery_type"):
                    st.caption(str(row["delivery_type"]))

            if str(row.get("status")) == "Delivered":
                existing_rating = row.get("rating")
                if existing_rating and str(existing_rating) != "nan":
                    st.success("You rated this order: " + ("⭐" * int(existing_rating)))
                else:
                    st.markdown("**Rate this order:**")
                    rating_val = st.radio(
                        "Stars",
                        [1, 2, 3, 4, 5],
                        horizontal=True,
                        key="rating_" + str(row["order_id"]),
                        format_func=lambda x: "⭐" * x,
                    )
                    if st.button("Submit Rating", key="rate_btn_" + str(row["order_id"])):
                        mask = st.session_state.orders_df["order_id"] == row["order_id"]
                        st.session_state.orders_df.loc[mask, "rating"] = rating_val
                        st.success("Rating submitted!")
                        st.rerun()

with tab_all:
    render_orders(filtered)

with tab_active:
    render_orders(filtered[filtered["status"].isin(ACTIVE_STATUSES)])

with tab_done:
    render_orders(filtered[filtered["status"].isin(COMPLETED_STATUSES)])

with tab_cancelled:
    render_orders(filtered[filtered["status"].isin(CANCELLED_STATUSES)])
