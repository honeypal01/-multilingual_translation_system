import pyrebase
import uuid
import datetime
import os
from firebase_config import config

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
storage = firebase.storage()
db = firebase.database()

def upload_user_file(file, uid, feature_name="general", metadata={}):
    """
    Uploads a file to Firebase Storage under the user’s folder and logs metadata in Realtime DB.
    Args:
        file: A file-like object from Streamlit uploader
        uid: Firebase UID of the user
        feature_name: 'document_translator', 'speech_to_speech', etc.
        metadata: Additional dict to store in Realtime DB (like language, voice type, etc.)
    """
    # Generate unique filename
    filename = f"{feature_name}/{str(uuid.uuid4())}_{file.name}"
    path_on_storage = f"users/{uid}/{filename}"

    # Save temp file
    temp_path = f"/tmp/{file.name}"
    with open(temp_path, "wb") as f:
        f.write(file.getbuffer())

    # Upload to Firebase Storage
    storage.child(path_on_storage).put(temp_path)

    # Get download URL
    file_url = storage.child(path_on_storage).get_url(None)

    # Prepare metadata for Realtime DB
    file_record = {
        "filename": file.name,
        "feature": feature_name,
        "download_url": file_url,
        "timestamp": datetime.datetime.now().isoformat(),
        "uid": uid,
        **metadata
    }

    # Store in Realtime DB under user’s path
    db.child("files").child(uid).push(file_record)

    # Clean up
    os.remove(temp_path)

    return file_url


def get_user_files(uid):
    """
    Returns a list of files uploaded by the user from Realtime DB.
    """
    files = db.child("files").child(uid).get()
    if files.each() is None:
        return []

    return [item.val() for item in files.each()]
