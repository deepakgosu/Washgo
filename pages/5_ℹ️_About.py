import streamlit as st
import pandas as pd

from utils.data import (
    init_session_state, SERVICES, AREAS, PARTNERS, FACILITIES,
    DELIVERY_FEE,
)

st.set_page_config(
    page_title="About & Pricing – WashGo",
    page_icon="ℹ️",
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

.section-heading {
    font-size: 26px; font-weight: 800; color: #1B5E20;
    margin: 36px 0 6px;
}
.section-sub { font-size: 15px; color: #757575; margin-bottom: 24px; }
.green-divider {
    height: 3px;
    background: linear-gradient(90deg, #2E7D32, #81C784, #2E7D32);
    border: none; border-radius: 2px; margin: 8px 0 28px;
}

/* Pricing table */
.pricing-table { width: 100%; border-collapse: collapse; border-radius: 12px; overflow: hidden; }
.pricing-table th {
    background: #2E7D32; color: #fff; padding: 14px 18px;
    text-align: left; font-size: 13px; text-transform: uppercase; letter-spacing: 0.6px;
}
.pricing-table td { padding: 13px 18px; font-size: 14px; border-bottom: 1px solid #F5F5F5; }
.pricing-table tr:hover td { background: #F1F8E9; }
.pricing-table tr:last-child td { border-bottom: none; }
.price-highlight { font-weight: 700; color: #FF6F00; font-size: 16px; }

/* Plan card */
.plan-card {
    background: #fff; border-radius: 20px; padding: 32px 28px; text-align: center;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08); border: 2px solid #E8F5E9;
    transition: transform 0.15s, box-shadow 0.15s;
}
.plan-card:hover { transform: translateY(-6px); box-shadow: 0 10px 32px rgba(46,125,50,0.15); }
.plan-card-popular {
    border-color: #FF6F00 !important;
    box-shadow: 0 6px 24px rgba(255,111,0,0.2) !important;
}
.plan-badge {
    background: #FF6F00; color: #fff; font-size: 11px; font-weight: 700;
    padding: 4px 14px; border-radius: 20px; display: inline-block; margin-bottom: 12px;
}
.plan-name  { font-size: 20px; font-weight: 800; color: #1B5E20; margin: 0; }
.plan-price { font-size: 42px; font-weight: 900; color: #2E7D32; margin: 12px 0 4px; }
.plan-per   { font-size: 14px; color: #9E9E9E; margin-bottom: 20px; }
.plan-feature { font-size: 14px; color: #424242; padding: 7px 0; border-bottom: 1px solid #F5F5F5; text-align: left; }
.plan-feature:last-of-type { border-bottom: none; }

/* Mission card */
.mission-card {
    background: linear-gradient(135deg, #E8F5E9, #F1F8E9);
    border-radius: 16px; padding: 28px 32px; border: 1px solid #C8E6C9;
    margin-bottom: 16px;
}

/* Area coverage grid */
.area-grid { display: flex; flex-wrap: wrap; gap: 10px; margin: 16px 0 28px; }
.area-chip {
    background: #E8F5E9; color: #1B5E20; font-size: 14px; font-weight: 600;
    padding: 8px 18px; border-radius: 24px; border: 1px solid #C8E6C9;
}

/* Team card */
.team-card {
    background: #fff; border-radius: 16px; padding: 24px 20px; text-align: center;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06); border: 1px solid #E8F5E9;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <span style='font-size:44px;'>ℹ️</span>
        <h2 style='margin:4px 0 0; font-size:24px; font-weight:800;'>WashGo</h2>
        <p style='font-size:12px; opacity:0.7; margin:0;'>About & Pricing</p>
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
    if st.button("🧺 Book Now", use_container_width=True):
        st.switch_page("pages/1_🧺_Book_Laundry.py")

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>ℹ️ About WashGo & Pricing</h1>
    <p>Everything you need to know about Hyderabad's favourite laundry service</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SERVICES & PRICING
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-heading'>🧺 Services & Pricing</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Transparent pricing with no hidden charges. Delivery fee of ₹49 applies per order.</div>", unsafe_allow_html=True)

pricing_rows = []
for name, info in SERVICES.items():
    pricing_rows.append({
        "Service": f"{info['icon']} {name}",
        "Price": f"₹{info['price']} / {info['unit']}",
        "Unit": info["unit"].capitalize(),
        "Turnaround": info["turnaround"],
        "Min Order": f"1 {info['unit']}",
        "Best For": {
            "Regular Wash": "Everyday clothing",
            "Express Wash": "Urgent laundry",
            "Dry Cleaning": "Formal wear",
            "Premium Care": "Delicate items",
            "Ironing Only": "Already washed",
            "Wash & Iron": "Complete service",
        }.get(name, "–"),
    })

pricing_df = pd.DataFrame(pricing_rows)
st.dataframe(
    pricing_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Service": st.column_config.TextColumn("Service", width="medium"),
        "Price": st.column_config.TextColumn("Price", width="small"),
        "Turnaround": st.column_config.TextColumn("⏱ Turnaround", width="small"),
    },
    height=260,
)

st.markdown(f"""
<div style='background:#FFF8E1; border-radius:10px; padding:14px 20px; margin-top:8px;
     border-left:4px solid #FF6F00; font-size:14px; color:#E65100;'>
    📦 <strong>Delivery Fee:</strong> ₹{DELIVERY_FEE} per order (flat rate, regardless of order size)
    &nbsp;|&nbsp; 🆓 <strong>Free delivery</strong> for Premium subscribers
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SUBSCRIPTION PLANS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-heading'>💳 Subscription Plans</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Save more with our monthly subscription plans. Cancel anytime.</div>", unsafe_allow_html=True)

p1, p2, p3 = st.columns(3)

plans = [
    {
        "name": "Basic",
        "icon": "🌱",
        "price": "₹999",
        "per": "per month",
        "popular": False,
        "badge": "",
        "color": "#2E7D32",
        "features": [
            "4 orders per month",
            "Regular Wash & Ironing",
            "Next-day delivery",
            "Standard support",
            "₹49 delivery fee applies",
            "WashGo app access",
        ],
    },
    {
        "name": "Pro",
        "icon": "⭐",
        "price": "₹1,799",
        "per": "per month",
        "popular": True,
        "badge": "Most Popular",
        "color": "#FF6F00",
        "features": [
            "8 orders per month",
            "All services included",
            "Same-day delivery eligible",
            "Priority support",
            "Free delivery on all orders",
            "WashGo app + web access",
        ],
    },
    {
        "name": "Premium",
        "icon": "👑",
        "price": "₹2,999",
        "per": "per month",
        "popular": False,
        "badge": "Best Value",
        "color": "#1565C0",
        "features": [
            "Unlimited orders",
            "All services + Premium Care",
            "Express same-day delivery",
            "Dedicated account manager",
            "Free delivery always",
            "Exclusive member discounts",
        ],
    },
]

for col, plan in zip([p1, p2, p3], plans):
    with col:
        popular_class = "plan-card-popular" if plan["popular"] else ""
        badge_html = f"<div class='plan-badge'>{plan['badge']}</div><br>" if plan["badge"] else "<br>"
        features_html = "".join(
            f"<div class='plan-feature'>✅ {feat}</div>"
            for feat in plan["features"]
        )
        st.markdown(f"""
        <div class='plan-card {popular_class}'>
            {badge_html}
            <div style='font-size:40px;'>{plan['icon']}</div>
            <p class='plan-name'>{plan['name']}</p>
            <div class='plan-price' style='color:{plan["color"]};'>{plan['price']}</div>
            <div class='plan-per'>{plan['per']}</div>
            {features_html}
            <br>
        </div>
        """, unsafe_allow_html=True)
        btn_label = "🟢 Get Started" if not plan["popular"] else "⭐ Choose Pro"
        if col.button(btn_label, key=f"plan_{plan['name']}", use_container_width=True,
                      type="primary" if plan["popular"] else "secondary"):
            st.switch_page("pages/1_🧺_Book_Laundry.py")

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ABOUT WASHGO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-heading'>🏢 About WashGo</div>", unsafe_allow_html=True)

ab1, ab2 = st.columns([3, 2])

with ab1:
    st.markdown("""
    <div class="mission-card">
        <h3 style='color:#1B5E20; margin-top:0;'>🎯 Our Mission</h3>
        <p style='color:#424242; line-height:1.8; font-size:15px;'>
            WashGo was founded in 2022 with a simple yet powerful mission:
            <strong>to make clean laundry effortless for every Hyderabadi</strong>.
        </p>
        <p style='color:#424242; line-height:1.8; font-size:15px;'>
            We are Hyderabad's fastest-growing on-demand laundry platform, connecting
            busy urban professionals with trusted laundry partners and professional-grade
            facilities across the city. From IT employees in Hitech City to families in
            Banjara Hills, WashGo delivers freshness at your doorstep.
        </p>
        <p style='color:#424242; line-height:1.8; font-size:15px;'>
            We believe your time is precious. Instead of spending it at the dhobighat,
            let WashGo handle the washing while you focus on what matters most.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='background:#E3F2FD; border-radius:16px; padding:24px 28px; border:1px solid #BBDEFB; margin-top:16px;'>
        <h3 style='color:#1565C0; margin-top:0;'>📊 WashGo in Numbers</h3>
        <div style='display:grid; grid-template-columns:1fr 1fr; gap:16px;'>
            <div style='text-align:center;'>
                <div style='font-size:32px; font-weight:800; color:#1565C0;'>2022</div>
                <div style='font-size:13px; color:#757575;'>Founded</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:32px; font-weight:800; color:#2E7D32;'>12+</div>
                <div style='font-size:13px; color:#757575;'>Areas Covered</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:32px; font-weight:800; color:#FF6F00;'>5</div>
                <div style='font-size:13px; color:#757575;'>Delivery Partners</div>
            </div>
            <div style='text-align:center;'>
                <div style='font-size:32px; font-weight:800; color:#6A1B9A;'>4</div>
                <div style='font-size:13px; color:#757575;'>Wash Facilities</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with ab2:
    st.markdown("""
    <div style='background:#fff; border-radius:16px; padding:24px; border:1px solid #E8F5E9;
         box-shadow:0 2px 12px rgba(0,0,0,0.06);'>
        <h3 style='color:#1B5E20; margin-top:0;'>✨ Why Choose WashGo?</h3>
    </div>
    """, unsafe_allow_html=True)

    reasons = [
        ("⚡", "Fast Turnaround", "Same-day and next-day delivery options available"),
        ("🔒", "Trusted & Safe", "Background-verified delivery partners"),
        ("💰", "Transparent Pricing", "No hidden charges, ever"),
        ("🌿", "Eco-Friendly", "Biodegradable detergents & water recycling"),
        ("📱", "Easy Tracking", "Real-time order tracking at every step"),
        ("⭐", "Quality Guarantee", "Re-wash guarantee if not satisfied"),
    ]
    for icon, title, desc in reasons:
        st.markdown(f"""
        <div style='display:flex; gap:14px; padding:12px 0; border-bottom:1px solid #F5F5F5;'>
            <div style='font-size:24px; flex-shrink:0;'>{icon}</div>
            <div>
                <div style='font-weight:700; color:#1B5E20; font-size:14px;'>{title}</div>
                <div style='color:#757575; font-size:13px;'>{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COVERAGE AREAS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-heading'>📍 Coverage Areas</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>We currently serve these 12 prime locations across Hyderabad</div>", unsafe_allow_html=True)

area_chips_html = "<div class='area-grid'>" + \
    "".join(f"<div class='area-chip'>📍 {area}</div>" for area in AREAS) + \
    "</div>"
st.markdown(area_chips_html, unsafe_allow_html=True)

# Map placeholder
st.markdown("""
<div style='background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
     border-radius:16px; padding: 60px 20px; text-align:center; border:2px dashed #A5D6A7;'>
    <div style='font-size:48px;'>🗺️</div>
    <h3 style='color:#2E7D32; margin:12px 0 6px;'>Hyderabad Coverage Map</h3>
    <p style='color:#616161; font-size:14px;'>
        Interactive map showing all 12 service areas.<br>
        Expanding to 20+ areas by Q3 2026!
    </p>
    <div style='margin-top:16px; display:flex; gap:12px; justify-content:center; flex-wrap:wrap;'>
        <span style='background:#2E7D32;color:#fff;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;'>
            ✅ Active Coverage
        </span>
        <span style='background:#FF6F00;color:#fff;padding:6px 16px;border-radius:20px;font-size:13px;font-weight:600;'>
            🔜 Coming Soon
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PARTNER FACILITIES
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-heading'>🏭 Our Partner Facilities</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>State-of-the-art laundry facilities powering WashGo's quality promise</div>", unsafe_allow_html=True)

fac_cols = st.columns(len(FACILITIES))
for col, fac in zip(fac_cols, FACILITIES):
    with col:
        stars = "⭐" * round(fac["rating"])
        st.markdown(f"""
        <div style='background:#fff; border-radius:14px; padding:20px; text-align:center;
             box-shadow:0 2px 10px rgba(0,0,0,0.06); border:1px solid #E8F5E9;'>
            <div style='font-size:36px; margin-bottom:8px;'>🏭</div>
            <div style='font-weight:700; color:#1B5E20; font-size:15px;'>{fac['name']}</div>
            <div style='color:#757575; font-size:13px; margin:4px 0;'>📍 {fac['area']}</div>
            <div style='font-size:14px;'>{stars}</div>
            <div style='color:#FF6F00; font-weight:700; font-size:14px;'>{fac['rating']}/5.0</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FAQ
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("<div class='section-heading'>❓ Frequently Asked Questions</div>", unsafe_allow_html=True)
st.markdown("<div class='section-sub'>Got questions? We've got answers.</div>", unsafe_allow_html=True)

faqs = [
    (
        "How does WashGo work?",
        """WashGo is a 3-step process:
1. **Book online** – Select your service, enter your address, and pick a convenient pickup time slot.
2. **We collect & clean** – Our delivery partner picks up your laundry and takes it to a certified facility.
3. **Fresh delivery** – Your cleaned, folded laundry is delivered back to you within the turnaround time.""",
    ),
    (
        "What areas does WashGo cover in Hyderabad?",
        """We currently serve **12 prime areas**: Hitech City, Gachibowli, Kondapur, Madhapur, Jubilee Hills,
Banjara Hills, Kukatpally, Miyapur, Begumpet, Secunderabad, Ameerpet, and SR Nagar.

We are expanding rapidly! More areas coming soon in 2026.""",
    ),
    (
        "How long does it take for my laundry to be returned?",
        """Turnaround times vary by service:
- **Regular Wash:** Next Day
- **Express Wash:** Same Day (order before 12 PM)
- **Ironing Only:** Same Day
- **Wash & Iron:** Next Day
- **Dry Cleaning:** 2–3 Days
- **Premium Care:** 2 Days""",
    ),
    (
        "What is the pricing structure?",
        f"""Pricing is straightforward:
- **Regular Wash:** ₹60/kg
- **Express Wash:** ₹100/kg
- **Dry Cleaning:** ₹150/piece
- **Premium Care:** ₹200/piece
- **Ironing Only:** ₹20/piece
- **Wash & Iron:** ₹80/kg

A flat **delivery fee of ₹{DELIVERY_FEE}** is charged per order. Subscribers on the Pro or Premium plan get free delivery.""",
    ),
    (
        "Is my laundry safe with WashGo?",
        """Absolutely! We take multiple precautions:
- All laundry is **tagged and tracked** individually.
- Our facilities are **CCTV-monitored** at all times.
- Delivery partners are **background-verified**.
- We use **eco-friendly, skin-safe detergents**.
- A **re-wash guarantee** is offered if you are not satisfied with the quality.""",
    ),
    (
        "How do I track my order?",
        """You can track your order in real-time on the **Track Order** page.
Simply enter your Order ID (e.g., WG12345) to see:
- Current status (Order Placed → Picked Up → At Facility → Processing → Out for Delivery → Delivered)
- Assigned delivery partner details
- Processing facility information
- Estimated delivery time""",
    ),
    (
        "What payment methods are accepted?",
        """WashGo accepts all major payment methods:
- **UPI** (PhonePe, GPay, Paytm, BHIM)
- **Credit/Debit Cards** (Visa, Mastercard, RuPay)
- **Cash on Delivery**
- **WashGo Wallet** (load money & get 5% cashback)

All digital payments are processed securely via encrypted gateways.""",
    ),
    (
        "How do I cancel or reschedule my order?",
        """You can cancel or reschedule your order **up to 2 hours before** the scheduled pickup time.
- Go to the **Track Order** page, enter your Order ID
- Contact our support team via WhatsApp at **+91 98765 43200**
- Or email us at **support@washgo.in**

Cancellations after pickup has been initiated are not eligible for a refund.""",
    ),
]

for question, answer in faqs:
    with st.expander(f"❓ {question}"):
        st.markdown(answer)

st.markdown("<div class='green-divider'></div>", unsafe_allow_html=True)

# ── Contact & Footer ──────────────────────────────────────────────────────────
st.markdown("<div class='section-heading'>📞 Contact Us</div>", unsafe_allow_html=True)

ct1, ct2, ct3 = st.columns(3)
contacts = [
    ("📱", "WhatsApp / Phone", "+91 98765 43200", "Mon–Sun · 8 AM – 8 PM"),
    ("📧", "Email Support", "support@washgo.in", "Response within 2 hours"),
    ("🏢", "Head Office", "Hitech City, Hyderabad", "Telangana – 500081"),
]
for col, (icon, title, val, note) in zip([ct1, ct2, ct3], contacts):
    with col:
        st.markdown(f"""
        <div style='background:#F1F8E9; border-radius:14px; padding:20px; text-align:center;
             border:1px solid #C8E6C9;'>
            <div style='font-size:32px;'>{icon}</div>
            <div style='font-weight:700; color:#1B5E20; font-size:14px; margin-top:8px;'>{title}</div>
            <div style='color:#212121; font-size:15px; font-weight:600; margin-top:4px;'>{val}</div>
            <div style='color:#9E9E9E; font-size:12px; margin-top:4px;'>{note}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
cta_col1, cta_col2, cta_col3 = st.columns([2, 1, 2])
with cta_col2:
    if st.button("🧺 Book Your First Order →", use_container_width=True, type="primary"):
        st.switch_page("pages/1_🧺_Book_Laundry.py")

st.markdown("""
<div style='text-align:center; color:#9E9E9E; font-size:13px; padding:24px 0 32px;'>
    © 2026 WashGo Technologies Pvt. Ltd. · Hyderabad, Telangana<br>
    Made with ❤️ in India · All rights reserved
</div>
""", unsafe_allow_html=True)
