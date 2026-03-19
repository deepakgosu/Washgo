import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from utils.data import (
    init_session_state, STATUSES, STATUS_COLORS, SERVICES, PARTNERS,
)
from utils import database as db

st.set_page_config(
    page_title="Track Order – WashGo",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 100%);
}
section[data-testid="stSidebar"] * { color: #fff !important; }

.page-header {
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: #fff; border-radius: 16px; padding: 28px 36px; margin-bottom: 28px;
}
.page-header h1 { margin: 0; font-size: 32px; font-weight: 800; }
.page-header p  { margin: 6px 0 0; color: #A5D6A7; font-size: 15px; }

.search-box {
    background: #fff; border-radius: 16px; padding: 28px 32px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07); border: 1px solid #E8F5E9;
    margin-bottom: 24px;
}

/* Status stepper */
.stepper { display: flex; align-items: flex-start; justify-content: center; gap: 0; margin: 28px 0 36px; }
.step-wrap { display: flex; flex-direction: column; align-items: center; flex: 1; }
.step-dot {
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 13px; z-index: 1;
}
.step-dot-done    { background: #43A047; color: #fff; }
.step-dot-current { background: #FF6F00; color: #fff; box-shadow: 0 0 0 4px rgba(255,111,0,0.2); }
.step-dot-pending { background: #E0E0E0; color: #9E9E9E; }
.step-label-t { font-size: 11px; font-weight: 600; margin-top: 6px; text-align: center; max-width: 72px; }
.step-line { flex: 1; height: 3px; margin-top: 16px; }
.step-line-done    { background: #43A047; }
.step-line-pending { background: #E0E0E0; }

/* Detail card */
.detail-card {
    background: #fff; border-radius: 16px; padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #E8F5E9;
    margin-bottom: 16px;
}
.detail-card-title { font-size: 15px; font-weight: 700; color: #1B5E20; margin-bottom: 14px; }
.detail-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #F5F5F5; font-size: 14px; }
.detail-row:last-child { border-bottom: none; }
.detail-key { color: #757575; }
.detail-val { color: #212121; font-weight: 600; text-align: right; max-width: 180px; }

/* Status badge */
.status-badge {
    display: inline-block; padding: 4px 14px; border-radius: 20px;
    font-size: 13px; font-weight: 700; color: #fff;
}

/* Timeline */
.timeline-item { display: flex; gap: 16px; margin-bottom: 16px; }
.timeline-dot { width: 14px; height: 14px; border-radius: 50%; margin-top: 4px; flex-shrink: 0; }
.timeline-line { width: 2px; background: #E0E0E0; margin: 0 6px; }
.timeline-content { flex: 1; }
.timeline-status { font-weight: 600; font-size: 14px; color: #212121; }
.timeline-time   { font-size: 12px; color: #9E9E9E; margin-top: 2px; }

/* Partner card */
.partner-card {
    background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
    border-radius: 16px; padding: 24px; border: 1px solid #C8E6C9;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <span style='font-size:44px;'>📍</span>
        <h2 style='margin:4px 0 0; font-size:24px; font-weight:800;'>WashGo</h2>
        <p style='font-size:12px; opacity:0.7; margin:0;'>Track Your Order</p>
    </div>
    <hr style='border-color:rgba(255,255,255,0.2); margin:12px 0;'>
    """, unsafe_allow_html=True)
    st.page_link("app.py", label="🏠 Home")
    st.page_link("pages/1_🧺_Book_Laundry.py", label="🧺 Book Laundry")
    st.page_link("pages/2_📍_Track_Order.py", label="📍 Track Order")
    st.page_link("pages/3_🚚_Partner_App.py", label="🚚 Partner App")
    st.page_link("pages/4_📊_Admin_Dashboard.py", label="📊 Admin Dashboard")
    st.page_link("pages/5_ℹ️_About.py", label="ℹ️ About & Pricing")
    st.markdown("<hr style='border-color:rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:13px; opacity:0.8; padding:8px 0;'>
        🔍 Enter your WashGo Order ID (e.g. WG12345) to track your laundry.
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>📍 Track Your Order</h1>
    <p>Real-time status of your laundry order</p>
</div>
""", unsafe_allow_html=True)

# ── Search ────────────────────────────────────────────────────────────────────
default_oid = st.session_state.last_order_id or ""

with st.container():
    st.markdown("<div class='search-box'>", unsafe_allow_html=True)
    sc1, sc2, sc3 = st.columns([3, 1, 1])
    with sc1:
        order_input = st.text_input(
            "Enter Order ID",
            value=default_oid,
            placeholder="e.g. WG10042",
            label_visibility="collapsed",
        )
    with sc2:
        search_btn = st.button("🔍 Search", use_container_width=True, type="primary")
    with sc3:
        if st.button("🧺 Book New Order", use_container_width=True):
            st.switch_page("pages/1_🧺_Book_Laundry.py")
    st.markdown("</div>", unsafe_allow_html=True)

# ── Lookup order ──────────────────────────────────────────────────────────────
search_oid = order_input.strip().upper()
df = st.session_state.orders_df

if search_oid:
    order_row = df[df["order_id"] == search_oid]

    if order_row.empty:
        st.error(f"❌ No order found with ID **{search_oid}**. Please check and try again.")
        st.info("💡 Tip: Order IDs look like **WG10042** – check your booking confirmation.")
    else:
        order = order_row.iloc[0]
        status_idx = int(order["status_idx"])
        current_status = STATUSES[status_idx]

        # ── Order Header ──────────────────────────────────────────────────────
        svc_info = SERVICES.get(order["service"], {})
        svc_icon = svc_info.get("icon", "🧺")

        hdr_col1, hdr_col2 = st.columns([3, 1])
        with hdr_col1:
            st.markdown(f"### {svc_icon} Order #{order['order_id']} — {order['service']}")
        with hdr_col2:
            badge_color = STATUS_COLORS.get(current_status, "#9E9E9E")
            st.markdown(f"""
            <div style='text-align:right; padding-top:8px;'>
                <span class='status-badge' style='background:{badge_color};'>{current_status}</span>
            </div>""", unsafe_allow_html=True)

        # ── Status Stepper ────────────────────────────────────────────────────
        stepper_html = "<div class='stepper'>"
        for i, status in enumerate(STATUSES):
            if i < status_idx:
                dot_cls = "step-dot-done"
                icon = "✓"
            elif i == status_idx:
                dot_cls = "step-dot-current"
                icon = str(i + 1)
            else:
                dot_cls = "step-dot-pending"
                icon = str(i + 1)

            label_color = "#1B5E20" if i <= status_idx else "#9E9E9E"
            stepper_html += f"""
            <div class='step-wrap'>
                <div class='step-dot {dot_cls}'>{icon}</div>
                <div class='step-label-t' style='color:{label_color};'>{status}</div>
            </div>"""

            if i < len(STATUSES) - 1:
                line_cls = "step-line-done" if i < status_idx else "step-line-pending"
                stepper_html += f"<div class='step-line {line_cls}'></div>"

        stepper_html += "</div>"
        st.markdown(stepper_html, unsafe_allow_html=True)

        # ── Two-column detail section ─────────────────────────────────────────
        left_col, right_col = st.columns([3, 2])

        with left_col:
            # Order Details
            unit_label = svc_info.get("unit", "kg")
            qty_val = float(order["weight_kg"]) if unit_label == "kg" else int(order["pieces"])

            st.markdown(f"""
            <div class='detail-card'>
                <div class='detail-card-title'>📋 Order Details</div>
                <div class='detail-row'><span class='detail-key'>Order ID</span><span class='detail-val'>{order['order_id']}</span></div>
                <div class='detail-row'><span class='detail-key'>Customer</span><span class='detail-val'>{order['customer_name']}</span></div>
                <div class='detail-row'><span class='detail-key'>Phone</span><span class='detail-val'>{order['phone']}</span></div>
                <div class='detail-row'><span class='detail-key'>Pickup Address</span><span class='detail-val'>{order['address']}</span></div>
                <div class='detail-row'><span class='detail-key'>Service</span><span class='detail-val'>{svc_icon} {order['service']}</span></div>
                <div class='detail-row'><span class='detail-key'>Quantity</span><span class='detail-val'>{qty_val} {unit_label}</span></div>
                <div class='detail-row'><span class='detail-key'>Pickup Slot</span><span class='detail-val'>{order['time_slot']}</span></div>
                <div class='detail-row'><span class='detail-key'>Delivery Type</span><span class='detail-val'>{order['delivery_type']}</span></div>
                <div class='detail-row'><span class='detail-key'>Amount</span><span class='detail-val' style='color:#FF6F00;'>₹{order['amount']:.2f}</span></div>
                <div class='detail-row'><span class='detail-key'>Payment</span><span class='detail-val'>{order['payment_method']} · {order['payment_status']}</span></div>
            </div>
            """, unsafe_allow_html=True)

            # Timeline
            st.markdown(f"""<div class='detail-card'><div class='detail-card-title'>🕐 Status Timeline</div>""",
                        unsafe_allow_html=True)

            created_at = order["created_at"]
            if isinstance(created_at, str):
                try:
                    created_at = datetime.fromisoformat(created_at)
                except Exception:
                    created_at = datetime.now() - timedelta(hours=4)

            offsets_hours = [0, 0.5, 1.5, 3, 5, 8]
            timeline_html = ""
            for i, status in enumerate(STATUSES):
                if i > status_idx:
                    break
                ts = created_at + timedelta(hours=offsets_hours[i])
                color = STATUS_COLORS.get(status, "#9E9E9E")
                timeline_html += f"""
                <div class='timeline-item'>
                    <div style='display:flex; flex-direction:column; align-items:center;'>
                        <div class='timeline-dot' style='background:{color};'></div>
                        {'<div class="timeline-line" style="flex:1;"></div>' if i < status_idx else ''}
                    </div>
                    <div class='timeline-content'>
                        <div class='timeline-status'>{status}</div>
                        <div class='timeline-time'>{ts.strftime("%d %b %Y · %I:%M %p")}</div>
                    </div>
                </div>"""

            st.markdown(timeline_html + "</div>", unsafe_allow_html=True)

        with right_col:
            # Partner Card
            partner_info = None
            for p in PARTNERS:
                if p["id"] == order["partner_id"]:
                    partner_info = p
                    break

            if partner_info:
                st.markdown(f"""
                <div class='partner-card'>
                    <div class='detail-card-title'>🚚 Delivery Partner</div>
                    <div style='display:flex; gap:16px; align-items:center;'>
                        <div style='font-size:40px;'>👤</div>
                        <div>
                            <div style='font-weight:700; font-size:16px; color:#1B5E20;'>{partner_info['name']}</div>
                            <div style='color:#616161; font-size:14px; margin-top:2px;'>📞 {partner_info['phone']}</div>
                            <div style='color:#616161; font-size:14px;'>⭐ {partner_info['rating']} rating</div>
                            <div style='color:#616161; font-size:14px;'>🚚 {partner_info['deliveries']} deliveries</div>
                            <div style='color:#616161; font-size:14px;'>📍 {partner_info['area']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # Facility Card
            st.markdown(f"""
            <div class='detail-card'>
                <div class='detail-card-title'>🏭 Processing Facility</div>
                <div style='display:flex; gap:16px; align-items:center;'>
                    <div style='font-size:36px;'>🏭</div>
                    <div>
                        <div style='font-weight:700; font-size:15px; color:#1B5E20;'>{order['facility']}</div>
                        <div style='color:#388E3C; font-size:14px; margin-top:4px;'>✅ Certified Partner Facility</div>
                        <div style='color:#616161; font-size:13px;'>Quality checked & professional care</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Special Instructions
            if order.get("special_instructions"):
                st.markdown(f"""
                <div class='detail-card'>
                    <div class='detail-card-title'>📝 Special Instructions</div>
                    <div style='color:#424242; font-size:14px; line-height:1.6;'>{order['special_instructions']}</div>
                </div>
                """, unsafe_allow_html=True)

            # Rating Widget (only if delivered and no rating yet)
            if current_status == "Delivered":
                existing_rating = order.get("rating")
                if pd.isna(existing_rating) or existing_rating is None:
                    st.markdown("""
                    <div class='detail-card'>
                        <div class='detail-card-title'>⭐ Rate Your Experience</div>
                    </div>
                    """, unsafe_allow_html=True)
                    rating_val = st.select_slider(
                        "Your Rating",
                        options=[1, 2, 3, 4, 5],
                        value=5,
                        format_func=lambda x: "⭐" * x,
                    )
                    rating_note = st.text_area("Leave a comment (optional)", height=70)
                    if st.button("Submit Rating ⭐", use_container_width=True, type="primary"):
                        mask = st.session_state.orders_df["order_id"] == search_oid
                        st.session_state.orders_df.loc[mask, "rating"] = rating_val
                        db.save_rating(search_oid, rating_val)
                        st.success(f"Thank you! You rated this order {rating_val} ⭐")
                        st.rerun()
                else:
                    st.markdown(f"""
                    <div class='detail-card'>
                        <div class='detail-card-title'>⭐ Your Rating</div>
                        <div style='font-size:28px;'>{"⭐" * int(existing_rating)}</div>
                        <div style='color:#616161; font-size:14px;'>{int(existing_rating)} out of 5 stars</div>
                    </div>
                    """, unsafe_allow_html=True)

else:
    # Landing state – no search yet
    st.markdown("""
    <div style='text-align:center; padding:60px 20px; color:#9E9E9E;'>
        <div style='font-size:64px; margin-bottom:16px;'>📦</div>
        <h3 style='color:#616161;'>Enter your Order ID above to track your laundry</h3>
        <p style='max-width:400px; margin:0 auto; line-height:1.6;'>
            Your Order ID was sent via WhatsApp/SMS after booking.
            It looks like <strong>WG10042</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
