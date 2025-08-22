# pages/login.py
# import streamlit as st
# from firebase_auth_utils import create_user, get_user_by_email

# def login_ui():
#     st.markdown("## 🔐 Login to your account")
#     email = st.text_input("Email")
#     uid = st.text_input("Firebase UID (for testing only)", key="uid_input")
    
#     if st.button("Login"):
#         if uid:
#             st.session_state.uid = uid
#             st.success("Logged in successfully!")
#             st.rerun()
#         else:
#             st.error("Please enter a UID (for now, until password auth is integrated).")

#     st.markdown("---")
#     st.markdown("## 🆕 New? Sign up below:")
#     name = st.text_input("Name", key="signup_name")
#     email_signup = st.text_input("Signup Email", key="signup_email")
#     password = st.text_input("Password", type="password")
#     if st.button("Sign Up"):
#         result = create_user(email_signup, password, name)
#         if isinstance(result, str):
#             st.error(result)
#         else:
#             st.success("Account created! Please copy your UID and log in manually for now.")
#             st.code(result.uid)



import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from firebase_auth_utils import create_user, get_user_by_email, authenticate_user

# --- Page Setup ---
st.set_page_config(page_title="Login | Multilingual Translator", page_icon="🔐", layout="centered")

# --- Custom CSS for Centered Box and Hover Effect ---
st.markdown("""
    <style>
    .login-container {
        max-width: 500px;
        margin: auto;
        padding: 2rem;
        border-radius: 12px;
        background-color: #f9f9f9;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease-in-out;
    }

    .stButton>button:hover {
        background-color: #007bff !important;
        color: white !important;
        transform: scale(1.03);
    }

    .stTextInput>div>input {
        transition: all 0.2s ease-in-out;
    }

    .stTextInput>div>input:focus {
        border-color: #007bff;
        box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
    }

    .language-select {
        margin-bottom: 1rem;
    }

    .forgot-password {
        text-align: right;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    st.image("https://img.icons8.com/color/96/translation.png", width=64)
    st.markdown("## 🔐 Login to Your Account")

    # Language Dropdown
    language = st.selectbox("🌍 Choose Language", ["English", "Hindi", "Spanish", "French", "German"], key="login_lang")

    # --- Login Section ---
    st.subheader("👤 Existing User")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")
    remember = st.checkbox("Remember Me")

    st.markdown('<div class="forgot-password"><a href="#">Forgot Password?</a></div>', unsafe_allow_html=True)

    if st.button("🔓 Login"):
        if login_email and login_password:
            user_record = authenticate_user(login_email, login_password)
            if user_record:
                st.session_state["uid"] = user_record.uid
                st.success("✅ Logged in successfully!")
                st.experimental_rerun()
                switch_page("dashboard")
            else:
                st.error("❌ Invalid credentials.")
        else:
            st.warning("⚠️ Please fill both fields.")

    st.markdown("---")

    # --- Sign Up Section ---
    st.subheader("🆕 New User")
    name = st.text_input("Full Name", key="signup_name")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")

    if st.button("📝 Sign Up"):
        if name and signup_email and signup_password:
            existing_user = get_user_by_email(signup_email)
            if existing_user:
                st.warning("⚠️ Email already registered.")
            else:
                result = create_user(signup_email, signup_password, name)
                if isinstance(result, str):
                    st.error(f"❌ {result}")
                else:
                    st.success("🎉 Account created successfully!")
                    st.session_state["uid"] = result.uid
                    st.experimental_rerun()
                    switch_page("dashboard")
        else:
            st.warning("⚠️ Please complete all sign-up fields.")

    st.markdown("</div>", unsafe_allow_html=True)
