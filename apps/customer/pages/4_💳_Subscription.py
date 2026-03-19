import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from utils.store import get_store, get_customer_orders

st.set_page_config(page_title="Subscription – WashGo", page_icon="💳", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F5F5F5; }
[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E0E0E0; }
[data-testid="stSidebar"] * { color: #1A1A1A !important; }

.page-title { font-size: 1.6rem; font-weight: 800; color: #1A1A1A; margin-bottom: 4px; }
.page-sub   { font-size: 0.9rem; color: #888; margin-bottom: 24px; }

.plan-card {
    background: #FFFFFF;
    border-radius: 20px;
    padding: 28px 24px;
    border: 2px solid #F0F0F0;
    height: 100%;
    position: relative;
}
.plan-card.popular {
    border-color: #00C853;
    box-shadow: 0 8px 32px rgba(0,200,83,0.12);
}
.plan-card.current-plan { border-color: #1A1A1A; }

.plan-badge {
    position: absolute;
    top: -12px; right: 20px;
    background: #00C853;
    color: #fff;
    padding: 3px 14px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
}
.plan-badge.current-badge { background: #1A1A1A; }

.plan-name  { font-size: 1.1rem; font-weight: 800; color: #1A1A1A; margin-bottom: 4px; }
.plan-price { font-size: 2rem; font-weight: 800; color: #1A1A1A; }
.plan-price span { font-size: 0.85rem; font-weight: 400; color: #888; }
.plan-period { font-size: 0.8rem; color: #888; margin-top: 2px; margin-bottom: 16px; }

.plan-features { list-style: none; padding: 0; margin: 0 0 20px; }
.plan-features li { font-size: 0.88rem; color: #555; padding: 5px 0; }
.plan-features li::before { content: "✓ "; color: #00C853; font-weight: 700; }
.plan-features li.disabled { color: #BBBBBB; }
.plan-features li.disabled::before { content: "✗ "; color: #BBBBBB; }

.savings-card {
    background: linear-gradient(135deg, #00C853, #00A846);
    color: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin-top: 28px;
    text-align: center;
}
.savings-card h3 { margin: 0 0 8px; font-size: 1.1rem; }
.savings-card p  { margin: 0; font-size: 2rem; font-weight: 800; }
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

st.markdown('<div class="page-title">💳 Subscription Plans</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Save more every time you wash.</div>', unsafe_allow_html=True)

cust = st.session_state.customer
current_plan = cust.get("subscription")

PLANS = [
    {
        "id": "basic",
        "name": "Basic",
        "price": "Free",
        "period": "",
        "features": [
            ("Pay per order", True),
            ("Standard delivery", True),
            ("10% order discount", False),
            ("Free delivery", False),
            ("Priority support", False),
            ("Express processing", False),
        ],
        "popular": False,
    },
    {
        "id": "plus",
        "name": "WashGo Plus",
        "price": "₹999",
        "period": "/month",
        "features": [
            ("Pay per order", True),
            ("Standard delivery", True),
            ("10% off all orders", True),
            ("Free delivery on orders ₹300+", True),
            ("Priority support", True),
            ("Express processing", False),
        ],
        "popular": True,
    },
    {
        "id": "premium",
        "name": "WashGo Premium",
        "price": "₹1,799",
        "period": "/month",
        "features": [
            ("Pay per order", True),
            ("Free delivery always", True),
            ("20% off all orders", True),
            ("Free delivery always", True),
            ("Dedicated support", True),
            ("Express processing guaranteed", True),
        ],
        "popular": False,
        "offer": "First 3 months: ₹1,499/month",
    },
]

cols = st.columns(3)
for i, plan in enumerate(PLANS):
    with cols[i]:
        is_current = current_plan == plan["id"] if current_plan else (plan["id"] == "basic" and not current_plan)
        card_cls = "plan-card"
        if plan.get("popular") and not is_current:
            card_cls += " popular"
        if is_current:
            card_cls += " current-plan"

        badge_html = ""
        if is_current:
            badge_html = '<div class="plan-badge current-badge">Current Plan</div>'
        elif plan.get("popular"):
            badge_html = '<div class="plan-badge">Most Popular</div>'

        features_html = '<ul class="plan-features">'
        for feat_name, enabled in plan["features"]:
            li_cls = "" if enabled else " disabled"
            features_html += '<li class="' + li_cls + '">' + feat_name + '</li>'
        features_html += "</ul>"

        offer_html = ""
        if plan.get("offer"):
            offer_html = '<div style="font-size:0.78rem;color:#FF6D00;font-weight:600;margin-bottom:12px;">🎁 ' + plan["offer"] + '</div>'

        st.markdown(
            '<div class="' + card_cls + '">'
            + badge_html +
            '<div class="plan-name">' + plan["name"] + '</div>'
            '<div class="plan-price">' + plan["price"] + '<span>' + plan["period"] + '</span></div>'
            '<div class="plan-period">Billed monthly · Cancel anytime</div>'
            + offer_html
            + features_html +
            '</div>',
            unsafe_allow_html=True
        )
        if is_current:
            st.success("Active Plan")
            if plan["id"] != "basic":
                if st.button("Cancel Plan", key="cancel_" + plan["id"], use_container_width=True):
                    st.session_state.customer["subscription"] = None
                    st.success("Plan cancelled.")
                    st.rerun()
        else:
            if plan["id"] == "basic":
                st.button("Downgrade to Free", key="sub_" + plan["id"], use_container_width=True, disabled=True)
            else:
                if st.button("Subscribe →", key="sub_" + plan["id"], use_container_width=True, type="primary"):
                    st.session_state.customer["subscription"] = plan["id"]
                    st.success("Subscribed to " + plan["name"] + "!")
                    st.rerun()

# ── Savings calculator ─────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("💰 Savings Calculator")

monthly_orders = st.slider("How many orders per month?", 1, 20, 4)
avg_order_val  = st.slider("Average order value (₹)", 100, 1000, 350)

normal_total  = monthly_orders * avg_order_val
plus_discount = normal_total * 0.10
plus_delivery = monthly_orders * 49 if avg_order_val >= 300 else 0
plus_savings  = plus_discount + plus_delivery - 999

premium_discount = normal_total * 0.20
premium_delivery = monthly_orders * 49
premium_savings  = premium_discount + premium_delivery - 1799

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        '<div class="savings-card"><h3>WashGo Plus Savings</h3><p>₹' + str(int(max(plus_savings, 0))) + '/mo</p></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        '<div class="savings-card" style="background:linear-gradient(135deg,#1A1A1A,#333);"><h3>WashGo Premium Savings</h3><p>₹' + str(int(max(premium_savings, 0))) + '/mo</p></div>',
        unsafe_allow_html=True
    )

# ── This month's savings ───────────────────────────────────────────────────────
if current_plan and current_plan != "basic":
    phone = cust.get("phone", "")
    orders = get_customer_orders(phone) if phone else st.session_state.orders_df.iloc[0:0]
    from datetime import datetime
    now = datetime.now()
    this_month = orders[
        (orders["created_at"].apply(lambda x: x.month if hasattr(x, "month") else 0) == now.month) &
        (orders["created_at"].apply(lambda x: x.year  if hasattr(x, "year")  else 0) == now.year)
    ] if not orders.empty else orders

    disc_rate = 0.20 if current_plan == "premium" else 0.10
    saved = this_month["amount"].sum() * disc_rate if not this_month.empty else 0
    st.info("This month you've saved approximately ₹" + str(int(saved)) + " with your " + current_plan.title() + " plan!")
