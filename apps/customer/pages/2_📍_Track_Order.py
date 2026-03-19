import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from utils.store import get_store, update_order_status
from utils.data import STATUSES, STATUS_COLORS, SERVICES, PARTNERS

st.set_page_config(page_title="Track Order – WashGo", page_icon="📍", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F5F5F5; }
[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E0E0E0; }
[data-testid="stSidebar"] * { color: #1A1A1A !important; }

.page-title { font-size: 1.6rem; font-weight: 800; color: #1A1A1A; margin-bottom: 4px; }
.page-sub   { font-size: 0.9rem; color: #888; margin-bottom: 24px; }

.timeline-wrap { padding: 8px 0; }
.tl-step {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 0;
    position: relative;
}
.tl-line {
    position: absolute;
    left: 15px;
    top: 32px;
    width: 2px;
    height: 40px;
    background: #E0E0E0;
}
.tl-line.done { background: #00C853; }
.tl-circle {
    width: 32px; height: 32px;
    border-radius: 50%;
    background: #E0E0E0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.8rem; font-weight: 700;
    color: #888;
    flex-shrink: 0;
    z-index: 1;
}
.tl-circle.done    { background: #00C853; color: #fff; }
.tl-circle.current { background: #1A1A1A; color: #fff; box-shadow: 0 0 0 4px rgba(0,200,83,0.3); }
.tl-content { padding-bottom: 32px; }
.tl-label   { font-size: 0.92rem; font-weight: 600; color: #1A1A1A; }
.tl-sub     { font-size: 0.8rem; color: #888; margin-top: 2px; }
.tl-sub.active { color: #00C853; }

.partner-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 16px;
    border: 1px solid #F0F0F0;
    display: flex;
    align-items: center;
    gap: 16px;
}
.partner-avatar {
    width: 52px; height: 52px;
    border-radius: 50%;
    background: #00C853;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem; font-weight: 700;
    color: #fff;
    flex-shrink: 0;
}
.partner-name    { font-size: 1rem; font-weight: 700; color: #1A1A1A; }
.partner-vehicle { font-size: 0.82rem; color: #888; margin-top: 2px; }
.partner-rating  { font-size: 0.88rem; color: #FFA000; margin-top: 2px; }

.order-summary {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 20px 24px;
    margin-top: 16px;
    border: 1px solid #F0F0F0;
}
.summary-row {
    display: flex; justify-content: space-between;
    font-size: 0.88rem; padding: 6px 0;
    border-bottom: 1px solid #F5F5F5;
}
.summary-row:last-child { border-bottom: none; }
.sl { color: #888; }
.sv { font-weight: 600; color: #1A1A1A; }
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

st.markdown('<div class="page-title">📍 Track Order</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Real-time status updates for your order.</div>', unsafe_allow_html=True)

order_id_input = st.text_input("Enter Order ID", placeholder="e.g. WG10023", value=st.session_state.get("last_order_id", "") or "")

df = st.session_state.orders_df

if order_id_input:
    row_df = df[df["order_id"] == order_id_input.strip().upper()]
    if row_df.empty:
        row_df = df[df["order_id"] == order_id_input.strip()]
    if row_df.empty:
        st.error("Order not found. Please check the Order ID.")
    else:
        row = row_df.iloc[0]
        current_idx = int(row.get("status_idx", 0))

        st.markdown("---")

        TIMELINE_STEPS = [
            ("Order Placed",      "🟢", "Your order has been confirmed."),
            ("Picked Up",         "🔵", row.get("partner_name", "Partner") + " picked up your laundry."),
            ("At Facility",       "🏭", row.get("facility", "Facility") + " received your order."),
            ("Processing",        "⚙️",  "Your laundry is being processed."),
            ("Out for Delivery",  "🚚", "On the way! Estimated arrival soon."),
            ("Delivered",         "✅", "Your laundry has been delivered."),
        ]

        st.markdown("### 🗺️ Order Status")
        st.markdown('<div class="timeline-wrap">', unsafe_allow_html=True)
        for i, (label, icon, detail) in enumerate(TIMELINE_STEPS):
            if i < current_idx:
                circle_cls = "done"
                sub_text   = "✓ " + detail
                sub_cls    = ""
            elif i == current_idx:
                circle_cls = "current"
                sub_text   = detail
                sub_cls    = "active"
            else:
                circle_cls = ""
                sub_text   = "Pending"
                sub_cls    = ""

            line_cls = "done" if i < current_idx else ""
            line_html = '<div class="tl-line ' + line_cls + '"></div>' if i < len(TIMELINE_STEPS) - 1 else ""

            st.markdown(
                '<div class="tl-step">'
                '<div style="position:relative;">'
                '<div class="tl-circle ' + circle_cls + '">' + icon + '</div>'
                + line_html +
                '</div>'
                '<div class="tl-content">'
                '<div class="tl-label">' + label + '</div>'
                '<div class="tl-sub ' + sub_cls + '">' + sub_text + '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # ── Partner card ───────────────────────────────────────────────────────
        if current_idx >= 1:
            partner_name = str(row.get("partner_name", "Partner"))
            initials = "".join([w[0].upper() for w in partner_name.split()[:2]])
            partner_data = next((p for p in PARTNERS if p["name"] == partner_name), None)
            rating = partner_data["rating"] if partner_data else 4.7
            phone  = partner_data["phone"]  if partner_data else "9876543210"
            stars  = "★" * int(rating) + "☆" * (5 - int(rating))
            vehicle_num = "TS-09-AB-" + str(1000 + hash(partner_name) % 9000)

            st.markdown("### 🚗 Your Delivery Partner")
            st.markdown(
                '<div class="partner-card">'
                '<div class="partner-avatar">' + initials + '</div>'
                '<div style="flex:1;">'
                '<div class="partner-name">' + partner_name + '</div>'
                '<div class="partner-vehicle">🏍️ Bike · ' + vehicle_num + '</div>'
                '<div class="partner-rating">' + stars + ' ' + str(rating) + '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
            with st.expander("📞 Contact Partner"):
                st.write("Phone: " + phone)
                st.info("Call your delivery partner at: **" + phone + "**")

        # ── Order summary ──────────────────────────────────────────────────────
        svc_icon = SERVICES.get(str(row.get("service", "")), {}).get("icon", "🧺")
        created_str = row["created_at"].strftime("%d %b %Y, %I:%M %p") if hasattr(row.get("created_at"), "strftime") else str(row.get("created_at", ""))[:16]

        st.markdown("### 📋 Order Summary")
        st.markdown(
            '<div class="order-summary">'
            '<div class="summary-row"><span class="sl">Order ID</span><span class="sv">' + str(row["order_id"]) + '</span></div>'
            '<div class="summary-row"><span class="sl">Service</span><span class="sv">' + svc_icon + " " + str(row.get("service", "")) + '</span></div>'
            '<div class="summary-row"><span class="sl">Area</span><span class="sv">' + str(row.get("area", "")) + '</span></div>'
            '<div class="summary-row"><span class="sl">Facility</span><span class="sv">' + str(row.get("facility", "")) + '</span></div>'
            '<div class="summary-row"><span class="sl">Amount</span><span class="sv">₹' + str(int(row.get("amount", 0))) + '</span></div>'
            '<div class="summary-row"><span class="sl">Payment</span><span class="sv">' + str(row.get("payment_method", "")) + '</span></div>'
            '<div class="summary-row"><span class="sl">Placed At</span><span class="sv">' + created_str + '</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

        # ── Simulate progress (demo) ──────────────────────────────────────────
        st.markdown("---")
        st.caption("Demo: Simulate order progress")
        if st.button("⚡ Simulate Next Status", use_container_width=True):
            if current_idx < len(STATUSES) - 1:
                new_status = STATUSES[current_idx + 1]
                update_order_status(row["order_id"], new_status)
                st.success("Status updated to: " + new_status)
                st.rerun()
            else:
                st.info("Order is already delivered!")
else:
    cust = st.session_state.customer
    if cust.get("phone"):
        active = df[
            (df["phone"] == cust["phone"]) &
            (~df["status"].isin(["Delivered"]))
        ]
        if not active.empty:
            st.markdown("**Your active orders:**")
            for _, row in active.iterrows():
                status_color = STATUS_COLORS.get(row["status"], "#888")
                if st.button(
                    str(row["order_id"]) + " · " + str(row["service"]) + " · " + str(row["status"]),
                    key="active_" + str(row["order_id"])
                ):
                    st.session_state["track_order_id"] = row["order_id"]
                    st.rerun()
