import firebase_admin
from firebase_admin import firestore
from datetime import datetime

db = firestore.client()

def log_file_download(uid, filename):
    db.collection("downloads").add({
        "uid": uid,
        "filename": filename,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def list_user_downloads(uid):
    docs = db.collection("downloads").where("uid", "==", uid)\
        .order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).stream()
    return [doc.to_dict() for doc in docs]
