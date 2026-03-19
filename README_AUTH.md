# Setting Up Google Login for WashGo

## Step 1 — Create Google Cloud Project

1. Go to https://console.cloud.google.com
2. Click **Select a project** (top bar) → **New Project**
3. Name it `washgo` → Click **Create**

## Step 2 — Enable Google Identity API

1. In the left menu → **APIs & Services** → **Library**
2. Search for **"Google+ API"** → Click it → Click **Enable**
3. Also enable **"Google Identity"** if shown

## Step 3 — Create OAuth Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth 2.0 Client IDs**
3. If prompted, configure the **OAuth consent screen** first:
   - User type: **External**
   - App name: `WashGo`
   - User support email: your email
   - Developer contact: your email
   - Click **Save and Continue** through all steps
4. Back at Create OAuth Client:
   - Application type: **Web application**
   - Name: `WashGo Web`
   - Authorized redirect URIs → **Add URI**:
     - `http://localhost:8501` (for local testing)
     - `https://your-app.streamlit.app` (for production — add later)
5. Click **Create**

## Step 4 — Download Credentials

1. A popup shows your **Client ID** and **Client Secret**
2. Click **Download JSON**
3. Rename the downloaded file to `google_credentials.json`
4. Place it in the root of the washgo_app folder:
   ```
   washgo_app/
   ├── google_credentials.json   ← here
   ├── app.py
   ├── pages/
   └── utils/
   ```

> ⚠️ IMPORTANT: Never share or upload this file. It's in .gitignore.

## Step 5 — Run the App

```bash
cd washgo_app
streamlit run app.py
```

The **Login with Google** button will appear in the sidebar.

## For Streamlit Cloud Deployment

Instead of uploading the JSON file (unsafe), use Streamlit Secrets:

1. In Streamlit Cloud dashboard → your app → **Settings** → **Secrets**
2. Paste the contents of your `google_credentials.json`
3. Update `utils/auth.py` to read from `st.secrets` instead of file

---

## How It Works

```
User clicks "Login with Google"
        ↓
Google shows permission screen
        ↓
User approves → Google sends auth code to WashGo
        ↓
WashGo exchanges code for user info (name, email, photo)
        ↓
Info stored in st.session_state["user_info"]
        ↓
User can now book orders — name pre-filled from Google account
```
