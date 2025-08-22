# import firebase_admin
# from firebase_admin import auth as admin_auth, credentials, firestore
# import pyrebase

# # ✅ Pyrebase config for client-side authentication
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

# # ✅ Initialize Pyrebase
# firebase = pyrebase.initialize_app(pyrebase_config)
# auth_client = firebase.auth()
# storage = firebase.storage()

# # ✅ Global db object
# db = None

# # ✅ Initialize Firebase Admin SDK
# if not firebase_admin._apps:
#     try:
#         cred = credentials.Certificate("serviceAccountKey.json")
#         firebase_admin.initialize_app(cred)
#         db = firestore.client()
#     except Exception as e:
#         raise RuntimeError(f"❌ Failed to initialize Firebase Admin SDK: {e}")

# import firebase_admin
# from firebase_admin import auth as admin_auth, credentials, firestore
# import pyrebase
# from datetime import datetime
# import os

# # ✅ Pyrebase config (client-side auth)
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

# # ✅ Initialize Pyrebase
# firebase = pyrebase.initialize_app(pyrebase_config)
# auth_client = firebase.auth()
# storage = firebase.storage()

# # ✅ Global Firestore DB
# db = None

# # ✅ Initialize Firebase Admin SDK
# try:
#     key_path = "serviceAccountKey.json"
#     if not firebase_admin._apps:
#         if not os.path.exists(key_path):
#             raise FileNotFoundError(f"⚠️ {key_path} not found. Make sure it exists in your working directory: {os.getcwd()}")

#         cred = credentials.Certificate(key_path)
#         firebase_admin.initialize_app(cred)
#         db = firestore.client()
#         print("✅ Firebase Admin SDK initialized successfully.")
# except Exception as e:
#     print(f"❌ Failed to initialize Firebase Admin SDK: {e}")
#     db = None



# import firebase_admin
# from firebase_admin import firestore
# from collections import Counter

# db = firestore.client()

# def fetch_user_data(uid):
#     user_ref = db.collection("users").document(uid)
#     return user_ref.get().to_dict() or {}

# def fetch_dashboard_stats(uid):
#     usage_ref = db.collection("usage").document(uid)
#     usage_data = usage_ref.get().to_dict() or {}

#     voice_data = db.collection("voice_history").where("uid", "==", uid).stream()
#     voice_count = sum(1 for _ in voice_data)

#     pair_counter = Counter()
#     history_ref = db.collection("history").where("uid", "==", uid)
#     recent_docs = history_ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).stream()
#     recent_activity = []
#     for doc in recent_docs:
#         d = doc.to_dict()
#         recent_activity.append(d)
#         if "src" in d and "dest" in d:
#             pair_counter[f"{d['src']} ➜ {d['dest']}"] += 1

#     top_pair = pair_counter.most_common(1)[0][0] if pair_counter else "N/A"

#     return {
#         "daily_usage": usage_data.get("daily_usage", {}),
#         "total_voice_outputs": voice_count,
#         "top_pair": top_pair,
#         "recent_activity": recent_activity
#     }


from firebase_admin import firestore, storage, db as realtime_db
from datetime import datetime
import os
import uuid

# Initialize Firestore client
db = firestore.client()

# Initialize Storage bucket (auto uses default bucket from initialization)
bucket = storage.bucket('multilingual-translation-sys.appspot.com')

# ========== Firestore: Usage Logging ==========
def log_file_download(uid, feature, details):
    try:
        db.collection("usage_logs").add({
            "uid": uid,
            "feature": feature,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        print(f"[Firestore] Logged file download: {feature} | {details}")
    except Exception as e:
        print(f"[Firestore] Logging failed: {e}")

def fetch_user_usage_logs(uid, feature=None, limit=10):
    try:
        ref = db.collection("usage_logs").where("uid", "==", uid)
        if feature:
            ref = ref.where("feature", "==", feature)
        docs = ref.order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"[Firestore] Fetch logs failed: {e}")
        return []

# ========== Firebase Storage Upload ==========
def upload_file_to_storage(uid, local_path, cloud_path):
    try:
        blob = bucket.blob(f"{uid}/{cloud_path}")
        blob.upload_from_filename(local_path)
        blob.make_public()  # Optional: remove if you want private access
        print(f"[Firebase Storage] Uploaded: {blob.public_url}")
        return blob.public_url
    except Exception as e:
        print(f"[Firebase Storage] Upload failed: {e}")
        return None

# ========== Realtime DB File Metadata ==========
def log_file_metadata_to_realtime_db(uid, metadata: dict):
    try:
        ref = realtime_db.reference(f"users/{uid}/files")
        unique_key = str(uuid.uuid4())
        ref.child(unique_key).set(metadata)
        print(f"[Realtime DB] Metadata logged: {metadata}")
    except Exception as e:
        print(f"[Realtime DB] Metadata log failed: {e}")
