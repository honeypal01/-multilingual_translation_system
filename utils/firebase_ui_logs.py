from firebase_admin import firestore
from datetime import datetime
import uuid

db = firestore.client()

def store_ui_submission(uid, name, message, lang):
    doc_id = str(uuid.uuid4())
    db.collection("ui_translations").document(doc_id).set({
        "uid": uid,
        "name": name,
        "message": message,
        "language": lang,
        "timestamp": datetime.utcnow().isoformat(),
        "id": doc_id
    })

def fetch_ui_history(uid, limit=15):
    try:
        docs = db.collection("ui_translations").where("uid", "==", uid)\
            .order_by("timestamp", direction=firestore.Query.DESCENDING).limit(limit).stream()
        return [doc.to_dict() for doc in docs]
    except Exception as e:
        print(f"[UI Translator] Fetch failed: {e}")
        return []

def update_ui_entry(uid, doc_id, new_msg):
    try:
        doc_ref = db.collection("ui_translations").document(doc_id)
        doc_ref.update({"message": new_msg})
    except Exception as e:
        print(f"[UI Translator] Update failed: {e}")

def delete_ui_entry(uid, doc_id):
    try:
        db.collection("ui_translations").document(doc_id).delete()
    except Exception as e:
        print(f"[UI Translator] Delete failed: {e}")
