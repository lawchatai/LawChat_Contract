from functools import wraps
from flask import g, request
from datetime import datetime
import hashlib
from pymongo import MongoClient
import os


uri = os.getenv("MONGO_URI")

db_client = MongoClient(uri)
db = db_client["user_database"]
audit_logs = db["audit_logs"]


def hash_ip(ip):
    return hashlib.sha256(ip.encode()).hexdigest()

def audit_log(action):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):

            response = fn(*args, **kwargs)

            try:
                audit_logs.insert_one({
                    "user_id": g.user["_id"],
                    "document_id": kwargs.get("doc_id"),
                    "action": action,
                    "ip_hash": hash_ip(request.remote_addr),
                    "user_agent": request.headers.get("User-Agent"),
                    "created_at": datetime.now()
                })
            except Exception as e:
                # ❗ never break main flow
                print("Audit log failed:", e)

            return response
        return wrapper
    return decorator
