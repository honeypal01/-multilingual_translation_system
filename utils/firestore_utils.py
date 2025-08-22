import datetime
import firebase_admin
from firebase_admin import storage
from firebase_admin import credentials, firestore

# Initialize Firestore
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def get_user_data(uid):
    doc = db.collection("users").document(uid).get()
    return doc.to_dict() if doc.exists else None


def update_user_profile(uid, name, photo_url):
    db.collection("users").document(uid).update({
        "name": name,
        "photo_url": photo_url
    })


def get_daily_usage(uid):
    doc_ref = db.collection("users").document(uid).collection("usage").document("daily")
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        sorted_data = sorted(data.items(), key=lambda x: x[0], reverse=True)[:7]
        return sorted_data[::-1]  # ascending order
    return []


def get_daily_voice_usage(uid):
    doc_ref = db.collection("users").document(uid).collection("usage").document("voice")
    doc = doc_ref.get()
    if doc.exists:
        data = doc.to_dict()
        sorted_data = sorted(data.items(), key=lambda x: x[0], reverse=True)[:7]
        return sorted_data[::-1]
    return []


def get_language_usage(uid):
    doc = db.collection("users").document(uid).collection("stats").document("languages").get()
    return doc.to_dict() if doc.exists else {}


def get_recent_activity(uid):
    logs = db.collection("users").document(uid).collection("activity") \
             .order_by("timestamp", direction=firestore.Query.DESCENDING).limit(5).stream()
    return [log.to_dict() for log in logs]


def list_user_files(uid):
    try:
        bucket = storage.bucket()
        prefix = f"downloads/{uid}/"
        blobs = list(bucket.list_blobs(prefix=prefix))
        return [blob.public_url for blob in blobs if not blob.name.endswith("/")]
    except Exception as e:
        print(f"Error listing files: {e}")
        return []