import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.data import init_session_state

st.set_page_config(
    page_title="WashGo — Investor Pitch Deck",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_session_state()

# ── Color Palette ──────────────────────────────────────────────────────────────
PRIMARY = "#2E7D32"
ACCENT  = "#FF6F00"
DARK    = "#1A237E"

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

#MainMenu {visibility: hidden;}
footer    {visibility: hidden;}

/* ── Slide containers ── */
.slide {
    background: #ffffff;
    border-radius: 20px;
    padding: 48px 56px;
    margin-bottom: 40px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    border: 1px solid #f0f0f0;
    position: relative;
    overflow: hidden;
}
.slide::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: linear-gradient(90deg, #2E7D32, #FF6F00, #1A237E);
}

/* ── Slide number badge ── */
.slide-badge {
    display: inline-block;
    background: #F3F4F6;
    color: #6B7280;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 20px;
}

/* ── Cover slide ── */
.cover-title {
    font-size: 88px;
    font-weight: 900;
    color: #2E7D32;
    letter-spacing: -4px;
    line-height: 1;
    margin: 0 0 12px;
}
.cover-tagline {
    font-size: 26px;
    font-weight: 600;
    color: #1A237E;
    margin: 0 0 16px;
}
.cover-subtitle {
    font-size: 20px;
    font-weight: 700;
    color: #FF6F00;
    background: #FFF3E0;
    display: inline-block;
    padding: 8px 24px;
    border-radius: 50px;
    margin-bottom: 32px;
}
.badge-row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 8px; }
.badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F1F8E9;
    border: 1.5px solid #C8E6C9;
    color: #2E7D32;
    font-size: 14px;
    font-weight: 600;
    padding: 8px 20px;
    border-radius: 50px;
}

/* ── Section headers ── */
.slide-title {
    font-size: 38px;
    font-weight: 800;
    color: #1A237E;
    margin: 0 0 6px;
    letter-spacing: -1px;
}
.slide-subtitle {
    font-size: 16px;
    color: #6B7280;
    margin: 0 0 32px;
    line-height: 1.6;
}

/* ── Problem cards ── */
.problem-card {
    border-radius: 16px;
    padding: 32px 28px;
    text-align: center;
    height: 100%;
}
.problem-card-1 { background: linear-gradient(135deg, #FFEBEE, #FFCDD2); border: 2px solid #EF9A9A; }
.problem-card-2 { background: linear-gradient(135deg, #FFF3E0, #FFE0B2); border: 2px solid #FFCC80; }
.problem-card-3 { background: linear-gradient(135deg, #FBE9E7, #FFCCBC); border: 2px solid #FFAB91; }
.problem-icon  { font-size: 52px; margin-bottom: 16px; }
.problem-title { font-size: 22px; font-weight: 800; color: #B71C1C; margin: 0 0 12px; }
.problem-title-2 { color: #E65100; }
.problem-title-3 { color: #BF360C; }
.problem-desc  { font-size: 15px; color: #5D4037; line-height: 1.6; }

/* ── Feature cards ── */
.feature-card {
    background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
    border-radius: 16px;
    padding: 28px 24px;
    text-align: center;
    border: 2px solid #C8E6C9;
    height: 100%;
}
.feature-icon  { font-size: 44px; margin-bottom: 12px; }
.feature-title { font-size: 17px; font-weight: 700; color: #1B5E20; }

/* ── Market metrics ── */
.market-ring {
    text-align: center;
    padding: 32px 20px;
}
.ring-label  { font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #9E9E9E; }
.ring-value  { font-size: 36px; font-weight: 900; line-height: 1.1; margin: 8px 0 4px; }
.ring-desc   { font-size: 14px; color: #6B7280; }
.ring-tam    { color: #1A237E; background: #E8EAF6; border-radius: 20px; padding: 28px; border: 3px solid #9FA8DA; }
.ring-sam    { color: #2E7D32; background: #E8F5E9; border-radius: 20px; padding: 28px; border: 3px solid #A5D6A7; }
.ring-som    { color: #FF6F00; background: #FFF3E0; border-radius: 20px; padding: 28px; border: 3px solid #FFCC80; }
.market-note {
    background: #E3F2FD;
    border-left: 5px solid #1976D2;
    border-radius: 8px;
    padding: 16px 24px;
    margin-top: 24px;
    font-size: 15px;
    font-weight: 600;
    color: #0D47A1;
}

/* ── Revenue cards ── */
.rev-card {
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    height: 100%;
}
.rev-card-1 { background: #E8F5E9; border: 2px solid #A5D6A7; }
.rev-card-2 { background: #E3F2FD; border: 2px solid #90CAF9; }
.rev-card-3 { background: #FFF3E0; border: 2px solid #FFCC80; }
.rev-icon   { font-size: 40px; margin-bottom: 12px; }
.rev-title  { font-size: 18px; font-weight: 800; color: #1A237E; margin: 0 0 8px; }
.rev-value  { font-size: 28px; font-weight: 900; color: #2E7D32; }
.rev-desc   { font-size: 14px; color: #6B7280; margin-top: 6px; }

/* ── Milestone checkboxes ── */
.milestone {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: #F1F8E9;
    border-radius: 10px;
    margin-bottom: 10px;
    font-size: 15px;
    font-weight: 600;
    color: #1B5E20;
    border: 1.5px solid #C8E6C9;
}

/* ── Roadmap quarter ── */
.quarter-card {
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    height: 100%;
}
.q1-card { background: #E8F5E9; border: 2px solid #A5D6A7; }
.q2-card { background: #E3F2FD; border: 2px solid #90CAF9; }
.q3-card { background: #FFF3E0; border: 2px solid #FFCC80; }
.q4-card { background: #EDE7F6; border: 2px solid #CE93D8; }
.q-label { font-size: 13px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 10px; }
.q1-label { color: #2E7D32; }
.q2-label { color: #1565C0; }
.q3-label { color: #E65100; }
.q4-label { color: #6A1B9A; }
.q-metric { font-size: 26px; font-weight: 900; margin: 6px 0; }
.q-desc   { font-size: 13px; color: #6B7280; line-height: 1.5; }

/* ── Break-even callout ── */
.breakeven-box {
    background: linear-gradient(135deg, #1A237E, #283593);
    color: white;
    border-radius: 16px;
    padding: 28px 36px;
    text-align: center;
    margin-top: 24px;
}
.breakeven-title { font-size: 18px; font-weight: 600; opacity: 0.85; margin-bottom: 8px; }
.breakeven-value { font-size: 42px; font-weight: 900; color: #FFD54F; }
.breakeven-sub   { font-size: 15px; opacity: 0.75; margin-top: 6px; }

/* ── Ask section ── */
.ask-big {
    background: linear-gradient(135deg, #2E7D32, #1B5E20);
    border-radius: 20px;
    padding: 48px;
    text-align: center;
    color: white;
    margin-bottom: 32px;
}
.ask-amount { font-size: 72px; font-weight: 900; color: #FFD54F; letter-spacing: -2px; }
.ask-label  { font-size: 18px; font-weight: 600; opacity: 0.85; margin-top: 4px; }
.ask-meta   { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin-top: 24px; }
.ask-chip {
    background: rgba(255,255,255,0.15);
    border: 1.5px solid rgba(255,255,255,0.3);
    border-radius: 50px;
    padding: 10px 24px;
    font-size: 15px;
    font-weight: 600;
}

/* ── Offer cards ── */
.offer-card {
    background: #F8F9FA;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 15px;
    font-weight: 600;
    color: #1A237E;
    border: 1.5px solid #E0E7FF;
}

/* ── Series A target ── */
.series-a-box {
    background: #FFF3E0;
    border-left: 5px solid #FF6F00;
    border-radius: 8px;
    padding: 20px 28px;
    margin-top: 20px;
    font-size: 15px;
    color: #E65100;
    font-weight: 600;
}

/* ── Contact slide ── */
.contact-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid #F0F0F0;
    font-size: 16px;
    color: #374151;
}
.contact-label {
    font-weight: 700;
    color: #1A237E;
    width: 130px;
    flex-shrink: 0;
}
.cta-green-btn {
    display: inline-block;
    background: linear-gradient(135deg, #2E7D32, #388E3C);
    color: white !important;
    font-size: 20px;
    font-weight: 800;
    padding: 18px 56px;
    border-radius: 50px;
    text-decoration: none;
    box-shadow: 0 6px 24px rgba(46,125,50,0.4);
    letter-spacing: 0.5px;
    cursor: pointer;
    border: none;
    margin-top: 24px;
}

/* ── Data table ── */
.pitch-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 15px;
    margin-top: 20px;
}
.pitch-table th {
    background: #2E7D32;
    color: white;
    padding: 12px 16px;
    text-align: left;
    font-weight: 700;
    font-size: 13px;
    letter-spacing: 0.5px;
}
.pitch-table th:first-child { border-radius: 8px 0 0 0; }
.pitch-table th:last-child  { border-radius: 0 8px 0 0; }
.pitch-table td {
    padding: 11px 16px;
    border-bottom: 1px solid #F0F0F0;
    color: #374151;
}
.pitch-table tr:nth-child(even) td { background: #F9FAFB; }
.pitch-table tr:hover td { background: #F1F8E9; }
.pitch-table .green-text { color: #2E7D32; font-weight: 700; }
.pitch-table .amber-text  { color: #FF6F00; font-weight: 700; }

/* ── Section divider ── */
.deck-divider {
    height: 3px;
    background: linear-gradient(90deg, #2E7D32, #FF6F00, #1A237E, transparent);
    border: none;
    border-radius: 2px;
    margin: 8px 0 48px;
}

/* ── Sidebar ToC ── */
.toc-link {
    display: block;
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 13px;
    font-weight: 600;
    color: #ffffff !important;
    text-decoration: none;
    margin-bottom: 4px;
    transition: background 0.15s;
}
.toc-link:hover { background: rgba(255,255,255,0.15); }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B5E20 0%, #2E7D32 60%, #388E3C 100%);
}
section[data-testid="stSidebar"] * { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar Table of Contents ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 12px;'>
        <span style='font-size:44px;'>💰</span>
        <h2 style='margin:6px 0 0; font-size:22px; font-weight:800;'>Pitch Deck</h2>
        <p style='font-size:12px; opacity:0.7; margin:2px 0 0;'>WashGo · Seed Round 2025</p>
    </div>
    <hr style='border-color:rgba(255,255,255,0.2); margin:12px 0;'>
    <p style='font-size:11px; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; opacity:0.6; margin:0 0 8px;'>Contents</p>
    """, unsafe_allow_html=True)

    toc_items = [
        ("#slide-1-cover",                "1 · Cover"),
        ("#slide-2-problem",              "2 · The Problem"),
        ("#slide-3-solution",             "3 · The Solution"),
        ("#slide-4-market-opportunity",   "4 · Market Opportunity"),
        ("#slide-5-business-model",       "5 · Business Model"),
        ("#slide-6-traction-roadmap",     "6 · Traction & Roadmap"),
        ("#slide-7-financial-projections","7 · Financial Projections"),
        ("#slide-8-use-of-funds",         "8 · Use of Funds"),
        ("#slide-9-the-ask",              "9 · The Ask"),
        ("#slide-10-contact",             "10 · Contact"),
    ]
    for anchor, label in toc_items:
        st.markdown(f"<a href='{anchor}' class='toc-link'>→ {label}</a>", unsafe_allow_html=True)

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.2); margin:16px 0 8px;'>
    <div style='font-size:11px; opacity:0.55; text-align:center; padding-bottom:8px;'>
        Confidential · WashGo Technologies<br>Hyderabad, 2025
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-1-cover"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 01 · Cover</div>
        <div class="cover-title">🧺 WashGo</div>
        <div class="cover-tagline">Hyderabad's On-Demand Laundry Platform</div>
        <div class="cover-subtitle">Seed Round — ₹1.5 Cr</div>
        <div class="badge-row">
            <span class="badge">🏙️ Hyderabad</span>
            <span class="badge">🧺 Laundry-Tech</span>
            <span class="badge">🌱 Seed Stage</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-2-problem"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 02 · Problem</div>
        <div class="slide-title">The Problem</div>
        <div class="slide-subtitle">Laundry is one of the most time-consuming and unreliable household tasks for urban professionals.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="problem-card problem-card-1">
            <div class="problem-icon">⏰</div>
            <div class="problem-title">No Time</div>
            <div class="problem-desc">
                Working professionals in Hyderabad spend <strong>3–4 hours every week</strong> on laundry —
                washing, drying, folding, and ironing. That's 200+ hours a year lost to chores.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="problem-card problem-card-2">
            <div class="problem-icon">😤</div>
            <div class="problem-title problem-title-2">Unreliable Dhobi</div>
            <div class="problem-desc">
                Traditional dhobis offer <strong>inconsistent quality</strong>, no order tracking, no service guarantees,
                and frequent no-shows — leaving customers frustrated and helpless.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="problem-card problem-card-3">
            <div class="problem-icon">🗺️</div>
            <div class="problem-title problem-title-3">Inconvenient</div>
            <div class="problem-desc">
                Laundromats require <strong>travel, long queues, and cash payments</strong>.
                There is no pickup, no delivery, and no way to plan around a busy schedule.
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — THE SOLUTION
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-3-solution"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 03 · Solution</div>
        <div class="slide-title">The Solution</div>
        <div class="slide-subtitle">
            WashGo connects customers with verified laundry facilities through a seamless app experience —
            scheduled pickups, real-time tracking, and guaranteed delivery. Clean clothes without leaving home.
        </div>
    </div>
    """, unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("📱", "Schedule Pickup in 60 Seconds", "Book a slot, choose your service, and a partner arrives at your door."),
        ("🔍", "Real-Time Order Tracking", "Follow your laundry every step — from pickup to processing to delivery."),
        ("✅", "Quality-Guaranteed Delivery", "Every order is inspected before delivery. 100% satisfaction or we redo it."),
        ("💳", "Cashless Digital Payments", "UPI, cards, and wallets. No cash, no hassle, instant receipts."),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card">
                <div class="feature-icon">{icon}</div>
                <div class="feature-title">{title}</div>
                <p style='font-size:13px; color:#4B5563; margin-top:8px; line-height:1.5;'>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — MARKET OPPORTUNITY
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-4-market-opportunity"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 04 · Market</div>
        <div class="slide-title">Market Opportunity</div>
        <div class="slide-subtitle">India's laundry sector is vast and largely unorganised — ripe for tech-enabled disruption.</div>
    </div>
    """, unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        <div class="market-ring ring-tam">
            <div class="ring-label">TAM</div>
            <div class="ring-value" style="color:#1A237E;">₹85,000 Cr</div>
            <div class="ring-desc" style="color:#3949AB; font-weight:600; margin-top:8px;">India Laundry Market</div>
            <div class="ring-desc" style="margin-top:6px;">Total addressable market across all laundry services in India — dry cleaning, wash & fold, commercial.</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="market-ring ring-sam">
            <div class="ring-label">SAM</div>
            <div class="ring-value" style="color:#2E7D32;">₹4,200 Cr</div>
            <div class="ring-desc" style="color:#388E3C; font-weight:600; margin-top:8px;">Organised Services, Tier-1 Cities</div>
            <div class="ring-desc" style="margin-top:6px;">Serviceable market — organised, app-based laundry platforms operating in metros and Tier-1 cities.</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="market-ring ring-som">
            <div class="ring-label">SOM</div>
            <div class="ring-value" style="color:#FF6F00;">₹180 Cr</div>
            <div class="ring-desc" style="color:#F57C00; font-weight:600; margin-top:8px;">Hyderabad Tech Corridor · Year 3</div>
            <div class="ring-desc" style="margin-top:6px;">Our obtainable share — Hyderabad's IT corridors (Gachibowli, Kondapur, Madhapur, HiTech City) by Year 3.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="market-note">
        💡 Only <strong>8% of India's laundry market is organised</strong> — the remaining 92% is served by informal dhobis and self-service.
        This represents <strong>massive whitespace</strong> for a technology-first platform like WashGo.
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — BUSINESS MODEL
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-5-business-model"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 05 · Business Model</div>
        <div class="slide-title">Business Model</div>
        <div class="slide-subtitle">Three complementary revenue streams built for high margins and recurring revenue.</div>
    </div>
    """, unsafe_allow_html=True)

    r1, r2, r3 = st.columns(3)
    with r1:
        st.markdown("""
        <div class="rev-card rev-card-1">
            <div class="rev-icon">💸</div>
            <div class="rev-title">Service Commission</div>
            <div class="rev-value">25%</div>
            <div class="rev-desc">Commission on every order placed through the WashGo platform, paid by our facility partners.</div>
        </div>
        """, unsafe_allow_html=True)
    with r2:
        st.markdown("""
        <div class="rev-card rev-card-2">
            <div class="rev-icon">🚚</div>
            <div class="rev-title">Delivery Fee</div>
            <div class="rev-value">₹49</div>
            <div class="rev-desc">Flat fee per pickup + delivery cycle, charged to the customer. Covers last-mile logistics cost.</div>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        st.markdown("""
        <div class="rev-card rev-card-3">
            <div class="rev-icon">🔄</div>
            <div class="rev-title">Subscriptions</div>
            <div class="rev-value">₹999 – ₹2,999</div>
            <div class="rev-desc">Monthly plans offering discounted rates + priority pickup. Drives predictable recurring revenue.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <table class="pitch-table">
        <thead>
            <tr>
                <th>Service</th>
                <th>Avg Order Value</th>
                <th>WashGo Revenue</th>
                <th>Gross Margin</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Regular Wash</td><td class="amber-text">₹350</td><td class="green-text">₹136</td><td>39%</td></tr>
            <tr><td>Express Wash</td><td class="amber-text">₹480</td><td class="green-text">₹169</td><td>35%</td></tr>
            <tr><td>Dry Cleaning</td><td class="amber-text">₹600</td><td class="green-text">₹199</td><td>33%</td></tr>
            <tr><td>Premium Care</td><td class="amber-text">₹800</td><td class="green-text">₹249</td><td>31%</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — TRACTION & ROADMAP
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-6-traction-roadmap"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 06 · Traction & Roadmap</div>
        <div class="slide-title">Traction & Roadmap</div>
        <div class="slide-subtitle">Strong early signals and a clear path to scale across all of Hyderabad.</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([1, 1])

    with left:
        st.markdown("<h4 style='color:#1A237E; font-weight:800; margin-bottom:16px;'>✅ Current Achievements</h4>",
                    unsafe_allow_html=True)
        milestones = [
            "Platform built — web + admin + partner app",
            "3 facility partnerships confirmed",
            "5 delivery partners onboarded",
            "Pilot area: Kondapur & Gachibowli",
        ]
        for m in milestones:
            st.markdown(f"""
            <div class="milestone">
                <span style='font-size:20px;'>✅</span>
                <span>{m}</span>
            </div>
            """, unsafe_allow_html=True)

    with right:
        # Plotly milestone / Gantt-style chart
        quarters = ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"]
        targets  = [100, 500, 2000, 5000]
        colors   = [PRIMARY, "#1565C0", ACCENT, DARK]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=quarters,
            y=targets,
            marker_color=colors,
            text=[f"{t:,} orders/mo" for t in targets],
            textposition="outside",
            textfont=dict(size=13, color="#374151"),
        ))
        fig.update_layout(
            title=dict(text="Orders per Month — Growth Roadmap", font=dict(size=15, color=DARK)),
            yaxis_title="Orders / Month",
            height=300,
            margin=dict(t=50, b=20, l=10, r=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(gridcolor="#F0F0F0"),
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    q1, q2, q3, q4 = st.columns(4)
    roadmap = [
        ("Q1 2025", "q1-card", "q1-label", "100", "orders/mo", "2 areas covered\nLaunch phase"),
        ("Q2 2025", "q2-card", "q2-label", "500", "orders/mo", "5 areas · Subscriptions\nlaunched"),
        ("Q3 2025", "q3-card", "q3-label", "2,000", "orders/mo", "10 areas · Corporate\ntie-ups secured"),
        ("Q4 2025", "q4-card", "q4-label", "5,000", "orders/mo", "Full Hyderabad\ncoverage"),
    ]
    for col, (label, card_cls, lbl_cls, metric, unit, desc) in zip([q1, q2, q3, q4], roadmap):
        with col:
            st.markdown(f"""
            <div class="quarter-card {card_cls}">
                <div class="q-label {lbl_cls}">{label}</div>
                <div class="q-metric">{metric}</div>
                <div style='font-size:12px; color:#6B7280;'>{unit}</div>
                <div class="q-desc" style='margin-top:10px;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — FINANCIAL PROJECTIONS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-7-financial-projections"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 07 · Financials</div>
        <div class="slide-title">Financial Projections</div>
        <div class="slide-subtitle">Conservative 18-month model reaching ₹25L/month revenue by Month 18.</div>
    </div>
    """, unsafe_allow_html=True)

    # Build projection data
    months = list(range(1, 19))
    month_labels = [f"M{m}" for m in months]

    # Orders: start 50, grow 30% M1-6, 20% M7-12, 15% M13-18
    orders = [50]
    for m in range(1, 18):
        if m < 6:   rate = 0.30
        elif m < 12: rate = 0.20
        else:        rate = 0.15
        orders.append(round(orders[-1] * (1 + rate)))

    avg_order  = 380
    commission = 0.25
    del_fee    = 49
    sub_rate   = 0.03
    avg_sub    = 1500
    var_cost   = 85
    fixed_cost = 120000

    revenues = []
    costs    = []
    for i, o in enumerate(orders):
        subs        = max(0, round(o * sub_rate * (i + 1) * 0.15))
        rev_comm    = round(o * avg_order * commission)
        rev_del     = round(o * del_fee)
        rev_sub     = round(subs * avg_sub)
        total_rev   = rev_comm + rev_del + rev_sub
        total_cost  = round(o * var_cost) + fixed_cost
        revenues.append(total_rev)
        costs.append(total_cost)

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="Monthly Revenue",
        x=month_labels, y=revenues,
        marker_color=PRIMARY,
        opacity=0.9,
    ))
    fig2.add_trace(go.Bar(
        name="Monthly Costs",
        x=month_labels, y=costs,
        marker_color="#EF5350",
        opacity=0.85,
    ))
    # Break-even line
    fig2.add_hline(
        y=0, line_dash="dot", line_color="#666",
        annotation_text="Break-even zone", annotation_position="top left",
    )
    fig2.update_layout(
        barmode="group",
        title=dict(text="Revenue vs Costs — Month 1 to Month 18 (₹)", font=dict(size=15, color=DARK)),
        height=380,
        margin=dict(t=50, b=20, l=10, r=10),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#F0F0F0", tickprefix="₹"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Key numbers table
    st.markdown("""
    <table class="pitch-table">
        <thead>
            <tr><th>Metric</th><th>Month 6</th><th>Month 12</th><th>Month 18</th></tr>
        </thead>
        <tbody>
            <tr><td>Orders / Month</td><td>500</td><td>2,000</td><td>5,000</td></tr>
            <tr><td>Revenue</td><td class="green-text">₹2.5L</td><td class="green-text">₹10L</td><td class="green-text">₹25L</td></tr>
            <tr><td>EBITDA</td><td style="color:#EF5350; font-weight:700;">−₹1.2L</td><td class="green-text">₹0.8L</td><td class="green-text">₹6.5L</td></tr>
            <tr><td>Subscribers</td><td>50</td><td>300</td><td>900</td></tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="breakeven-box">
        <div class="breakeven-title">📍 Break-Even Point</div>
        <div class="breakeven-value">Month 11</div>
        <div class="breakeven-sub">At 1,600 orders/month — operating cash-flow positive</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — USE OF FUNDS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-8-use-of-funds"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 08 · Use of Funds</div>
        <div class="slide-title">Use of Funds</div>
        <div class="slide-subtitle">₹1.5 Crore deployed across five strategic areas to reach Series A milestones.</div>
    </div>
    """, unsafe_allow_html=True)

    donut_left, donut_right = st.columns([1.2, 1])

    with donut_left:
        labels = [
            "Tech & Product",
            "Operations & Logistics",
            "Marketing & Acquisition",
            "Team (3 hires)",
            "Working Capital",
        ]
        values = [37.5, 45, 37.5, 22.5, 7.5]
        donut_colors = [PRIMARY, DARK, ACCENT, "#7B1FA2", "#00838F"]

        fig3 = go.Figure(go.Pie(
            labels=labels,
            values=values,
            hole=0.52,
            marker=dict(colors=donut_colors, line=dict(color="white", width=3)),
            textinfo="label+percent",
            textfont=dict(size=13),
            hovertemplate="<b>%{label}</b><br>₹%{value}L (%{percent})<extra></extra>",
        ))
        fig3.add_annotation(
            text="₹1.5 Cr<br><span style='font-size:10px'>Seed Round</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=DARK),
            align="center",
        )
        fig3.update_layout(
            showlegend=False,
            height=380,
            margin=dict(t=20, b=20, l=10, r=10),
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig3, use_container_width=True)

    with donut_right:
        alloc_rows = [
            ("💻", "Tech & Product",            "₹37.5L", "25%", PRIMARY),
            ("🚚", "Operations & Logistics",    "₹45L",   "30%", DARK),
            ("📣", "Marketing & Acquisition",   "₹37.5L", "25%", ACCENT),
            ("👥", "Team (3 hires)",             "₹22.5L", "15%", "#7B1FA2"),
            ("🏦", "Working Capital",            "₹7.5L",  "5%",  "#00838F"),
        ]
        st.markdown("<br><br>", unsafe_allow_html=True)
        for icon, name, amount, pct, color in alloc_rows:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:14px; padding:12px 16px;
                        border-radius:10px; margin-bottom:8px;
                        background:#F9FAFB; border-left:5px solid {color};'>
                <span style='font-size:22px;'>{icon}</span>
                <div style='flex:1;'>
                    <div style='font-size:14px; font-weight:700; color:#1A237E;'>{name}</div>
                    <div style='font-size:13px; color:#6B7280;'>{pct} of total raise</div>
                </div>
                <div style='font-size:18px; font-weight:900; color:{color};'>{amount}</div>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — THE ASK
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-9-the-ask"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 09 · The Ask</div>
        <div class="slide-title">The Ask</div>
        <div class="slide-subtitle">We are raising our first external round to execute the Hyderabad playbook and reach Series A-ready metrics.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="ask-big">
        <div class="ask-amount">₹1.5 Crore</div>
        <div class="ask-label">Seed Round — 18-Month Runway to Series A Readiness</div>
        <div class="ask-meta">
            <span class="ask-chip">📄 Instrument: SAFE / Convertible Note</span>
            <span class="ask-chip">🏷️ Valuation Cap: ₹8 Crore</span>
            <span class="ask-chip">🕐 18-Month Runway</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    ask_l, ask_r = st.columns(2)

    with ask_l:
        st.markdown("<h4 style='color:#1A237E; font-weight:800; margin-bottom:16px;'>🎯 What We Offer Investors</h4>",
                    unsafe_allow_html=True)
        offers = [
            ("🪑", "Board Observer Seat"),
            ("📊", "Monthly Investor Updates"),
            ("⚡", "Pro-Rata Rights in Series A"),
            ("🗺️", "Early Access to Expansion Markets"),
        ]
        for icon, text in offers:
            st.markdown(f"""
            <div class="offer-card">
                <span style='font-size:22px;'>{icon}</span>
                <span>{text}</span>
            </div>
            """, unsafe_allow_html=True)

    with ask_r:
        st.markdown("<h4 style='color:#1A237E; font-weight:800; margin-bottom:16px;'>🚀 Target Series A Milestones</h4>",
                    unsafe_allow_html=True)
        st.markdown("""
        <div class="series-a-box">
            <div style='font-size:22px; font-weight:900; margin-bottom:8px;'>₹8–10 Crore</div>
            <div>Series A target raise at <strong>₹40 Crore valuation</strong></div>
        </div>
        """, unsafe_allow_html=True)

        milestones_a = [
            ("📦", "5,000+ orders/month"),
            ("💰", "₹25L+ MRR"),
            ("📈", "EBITDA positive for 3+ months"),
            ("🌆", "Full Hyderabad coverage"),
            ("👥", "900+ active subscribers"),
        ]
        for icon, text in milestones_a:
            st.markdown(f"""
            <div style='display:flex; align-items:center; gap:10px; padding:10px 14px;
                        border-radius:8px; margin-bottom:8px; background:#F1F8E9;
                        font-size:14px; font-weight:600; color:#1B5E20;
                        border:1.5px solid #C8E6C9;'>
                <span style='font-size:18px;'>{icon}</span>
                <span>{text}</span>
            </div>
            """, unsafe_allow_html=True)

st.markdown('<hr class="deck-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — CONTACT / CTA
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<a name="slide-10-contact"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown("""
    <div class="slide">
        <div class="slide-badge">Slide 10 · Contact</div>
        <div class="slide-title">Let's Build This Together</div>
        <div class="slide-subtitle">We're looking for investors who share our vision of making professional laundry accessible to every urban household in India.</div>
    </div>
    """, unsafe_allow_html=True)

    contact_l, contact_r = st.columns([1.3, 1])

    with contact_l:
        st.markdown("""
        <div style='background:#F9FAFB; border-radius:16px; padding:32px; border:1px solid #E5E7EB;'>
            <div class="contact-row">
                <span class="contact-label">🏢 Company</span>
                <span>WashGo Technologies Pvt. Ltd.</span>
            </div>
            <div class="contact-row">
                <span class="contact-label">📍 Location</span>
                <span>Hyderabad, Telangana — 500032</span>
            </div>
            <div class="contact-row">
                <span class="contact-label">📧 Email</span>
                <span><a href="mailto:founders@washgo.in" style="color:#2E7D32; font-weight:700; text-decoration:none;">founders@washgo.in</a></span>
            </div>
            <div class="contact-row">
                <span class="contact-label">🌐 Website</span>
                <span style="color:#9CA3AF; font-style:italic;">www.washgo.in <em>(coming soon)</em></span>
            </div>
            <div class="contact-row" style="border-bottom:none;">
                <span class="contact-label">💼 LinkedIn</span>
                <span style="color:#9CA3AF; font-style:italic;">linkedin.com/company/washgo-in <em>(coming soon)</em></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with contact_r:
        st.markdown("""
        <div style='text-align:center; padding: 32px 20px;
                    background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
                    border-radius:16px; border:2px solid #C8E6C9;'>
            <div style='font-size:52px; margin-bottom:12px;'>☎️</div>
            <div style='font-size:18px; font-weight:700; color:#1B5E20; margin-bottom:6px;'>Ready to invest?</div>
            <div style='font-size:14px; color:#6B7280; margin-bottom:24px; line-height:1.6;'>
                Book a 30-minute call with our founders to learn more about WashGo's vision, traction, and opportunity.
            </div>
            <a href="mailto:founders@washgo.in?subject=Investor%20Call%20Request%20—%20WashGo"
               class="cta-green-btn">
                📅 Schedule a 30-min Call
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:40px; padding:20px;
                background:#1A237E; border-radius:12px; color:white;
                font-size:13px; opacity:0.9;'>
        <strong>Confidential — For Authorised Recipients Only</strong><br>
        This document contains forward-looking statements and projections.
        Past performance is not indicative of future results.
        © 2025 WashGo Technologies Pvt. Ltd. All rights reserved.
    </div>
    """, unsafe_allow_html=True)
