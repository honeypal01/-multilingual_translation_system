import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_config.json")  # Path to your Firebase service account JSON
    firebase_admin.initialize_app(cred)

firestore_db = firestore.client()
