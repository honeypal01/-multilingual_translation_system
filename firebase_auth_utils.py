

# # firebase_auth_utils.py
# import firebase_admin
# from firebase_admin import auth as admin_auth, credentials, firestore
# import pyrebase
# from utils.firebase_setup import auth_client, db, storage

# # ✅ Pyrebase config for client-side authentication (used for login)
# pyrebase_config = {
#     "apiKey": "AIzaSyA_OSIMH6hKgK0WBsw2ZBHMHln4TK6cAhY",
#     "authDomain": "multilingual-translation-sys.firebaseapp.com",
#     "databaseURL": "https://multilingual-translation-sys-default-rtdb.firebaseio.com/",
#     "projectId": "multilingual-translation-sys",
#     "storageBucket": "multilingual-translation-sys.appspot.com",
#     "messagingSenderId": "740960180828",
#     "appId": "1:740960180828:web:4f1efd834466c675712499",
#     "measurementId": "G-58BWM8CVW0"
# }

# # ✅ Initialize Pyrebase (for client-side auth like login/signup)
# firebase = pyrebase.initialize_app(pyrebase_config)
# auth_client = firebase.auth()
# storage = firebase.storage()

# # ✅ Initialize Firebase Admin SDK (for secure Firestore + Admin tasks)
# if not firebase_admin._apps:
#     try:
#         cred = credentials.Certificate("serviceAccountKey.json")
#         firebase_admin.initialize_app(cred)
#         db = firestore.client()
#     except FileNotFoundError:
#         raise FileNotFoundError("❌ 'serviceAccountKey.json' not found. Please place it in your project directory.")

# # 🔐 Login using email & password via Pyrebase and verify UID via ID token
# def login_user(email, password):
#     try:
#         # Step 1: Sign in using Pyrebase (client auth)
#         user = auth_client.sign_in_with_email_and_password(email.strip(), password)
#         id_token = user['idToken']

#         # Step 2: Get UID from ID token using Admin SDK
#         decoded_token = admin_auth.verify_id_token(id_token)
#         uid = decoded_token['uid']

#         # Step 3: Fetch user details from Firestore
#         user_doc = db.collection("users").document(uid).get()
#         return uid, user_doc.to_dict() if user_doc.exists else {}
#     except Exception as e:
#         print("❌ Login error:", e)
#         return None, None

# # 🆕 Signup user and save their data to Firestore
# def signup_user(email, password, name, photo_url=None):
#     try:
#         # First check if user already exists
#         try:
#             admin_auth.get_user_by_email(email.strip())
#             return False, "⚠️ This email is already registered."
#         except admin_auth.UserNotFoundError:
#             pass  # Safe to proceed

#         # Create the user in Firebase Auth
#         user = admin_auth.create_user(
#             email=email.strip(),
#             password=password,
#             display_name=name,
#             photo_url=photo_url if photo_url else None
#         )

#         # Store user info in Firestore
#         user_data = {
#             "name": name,
#             "email": email.strip(),
#             "createdAt": firestore.SERVER_TIMESTAMP
#         }
#         if photo_url:
#             user_data["photo"] = photo_url

#         db.collection("users").document(user.uid).set(user_data)

#         return True, "✅ User created successfully!"
#     except Exception as e:
#         print("❌ Signup error:", e)
#         return False, f"❌ Signup failed: {e}"

# # ☁️ Upload profile picture and return download URL
# def upload_profile_picture(file, email):
#     try:
#         filename = f"profile_pics/{email.replace('@', '_at_')}.png"
#         storage.child(filename).put(file)
#         url = storage.child(filename).get_url(None)
#         return url
#     except Exception as e:
#         print("❌ Failed to upload profile picture:", e)
#         return None

# # 🔍 Utility: Get Firebase user by email
# def get_user_by_email(email):
#     try:
#         return admin_auth.get_user_by_email(email.strip())
#     except admin_auth.UserNotFoundError:
#         return None
#     except Exception as e:
#         print("❌ Error getting user:", e)
#         return None


# firebase_auth_utils.py

# import firebase_admin
# from firebase_admin import auth as admin_auth, credentials, firestore
# import pyrebase
# from utils.firebase_setup import auth_client, db, storage

# # ✅ Pyrebase config for client-side authentication (used for login)
# pyrebase_config = {
#     "apiKey": "AIzaSyA_OSIMH6hKgK0WBsw2ZBHMHln4TK6cAhY",
#     "authDomain": "multilingual-translation-sys.firebaseapp.com",
#     "databaseURL": "https://multilingual-translation-sys-default-rtdb.firebaseio.com/",
#     "projectId": "multilingual-translation-sys",
#     "storageBucket": "multilingual-translation-sys.appspot.com",
#     "messagingSenderId": "740960180828",
#     "appId": "1:740960180828:web:4f1efd834466c675712499",
#     "measurementId": "G-58BWM8CVW0"
# }

# # ✅ Initialize Pyrebase (for client-side auth like login/signup)
# firebase = pyrebase.initialize_app(pyrebase_config)
# auth_client = firebase.auth()
# storage = firebase.storage()

# # ✅ Initialize Firebase Admin SDK (for Firestore access)
# if not firebase_admin._apps:
#     try:
#         cred = credentials.Certificate("serviceAccountKey.json")
#         firebase_admin.initialize_app(cred)
#         db = firestore.client()
#     except FileNotFoundError:
#         raise FileNotFoundError("❌ 'serviceAccountKey.json' not found. Please place it in your project directory.")

# # 🔐 Login using email & password via Pyrebase and verify UID
# def login_user(email, password):
#     try:
#         # Step 1: Sign in using Pyrebase
#         user = auth_client.sign_in_with_email_and_password(email.strip(), password)
#         id_token = user['idToken']

#         # Step 2: Decode ID token to get UID
#         decoded_token = admin_auth.verify_id_token(id_token)
#         uid = decoded_token['uid']

#         # Step 3: Get user details from Firestore
#         user_doc = db.collection("users").document(uid).get()

#         if user_doc.exists:
#             return uid, user_doc.to_dict()
#         else:
#             print(f"⚠️ Firestore user document not found for UID: {uid}")
#             return None, None

#     except Exception as e:
#         print("❌ Login error:", e)
#         return None, None

# # 🆕 Signup user and save their data to Firestore
# def signup_user(email, password, name, photo_url=None):
#     try:
#         # Check if user already exists
#         try:
#             admin_auth.get_user_by_email(email.strip())
#             return False, "⚠️ This email is already registered."
#         except admin_auth.UserNotFoundError:
#             pass  # Continue if not found

#         # Create user in Firebase Auth
#         user = admin_auth.create_user(
#             email=email.strip(),
#             password=password,
#             display_name=name,
#             photo_url=photo_url if photo_url else None
#         )

#         # Prepare user data for Firestore
#         user_data = {
#             "name": name,
#             "email": email.strip(),
#             "createdAt": firestore.SERVER_TIMESTAMP
#         }
#         if photo_url:
#             user_data["photo"] = photo_url

#         # Save to Firestore
#         db.collection("users").document(user.uid).set(user_data)

#         return True, "✅ User created successfully!"

#     except Exception as e:
#         print("❌ Signup error:", e)
#         return False, f"❌ Signup failed: {e}"

# # ☁️ Upload profile picture to Firebase Storage and return download URL
# def upload_profile_picture(file, email):
#     try:
#         filename = f"profile_pics/{email.replace('@', '_at_')}.png"
#         storage.child(filename).put(file)
#         url = storage.child(filename).get_url(None)
#         return url
#     except Exception as e:
#         print("❌ Failed to upload profile picture:", e)
#         return None

# # 🔍 Utility: Get Firebase user by email
# def get_user_by_email(email):
#     try:
#         return admin_auth.get_user_by_email(email.strip())
#     except admin_auth.UserNotFoundError:
#         return None
#     except Exception as e:
#         print("❌ Error getting user by email:", e)
#         return None


import firebase_admin
from firebase_admin import auth as admin_auth, credentials, firestore
import pyrebase
import os
import json
import logging
import tempfile
from utils.firebase_setup import auth_client as external_auth_client, db as external_db, storage as external_storage

# 🔧 Pyrebase config
pyrebase_config = {
    "apiKey": "AIzaSyA_OSIMH6hKgK0WBsw2ZBHMHln4TK6cAhY",
    "authDomain": "multilingual-translation-sys.firebaseapp.com",
    "databaseURL": "https://multilingual-translation-sys-default-rtdb.firebaseio.com/",
    "projectId": "multilingual-translation-sys",
    "storageBucket": "multilingual-translation-sys.appspot.com",
    "messagingSenderId": "740960180828",
    "appId": "1:740960180828:web:4f1efd834466c675712499",
    "measurementId": "G-58BWM8CVW0"
}

firebase = pyrebase.initialize_app(pyrebase_config)
auth_client = firebase.auth()
storage = firebase.storage()

# 🔐 Initialize Firebase Admin SDK
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

# Alias for main.py
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

# 🔁 Password Reset
def send_password_reset(email):
    try:
        auth_client.send_password_reset_email(email.strip())
        return True, "✅ Password reset email sent."
    except Exception as e:
        logging.error(f"❌ Password reset error: {e}")
        return False, str(e)

# 💾 Session Persistence using OS-safe temp file
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

# ✨ Alias for backward compatibility
create_user = signup_user

