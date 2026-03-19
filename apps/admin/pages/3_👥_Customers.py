import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
import pandas as pd
from utils.store import get_store

st.set_page_config(page_title="Customers – WashGo Admin", page_icon="👥", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0F172A; color: #F1F5F9; }
.stApp { background: #0F172A; }
[data-testid="stSidebar"] { background: #1E293B !important; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
h1,h2,h3,h4 { color: #F1F5F9 !important; }
.stTextInput input { background: #1E293B !important; color: #F1F5F9 !important; border: 1px solid #334155 !important; }

.cust-row {
    background: #1E293B;
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 8px;
    border: 1px solid #334155;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.cname { font-size: 0.92rem; font-weight: 700; color: #F1F5F9; }
.cmeta { font-size: 0.78rem; color: #94A3B8; margin-top: 2px; }
.cval  { font-size: 0.9rem; font-weight: 700; color: #10B981; }

.top-badge {
    display: inline-block; padding: 2px 8px; border-radius: 10px;
    background: rgba(245,158,11,0.2); color: #F59E0B;
    font-size: 0.7rem; font-weight: 700;
}
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

st.title("👥 Customer Management")

df = st.session_state.orders_df.copy()

# ── Aggregate customer data ────────────────────────────────────────────────────
cust_grp = df.groupby(["customer_name", "phone", "area"]).agg(
    total_orders=("order_id", "count"),
    total_spent=("amount", "sum"),
    last_order=("created_at", "max"),
).reset_index()

cust_grp["total_spent"] = cust_grp["total_spent"].round(0).astype(int)
cust_grp["last_order_str"] = cust_grp["last_order"].apply(
    lambda x: x.strftime("%d %b %Y") if hasattr(x, "strftime") else str(x)[:10]
)

# ── Search ─────────────────────────────────────────────────────────────────────
search = st.text_input("🔍 Search by name or phone", placeholder="e.g. Priya or 9876...")
if search.strip():
    mask = (
        cust_grp["customer_name"].str.contains(search.strip(), case=False, na=False) |
        cust_grp["phone"].str.contains(search.strip(), case=False, na=False)
    )
    cust_filtered = cust_grp[mask]
else:
    cust_filtered = cust_grp

st.caption(str(len(cust_filtered)) + " customers")

# ── Customer list ──────────────────────────────────────────────────────────────
for _, row in cust_filtered.sort_values("total_orders", ascending=False).iterrows():
    name = str(row["customer_name"])
    phone = str(row["phone"])
    area  = str(row["area"])
    n_ord = int(row["total_orders"])
    spent = int(row["total_spent"])
    last  = row["last_order_str"]
    top_badge = '<span class="top-badge">⭐ Top Customer</span>' if n_ord >= 5 else ""

    st.markdown(
        '<div class="cust-row">'
        '<div>'
        '<div class="cname">' + name + ' ' + top_badge + '</div>'
        '<div class="cmeta">📞 ' + phone + ' · 📍 ' + area + '</div>'
        '<div class="cmeta">Last order: ' + last + '</div>'
        '</div>'
        '<div style="text-align:right;">'
        '<div class="cval">' + str(n_ord) + ' orders</div>'
        '<div style="font-size:0.88rem;color:#F1F5F9;margin-top:2px;">₹' + str(spent) + ' spent</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    with st.expander("View Details — " + name):
        cust_orders = df[df["phone"] == phone].sort_values("created_at", ascending=False)
        st.markdown("**Order History (" + str(len(cust_orders)) + " orders)**")
        for _, ord_row in cust_orders.head(10).iterrows():
            created_str = ord_row["created_at"].strftime("%d %b %Y") if hasattr(ord_row.get("created_at"), "strftime") else ""
            st.caption(
                str(ord_row["order_id"]) + " · " + str(ord_row.get("service", "")) +
                " · " + str(ord_row.get("status", "")) + " · ₹" + str(int(ord_row.get("amount", 0))) +
                " · " + created_str
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💸 Issue Refund", key="refund_" + phone):
                st.success("Refund issued to " + name + " (demo)")
        with col2:
            if st.button("🚫 Block Customer", key="block_cust_" + phone):
                st.error(name + " has been blocked (demo)")
        with col3:
            disc = st.number_input("Discount %", 0, 100, 10, key="disc_" + phone)
            if st.button("Apply Discount", key="apply_disc_" + phone):
                st.success(str(disc) + "% discount applied to " + name + " (demo)")

# ── Top customers leaderboard ──────────────────────────────────────────────────
st.markdown("---")
st.subheader("🏆 Top Customers Leaderboard")

top_by_orders = cust_grp.sort_values("total_orders", ascending=False).head(5)
top_by_spend  = cust_grp.sort_values("total_spent",  ascending=False).head(5)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**By Order Count**")
    for rank, (_, row) in enumerate(top_by_orders.iterrows(), 1):
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][rank - 1]
        st.markdown(medal + " **" + str(row["customer_name"]) + "** — " + str(int(row["total_orders"])) + " orders")

with col2:
    st.markdown("**By Total Spend**")
    for rank, (_, row) in enumerate(top_by_spend.iterrows(), 1):
        medal = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"][rank - 1]
        st.markdown(medal + " **" + str(row["customer_name"]) + "** — ₹" + str(int(row["total_spent"])))
