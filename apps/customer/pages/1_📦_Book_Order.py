import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

import streamlit as st
from datetime import datetime, timedelta
import random

from utils.store import get_store, add_order
from utils.data import SERVICES, AREAS, TIME_SLOTS, DELIVERY_FEE, PARTNERS, FACILITIES

st.set_page_config(page_title="Book Order – WashGo", page_icon="📦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #F5F5F5; }
[data-testid="stSidebar"] { background: #FFFFFF !important; border-right: 1px solid #E0E0E0; }
[data-testid="stSidebar"] * { color: #1A1A1A !important; }

.page-title { font-size: 1.6rem; font-weight: 800; color: #1A1A1A; margin-bottom: 4px; }
.page-sub   { font-size: 0.9rem; color: #888; margin-bottom: 24px; }

.step-bar {
    display: flex;
    gap: 8px;
    margin-bottom: 28px;
    align-items: center;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #BBBBBB;
}
.step-circle {
    width: 28px; height: 28px;
    border-radius: 50%;
    background: #E0E0E0;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.75rem; font-weight: 700; color: #888;
}
.step-circle.active { background: #00C853; color: #fff; }
.step-circle.done   { background: #1A1A1A; color: #fff; }
.step-item.active-label { color: #1A1A1A; }
.step-div { flex: 1; height: 2px; background: #E0E0E0; border-radius: 2px; }
.step-div.done { background: #00C853; }

.svc-card {
    background: #FFFFFF;
    border: 2px solid #F0F0F0;
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 20px;
    transition: all 0.2s;
}
.svc-card.selected { border-color: #00C853; background: #F0FFF4; }
.svc-icon-big { font-size: 2.4rem; }
.svc-card-name { font-size: 1rem; font-weight: 700; color: #1A1A1A; }
.svc-card-desc { font-size: 0.82rem; color: #888; margin-top: 3px; }
.svc-card-price { font-size: 1rem; font-weight: 700; color: #00C853; margin-left: auto; white-space: nowrap; }
.svc-turnaround { font-size: 0.75rem; color: #888; margin-top: 2px; text-align: right; }

.slot-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }
.slot-btn {
    padding: 10px 18px;
    border-radius: 10px;
    border: 2px solid #E0E0E0;
    background: #FFFFFF;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    color: #1A1A1A;
    transition: all 0.2s;
}
.slot-btn.selected { border-color: #00C853; background: #F0FFF4; color: #00C853; }

.price-box {
    background: #F8F8F8;
    border-radius: 12px;
    padding: 16px 20px;
    margin-top: 12px;
}
.price-row { display: flex; justify-content: space-between; font-size: 0.88rem; color: #555; margin-bottom: 6px; }
.price-total { display: flex; justify-content: space-between; font-size: 1rem; font-weight: 700; color: #1A1A1A; border-top: 1px solid #E0E0E0; padding-top: 8px; margin-top: 4px; }

.confirm-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    border: 1px solid #F0F0F0;
}
.confirm-row { display: flex; justify-content: space-between; font-size: 0.88rem; padding: 6px 0; border-bottom: 1px solid #F5F5F5; }
.confirm-row:last-child { border-bottom: none; }
.confirm-label { color: #888; }
.confirm-val   { font-weight: 600; color: #1A1A1A; }

.success-box {
    text-align: center;
    background: #FFFFFF;
    border-radius: 20px;
    padding: 48px 32px;
    max-width: 480px;
    margin: 40px auto;
    border: 2px solid #00C853;
}
.success-icon  { font-size: 4rem; }
.success-title { font-size: 1.5rem; font-weight: 800; color: #1A1A1A; margin: 16px 0 8px; }
.success-oid   { font-size: 1.2rem; font-weight: 700; color: #00C853; }
.success-sub   { color: #888; font-size: 0.9rem; margin-top: 8px; }
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

# ── Handle pre-selected service ───────────────────────────────────────────────
bd = st.session_state.booking_data

st.markdown('<div class="page-title">📦 Book a Wash</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Schedule a pickup in minutes.</div>', unsafe_allow_html=True)

step = st.session_state.get("booking_step", 1)

# Step bar
def step_class(n):
    if n < step:   return "done"
    if n == step:  return "active"
    return ""

def label_class(n):
    return "active-label" if n == step else ""

div_done = ["done" if i < step else "" for i in range(1, 5)]

st.markdown(
    '<div class="step-bar">'
    '<div class="step-item ' + label_class(1) + '"><div class="step-circle ' + step_class(1) + '">1</div>Service</div>'
    '<div class="step-div ' + div_done[0] + '"></div>'
    '<div class="step-item ' + label_class(2) + '"><div class="step-circle ' + step_class(2) + '">2</div>Details</div>'
    '<div class="step-div ' + div_done[1] + '"></div>'
    '<div class="step-item ' + label_class(3) + '"><div class="step-circle ' + step_class(3) + '">3</div>Schedule</div>'
    '<div class="step-div ' + div_done[2] + '"></div>'
    '<div class="step-item ' + label_class(4) + '"><div class="step-circle ' + step_class(4) + '">4</div>Confirm</div>'
    '</div>',
    unsafe_allow_html=True
)

# ── SUCCESS SCREEN ────────────────────────────────────────────────────────────
if step == 99:
    oid = st.session_state.get("last_order_id", "WG#####")
    st.balloons()
    st.markdown(
        '<div class="success-box">'
        '<div class="success-icon">✅</div>'
        '<div class="success-title">Order Placed!</div>'
        '<div class="success-oid">' + str(oid) + '</div>'
        '<div class="success-sub">Your pickup is scheduled. We\'ll keep you updated.</div>'
        '</div>',
        unsafe_allow_html=True
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Track Order →", use_container_width=True, type="primary"):
            st.session_state.booking_step = 1
            st.session_state.booking_data = {}
            st.switch_page("pages/2_📍_Track_Order.py")
    with col2:
        if st.button("Book Another", use_container_width=True):
            st.session_state.booking_step = 1
            st.session_state.booking_data = {}
            st.rerun()
    st.stop()

# ── STEP 1 — Choose Service ───────────────────────────────────────────────────
if step == 1:
    st.subheader("Step 1 — Choose a Service")
    selected_svc = bd.get("service", None)
    svc_descriptions = {
        "Regular Wash":  "Full machine wash with premium detergent. Best for everyday clothes.",
        "Express Wash":  "Same-day turnaround. Ideal when you need clothes fast.",
        "Dry Cleaning":  "Professional dry cleaning for suits, sarees, and delicates.",
        "Premium Care":  "Hand-washed with extra care for your luxury garments.",
        "Ironing Only":  "Crisp, wrinkle-free clothes pressed to perfection.",
        "Wash & Iron":   "Complete service — washed, dried, and ironed.",
    }
    for svc_name, svc in SERVICES.items():
        is_sel = selected_svc == svc_name
        card_class = "svc-card selected" if is_sel else "svc-card"
        desc = svc_descriptions.get(svc_name, "")
        check = " ✓" if is_sel else ""
        st.markdown(
            '<div class="' + card_class + '">'
            '<div class="svc-icon-big">' + svc["icon"] + '</div>'
            '<div style="flex:1;">'
            '<div class="svc-card-name">' + svc_name + check + '</div>'
            '<div class="svc-card-desc">' + desc + '</div>'
            '</div>'
            '<div style="text-align:right;">'
            '<div class="svc-card-price">₹' + str(svc["price"]) + '/' + svc["unit"] + '</div>'
            '<div class="svc-turnaround">' + svc["turnaround"] + '</div>'
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )
        if st.button("Select " + svc_name, key="sel_" + svc_name, use_container_width=True):
            bd["service"] = svc_name
            st.session_state.booking_data = bd
            st.session_state.booking_step = 2
            st.rerun()

# ── STEP 2 — Pickup Details ───────────────────────────────────────────────────
elif step == 2:
    st.subheader("Step 2 — Pickup Details")
    cust = st.session_state.customer
    svc_name = bd.get("service", "Regular Wash")
    svc = SERVICES[svc_name]

    area = st.selectbox("Pickup Area", AREAS, index=AREAS.index(cust.get("area", AREAS[0])) if cust.get("area") in AREAS else 0)
    address = st.text_input("Full Address", value=cust.get("addresses", [""])[0] if cust.get("addresses") else "")
    instructions = st.text_area("Special Instructions (optional)", placeholder="e.g. No fabric softener, separate whites")

    if svc["unit"] == "kg":
        weight = st.slider("Estimated Weight (kg)", 2, 20, 5)
        qty = weight
        st.info("Estimated weight: " + str(weight) + " kg")
    else:
        pieces = st.slider("Number of Pieces", 1, 30, 5)
        qty = pieces
        st.info("Number of pieces: " + str(pieces))

    base_price = round(qty * svc["price"], 2)
    total_price = base_price + DELIVERY_FEE
    st.markdown(
        '<div class="price-box">'
        '<div class="price-row"><span>Service (' + str(qty) + ' ' + svc["unit"] + ' × ₹' + str(svc["price"]) + ')</span><span>₹' + str(base_price) + '</span></div>'
        '<div class="price-row"><span>Delivery Fee</span><span>₹' + str(DELIVERY_FEE) + '</span></div>'
        '<div class="price-total"><span>Estimated Total</span><span>₹' + str(total_price) + '</span></div>'
        '</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.booking_step = 1
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            if not address.strip():
                st.error("Please enter your pickup address.")
            else:
                bd.update({"area": area, "address": address, "instructions": instructions,
                           "qty": qty, "base_price": base_price, "total_price": total_price})
                st.session_state.booking_data = bd
                st.session_state.booking_step = 3
                st.rerun()

# ── STEP 3 — Schedule ─────────────────────────────────────────────────────────
elif step == 3:
    st.subheader("Step 3 — Schedule Pickup")

    today = datetime.now().date()
    date_options = [today + timedelta(days=i) for i in range(7)]
    date_labels  = [d.strftime("%a, %d %b") for d in date_options]
    date_idx = st.radio("Pickup Date", range(len(date_labels)), format_func=lambda i: date_labels[i], horizontal=True)
    chosen_date = date_options[date_idx]

    st.markdown("**Pickup Time Slot**")
    slot_cols = st.columns(3)
    selected_slot = bd.get("time_slot", None)
    for i, slot in enumerate(TIME_SLOTS):
        with slot_cols[i % 3]:
            btn_label = ("✓ " if selected_slot == slot else "") + slot
            if st.button(btn_label, key="slot_" + str(i), use_container_width=True):
                bd["time_slot"] = slot
                st.session_state.booking_data = bd
                st.rerun()

    delivery_type = st.radio("Delivery Type", ["Same Day", "Next Day"], horizontal=True, index=0)

    svc_name = bd.get("service", "Regular Wash")
    turnaround = SERVICES[svc_name]["turnaround"]
    if delivery_type == "Same Day":
        est_delivery = chosen_date
    else:
        est_delivery = chosen_date + timedelta(days=1)
    st.info("Estimated delivery: " + est_delivery.strftime("%A, %d %b"))

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.booking_step = 2
            st.rerun()
    with col2:
        if st.button("Next →", use_container_width=True, type="primary"):
            if not bd.get("time_slot"):
                st.error("Please select a pickup time slot.")
            else:
                bd.update({"pickup_date": str(chosen_date), "delivery_type": delivery_type,
                           "est_delivery": str(est_delivery)})
                st.session_state.booking_data = bd
                st.session_state.booking_step = 4
                st.rerun()

# ── STEP 4 — Review & Confirm ─────────────────────────────────────────────────
elif step == 4:
    st.subheader("Step 4 — Review & Confirm")

    svc_name   = bd.get("service", "Regular Wash")
    area       = bd.get("area", "")
    address    = bd.get("address", "")
    qty        = bd.get("qty", 0)
    base_price = bd.get("base_price", 0)
    total      = bd.get("total_price", 0)
    slot       = bd.get("time_slot", "")
    pickup_date = bd.get("pickup_date", "")
    delivery_type = bd.get("delivery_type", "Next Day")
    est_delivery  = bd.get("est_delivery", "")
    instructions  = bd.get("instructions", "")

    svc = SERVICES[svc_name]

    st.markdown(
        '<div class="confirm-card">'
        '<div class="confirm-row"><span class="confirm-label">Service</span><span class="confirm-val">' + svc["icon"] + " " + svc_name + '</span></div>'
        '<div class="confirm-row"><span class="confirm-label">Quantity</span><span class="confirm-val">' + str(qty) + " " + svc["unit"] + '</span></div>'
        '<div class="confirm-row"><span class="confirm-label">Pickup</span><span class="confirm-val">' + pickup_date + " · " + slot + '</span></div>'
        '<div class="confirm-row"><span class="confirm-label">Area</span><span class="confirm-val">' + area + '</span></div>'
        '<div class="confirm-row"><span class="confirm-label">Address</span><span class="confirm-val">' + address + '</span></div>'
        '<div class="confirm-row"><span class="confirm-label">Delivery Type</span><span class="confirm-val">' + delivery_type + '</span></div>'
        '<div class="confirm-row"><span class="confirm-label">Est. Delivery</span><span class="confirm-val">' + est_delivery + '</span></div>'
        + ('<div class="confirm-row"><span class="confirm-label">Instructions</span><span class="confirm-val">' + instructions + '</span></div>' if instructions else '') +
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="price-box">'
        '<div class="price-row"><span>Service Cost</span><span>₹' + str(base_price) + '</span></div>'
        '<div class="price-row"><span>Delivery Fee</span><span>₹' + str(DELIVERY_FEE) + '</span></div>'
        '<div class="price-total"><span>Total</span><span>₹' + str(total) + '</span></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("**Payment Method**")
    payment = st.radio("", ["UPI", "Card", "Cash", "Wallet"], horizontal=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.booking_step = 3
            st.rerun()
    with col2:
        if st.button("✅ Confirm Order", use_container_width=True, type="primary"):
            cust = st.session_state.customer
            order_id = "WG" + str(random.randint(10000, 99999))
            partner = random.choice(PARTNERS)
            facility = random.choice(FACILITIES)
            order = {
                "order_id": order_id,
                "customer_name": cust["name"],
                "phone": cust["phone"],
                "area": area,
                "address": address,
                "service": svc_name,
                "weight_kg": qty if svc["unit"] == "kg" else 0,
                "pieces": qty if svc["unit"] == "piece" else 0,
                "delivery_type": delivery_type,
                "time_slot": slot,
                "status": "Order Placed",
                "status_idx": 0,
                "partner_id": partner["id"],
                "partner_name": partner["name"],
                "facility": facility["name"],
                "amount": total,
                "payment_method": payment,
                "payment_status": "Pending",
                "created_at": datetime.now(),
                "rating": None,
                "special_instructions": instructions,
            }
            add_order(order)
            st.session_state.last_order_id = order_id
            st.session_state.booking_step = 99
            st.rerun()
