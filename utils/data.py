import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import streamlit as st
from utils import database as db

AREAS = [
    "Hitech City", "Gachibowli", "Kondapur", "Madhapur",
    "Jubilee Hills", "Banjara Hills", "Kukatpally", "Miyapur",
    "Begumpet", "Secunderabad", "Ameerpet", "SR Nagar",
]

SERVICES = {
    "Regular Wash":  {"price": 60,  "unit": "kg",    "turnaround": "Next Day",  "icon": "🧺"},
    "Express Wash":  {"price": 100, "unit": "kg",    "turnaround": "Same Day",  "icon": "⚡"},
    "Dry Cleaning":  {"price": 150, "unit": "piece", "turnaround": "2-3 Days", "icon": "👔"},
    "Premium Care":  {"price": 200, "unit": "piece", "turnaround": "2 Days",   "icon": "✨"},
    "Ironing Only":  {"price": 20,  "unit": "piece", "turnaround": "Same Day",  "icon": "👕"},
    "Wash & Iron":   {"price": 80,  "unit": "kg",    "turnaround": "Next Day",  "icon": "🌟"},
}

STATUSES = [
    "Order Placed", "Picked Up", "At Facility",
    "Processing", "Out for Delivery", "Delivered",
]

STATUS_COLORS = {
    "Order Placed":       "#FFA000",
    "Picked Up":          "#1E88E5",
    "At Facility":        "#8E24AA",
    "Processing":         "#039BE5",
    "Out for Delivery":   "#F4511E",
    "Delivered":          "#43A047",
}

PARTNERS = [
    {"id": "P001", "name": "Ravi Kumar",    "rating": 4.8, "deliveries": 234, "phone": "9876543210", "area": "Gachibowli"},
    {"id": "P002", "name": "Suresh Reddy",  "rating": 4.6, "deliveries": 189, "phone": "9876543211", "area": "Kondapur"},
    {"id": "P003", "name": "Venkat Rao",    "rating": 4.9, "deliveries": 312, "phone": "9876543212", "area": "Madhapur"},
    {"id": "P004", "name": "Prasad Naidu",  "rating": 4.7, "deliveries": 156, "phone": "9876543213", "area": "Hitech City"},
    {"id": "P005", "name": "Kiran Babu",    "rating": 4.5, "deliveries":  98, "phone": "9876543214", "area": "Kukatpally"},
]

FACILITIES = [
    {"name": "CleanPro Laundry",  "area": "Gachibowli", "rating": 4.7},
    {"name": "FreshWash Center",  "area": "Kondapur",   "rating": 4.8},
    {"name": "QuickClean Hub",    "area": "Madhapur",   "rating": 4.6},
    {"name": "Premium Wash",      "area": "Hitech City","rating": 4.9},
]

TIME_SLOTS = [
    "8:00 AM – 10:00 AM", "10:00 AM – 12:00 PM",
    "12:00 PM – 2:00 PM",  "2:00 PM – 4:00 PM",
    "4:00 PM – 6:00 PM",   "6:00 PM – 8:00 PM",
]

CUSTOMERS = [
    "Arun Sharma", "Priya Reddy", "Rahul Gupta", "Sneha Patel",
    "Vikram Singh", "Kavya Nair", "Rohit Kumar", "Ananya Iyer",
    "Sai Krishna", "Deepika Rao", "Naveen Babu", "Pooja Mehta",
    "Arjun Verma", "Divya Krishnan", "Manoj Tiwari",
]

DELIVERY_FEE = 49


def generate_sample_orders(n: int = 60) -> pd.DataFrame:
    random.seed(42)
    orders = []
    base_date = datetime.now() - timedelta(days=30)

    for i in range(n):
        service = random.choice(list(SERVICES.keys()))
        svc = SERVICES[service]
        area = random.choice(AREAS)
        weight = round(random.uniform(2, 12), 1)
        pieces = random.randint(3, 25)
        qty = weight if svc["unit"] == "kg" else pieces
        amount = round(qty * svc["price"] + DELIVERY_FEE, 2)

        created = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(8, 20),
            minutes=random.randint(0, 59),
        )
        status_idx = random.randint(0, 5)
        partner = random.choice(PARTNERS)

        orders.append({
            "order_id":            f"WG{10000 + i}",
            "customer_name":       random.choice(CUSTOMERS),
            "phone":               f"9{random.randint(100000000, 999999999)}",
            "area":                area,
            "address":             f"Flat {random.randint(1,50)}, {random.choice(['Lotus Pond', 'Rainbow Colony', 'Green Valley', 'Tech Park Rd'])}, {area}",
            "service":             service,
            "weight_kg":           weight,
            "pieces":              pieces,
            "delivery_type":       random.choice(["Same Day", "Next Day"]),
            "time_slot":           random.choice(TIME_SLOTS),
            "status":              STATUSES[status_idx],
            "status_idx":          status_idx,
            "partner_id":          partner["id"],
            "partner_name":        partner["name"],
            "facility":            random.choice(FACILITIES)["name"],
            "amount":              amount,
            "payment_method":      random.choice(["UPI", "Card", "Cash", "Wallet"]),
            "payment_status":      "Paid" if status_idx > 1 else random.choice(["Paid", "Pending"]),
            "created_at":          created,
            "rating":              random.choice([3, 4, 4, 5, 5, 5]) if status_idx == 5 else None,
            "special_instructions": random.choice(["", "Handle with care", "No fabric softener", "Separate colours", "", ""]),
        })

    return pd.DataFrame(orders)


def init_session_state():
    if "orders_df" not in st.session_state:
        # Try PostgreSQL first; fall back to in-memory sample data
        if db.is_available():
            db.create_tables()
            if db.is_orders_empty():
                sample = generate_sample_orders(60)
                db.seed_orders(sample)
                db.seed_partners(PARTNERS)
                st.session_state.orders_df = sample
            else:
                loaded = db.load_orders()
                st.session_state.orders_df = (
                    loaded if loaded is not None else generate_sample_orders(60)
                )
        else:
            st.session_state.orders_df = generate_sample_orders(60)

    if "logged_in_partner" not in st.session_state:
        st.session_state.logged_in_partner = None
    if "booking_step" not in st.session_state:
        st.session_state.booking_step = 1
    if "booking_data" not in st.session_state:
        st.session_state.booking_data = {}
    if "last_order_id" not in st.session_state:
        st.session_state.last_order_id = None
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
