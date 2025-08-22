import os
import datetime
import uuid
import firebase_admin
from firebase_admin import credentials, storage, firestore

# Initialize Firebase if not already done
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'multilingual-translation-sys.appspot.com'
    })

db = firestore.client()
bucket = storage.bucket()

def upload_file_to_firebase(file_data, file_name, uid, translator_type="general"):
    # Create a unique path: downloads/uid/filename_timestamp.ext
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ext = file_name.split('.')[-1]
    path = f'downloads/{uid}/{translator_type}_{timestamp}.{ext}'

    # Upload file
    blob = bucket.blob(path)
    blob.upload_from_file(file_data, content_type=f"application/{ext}")
    blob.make_public()

    # Log download
    log_file_download(uid, blob.public_url, translator_type)

    return blob.public_url

def log_file_download(uid, download_url, translator_type="general"):
    data = {
        "uid": uid,
        "download_url": download_url,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "translator_type": translator_type
    }
    db.collection("downloads").add(data)

def get_user_downloads(uid):
    results = db.collection("downloads").where("uid", "==", uid).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).stream()
    return [r.to_dict() for r in results]
