import sys
import types
import streamlit as st
from datetime import datetime
from firebase_admin import firestore
from urllib.parse import urlencode
import requests

# Patch for deprecated torch.classes
sys.modules['torch.classes'] = types.SimpleNamespace()

# ✅ Streamlit page config
st.set_page_config(page_title="🌍 Multilingual Translator", layout="centered")

# ✅ Firebase Authentication helpers
from firebase_auth_utils import (
    authenticate_user as login_user,
    create_user as signup_user,
    auth_client,
    upload_profile_picture
)

# === Google OAuth Helpers ===
def get_google_auth_url():
    params = {
        "client_id": st.secrets["GOOGLE_CLIENT_ID"],
        "redirect_uri": "http://localhost:8501",
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"

def get_tokens(auth_code):
    data = {
        "code": auth_code,
        "client_id": st.secrets["GOOGLE_CLIENT_ID"],
        "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
        "redirect_uri": "http://localhost:8501",
        "grant_type": "authorization_code"
    }
    response = requests.post("https://oauth2.googleapis.com/token", data=data)
    return response.json()

def get_user_info(access_token):
    response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return response.json()

# ✅ Global session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "page" not in st.session_state:
    st.session_state.page = "🏠 Dashboard"

# ✅ Import dashboard only after login
if st.session_state.logged_in:
    from _pages_backup import dashboard

# ✅ Firestore logging function
def log_auth_event(uid, email, event_type, name=None, profile_photo=None):
    db = firestore.client()
    db.collection("auth_logs").add({
        "uid": uid,
        "email": email,
        "event_type": event_type,
        "timestamp": datetime.utcnow(),
        "name": name,
        "profile_photo": profile_photo,
    })

# ✅ Inject custom CSS
st.markdown("""
<style>
body { font-family: 'Times New Roman', serif; }
.login-box {
    background-color: #ffffff0a;
    padding: 40px 30px;
    border-radius: 16px;
    max-width: 480px;
    margin: auto;
    box-shadow: 0 0 25px rgba(255, 255, 255, 0.1);
}
h2, h3 { text-align: center; color: #ffffff; }
button[kind="primary"] {
    border-radius: 8px;
    transition: background-color 0.3s ease, transform 0.2s ease;
}
button[kind="primary"]:hover {
    background-color: #1f77d0 !important;
    color: white !important;
    transform: scale(1.02);
}
img { border-radius: 50%; margin-top: 10px; }
</style>
""", unsafe_allow_html=True)

# ✅ Login & Signup UI
def login_ui():
    st.markdown('<div class="login-box"><h2>🔐 Login or Sign Up</h2></div>', unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>👋 Welcome to the Multilingual Translation System</h4>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Sign Up"])

    # === Login Tab ===
    with tab1:
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Password", type="password", key="login_password")

        col1, col2 = st.columns([2, 1])
        with col1:
            if st.button("✅ Login"):
                uid, user_data = login_user(email, password)
                if uid:
                    st.session_state.logged_in = True
                    st.session_state.uid = uid
                    st.session_state.name = user_data.get("name", "User")
                    st.session_state.photo = user_data.get("photo", None)
                    st.session_state.email = email
                    st.session_state.page = "🏠 Dashboard"

                    log_auth_event(uid, email, "login", st.session_state.name, st.session_state.photo)
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")

        with col2:
            if st.button("🔁 Forgot Password?"):
                st.session_state.page = "🔁 Reset Password"
                st.rerun()

        # 🌐 Google Login
        st.markdown("----")
        st.markdown("##### 🔑 Or Sign In with Google")

        auth_url = get_google_auth_url()
        st.markdown(f"""
            <a href="{auth_url}">
                <button style="background-color:#4285F4;color:white;padding:10px 20px;
                border:none;border-radius:5px;font-size:16px;margin-top:10px;">
                    🔐 Sign in with Google
                </button>
            </a>
        """, unsafe_allow_html=True)

        # ✅ Handle Google OAuth callback
        query_params = st.experimental_get_query_params()
        if "code" in query_params and not st.session_state.get("logged_in"):
            auth_code = query_params["code"][0]
            tokens = get_tokens(auth_code)

            if "access_token" in tokens:
                user_info = get_user_info(tokens["access_token"])

                # Save into session
                st.session_state.logged_in = True
                st.session_state.uid = user_info.get("id")
                st.session_state.name = user_info.get("name")
                st.session_state.email = user_info.get("email")
                st.session_state.photo = user_info.get("picture")
                st.session_state.page = "🏠 Dashboard"

                log_auth_event(
                    uid=st.session_state.uid,
                    email=st.session_state.email,
                    event_type="google_login",
                    name=st.session_state.name,
                    profile_photo=st.session_state.photo
                )

                st.success(f"🎉 Welcome, {st.session_state.name}!")
                st.rerun()
            else:
                st.error("❌ Google login failed. Try again.")

    # === Signup Tab ===
    with tab2:
        signup_email = st.text_input("📧 Email", key="signup_email")
        signup_name = st.text_input("📝 Name", key="signup_name")
        signup_password = st.text_input("🔑 Password", type="password", key="signup_password")
        uploaded_file = st.file_uploader("🖼️ Upload Profile Picture", type=["jpg", "jpeg", "png"])

        if st.button("🆕 Create Account"):
            image_url = upload_profile_picture(uploaded_file, signup_email) if uploaded_file else None
            success, message = signup_user(signup_email, signup_password, signup_name, image_url)
            if success:
                st.success(message)
                st.info("You can now log in.")
                user = auth_client.get_user_by_email(signup_email)
                log_auth_event(user.uid, signup_email, "signup", signup_name, image_url)
            else:
                st.error(message)

# ✅ Password Reset Page
def reset_password_page():
    st.markdown("## 🔁 Reset Your Password")
    email = st.text_input("📧 Email")
    if st.button("📤 Send Reset Email"):
        try:
            auth_client.send_password_reset_email(email)
            st.success("📩 Reset link sent to your email.")
        except Exception as e:
            st.error(f"❌ {e}")
    if st.button("🔙 Back to Login"):
        st.session_state.page = "🏠 Dashboard"
        st.rerun()

# ✅ Main App Controller
def main():
    if st.session_state.get("page") == "🔁 Reset Password":
        reset_password_page()
        return

    if st.session_state.logged_in:
        from _pages_backup import dashboard
        with st.sidebar:
            st.image(st.session_state.get("photo") or "https://cdn-icons-png.flaticon.com/512/149/149071.png", width=100)
            st.markdown(f"🧑‍💼 **{st.session_state.get('name', 'User')}**")
            st.markdown(f"📧 `{st.session_state.get('email')}`")
            if st.button("🚪 Logout"):
                for key in ["logged_in", "uid", "name", "photo", "email", "page"]:
                    st.session_state.pop(key, None)
                st.rerun()

        dashboard.run(st.session_state.uid)
    else:
        login_ui()

# ✅ Run App
if __name__ == "__main__":
    main()
