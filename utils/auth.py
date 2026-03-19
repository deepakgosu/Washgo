"""
WashGo – Google Authentication Helper
--------------------------------------
Uses streamlit-google-auth for OAuth 2.0 login.

Setup required (see README_AUTH.md):
  1. Create Google Cloud project & OAuth 2.0 credentials
  2. Download credentials JSON → save as google_credentials.json
  3. Add redirect URI: http://localhost:8501
"""

import streamlit as st
from streamlit_google_auth import Authenticate

# ── Constants ─────────────────────────────────────────────────────────────────
COOKIE_NAME = "washgo_auth"
COOKIE_KEY  = "washgo_super_secret_cookie_key_2025"
CREDENTIALS_PATH = "google_credentials.json"
REDIRECT_URI = "http://localhost:8501"


def get_authenticator() -> Authenticate:
    """Return a cached Authenticate instance."""
    if "authenticator" not in st.session_state:
        st.session_state.authenticator = Authenticate(
            secret_credentials_path=CREDENTIALS_PATH,
            cookie_name=COOKIE_NAME,
            cookie_key=COOKIE_KEY,
            redirect_uri=REDIRECT_URI,
        )
    return st.session_state.authenticator


def check_auth() -> bool:
    """
    Run the auth check and return True if the user is logged in.
    Call this at the top of every page before rendering content.
    """
    auth = get_authenticator()
    auth.check_authentification()
    return st.session_state.get("connected", False)


def render_login_page():
    """Render a full-page login UI with Google button."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    section[data-testid="stSidebar"] { display: none; }
    </style>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #1B5E20, #2E7D32);
            border-radius: 24px; padding: 48px 40px 40px;
            text-align: center; margin-top: 60px;
            box-shadow: 0 8px 40px rgba(46,125,50,0.25);
        ">
            <div style="font-size:64px; margin-bottom:8px;">🧺</div>
            <h1 style="color:#fff; font-size:36px; font-weight:800;
                       margin:0 0 6px; letter-spacing:-1px;">WashGo</h1>
            <p style="color:#A5D6A7; font-size:15px; margin:0 0 32px;">
                Hyderabad's #1 On-Demand Laundry Service
            </p>
            <div style="
                background: rgba(255,255,255,0.08);
                border-radius: 12px; padding: 20px;
                margin-bottom: 28px;
            ">
                <p style="color:#C8E6C9; font-size:13px; margin:0; line-height:1.7;">
                    🚀 Schedule laundry pickup in 60 seconds<br>
                    📍 Real-time order tracking<br>
                    ✅ Quality-guaranteed delivery<br>
                    💳 Cashless digital payments
                </p>
            </div>
            <p style="color:#81C784; font-size:13px; margin:0 0 20px;">
                Sign in to book your first order
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        auth = get_authenticator()
        auth.login()

        st.markdown("""
        <p style="text-align:center; color:#9E9E9E; font-size:12px; margin-top:16px;">
            By signing in, you agree to WashGo's Terms of Service.<br>
            We only access your name, email, and profile photo.
        </p>
        """, unsafe_allow_html=True)


def render_user_sidebar():
    """
    Render user avatar + name + logout in the sidebar.
    Call inside a `with st.sidebar:` block after auth check.
    """
    if not st.session_state.get("connected"):
        return

    user = st.session_state.get("user_info", {})
    name    = user.get("name", "Customer")
    email   = user.get("email", "")
    picture = user.get("picture", "")

    if picture:
        st.markdown(f"""
        <div style="text-align:center; padding:12px 0 4px;">
            <img src="{picture}" width="64" height="64"
                 style="border-radius:50%; border:3px solid #81C784;"/>
            <div style="font-weight:700; font-size:15px; margin-top:8px;">{name}</div>
            <div style="font-size:11px; opacity:0.7;">{email}</div>
        </div>
        <hr style="border-color:rgba(255,255,255,0.2); margin:12px 0;">
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align:center; padding:12px 0 4px;">
            <div style="font-size:40px;">👤</div>
            <div style="font-weight:700; font-size:15px; margin-top:8px;">{name}</div>
            <div style="font-size:11px; opacity:0.7;">{email}</div>
        </div>
        <hr style="border-color:rgba(255,255,255,0.2); margin:12px 0;">
        """, unsafe_allow_html=True)

    auth = get_authenticator()
    if st.button("🚪 Sign Out", use_container_width=True):
        auth.logout()


def require_login() -> bool:
    """
    Gate a page behind login.
    Returns True if logged in (page should render normally).
    Returns False and shows login page if not logged in.

    Usage at the top of any page:
        from utils.auth import require_login
        if not require_login():
            st.stop()
    """
    if check_auth():
        return True
    render_login_page()
    return False
