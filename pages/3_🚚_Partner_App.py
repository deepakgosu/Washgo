import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from utils.data import (
    init_session_state, PARTNERS, STATUSES, STATUS_COLORS, SERVICES,
)
from utils import database as db

st.set_page_config(
    page_title="Partner App – WashGo",
    page_icon="🚚",
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

.login-card {
    max-width: 440px; margin: 60px auto; background: #fff;
    border-radius: 20px; padding: 40px 36px;
    box-shadow: 0 4px 32px rgba(0,0,0,0.1); border: 1px solid #E8F5E9;
}
.login-title { text-align:center; font-size:24px; font-weight:800; color:#1B5E20; margin-bottom:8px; }
.login-sub   { text-align:center; font-size:14px; color:#757575; margin-bottom:28px; }

.metric-card {
    background: #fff; border-radius: 16px; padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center;
    border-top: 4px solid #2E7D32;
}
.metric-value { font-size: 30px; font-weight: 800; color: #2E7D32; }
.metric-label { font-size: 12px; color: #757575; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }

.order-card {
    background: #fff; border-radius: 16px; padding: 20px 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #E8F5E9;
    margin-bottom: 16px; border-left: 4px solid #2E7D32;
}
.order-card-id    { font-size: 13px; font-weight: 700; color: #FF6F00; }
.order-card-name  { font-size: 16px; font-weight: 700; color: #212121; margin: 4px 0; }
.order-card-meta  { font-size: 13px; color: #757575; }
.status-badge {
    display: inline-block; padding: 3px 12px; border-radius: 20px;
    font-size: 12px; font-weight: 700; color: #fff;
}
.completed-card {
    background: #F1F8E9; border-radius: 16px; padding: 16px 20px;
    border: 1px solid #C8E6C9; margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <span style='font-size:44px;'>🚚</span>
        <h2 style='margin:4px 0 0; font-size:24px; font-weight:800;'>WashGo</h2>
        <p style='font-size:12px; opacity:0.7; margin:0;'>Partner App</p>
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

    if st.session_state.logged_in_partner is not None:
        p = st.session_state.logged_in_partner
        st.markdown(f"""
        <div style='background:rgba(255,255,255,0.1); border-radius:12px; padding:14px; margin-bottom:12px;'>
            <div style='font-weight:700; font-size:15px;'>👤 {p['name']}</div>
            <div style='font-size:12px; opacity:0.8;'>ID: {p['id']} · ⭐ {p['rating']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in_partner = None
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.logged_in_partner is None:
    st.markdown("""
    <div class="page-header">
        <h1>🚚 Partner Login</h1>
        <p>WashGo Delivery Partner Portal</p>
    </div>
    """, unsafe_allow_html=True)

    _, login_col, _ = st.columns([1, 2, 1])
    with login_col:
        st.markdown("""
        <div style='background:#fff; border-radius:20px; padding:40px 36px;
             box-shadow:0 4px 32px rgba(0,0,0,0.1); border:1px solid #E8F5E9;'>
        <div style='text-align:center; font-size:52px; margin-bottom:8px;'>🚚</div>
        <div style='text-align:center; font-size:22px; font-weight:800; color:#1B5E20; margin-bottom:6px;'>Partner Login</div>
        <div style='text-align:center; font-size:14px; color:#757575; margin-bottom:24px;'>Sign in to your WashGo Partner account</div>
        </div>
        """, unsafe_allow_html=True)

        partner_ids = [p["id"] for p in PARTNERS]
        partner_labels = [f"{p['id']} – {p['name']}" for p in PARTNERS]
        selected_label = st.selectbox("Select Partner ID", partner_labels)
        partner_id = selected_label.split(" – ")[0]

        phone_input = st.text_input("Phone Number", placeholder="Enter your registered phone", type="password")
        login_btn = st.button("Login →", use_container_width=True, type="primary")

        if login_btn:
            matched = next((p for p in PARTNERS if p["id"] == partner_id), None)
            if matched and (phone_input == matched["phone"] or phone_input == ""):
                st.session_state.logged_in_partner = matched
                st.success(f"Welcome, {matched['name']}! Redirecting…")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")
                st.info("💡 Demo: Select any Partner ID and leave phone blank, or enter the registered phone.")

# ══════════════════════════════════════════════════════════════════════════════
# PARTNER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
else:
    partner = st.session_state.logged_in_partner
    df = st.session_state.orders_df

    # Filter orders for this partner
    partner_orders = df[df["partner_id"] == partner["id"]].copy()
    active_orders = partner_orders[partner_orders["status"] != "Delivered"]
    completed_orders = partner_orders[partner_orders["status"] == "Delivered"]

    today = datetime.now().date()
    today_orders = partner_orders[
        partner_orders["created_at"].apply(
            lambda x: x.date() if hasattr(x, "date") else datetime.fromisoformat(str(x)).date()
        ) == today
    ]

    today_completed = today_orders[today_orders["status"] == "Delivered"]
    today_pending   = today_orders[today_orders["status"] != "Delivered"]
    today_earnings  = today_completed["amount"].sum()

    # ── Page Header ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="page-header">
        <h1>🚚 Welcome, {partner['name']}!</h1>
        <p>Partner ID: {partner['id']} · ⭐ {partner['rating']} Rating · 📍 {partner['area']}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Today's Stats ─────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    stats = [
        (len(today_orders),      "📦", "Today's Orders",    "#2E7D32"),
        (len(today_completed),   "✅", "Completed Today",   "#43A047"),
        (len(today_pending),     "⏳", "Pending",           "#FF6F00"),
        (f"₹{today_earnings:.0f}", "💰", "Today's Earnings", "#1565C0"),
    ]
    for col, (val, icon, label, color) in zip([m1, m2, m3, m4], stats):
        with col:
            st.markdown(f"""
            <div class="metric-card" style='border-top-color:{color};'>
                <div style='font-size:28px;'>{icon}</div>
                <div class="metric-value" style='color:{color};'>{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs ──────────────────────────────────────────────────────────────────
    tab_active, tab_completed, tab_earnings = st.tabs(
        ["📦 Active Orders", "✅ Completed Orders", "💰 Earnings"]
    )

    # ── Tab 1: Active Orders ──────────────────────────────────────────────────
    with tab_active:
        if active_orders.empty:
            st.markdown("""
            <div style='text-align:center; padding:48px; color:#9E9E9E;'>
                <div style='font-size:48px;'>🎉</div>
                <h3 style='color:#616161;'>All caught up!</h3>
                <p>No active orders assigned to you right now.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**{len(active_orders)} active order(s) assigned to you**")
            for _, row in active_orders.iterrows():
                badge_color = STATUS_COLORS.get(row["status"], "#9E9E9E")
                svc_icon = SERVICES.get(row["service"], {}).get("icon", "🧺")

                with st.container():
                    st.markdown(f"""
                    <div class="order-card">
                        <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                            <div>
                                <div class="order-card-id">{row['order_id']}</div>
                                <div class="order-card-name">{row['customer_name']}</div>
                                <div class="order-card-meta">📍 {row['address']}</div>
                                <div class="order-card-meta" style='margin-top:4px;'>
                                    {svc_icon} {row['service']} &nbsp;·&nbsp; ₹{row['amount']:.2f}
                                    &nbsp;·&nbsp; {row['payment_method']}
                                </div>
                                <div class="order-card-meta" style='margin-top:4px;'>🕐 {row['time_slot']}</div>
                            </div>
                            <span class='status-badge' style='background:{badge_color};'>{row['status']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Status update
                    current_idx = STATUSES.index(row["status"]) if row["status"] in STATUSES else 0
                    next_statuses = STATUSES[current_idx:]
                    upd_col1, upd_col2 = st.columns([3, 1])
                    with upd_col1:
                        new_status = st.selectbox(
                            "Update Status",
                            next_statuses,
                            key=f"status_sel_{row['order_id']}",
                            label_visibility="collapsed",
                        )
                    with upd_col2:
                        if st.button("Update ✓", key=f"upd_{row['order_id']}", use_container_width=True, type="primary"):
                            mask = st.session_state.orders_df["order_id"] == row["order_id"]
                            new_idx = STATUSES.index(new_status)
                            st.session_state.orders_df.loc[mask, "status"] = new_status
                            st.session_state.orders_df.loc[mask, "status_idx"] = new_idx
                            db.update_order_status(row["order_id"], new_status, new_idx)
                            st.success(f"Order {row['order_id']} updated to **{new_status}**")
                            st.rerun()

                    st.markdown("---")

    # ── Tab 2: Completed Orders ───────────────────────────────────────────────
    with tab_completed:
        if completed_orders.empty:
            st.markdown("""
            <div style='text-align:center; padding:48px; color:#9E9E9E;'>
                <div style='font-size:48px;'>📭</div>
                <h3 style='color:#616161;'>No completed orders yet</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**{len(completed_orders)} delivered order(s)**")
            total_earnings = completed_orders["amount"].sum()
            avg_rating_val = completed_orders["rating"].dropna().mean()

            ce1, ce2 = st.columns(2)
            with ce1:
                st.metric("Total Earnings", f"₹{total_earnings:,.2f}")
            with ce2:
                st.metric("Avg Rating", f"{avg_rating_val:.1f} ⭐" if not pd.isna(avg_rating_val) else "N/A")

            st.markdown("<br>", unsafe_allow_html=True)
            for _, row in completed_orders.iterrows():
                svc_icon = SERVICES.get(row["service"], {}).get("icon", "🧺")
                rating_str = ("⭐" * int(row["rating"])) if pd.notna(row["rating"]) else "Not rated"
                st.markdown(f"""
                <div class='completed-card'>
                    <div style='display:flex; justify-content:space-between;'>
                        <div>
                            <div style='font-weight:700; color:#1B5E20;'>{row['order_id']} — {row['customer_name']}</div>
                            <div style='font-size:13px; color:#616161;'>{svc_icon} {row['service']} · ₹{row['amount']:.2f}</div>
                            <div style='font-size:13px; color:#616161;'>📍 {row['area']}</div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-size:16px;'>{rating_str}</div>
                            <div style='font-size:12px; color:#9E9E9E;'>
                                {row['created_at'].strftime('%d %b') if hasattr(row['created_at'],'strftime') else str(row['created_at'])[:10]}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 3: Earnings ───────────────────────────────────────────────────────
    with tab_earnings:
        total_all_earnings = partner_orders["amount"].sum()
        total_deliveries   = len(completed_orders)
        avg_order_val      = partner_orders["amount"].mean() if not partner_orders.empty else 0

        e1, e2, e3 = st.columns(3)
        with e1:
            st.metric("Total Earnings", f"₹{total_all_earnings:,.2f}")
        with e2:
            st.metric("Total Deliveries", total_deliveries)
        with e3:
            st.metric("Avg Order Value", f"₹{avg_order_val:.2f}")

        st.markdown("<br>", unsafe_allow_html=True)

        # Daily earnings chart (last 7 days)
        if not partner_orders.empty:
            partner_orders = partner_orders.copy()
            partner_orders["date"] = partner_orders["created_at"].apply(
                lambda x: x.date() if hasattr(x, "date") else datetime.fromisoformat(str(x)).date()
            )
            last_7 = [(datetime.now().date() - timedelta(days=i)) for i in range(6, -1, -1)]
            daily_earn = []
            for d in last_7:
                day_orders = partner_orders[partner_orders["date"] == d]
                daily_earn.append({
                    "Date": d.strftime("%d %b"),
                    "Earnings (₹)": day_orders["amount"].sum(),
                    "Orders": len(day_orders),
                })
            earn_df = pd.DataFrame(daily_earn)

            fig = px.bar(
                earn_df, x="Date", y="Earnings (₹)",
                title="Daily Earnings – Last 7 Days",
                color_discrete_sequence=["#2E7D32"],
                text="Earnings (₹)",
            )
            fig.update_traces(texttemplate="₹%{text:.0f}", textposition="outside")
            fig.update_layout(
                plot_bgcolor="#FAFAFA", paper_bgcolor="#FAFAFA",
                font=dict(family="Inter"), showlegend=False,
                title_font=dict(size=16, color="#1B5E20"),
                margin=dict(t=50, b=30),
            )
            st.plotly_chart(fig, use_container_width=True)

            # Service breakdown
            if not partner_orders.empty:
                svc_earn = partner_orders.groupby("service")["amount"].sum().reset_index()
                svc_earn.columns = ["Service", "Earnings"]
                fig2 = px.pie(
                    svc_earn, names="Service", values="Earnings",
                    title="Earnings by Service",
                    color_discrete_sequence=px.colors.sequential.Greens_r,
                )
                fig2.update_layout(
                    paper_bgcolor="#FAFAFA",
                    font=dict(family="Inter"),
                    title_font=dict(size=16, color="#1B5E20"),
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No earnings data available yet.")
