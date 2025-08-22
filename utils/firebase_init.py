# firebase_init.py

import firebase_admin
from firebase_admin import credentials, firestore, storage, db

# Load your Firebase service account key JSON
cred = credentials.Certificate("firebase_config.json")

# Initialize the Firebase app with correct config
firebase_admin.initialize_app(cred, {
    "storageBucket": "multilingual-translation-sys.appspot.com",  # ✅ Replace with your actual bucket
    "databaseURL": "https://multilingual-translation-sys-default-rtdb.firebaseio.com"
})

# Clients for Firestore, Storage, Realtime DB
firestore_db = firestore.client()
storage_bucket = storage.bucket()
realtime_db = db
