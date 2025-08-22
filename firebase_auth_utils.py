import firebase_admin
from firebase_admin import auth as admin_auth, credentials, firestore
import pyrebase
import os
import json
import logging
import tempfile
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# 🔧 Pyrebase config from .env
pyrebase_config = {
    "apiKey": os.getenv("FIREBASE_API_KEY"),
    "authDomain": os.getenv("FIREBASE_AUTH_DOMAIN"),
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL"),
    "projectId": os.getenv("FIREBASE_PROJECT_ID"),
    "storageBucket": os.getenv("FIREBASE_STORAGE_BUCKET"),
    "messagingSenderId": os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    "appId": os.getenv("FIREBASE_APP_ID"),
    "measurementId": os.getenv("FIREBASE_MEASUREMENT_ID")
}

# ✅ Initialize Pyrebase (Client-side Auth)
firebase = pyrebase.initialize_app(pyrebase_config)
auth_client = firebase.auth()
storage = firebase.storage()

# ✅ Initialize Firebase Admin SDK
if not firebase_admin._apps:
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        db = firestore.client()
    except FileNotFoundError:
        raise FileNotFoundError("❌ 'serviceAccountKey.json' not found.")

# 📥 Email/Password Login
def login_user(email, password):
    try:
        user = auth_client.sign_in_with_email_and_password(email.strip(), password)
        id_token = user['idToken']
        decoded_token = admin_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_doc = db.collection("users").document(uid).get()
        return (uid, user_doc.to_dict()) if user_doc.exists else (None, None)
    except Exception as e:
        logging.error(f"❌ Login error: {e}")
        return None, None

# ✅ Alias for main.py
authenticate_user = login_user

# 🆕 Signup with Email/Password
def signup_user(email, password, name, photo_url=None):
    try:
        try:
            admin_auth.get_user_by_email(email.strip())
            return False, "⚠️ Email already registered."
        except firebase_admin._auth_utils.UserNotFoundError:
            pass

        user = admin_auth.create_user(
            email=email.strip(),
            password=password,
            display_name=name,
            photo_url=photo_url if photo_url else None
        )

        user_data = {
            "name": name,
            "email": email.strip(),
            "createdAt": firestore.SERVER_TIMESTAMP
        }
        if photo_url:
            user_data["photo"] = photo_url

        db.collection("users").document(user.uid).set(user_data)
        return True, "✅ User created successfully!"
    except Exception as e:
        logging.error(f"❌ Signup error: {e}")
        return False, f"❌ Signup failed: {e}"

# ☁️ Upload Profile Picture
def upload_profile_picture(file, email):
    try:
        filename = f"profile_pics/{email.strip().replace('@', '_at_')}.png"
        storage.child(filename).put(file)
        return storage.child(filename).get_url(None)
    except Exception as e:
        logging.error(f"❌ Upload failed: {e}")
        return None

# 🔍 Get User by Email
def get_user_by_email(email):
    try:
        return admin_auth.get_user_by_email(email.strip())
    except firebase_admin._auth_utils.UserNotFoundError:
        return None
    except Exception as e:
        logging.error(f"❌ Error getting user by email: {e}")
        return None

# 🔐 Google OAuth Login via ID Token
def google_login(id_token):
    try:
        decoded_token = admin_auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        user_doc = db.collection("users").document(uid).get()
        return (uid, user_doc.to_dict()) if user_doc.exists else (None, None)
    except Exception as e:
        logging.error(f"❌ Google login error: {e}")
        return None, None

# 🔁 Password Reset (Pyrebase)
def send_password_reset(email):
    try:
        auth_client.send_password_reset_email(email.strip())
        return True, "✅ Password reset email sent."
    except Exception as e:
        logging.error(f"❌ Password reset error: {e}")
        return False, str(e)

# 💾 Session Persistence
SESSION_FILE = os.path.join(tempfile.gettempdir(), "mlts_session.json")

def save_session(email, password):
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump({"email": email, "password": password}, f)
    except Exception as e:
        logging.error(f"❌ Failed to save session: {e}")

def load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"❌ Failed to load session: {e}")
    return None

def clear_session():
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)

# 📦 Public API
__all__ = [
    "authenticate_user",
    "signup_user",
    "create_user",
    "upload_profile_picture",
    "get_user_by_email",
    "google_login",
    "send_password_reset",
    "save_session",
    "load_session",
    "clear_session"
]

# ✨ Backward compatibility alias
create_user = signup_user
