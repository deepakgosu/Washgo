import streamlit as st
import pandas as pd
import random
import string
from datetime import datetime, timedelta

from utils.data import (
    init_session_state, SERVICES, AREAS, PARTNERS, FACILITIES,
    TIME_SLOTS, DELIVERY_FEE, STATUSES, STATUS_COLORS,
)

st.set_page_config(
    page_title="Book Laundry – WashGo",
    page_icon="🧺",
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

/* Step indicator */
.step-indicator {
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 32px; gap: 0;
}
.step-circle {
    width: 40px; height: 40px; border-radius: 50%; display: flex;
    align-items: center; justify-content: center; font-weight: 700; font-size: 15px;
    z-index: 1;
}
.step-active   { background: #2E7D32; color: #fff; box-shadow: 0 0 0 4px #C8E6C9; }
.step-done     { background: #43A047; color: #fff; }
.step-pending  { background: #E0E0E0; color: #9E9E9E; }
.step-label    { font-size: 12px; font-weight: 600; margin-top: 6px; color: #616161; }
.step-connector { flex: 1; height: 3px; max-width: 80px; background: #E0E0E0; }
.step-connector-done { background: #43A047; }

/* Form card */
.form-card {
    background: #fff; border-radius: 16px; padding: 28px 32px;
    box-shadow: 0 2px 16px rgba(0,0,0,0.07); border: 1px solid #E8F5E9;
    margin-bottom: 20px;
}
.form-section-title {
    font-size: 18px; font-weight: 700; color: #1B5E20; margin-bottom: 16px;
    padding-bottom: 10px; border-bottom: 2px solid #E8F5E9;
}

/* Service radio card */
.service-option {
    background: #F9FBE7; border: 2px solid #DCEDC8; border-radius: 12px;
    padding: 14px 18px; margin-bottom: 8px; cursor: pointer;
    transition: border-color 0.15s, background 0.15s;
}
.service-option:hover { border-color: #2E7D32; background: #F1F8E9; }

/* Summary card */
.summary-card {
    background: #F1F8E9; border-radius: 16px; padding: 24px;
    border: 2px solid #C8E6C9; position: sticky; top: 20px;
}
.summary-title { font-size: 16px; font-weight: 700; color: #1B5E20; margin-bottom: 16px; }
.summary-row { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }
.summary-row-bold { font-weight: 700; color: #1B5E20; font-size: 16px; border-top: 1px solid #C8E6C9; padding-top: 10px; margin-top: 4px; }
.summary-label { color: #616161; }
.summary-value { color: #212121; font-weight: 600; }

/* Success box */
.success-box {
    background: linear-gradient(135deg, #1B5E20, #2E7D32);
    border-radius: 20px; padding: 40px; text-align: center; color: #fff;
    margin: 20px 0;
}
.order-id-badge {
    background: #FF6F00; color: #fff; font-size: 28px; font-weight: 800;
    padding: 12px 32px; border-radius: 50px; display: inline-block; margin: 16px 0;
    letter-spacing: 2px;
}

/* Green button override */
.stButton>button[kind="primary"] {
    background: #2E7D32 !important; color: #fff !important;
    border: none !important; border-radius: 8px !important; font-weight: 600 !important;
}
.stButton>button[kind="primary"]:hover { background: #1B5E20 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:16px 0 8px;'>
        <span style='font-size:44px;'>🧺</span>
        <h2 style='margin:4px 0 0; font-size:24px; font-weight:800;'>WashGo</h2>
        <p style='font-size:12px; opacity:0.7; margin:0;'>Book Laundry</p>
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
        💡 <strong>Tip:</strong> Express Wash delivers same day if ordered before 12 PM.
    </div>
    """, unsafe_allow_html=True)

# ── Page Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-header">
    <h1>🧺 Book Laundry</h1>
    <p>Schedule a pickup in under 2 minutes</p>
</div>
""", unsafe_allow_html=True)


# ── Step Indicator ────────────────────────────────────────────────────────────
def render_step_indicator(current_step: int):
    steps_info = ["Service & Location", "Schedule Pickup", "Confirmation"]
    html = "<div class='step-indicator'>"
    for i, label in enumerate(steps_info, start=1):
        if i < current_step:
            cls = "step-done"
            icon = "✓"
        elif i == current_step:
            cls = "step-active"
            icon = str(i)
        else:
            cls = "step-pending"
            icon = str(i)

        html += f"""
        <div style='display:flex;flex-direction:column;align-items:center;'>
            <div class='step-circle {cls}'>{icon}</div>
            <div class='step-label'>{label}</div>
        </div>"""
        if i < 3:
            connector_cls = "step-connector-done" if i < current_step else ""
            html += f"<div class='step-connector {connector_cls}' style='margin-bottom:22px;'></div>"

    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


current_step = st.session_state.booking_step
render_step_indicator(current_step)

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 – Service & Location
# ═══════════════════════════════════════════════════════════════════════════════
if current_step == 1:
    left_col, right_col = st.columns([3, 2])

    with left_col:
        # Customer Details
        st.markdown("<div class='form-section-title'>👤 Customer Details</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Full Name *", placeholder="e.g. Rahul Sharma",
                                 value=st.session_state.booking_data.get("customer_name", ""))
        with c2:
            phone = st.text_input("Phone Number *", placeholder="10-digit mobile number",
                                  value=st.session_state.booking_data.get("phone", ""),
                                  max_chars=10)

        st.markdown("<div class='form-section-title' style='margin-top:20px;'>📍 Pickup Location</div>", unsafe_allow_html=True)
        c3, c4 = st.columns([1, 2])
        with c3:
            area_list = AREAS
            saved_area = st.session_state.booking_data.get("area", AREAS[0])
            area_idx = area_list.index(saved_area) if saved_area in area_list else 0
            area = st.selectbox("Area *", AREAS, index=area_idx)
        with c4:
            address = st.text_area("Full Address *", placeholder="Flat/House No, Street, Landmark",
                                   height=80,
                                   value=st.session_state.booking_data.get("address", ""))

        # Service Selection
        st.markdown("<div class='form-section-title' style='margin-top:20px;'>🧺 Select Service</div>", unsafe_allow_html=True)
        service_names = list(SERVICES.keys())
        saved_service = st.session_state.booking_data.get("service", service_names[0])
        svc_idx = service_names.index(saved_service) if saved_service in service_names else 0

        service_labels = []
        for svc_name, svc_info in SERVICES.items():
            label = f"{svc_info['icon']} {svc_name}  ·  ₹{svc_info['price']}/{svc_info['unit']}  ·  ⏱ {svc_info['turnaround']}"
            service_labels.append(label)

        selected_label = st.radio(
            "Service",
            service_labels,
            index=svc_idx,
            label_visibility="collapsed",
        )
        selected_service_name = service_names[service_labels.index(selected_label)]
        selected_service = SERVICES[selected_service_name]

        # Qty
        st.markdown("<div class='form-section-title' style='margin-top:20px;'>⚖️ Quantity</div>", unsafe_allow_html=True)
        if selected_service["unit"] == "kg":
            qty = st.number_input(
                f"Weight (kg)",
                min_value=1.0, max_value=30.0, step=0.5,
                value=float(st.session_state.booking_data.get("qty", 3.0)),
            )
        else:
            qty = st.number_input(
                f"Number of pieces",
                min_value=1, max_value=50, step=1,
                value=int(st.session_state.booking_data.get("qty", 3)),
            )

        st.markdown("<div class='form-section-title' style='margin-top:20px;'>📝 Special Instructions</div>", unsafe_allow_html=True)
        instructions = st.text_area(
            "Any special instructions?",
            placeholder="e.g. Handle with care, No fabric softener, Separate colours…",
            height=80,
            value=st.session_state.booking_data.get("special_instructions", ""),
            label_visibility="collapsed",
        )

    with right_col:
        subtotal = round(qty * selected_service["price"], 2)
        total = subtotal + DELIVERY_FEE
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-title">🧾 Order Preview</div>
            <div class="summary-row">
                <span class="summary-label">Service</span>
                <span class="summary-value">{selected_service['icon']} {selected_service_name}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Quantity</span>
                <span class="summary-value">{qty} {selected_service['unit']}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Rate</span>
                <span class="summary-value">₹{selected_service['price']}/{selected_service['unit']}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Subtotal</span>
                <span class="summary-value">₹{subtotal:.2f}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Delivery Fee</span>
                <span class="summary-value">₹{DELIVERY_FEE}</span>
            </div>
            <div class="summary-row summary-row-bold">
                <span>Total</span>
                <span style='color:#FF6F00;'>₹{total:.2f}</span>
            </div>
            <div style='margin-top:16px; padding:10px; background:#E8F5E9; border-radius:8px; font-size:13px; color:#388E3C;'>
                ⏱ Estimated delivery: <strong>{selected_service['turnaround']}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([3, 1, 1])
    with btn_col3:
        continue_clicked = st.button("Continue →", type="primary", use_container_width=True)

    if continue_clicked:
        errors = []
        if not name.strip():
            errors.append("Please enter your full name.")
        if not phone.strip() or not phone.strip().isdigit() or len(phone.strip()) != 10:
            errors.append("Please enter a valid 10-digit phone number.")
        if not area:
            errors.append("Please select your area.")
        if not address.strip():
            errors.append("Please enter your pickup address.")

        if errors:
            for err in errors:
                st.error(err)
        else:
            st.session_state.booking_data = {
                "customer_name": name.strip(),
                "phone": phone.strip(),
                "area": area,
                "address": address.strip(),
                "service": selected_service_name,
                "qty": qty,
                "unit": selected_service["unit"],
                "price_per_unit": selected_service["price"],
                "subtotal": subtotal,
                "total": total,
                "service_icon": selected_service["icon"],
                "turnaround": selected_service["turnaround"],
                "special_instructions": instructions.strip(),
            }
            st.session_state.booking_step = 2
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 – Schedule Pickup
# ═══════════════════════════════════════════════════════════════════════════════
elif current_step == 2:
    bd = st.session_state.booking_data
    left_col, right_col = st.columns([3, 2])

    with left_col:
        st.markdown("<div class='form-section-title'>📅 Pickup Schedule</div>", unsafe_allow_html=True)

        today = datetime.now().date()
        max_date = today + timedelta(days=7)
        pickup_date = st.date_input(
            "Pickup Date *",
            value=bd.get("pickup_date", today),
            min_value=today,
            max_value=max_date,
        )

        st.markdown("<div class='form-section-title' style='margin-top:20px;'>🕐 Pickup Time Slot</div>", unsafe_allow_html=True)
        saved_slot = bd.get("time_slot", TIME_SLOTS[0])
        slot_idx = TIME_SLOTS.index(saved_slot) if saved_slot in TIME_SLOTS else 0
        time_slot = st.radio(
            "Time Slot",
            TIME_SLOTS,
            index=slot_idx,
            label_visibility="collapsed",
        )

        st.markdown("<div class='form-section-title' style='margin-top:20px;'>🚚 Delivery & Payment</div>", unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            delivery_type = st.radio(
                "Delivery Type",
                ["Same Day", "Next Day"],
                index=0 if bd.get("delivery_type", "Next Day") == "Same Day" else 1,
            )
        with d2:
            payment_method = st.radio(
                "Payment Method",
                ["UPI", "Card", "Cash", "Wallet"],
                index=["UPI", "Card", "Cash", "Wallet"].index(bd.get("payment_method", "UPI")),
            )

    with right_col:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-title">🧾 Order Summary</div>
            <div class="summary-row">
                <span class="summary-label">Customer</span>
                <span class="summary-value">{bd.get('customer_name','–')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Phone</span>
                <span class="summary-value">{bd.get('phone','–')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Area</span>
                <span class="summary-value">📍 {bd.get('area','–')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Service</span>
                <span class="summary-value">{bd.get('service_icon','🧺')} {bd.get('service','–')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Quantity</span>
                <span class="summary-value">{bd.get('qty','–')} {bd.get('unit','')}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Subtotal</span>
                <span class="summary-value">₹{bd.get('subtotal',0):.2f}</span>
            </div>
            <div class="summary-row">
                <span class="summary-label">Delivery Fee</span>
                <span class="summary-value">₹{DELIVERY_FEE}</span>
            </div>
            <div class="summary-row summary-row-bold">
                <span>Total Payable</span>
                <span style='color:#FF6F00;'>₹{bd.get('total',0):.2f}</span>
            </div>
            <div style='margin-top:12px;padding:8px;background:#E8F5E9;border-radius:8px;font-size:12px;color:#388E3C;'>
                📍 {bd.get('address','–')}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2, b3 = st.columns([1, 2, 1])
    with b1:
        if st.button("← Back", use_container_width=True):
            st.session_state.booking_step = 1
            st.rerun()
    with b3:
        confirm_clicked = st.button("Confirm Order →", type="primary", use_container_width=True)

    if confirm_clicked:
        st.session_state.booking_data.update({
            "pickup_date": pickup_date,
            "time_slot": time_slot,
            "delivery_type": delivery_type,
            "payment_method": payment_method,
        })
        st.session_state.booking_step = 3
        st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 – Confirmation
# ═══════════════════════════════════════════════════════════════════════════════
elif current_step == 3:
    bd = st.session_state.booking_data

    # Generate order only once per booking
    if "confirmed_order_id" not in st.session_state.booking_data:
        with st.spinner("Placing your order…"):
            import time; time.sleep(1.2)

        order_id = "WG" + "".join(random.choices(string.digits, k=5))
        partner = random.choice(PARTNERS)
        facility = random.choice(FACILITIES)

        st.session_state.booking_data["confirmed_order_id"] = order_id
        st.session_state.booking_data["assigned_partner"] = partner
        st.session_state.booking_data["assigned_facility"] = facility["name"]
        st.session_state.last_order_id = order_id

        # Add to orders dataframe
        new_row = {
            "order_id": order_id,
            "customer_name": bd.get("customer_name"),
            "phone": bd.get("phone"),
            "area": bd.get("area"),
            "address": bd.get("address"),
            "service": bd.get("service"),
            "weight_kg": bd.get("qty") if bd.get("unit") == "kg" else 0,
            "pieces": bd.get("qty") if bd.get("unit") == "piece" else 0,
            "delivery_type": bd.get("delivery_type", "Next Day"),
            "time_slot": bd.get("time_slot"),
            "status": "Order Placed",
            "status_idx": 0,
            "partner_id": partner["id"],
            "partner_name": partner["name"],
            "facility": facility["name"],
            "amount": bd.get("total"),
            "payment_method": bd.get("payment_method"),
            "payment_status": "Pending",
            "created_at": datetime.now(),
            "rating": None,
            "special_instructions": bd.get("special_instructions", ""),
        }
        new_df = pd.DataFrame([new_row])
        st.session_state.orders_df = pd.concat(
            [st.session_state.orders_df, new_df], ignore_index=True
        )

    st.balloons()

    order_id = st.session_state.booking_data["confirmed_order_id"]
    partner = st.session_state.booking_data["assigned_partner"]
    facility_name = st.session_state.booking_data["assigned_facility"]

    st.markdown(f"""
    <div class="success-box">
        <div style='font-size:64px;'>🎉</div>
        <h2 style='margin:8px 0; font-size:28px;'>Order Placed Successfully!</h2>
        <p style='color:#A5D6A7; margin-bottom:20px;'>Your laundry is in good hands</p>
        <div class="order-id-badge">{order_id}</div>
        <p style='color:#C8E6C9; margin-top:16px; font-size:14px;'>
            Save this Order ID to track your laundry anytime
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📋 Order Details")
        details = {
            "Order ID": order_id,
            "Customer": bd.get("customer_name"),
            "Phone": bd.get("phone"),
            "Area": bd.get("area"),
            "Service": f"{bd.get('service_icon','')} {bd.get('service')}",
            "Quantity": f"{bd.get('qty')} {bd.get('unit')}",
            "Pickup Date": str(bd.get("pickup_date")),
            "Time Slot": bd.get("time_slot"),
            "Delivery Type": bd.get("delivery_type"),
            "Payment": bd.get("payment_method"),
            "Amount": f"₹{bd.get('total'):.2f}",
            "Status": "✅ Order Placed",
        }
        for k, v in details.items():
            col_a, col_b = st.columns([1, 1])
            col_a.markdown(f"**{k}**")
            col_b.markdown(str(v))
        st.divider()

    with c2:
        st.markdown("#### 🚚 Assigned Partner")
        st.markdown(f"""
        <div style='background:#F1F8E9; border-radius:12px; padding:20px; border:1px solid #C8E6C9; margin-bottom:12px;'>
            <div style='font-size:32px; margin-bottom:8px;'>👤</div>
            <div style='font-weight:700; font-size:16px; color:#1B5E20;'>{partner['name']}</div>
            <div style='color:#616161; font-size:14px;'>📞 {partner['phone']}</div>
            <div style='color:#616161; font-size:14px;'>⭐ {partner['rating']} · {partner['deliveries']} deliveries</div>
            <div style='color:#616161; font-size:14px;'>📍 {partner['area']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🏭 Processing Facility")
        st.markdown(f"""
        <div style='background:#E8F5E9; border-radius:12px; padding:20px; border:1px solid #A5D6A7;'>
            <div style='font-size:32px; margin-bottom:8px;'>🏭</div>
            <div style='font-weight:700; font-size:16px; color:#1B5E20;'>{facility_name}</div>
            <div style='color:#388E3C; font-size:14px;'>✅ Verified & Trusted Partner</div>
        </div>
        """, unsafe_allow_html=True)

        if bd.get("special_instructions"):
            st.markdown("#### 📝 Special Instructions")
            st.info(bd.get("special_instructions"))

    st.markdown("<br>", unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns([1, 1, 1])
    with btn1:
        if st.button("📍 Track Your Order", use_container_width=True, type="primary"):
            st.session_state.last_order_id = order_id
            st.switch_page("pages/2_📍_Track_Order.py")
    with btn3:
        if st.button("🧺 Book Another Order", use_container_width=True):
            st.session_state.booking_step = 1
            st.session_state.booking_data = {}
            st.rerun()
