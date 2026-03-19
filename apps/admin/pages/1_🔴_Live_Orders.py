import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
import pandas as pd
from utils.store import get_store, update_order_status
from utils.data import AREAS, SERVICES, STATUSES, STATUS_COLORS, PARTNERS

st.set_page_config(page_title="Live Orders – WashGo Admin", page_icon="🔴", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0F172A; color: #F1F5F9; }
.stApp { background: #0F172A; }
[data-testid="stSidebar"] { background: #1E293B !important; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
h1,h2,h3,h4 { color: #F1F5F9 !important; }
.stTextInput input, .stSelectbox select { background: #1E293B !important; color: #F1F5F9 !important; border: 1px solid #334155 !important; }
.status-badge { display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 0.7rem; font-weight: 600; }
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

st.title("🔴 Live Orders")

df = st.session_state.orders_df.copy()

# ── Filters ───────────────────────────────────────────────────────────────────
with st.container():
    fc1, fc2, fc3, fc4, fc5 = st.columns(5)
    with fc1:
        f_status = st.selectbox("Status", ["All"] + STATUSES)
    with fc2:
        f_area = st.selectbox("Area", ["All"] + AREAS)
    with fc3:
        f_svc = st.selectbox("Service", ["All"] + list(SERVICES.keys()))
    with fc4:
        from datetime import date
        f_date = st.date_input("From Date", value=date(2024, 1, 1))
    with fc5:
        f_partner = st.selectbox("Partner", ["All"] + [p["name"] for p in PARTNERS])

filtered = df.copy()
if f_status != "All":
    filtered = filtered[filtered["status"] == f_status]
if f_area != "All":
    filtered = filtered[filtered["area"] == f_area]
if f_svc != "All":
    filtered = filtered[filtered["service"] == f_svc]
if f_partner != "All":
    filtered = filtered[filtered["partner_name"] == f_partner]
filtered["_date"] = filtered["created_at"].apply(lambda x: x.date() if hasattr(x, "date") else date.today())
filtered = filtered[filtered["_date"] >= f_date]
filtered = filtered.sort_values("created_at", ascending=False)

st.caption(str(len(filtered)) + " orders found")

# ── Bulk actions ──────────────────────────────────────────────────────────────
with st.expander("⚡ Bulk Actions"):
    bulk_ids = st.multiselect("Select Order IDs", filtered["order_id"].tolist())
    bulk_status = st.selectbox("Update all selected to", STATUSES, key="bulk_status")
    if st.button("Apply Bulk Update", type="primary"):
        if bulk_ids:
            for oid in bulk_ids:
                update_order_status(oid, bulk_status)
            st.success("Updated " + str(len(bulk_ids)) + " orders to: " + bulk_status)
            st.rerun()

# ── Export ─────────────────────────────────────────────────────────────────────
csv = filtered.drop(columns=["_date"], errors="ignore").to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", csv, "washgo_orders.csv", "text/csv")

# ── Orders table ──────────────────────────────────────────────────────────────
st.subheader("Orders Table")
partner_names = ["(Keep Current)"] + [p["name"] for p in PARTNERS]

for _, row in filtered.iterrows():
    color    = STATUS_COLORS.get(str(row.get("status", "")), "#888")
    svc_icon = SERVICES.get(str(row.get("service", "")), {}).get("icon", "🧺")
    created_str = row["created_at"].strftime("%d %b %Y %I:%M %p") if hasattr(row.get("created_at"), "strftime") else ""

    with st.expander(
        str(row["order_id"]) + " | " + str(row.get("customer_name", "")) + " | " + str(row.get("area", "")) +
        " | " + str(row.get("service", "")) + " | " + str(row.get("status", "")) + " | ₹" + str(int(row.get("amount", 0)))
    ):
        col_info, col_actions = st.columns([3, 2])

        with col_info:
            st.markdown(
                '<span class="status-badge" style="background:' + color + '22;color:' + color + ';">' + str(row.get("status", "")) + '</span>',
                unsafe_allow_html=True
            )
            st.write("**Customer:** " + str(row.get("customer_name", "")) + " · " + str(row.get("phone", "")))
            st.write("**Address:** " + str(row.get("address", "")))
            st.write("**Service:** " + svc_icon + " " + str(row.get("service", "")))
            st.write("**Partner:** " + str(row.get("partner_name", "")))
            st.write("**Facility:** " + str(row.get("facility", "")))
            st.write("**Payment:** " + str(row.get("payment_method", "")) + " · " + str(row.get("payment_status", "")))
            st.write("**Created:** " + created_str)
            if row.get("special_instructions"):
                st.write("**Instructions:** " + str(row["special_instructions"]))

        with col_actions:
            st.markdown("**Change Status**")
            new_status = st.selectbox(
                "Status", STATUSES,
                index=STATUSES.index(str(row.get("status"))) if str(row.get("status")) in STATUSES else 0,
                key="status_sel_" + str(row["order_id"])
            )
            if st.button("Update Status", key="update_status_" + str(row["order_id"]), type="primary"):
                update_order_status(str(row["order_id"]), new_status)
                st.success("Updated!")
                st.rerun()

            st.markdown("**Reassign Partner**")
            new_partner = st.selectbox(
                "Partner", partner_names,
                key="partner_sel_" + str(row["order_id"])
            )
            if st.button("Reassign", key="reassign_" + str(row["order_id"])):
                if new_partner != "(Keep Current)":
                    p_obj = next((p for p in PARTNERS if p["name"] == new_partner), None)
                    if p_obj:
                        mask = st.session_state.orders_df["order_id"] == str(row["order_id"])
                        st.session_state.orders_df.loc[mask, "partner_id"]   = p_obj["id"]
                        st.session_state.orders_df.loc[mask, "partner_name"] = p_obj["name"]
                        st.success("Reassigned to " + new_partner)
                        st.rerun()
