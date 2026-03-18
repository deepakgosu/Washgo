import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

from utils.data import (
    init_session_state, SERVICES, AREAS, PARTNERS, FACILITIES,
    STATUSES, STATUS_COLORS, DELIVERY_FEE,
)

st.set_page_config(
    page_title="Admin Dashboard – WashGo",
    page_icon="📊",
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

.admin-header {
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    color: #fff; border-radius: 16px; padding: 28px 36px; margin-bottom: 28px;
    display: flex; justify-content: space-between; align-items: center;
}
.admin-header h1 { margin: 0; font-size: 28px; font-weight: 800; }
.admin-header p  { margin: 4px 0 0; color: #A5D6A7; font-size: 14px; }

.kpi-card {
    background: #fff; border-radius: 16px; padding: 22px 24px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07); border-left: 6px solid #2E7D32;
}
.kpi-value  { font-size: 32px; font-weight: 800; color: #1B5E20; }
.kpi-label  { font-size: 12px; color: #757575; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }
.kpi-change { font-size: 13px; margin-top: 6px; font-weight: 600; }

.section-title { font-size: 18px; font-weight: 700; color: #1B5E20; margin: 24px 0 12px; }
.chart-card {
    background: #fff; border-radius: 16px; padding: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #E8F5E9;
}

.status-bar-wrap { margin-bottom: 10px; }
.status-bar-label { display: flex; justify-content: space-between; margin-bottom: 4px; font-size: 13px; }
.status-bar-outer { background: #F5F5F5; border-radius: 6px; height: 22px; }
.status-bar-inner { border-radius: 6px; height: 100%; display: flex; align-items: center;
                    padding-left: 10px; font-size: 12px; font-weight: 700; color: #fff; }

.partner-row {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 0; border-bottom: 1px solid #F5F5F5; font-size: 14px;
}
.partner-row:last-child { border-bottom: none; }

.login-wrap {
    max-width: 400px; margin: 80px auto; background: #fff;
    border-radius: 20px; padding: 44px 36px;
    box-shadow: 0 4px 32px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <span style='font-size:44px;'>📊</span>
        <h2 style='margin:4px 0 0; font-size:24px; font-weight:800;'>WashGo</h2>
        <p style='font-size:12px; opacity:0.7; margin:0;'>Admin Dashboard</p>
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

    if st.session_state.admin_logged_in:
        st.markdown("**🗓 Date Range Filter**")
        df_full = st.session_state.orders_df
        min_date = df_full["created_at"].min()
        max_date = df_full["created_at"].max()
        if hasattr(min_date, "date"):
            min_d, max_d = min_date.date(), max_date.date()
        else:
            min_d = max_d = datetime.now().date()

        date_range = st.date_input(
            "Select Date Range",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d,
            label_visibility="collapsed",
        )

        st.markdown("**📍 Area Filter**")
        selected_areas = st.multiselect(
            "Areas", AREAS, default=[], label_visibility="collapsed",
            placeholder="All areas",
        )

        st.markdown("<hr style='border-color:rgba(255,255,255,0.2);'>", unsafe_allow_html=True)

        # Download CSV
        csv_bytes = df_full.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Download Orders CSV",
            data=csv_bytes,
            file_name="washgo_orders.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.markdown("<hr style='border-color:rgba(255,255,255,0.2);'>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_logged_in = False
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN GATE
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.admin_logged_in:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 0;'>
        <span style='font-size:56px;'>📊</span>
        <h2 style='color:#1B5E20; font-size:28px; font-weight:800;'>Admin Login</h2>
        <p style='color:#757575;'>WashGo Operations Dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    _, lc, _ = st.columns([1, 2, 1])
    with lc:
        with st.form("admin_login"):
            username = st.text_input("Username", placeholder="admin")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            login_btn = st.form_submit_button("Login →", use_container_width=True, type="primary")

        if login_btn:
            if username == "admin" and password == "washgo123":
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful! Loading dashboard…")
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Use admin / washgo123")
        st.markdown("""
        <div style='text-align:center; background:#E8F5E9; border-radius:8px;
             padding:12px; margin-top:12px; font-size:13px; color:#388E3C;'>
            Demo credentials: <strong>admin</strong> / <strong>washgo123</strong>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ADMIN DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
else:
    df_all = st.session_state.orders_df.copy()

    # ── Apply sidebar date/area filters ──────────────────────────────────────
    try:
        if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
            start_d, end_d = date_range
            df_all = df_all[
                df_all["created_at"].apply(
                    lambda x: x.date() if hasattr(x, "date") else datetime.fromisoformat(str(x)).date()
                ).between(start_d, end_d)
            ]
    except Exception:
        pass

    try:
        if selected_areas:
            df_all = df_all[df_all["area"].isin(selected_areas)]
    except Exception:
        pass

    # ── Header ────────────────────────────────────────────────────────────────
    today_str = datetime.now().strftime("%A, %d %B %Y")
    st.markdown(f"""
    <div class="admin-header">
        <div>
            <h1>📊 WashGo Operations Dashboard</h1>
            <p>{today_str} · {len(df_all):,} orders in view</p>
        </div>
        <div style='font-size:13px; background:rgba(255,255,255,0.15); border-radius:10px; padding:10px 18px;'>
            🟢 System Online &nbsp;·&nbsp; v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Row ───────────────────────────────────────────────────────────────
    total_revenue   = df_all["amount"].sum()
    total_orders    = len(df_all)
    avg_order_val   = df_all["amount"].mean() if total_orders else 0
    active_partners = len(PARTNERS)
    avg_rating      = df_all["rating"].dropna().mean() if not df_all.empty else 0

    k1, k2, k3, k4 = st.columns(4)
    kpis = [
        (f"₹{total_revenue:,.0f}", "💰 Total Revenue",     "#2E7D32", ""),
        (f"{total_orders:,}",      "📦 Total Orders",      "#1565C0", ""),
        (f"₹{avg_order_val:,.0f}", "🧾 Avg Order Value",   "#FF6F00", ""),
        (f"{active_partners}",     "🚚 Active Partners",   "#6A1B9A", ""),
    ]
    for col, (val, label, color, change) in zip([k1, k2, k3, k4], kpis):
        with col:
            st.markdown(f"""
            <div class="kpi-card" style='border-left-color:{color};'>
                <div class="kpi-value" style='color:{color};'>{val}</div>
                <div class="kpi-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 2: Line + Pie + Bar ───────────────────────────────────────────────
    r2c1, r2c2, r2c3 = st.columns(3)

    with r2c1:
        # Orders per day (last 30 days)
        df_all_copy = df_all.copy()
        df_all_copy["date"] = df_all_copy["created_at"].apply(
            lambda x: x.date() if hasattr(x, "date") else datetime.fromisoformat(str(x)).date()
        )
        last30 = [(datetime.now().date() - timedelta(days=i)) for i in range(29, -1, -1)]
        daily_counts = df_all_copy.groupby("date").size().reset_index(name="Orders")
        all_dates = pd.DataFrame({"date": last30})
        daily_counts = all_dates.merge(daily_counts, on="date", how="left").fillna(0)
        daily_counts["Date"] = daily_counts["date"].apply(lambda x: x.strftime("%d %b"))

        fig_line = px.line(
            daily_counts, x="Date", y="Orders",
            title="Orders Per Day (Last 30 Days)",
            color_discrete_sequence=["#2E7D32"],
            markers=True,
        )
        fig_line.update_layout(
            plot_bgcolor="#FAFAFA", paper_bgcolor="#fff",
            font=dict(family="Inter"), title_font=dict(size=14, color="#1B5E20"),
            margin=dict(t=44, b=20, l=20, r=20),
            xaxis=dict(tickangle=-45, showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="#F0F0F0"),
        )
        fig_line.update_traces(line_width=2.5)
        st.plotly_chart(fig_line, use_container_width=True)

    with r2c2:
        # Orders by service
        if not df_all.empty:
            svc_counts = df_all["service"].value_counts().reset_index()
            svc_counts.columns = ["Service", "Orders"]
            fig_pie = px.pie(
                svc_counts, names="Service", values="Orders",
                title="Orders by Service",
                color_discrete_sequence=px.colors.sequential.Greens_r,
                hole=0.0,
            )
            fig_pie.update_layout(
                paper_bgcolor="#fff", font=dict(family="Inter"),
                title_font=dict(size=14, color="#1B5E20"),
                margin=dict(t=44, b=20),
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data available.")

    with r2c3:
        # Orders by area (top 8)
        if not df_all.empty:
            area_counts = df_all["area"].value_counts().head(8).reset_index()
            area_counts.columns = ["Area", "Orders"]
            fig_bar = px.bar(
                area_counts, x="Orders", y="Area", orientation="h",
                title="Orders by Area (Top 8)",
                color="Orders",
                color_continuous_scale="Greens",
            )
            fig_bar.update_layout(
                plot_bgcolor="#FAFAFA", paper_bgcolor="#fff",
                font=dict(family="Inter"), title_font=dict(size=14, color="#1B5E20"),
                margin=dict(t=44, b=20, l=10, r=20),
                yaxis=dict(autorange="reversed"),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No data available.")

    # ── Row 3: Revenue by service + Payment split ─────────────────────────────
    r3c1, r3c2 = st.columns(2)

    with r3c1:
        if not df_all.empty:
            rev_by_svc = df_all.groupby("service")["amount"].sum().reset_index()
            rev_by_svc.columns = ["Service", "Revenue"]
            rev_by_svc = rev_by_svc.sort_values("Revenue", ascending=True)
            fig_rev = px.bar(
                rev_by_svc, x="Revenue", y="Service", orientation="h",
                title="Revenue by Service (₹)",
                color="Revenue",
                color_continuous_scale="Greens",
                text="Revenue",
            )
            fig_rev.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            fig_rev.update_layout(
                plot_bgcolor="#FAFAFA", paper_bgcolor="#fff",
                font=dict(family="Inter"), title_font=dict(size=14, color="#1B5E20"),
                margin=dict(t=44, b=20, l=10, r=80),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_rev, use_container_width=True)
        else:
            st.info("No data available.")

    with r3c2:
        if not df_all.empty:
            pay_counts = df_all["payment_method"].value_counts().reset_index()
            pay_counts.columns = ["Method", "Count"]
            fig_donut = px.pie(
                pay_counts, names="Method", values="Count",
                title="Payment Method Split",
                hole=0.5,
                color_discrete_sequence=["#2E7D32", "#FF6F00", "#1565C0", "#6A1B9A"],
            )
            fig_donut.update_layout(
                paper_bgcolor="#fff", font=dict(family="Inter"),
                title_font=dict(size=14, color="#1B5E20"),
                margin=dict(t=44, b=20),
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        else:
            st.info("No data available.")

    # ── Row 4: Partner performance + Status funnel ────────────────────────────
    r4c1, r4c2 = st.columns(2)

    with r4c1:
        st.markdown("<div class='section-title'>🚚 Partner Performance</div>", unsafe_allow_html=True)
        partner_table_rows = []
        for p in PARTNERS:
            p_orders = df_all[df_all["partner_id"] == p["id"]]
            p_delivered = p_orders[p_orders["status"] == "Delivered"]
            p_earnings  = p_orders["amount"].sum()
            p_avg_rating = p_orders["rating"].dropna().mean()
            partner_table_rows.append({
                "Partner": p["name"],
                "ID": p["id"],
                "Area": p["area"],
                "Deliveries": len(p_delivered),
                "Rating": round(p_avg_rating, 1) if not pd.isna(p_avg_rating) else p["rating"],
                "Earnings (₹)": round(p_earnings, 2),
            })
        perf_df = pd.DataFrame(partner_table_rows)
        st.dataframe(
            perf_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Earnings (₹)": st.column_config.NumberColumn("Earnings (₹)", format="₹%.2f"),
                "Rating": st.column_config.NumberColumn("Rating", format="⭐ %.1f"),
            },
        )

    with r4c2:
        st.markdown("<div class='section-title'>📊 Order Status Funnel</div>", unsafe_allow_html=True)
        if not df_all.empty:
            status_counts = df_all["status"].value_counts()
            max_count = status_counts.max() if not status_counts.empty else 1

            for status in STATUSES:
                count = status_counts.get(status, 0)
                pct = (count / max_count * 100) if max_count else 0
                color = STATUS_COLORS.get(status, "#9E9E9E")
                st.markdown(f"""
                <div class="status-bar-wrap">
                    <div class="status-bar-label">
                        <span style='font-weight:600;color:#424242;'>{status}</span>
                        <span style='color:#757575;'>{count} orders</span>
                    </div>
                    <div class="status-bar-outer">
                        <div class="status-bar-inner" style='width:{max(pct,3):.0f}%; background:{color};'>
                            {f"{pct:.0f}%" if pct > 8 else ""}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No data available.")

    # ── Orders Table ──────────────────────────────────────────────────────────
    st.markdown("<div class='section-title'>📋 Orders Table</div>", unsafe_allow_html=True)

    # Filters
    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1:
        filter_area = st.multiselect("Filter by Area", AREAS, key="tbl_area",
                                     placeholder="All areas", label_visibility="collapsed")
    with fc2:
        filter_service = st.multiselect("Filter by Service", list(SERVICES.keys()), key="tbl_svc",
                                        placeholder="All services", label_visibility="collapsed")
    with fc3:
        filter_status = st.multiselect("Filter by Status", STATUSES, key="tbl_status",
                                       placeholder="All statuses", label_visibility="collapsed")
    with fc4:
        filter_payment = st.multiselect("Filter by Payment", ["UPI", "Card", "Cash", "Wallet"], key="tbl_pay",
                                        placeholder="All methods", label_visibility="collapsed")

    table_df = df_all.copy()
    if filter_area:
        table_df = table_df[table_df["area"].isin(filter_area)]
    if filter_service:
        table_df = table_df[table_df["service"].isin(filter_service)]
    if filter_status:
        table_df = table_df[table_df["status"].isin(filter_status)]
    if filter_payment:
        table_df = table_df[table_df["payment_method"].isin(filter_payment)]

    display_cols = ["order_id", "customer_name", "area", "service", "amount", "status", "payment_method", "created_at"]
    display_df = table_df[display_cols].copy()
    display_df.columns = ["Order ID", "Customer", "Area", "Service", "Amount (₹)", "Status", "Payment", "Date"]
    display_df["Date"] = display_df["Date"].apply(
        lambda x: x.strftime("%d %b %Y %H:%M") if hasattr(x, "strftime") else str(x)[:16]
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=400,
        column_config={
            "Amount (₹)": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
        },
    )
    st.caption(f"Showing {len(display_df):,} of {len(df_all):,} orders")
