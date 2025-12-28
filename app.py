from bson import ObjectId
from flask import Flask, render_template, request, jsonify, g, session, redirect, url_for, abort
from flask.cli import load_dotenv
from flask_session import Session
from datetime import datetime, timedelta
from routes.nda_routes import nda_bp
from routes.nda_routes import cleanup_expired_documents
from pymongo import MongoClient
from functools import wraps
import os
import hmac, hashlib, time, base64, json


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(nda_bp, url_prefix="/nda")

uri = os.getenv("MONGO_URI")

db_client = MongoClient(uri)
db = db_client["user_database"]  # Your database name
users_collection = db["users"]   # Collection for storing user data

app.secret_key = os.getenv("SECRET_KEY")

IS_PROD = os.getenv("FLASK_ENV") == "production"

app.config.update(
    SESSION_TYPE="mongodb",
    SESSION_MONGODB=db_client,
    SESSION_MONGODB_DB="user_database",
    SESSION_MONGODB_COLLECTION="sessions",
    SESSION_USE_SIGNER=True,
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=timedelta(days=5),

    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=IS_PROD,
    SESSION_COOKIE_SAMESITE="None" if IS_PROD else "Lax",
    SESSION_COOKIE_DOMAIN=".lawchatai.in" if IS_PROD else None,
)

Session(app)

def base64url_decode(data):
    data += "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(data)

def verify_sso_token(token):
    secret = os.getenv("SSO_SHARED_SECRET")
    if not secret:
        raise RuntimeError("SSO_SHARED_SECRET not set")

    try:
        payload_b64, signature = token.split(".")

        expected_signature = hmac.new(
            secret.encode(),
            payload_b64.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_signature):
            return None

        payload = json.loads(
            base64url_decode(payload_b64).decode()
        )

        if payload["exp"] < int(time.time()):
            return None

        return payload["user_id"]

    except Exception:
        return None

@app.route("/sso")
def sso_login():
    code = request.args.get("code")
    if not code:
        abort(401)

    record = db["sso_codes"].find_one_and_update(
        {
            "code": hashlib.sha256(code.encode()).hexdigest(),
            "used": False,
            "expires_at": {"$gt": datetime.utcnow()}
        },
        {"$set": {"used": True}}
    )

    if not record:
        abort(401)

    user = users_collection.find_one(
        {"_id": ObjectId(record["user_id"])}
    )

    if not user:
        abort(404)

    session.clear()
    session["user_id"] = str(user["_id"])
    session.permanent = True

    session.modified = True

    return redirect("/")


@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id:
        g.user = users_collection.find_one({"_id": ObjectId(user_id)})
    else:
        g.user = None


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user:
            return redirect(f"https://lawchatai.in/login?next={request.path}")
        return f(*args, **kwargs)
    return wrapper


@app.route("/")
@login_required
def select_agreement():
    return render_template("agreement.html")

@app.route("/nda")
@login_required
def nda():
    agreement_type = request.args.get("type", "emp-nda")

    # Fetch dynamic fields from g.user
    account_type = g.user.get("account_type", "basic")
    credit_contract = g.user.get("credit_contract", 0)

    return render_template(
        "emp_nda.html",
        agreement_type=agreement_type,
        account_type=account_type,
        credit_contract=credit_contract
    )

@app.route("/lawchat/contract/cleanup-docs")
@login_required
def cleanup_docs():
    cleanup_expired_documents()
    return jsonify({"status": "cleanup completed"})


@app.route("/employment-agreement")
def employment_agreement():
    return "<h2>Employment Agreement – Coming Soon</h2>"

# if __name__ == "__main__":
#     app.run(debug=True, ssl)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001,ssl_context='adhoc', debug=True)
