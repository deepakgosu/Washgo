import streamlit as st
import pandas as pd
from utils.data import (
    init_session_state, SERVICES, AREAS, PARTNERS, FACILITIES,
    TIME_SLOTS, DELIVERY_FEE
)

st.set_page_config(
    page_title="WashGo – Laundry on Demand",
    page_icon="🧺",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Hide default Streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 60%, #388E3C 100%);
}
section[data-testid="stSidebar"] * { color: #ffffff !important; }
section[data-testid="stSidebar"] .stButton>button {
    background: #FF6F00; color: #fff !important;
    border: none; border-radius: 8px; font-weight: 600;
    width: 100%; margin-top: 8px;
}
section[data-testid="stSidebar"] .stButton>button:hover { background: #E65100; }

/* Hero */
.hero-box {
    background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 50%, #388E3C 100%);
    border-radius: 20px; padding: 60px 48px; margin-bottom: 32px;
    text-align: center; color: #ffffff;
    box-shadow: 0 8px 32px rgba(46,125,50,0.25);
}
.hero-title { font-size: 72px; font-weight: 800; letter-spacing: -2px; margin: 0; }
.hero-tagline { font-size: 24px; font-weight: 600; color: #C8E6C9; margin: 8px 0 16px; }
.hero-sub { font-size: 16px; color: #A5D6A7; max-width: 560px; margin: 0 auto 32px; line-height: 1.6; }

/* CTA buttons */
.cta-row { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
.cta-primary {
    background: #FF6F00; color: #fff; border: none;
    padding: 14px 36px; border-radius: 50px; font-size: 16px; font-weight: 700;
    cursor: pointer; text-decoration: none; display: inline-block;
    box-shadow: 0 4px 12px rgba(255,111,0,0.4);
    transition: transform 0.15s, box-shadow 0.15s;
}
.cta-primary:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(255,111,0,0.5); }
.cta-secondary {
    background: transparent; color: #fff;
    border: 2px solid #ffffff; padding: 14px 36px; border-radius: 50px;
    font-size: 16px; font-weight: 700; cursor: pointer; text-decoration: none;
    display: inline-block; transition: background 0.15s;
}
.cta-secondary:hover { background: rgba(255,255,255,0.1); }

/* Metric card */
.metric-card {
    background: #ffffff; border-radius: 16px; padding: 24px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07); text-align: center;
    border-top: 4px solid #2E7D32;
}
.metric-value { font-size: 36px; font-weight: 800; color: #2E7D32; }
.metric-label { font-size: 13px; color: #757575; font-weight: 500; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 4px; }

/* Section heading */
.section-heading {
    font-size: 28px; font-weight: 700; color: #1B5E20;
    margin: 40px 0 4px; text-align: center;
}
.section-sub { font-size: 15px; color: #757575; text-align: center; margin-bottom: 28px; }

/* How-it-works step */
.step-card {
    background: #F1F8E9; border-radius: 16px; padding: 32px 24px;
    text-align: center; border: 1px solid #DCEDC8;
}
.step-icon { font-size: 48px; margin-bottom: 12px; }
.step-num { font-size: 12px; font-weight: 700; color: #2E7D32; text-transform: uppercase; letter-spacing: 1px; }
.step-title { font-size: 18px; font-weight: 700; color: #1B5E20; margin: 6px 0; }
.step-desc { font-size: 14px; color: #616161; line-height: 1.5; }

/* Service card */
.service-card {
    background: #ffffff; border-radius: 16px; padding: 24px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #E8F5E9;
    transition: transform 0.15s, box-shadow 0.15s;
    height: 100%;
}
.service-card:hover { transform: translateY(-4px); box-shadow: 0 8px 24px rgba(46,125,50,0.12); }
.service-icon { font-size: 36px; margin-bottom: 10px; }
.service-name { font-size: 17px; font-weight: 700; color: #1B5E20; margin: 4px 0; }
.service-price { font-size: 22px; font-weight: 800; color: #FF6F00; }
.service-meta { font-size: 13px; color: #9E9E9E; margin-top: 4px; }
.service-tag {
    display: inline-block; background: #E8F5E9; color: #2E7D32;
    font-size: 11px; font-weight: 600; padding: 3px 10px;
    border-radius: 20px; margin-top: 8px;
}

/* Area badge */
.area-badge {
    display: inline-block; background: #E8F5E9; color: #1B5E20;
    font-size: 13px; font-weight: 600; padding: 6px 16px;
    border-radius: 20px; margin: 4px; border: 1px solid #C8E6C9;
}

/* Divider */
.green-divider { height: 3px; background: linear-gradient(90deg, #2E7D32, #81C784, #2E7D32); border: none; border-radius: 2px; margin: 8px 0 32px; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
        <span style='font-size:48px;'>🧺</span>
        <h2 style='margin:4px 0 0; font-size:26px; font-weight:800; letter-spacing:-0.5px;'>WashGo</h2>
        <p style='font-size:12px; opacity:0.75; margin:0;'>Hyderabad's #1 Laundry App</p>
    </div>
    <hr style='border-color:rgba(255,255,255,0.2); margin:16px 0;'>
    """, unsafe_allow_html=True)

    st.markdown("**Quick Navigation**")
    st.page_link("app.py", label="🏠 Home", )
    st.page_link("pages/1_🧺_Book_Laundry.py", label="🧺 Book Laundry")
    st.page_link("pages/2_📍_Track_Order.py", label="📍 Track Order")
    st.page_link("pages/3_🚚_Partner_App.py", label="🚚 Partner App")
    st.page_link("pages/4_📊_Admin_Dashboard.py", label="📊 Admin Dashboard")
    st.page_link("pages/5_ℹ️_About.py", label="ℹ️ About & Pricing")

    st.markdown("<hr style='border-color:rgba(255,255,255,0.2); margin:16px 0;'>", unsafe_allow_html=True)
    st.markdown("**Ready to get started?**")
    if st.button("🧺 New Order", use_container_width=True):
        st.switch_page("pages/1_🧺_Book_Laundry.py")

    st.markdown("""
    <div style='margin-top:auto; padding-top:32px; font-size:11px; opacity:0.6; text-align:center;'>
        WashGo v2.0 · Hyderabad<br>
        Mon–Sun · 8 AM – 8 PM
    </div>
    """, unsafe_allow_html=True)

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <div class="hero-title">🧺 WashGo</div>
    <div class="hero-tagline">Hyderabad's #1 On-Demand Laundry Service</div>
    <div class="hero-sub">
        Skip the hassle of laundry day. Schedule a pickup, we wash & care for your clothes,
        then deliver them fresh to your door — all within 24 hours.
    </div>
</div>
""", unsafe_allow_html=True)

col_b1, col_b2, col_b3 = st.columns([2, 1, 2])
with col_b2:
    if st.button("📅 Book Now →", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🧺_Book_Laundry.py")
col_t1, col_t2, col_t3 = st.columns([2, 1, 2])
with col_t2:
    if st.button("📍 Track Order", use_container_width=True):
        st.switch_page("pages/2_📍_Track_Order.py")

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ── KPI Metrics ───────────────────────────────────────────────────────────────
df = st.session_state.orders_df
total_orders = len(df)
total_revenue = df["amount"].sum()
avg_rating = df["rating"].dropna().mean()
active_partners = len(PARTNERS)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_orders:,}</div>
        <div class="metric-label">📦 Total Orders</div>
    </div>""", unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">₹{total_revenue:,.0f}</div>
        <div class="metric-label">💰 Total Revenue</div>
    </div>""", unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_rating:.1f} ⭐</div>
        <div class="metric-label">😊 Average Rating</div>
    </div>""", unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{active_partners}</div>
        <div class="metric-label">🚚 Active Partners</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── How It Works ──────────────────────────────────────────────────────────────
st.markdown("<div class='section-heading'>How It Works</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Three simple steps to fresh, clean laundry at your doorstep</div>", unsafe_allow_html=True)

h1, h2, h3 = st.columns(3)
steps = [
    ("🗓️", "1", "Schedule Pickup", "Choose your service, area and a convenient pickup time slot from our app."),
    ("🧺", "2", "We Wash & Care", "Our expert facility team handles your laundry with premium detergents and care."),
    ("🚚", "3", "Delivered Fresh", "Your clothes are delivered clean, folded and fresh right to your door."),
]
for col, (icon, num, title, desc) in zip([h1, h2, h3], steps):
    with col:
        st.markdown(f"""
        <div class="step-card">
            <div class="step-icon">{icon}</div>
            <div class="step-num">Step {num}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ── Services Overview ─────────────────────────────────────────────────────────
st.markdown("<div class='section-heading'>Our Services</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Professional laundry care for every need and budget</div>", unsafe_allow_html=True)

service_items = list(SERVICES.items())
row1 = st.columns(3)
row2 = st.columns(3)
all_cols = row1 + row2

for col, (name, info) in zip(all_cols, service_items):
    with col:
        st.markdown(f"""
        <div class="service-card">
            <div class="service-icon">{info['icon']}</div>
            <div class="service-name">{name}</div>
            <div class="service-price">₹{info['price']}<span style='font-size:14px;font-weight:400;color:#9E9E9E;'>/{info['unit']}</span></div>
            <div class="service-meta">⏱ {info['turnaround']}</div>
            <div class="service-tag">{info['unit'].upper()} BASED</div>
        </div>
        <br>""", unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ── Coverage Areas ────────────────────────────────────────────────────────────
st.markdown("<div class='section-heading'>Coverage Areas</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Currently serving 12 prime neighbourhoods across Hyderabad</div>", unsafe_allow_html=True)

badges_html = "".join(f"<span class='area-badge'>📍 {area}</span>" for area in AREAS)
st.markdown(f"<div style='text-align:center; padding: 8px 0 32px;'>{badges_html}</div>", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; color:#9E9E9E; font-size:13px; padding: 12px 0 32px;'>
    © 2026 WashGo Technologies Pvt. Ltd. · Hyderabad, Telangana &nbsp;|&nbsp;
    All rights reserved &nbsp;|&nbsp; Mon–Sun · 8 AM – 8 PM
</div>
""", unsafe_allow_html=True)
