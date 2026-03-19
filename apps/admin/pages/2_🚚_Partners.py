import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
import pandas as pd
from utils.store import get_store
from utils.data import AREAS, PARTNERS

st.set_page_config(page_title="Partners – WashGo Admin", page_icon="🚚", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: #0F172A; color: #F1F5F9; }
.stApp { background: #0F172A; }
[data-testid="stSidebar"] { background: #1E293B !important; border-right: 1px solid #334155; }
[data-testid="stSidebar"] * { color: #F1F5F9 !important; }
h1,h2,h3,h4 { color: #F1F5F9 !important; }
.stTextInput input, .stSelectbox select, .stTextArea textarea {
    background: #1E293B !important; color: #F1F5F9 !important; border: 1px solid #334155 !important;
}

.partner-card {
    background: #1E293B;
    border-radius: 16px;
    padding: 20px;
    border: 1px solid #334155;
    margin-bottom: 16px;
}
.p-name  { font-size: 1.1rem; font-weight: 700; color: #F1F5F9; }
.p-sub   { font-size: 0.82rem; color: #94A3B8; margin-top: 2px; }
.online-badge { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.72rem; font-weight: 700; margin-top: 6px; }
.online-badge.on  { background: rgba(16,185,129,0.2); color: #10B981; }
.online-badge.off { background: rgba(239,68,68,0.15); color: #EF4444; }

.star-bar { display: flex; gap: 4px; margin: 6px 0; }
.star { color: #F59E0B; font-size: 1rem; }
.star.empty { color: #334155; }
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

st.title("🚚 Partner Management")

df = st.session_state.orders_df
partners = st.session_state.partners

# ── Partner cards (2 per row) ──────────────────────────────────────────────────
st.subheader("All Partners")
cols = st.columns(2)
for i, p in enumerate(partners):
    with cols[i % 2]:
        online_cls  = "on" if p.get("online") else "off"
        online_text = "🟢 Online" if p.get("online") else "⚫ Offline"
        rating = p.get("rating", 4.5)
        star_html = ""
        for s in range(5):
            star_html += '<span class="star' + (" empty" if s >= int(rating) else "") + '">★</span>'

        p_orders = df[df["partner_id"] == p["id"]]
        total_deliveries = len(p_orders[p_orders["status"] == "Delivered"])

        st.markdown(
            '<div class="partner-card">'
            '<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
            '<div>'
            '<div class="p-name">' + p["name"] + '</div>'
            '<div class="p-sub">📍 ' + p.get("area", "") + ' · 📞 ' + p.get("phone", "") + '</div>'
            '<div class="star-bar">' + star_html + ' <span style="font-size:0.8rem;color:#94A3B8;margin-left:4px;">' + str(rating) + '</span></div>'
            '</div>'
            '<span class="online-badge ' + online_cls + '">' + online_text + '</span>'
            '</div>'
            '<div style="margin-top:10px;display:flex;gap:16px;">'
            '<div style="font-size:0.82rem;color:#94A3B8;">Total Deliveries: <span style="color:#F1F5F9;font-weight:700;">' + str(total_deliveries) + '</span></div>'
            '<div style="font-size:0.82rem;color:#94A3B8;">Today: <span style="color:#10B981;font-weight:700;">' + str(p.get("today_trips", 0)) + ' trips · ₹' + str(int(p.get("today_earnings", 0))) + '</span></div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.expander("View Details — " + p["name"]):
            st.write("**Vehicle:** " + p.get("vehicle_number", "N/A"))
            st.write("**Rating:** " + str(p.get("rating", "")) + " ⭐")
            st.write("**Total Deliveries:** " + str(total_deliveries))
            st.write("**Today's Trips:** " + str(p.get("today_trips", 0)))
            st.write("**Today's Earnings:** ₹" + str(int(p.get("today_earnings", 0))))
            st.write("**Online Hours:** " + str(p.get("online_hours", 0)) + "h")

            recent_10 = p_orders.sort_values("created_at", ascending=False).head(10)
            if not recent_10.empty:
                st.markdown("**Recent Orders:**")
                for _, row in recent_10.iterrows():
                    st.caption(str(row["order_id"]) + " · " + str(row.get("service", "")) + " · " + str(row.get("status", "")) + " · ₹" + str(int(row.get("amount", 0))))

            # Rating breakdown (simulated)
            st.markdown("**Rating Breakdown:**")
            rating_dist = {5: 60, 4: 25, 3: 10, 2: 3, 1: 2}
            for stars in range(5, 0, -1):
                pct = rating_dist.get(stars, 0)
                st.markdown(str(stars) + "★ — " + str(pct) + "%")

            col_block, _ = st.columns(2)
            with col_block:
                if st.button("🚫 Block Partner", key="block_" + p["id"], type="secondary"):
                    st.error(p["name"] + " has been blocked (demo).")

# ── Add Partner form ──────────────────────────────────────────────────────────
st.markdown("---")
with st.expander("➕ Add New Partner"):
    with st.form("add_partner_form"):
        new_name  = st.text_input("Full Name")
        new_phone = st.text_input("Phone Number")
        new_area  = st.selectbox("Area", AREAS)
        new_veh   = st.text_input("Vehicle Number", placeholder="TS-09-AB-1234")
        submitted = st.form_submit_button("Add Partner", type="primary")
        if submitted:
            if new_name.strip() and new_phone.strip():
                new_id = "P" + str(len(st.session_state.partners) + 1).zfill(3)
                new_partner = {
                    "id": new_id,
                    "name": new_name.strip(),
                    "phone": new_phone.strip(),
                    "area": new_area,
                    "rating": 5.0,
                    "deliveries": 0,
                    "online": False,
                    "current_order": None,
                    "today_earnings": 0.0,
                    "today_trips": 0,
                    "online_hours": 0.0,
                    "vehicle_number": new_veh.strip(),
                }
                st.session_state.partners.append(new_partner)
                st.success("Partner " + new_name + " added with ID: " + new_id)
                st.rerun()
            else:
                st.error("Please fill in all required fields.")

# ── Performance table ──────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("📊 Performance Table")

perf_data = []
for p in partners:
    p_orders = df[df["partner_id"] == p["id"]]
    total_del = len(p_orders[p_orders["status"] == "Delivered"])
    total_ord = len(p_orders)
    acc_rate  = round(total_del / total_ord * 100, 1) if total_ord > 0 else 0
    mtd_earn  = int(p_orders[p_orders["status"] == "Delivered"]["amount"].sum() * 0.25)
    perf_data.append({
        "Partner": p["name"],
        "Rating": p.get("rating", 0),
        "Deliveries": total_del,
        "Acceptance Rate": str(acc_rate) + "%",
        "Earnings MTD": "₹" + str(mtd_earn),
        "Status": "Online" if p.get("online") else "Offline",
    })

perf_df = pd.DataFrame(perf_data)
st.dataframe(perf_df, use_container_width=True, hide_index=True)
