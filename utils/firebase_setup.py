# import pyrebase

# # ✅ Firebase Config (already shared by you)
# config = {
#     "apiKey": "AIzaSyA_OSIMH6hKgK0WBsw2ZBHMHln4TK6cAhY",
#     "authDomain": "multilingual-translation-sys.firebaseapp.com",
#     "projectId": "multilingual-translation-sys",
#     "storageBucket": "multilingual-translation-sys.appspot.com",
#     "messagingSenderId": "740960180828",
#     "appId": "1:740960180828:web:4f1efd834466c675712499",
#     "measurementId": "G-58BWM8CVW0",
#     "databaseURL": ""
# }

# # 🔌 Initialize Firebase
# firebase = pyrebase.initialize_app(config)

# # 🔐 Auth
# auth_client = firebase.auth()

# # ☁️ Storage (used for profile picture uploads)
# storage = firebase.storage()

# # 🗂️ Firestore (via firebase_admin, for user details etc.)
# import firebase_admin
# from firebase_admin import credentials, firestore

# # Initialize Firebase Admin SDK only once
# if not firebase_admin._apps:
#     cred = credentials.Certificate("firebase_config.json")  # path to your service account JSON
#     firebase_admin.initialize_app(cred)

# db = firestore.client()


# utils/firebase_setup.py

import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore, auth as admin_auth

# ✅ Firebase Config
config = {
    "apiKey": "AIzaSyA_OSIMH6hKgK0WBsw2ZBHMHln4TK6cAhY",
    "authDomain": "multilingual-translation-sys.firebaseapp.com",
    "projectId": "multilingual-translation-sys",
    "storageBucket": "multilingual-translation-sys.appspot.com",
    "messagingSenderId": "740960180828",
    "appId": "1:740960180828:web:4f1efd834466c675712499",
    "measurementId": "G-58BWM8CVW0",
    "databaseURL": ""  # Required if using Realtime Database (not Firestore)
}

# 🔌 Initialize Pyrebase
firebase = pyrebase.initialize_app(config)
auth_client = firebase.auth()
storage = firebase.storage()

# === Firebase Admin SDK Initialization ===
firebase_app = None
db = None

def init_firebase():
    global firebase_app, db
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase_config.json")  # Ensure this file exists!
        firebase_app = firebase_admin.initialize_app(cred)
        db = firestore.client()

def get_firestore_client():
    if not firebase_admin._apps:
        init_firebase()
    return firestore.client()

def get_auth_client():
    return auth_client

def get_storage():
    return storage

def get_user_id(email):
    """
    Look up a user in Firebase Auth by email and return their UID.
    """
    try:
        user_record = admin_auth.get_user_by_email(email)
        return user_record.uid
    except firebase_admin._auth_utils.UserNotFoundError:
        return None
