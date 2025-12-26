from services.audit import audit_log
from services.nda_service import generate_employment_nda
from services.pdf_service import save_pdf_to_r2, PDFServiceError, generate_pdf_remote, r2_client
from services.nda_formatter import format_nda_text
from flask import Blueprint, render_template, request, send_file, g, abort, current_app, flash, redirect, url_for
import io
from datetime import datetime, timedelta
from pymongo import MongoClient
from flask import redirect, abort, request
from bson import ObjectId
import boto3
import os

nda_bp = Blueprint("nda", __name__)

uri = os.getenv("MONGO_URI")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")

db_client = MongoClient(uri)
db = db_client["user_database"]
document_history = db["document_history"]
users_collection = db["users"]

@nda_bp.route("/")
def nda_form():
    return render_template("agreement.html")

@nda_bp.route("/generate", methods=["POST"])
def generate_nda():
    form_data = request.form.to_dict(flat=False)

    nda_text = generate_employment_nda(form_data)

    return render_template(
        "nda_preview.html",
        nda_text=nda_text,
        form_data=form_data
    )

def reserve_contract_credit(user_id):
    # user_id is already an ObjectId

    # 1️⃣ Unlimited plan
    unlimited = users_collection.find_one(
        {
            "_id": user_id,
            "account_type": "Premium_contract"
        }
    )

    if unlimited:
        return True, "unlimited"

    # 2️⃣ Limited plan (atomic reserve)
    result = users_collection.find_one_and_update(
        {
            "_id": user_id,
            "account_type": "Premium",
            "credit_contract": {"$gt": 15}
        },
        {
            "$inc": {"credit_contract": -15}
        },
        return_document=True
    )

    if result:
        return True, "limited"

    return False, "Contract credits exhausted"


def rollback_contract_credit(user_id):
    users_collection.update_one(
        {"_id": user_id, "account_type": "Premium"},
        {"$inc": {"credit_contract": 15}}
    )


@nda_bp.route("/generate-pdf", methods=["POST"])
@audit_log("document_generated")
def generate_pdf():
    if not g.user:
        abort(401)

    user = g.user
    user_id = ObjectId(user["_id"])
    user_name = user["name"]
    email = user["email"]

    # 🔐 STEP 1: Plan + Credit Validation (BEFORE PDF generation)
    allowed, mode = reserve_contract_credit(user_id)
    if not allowed:
        abort(403, description="Contract credits exhausted. Upgrade your plan.")

    nda_text = request.form.get("nda_text")

    # 2️⃣ Format NDA
    formatted_clauses = format_nda_text(nda_text)

    html = render_template(
        "nda_pdf.html",
        content=formatted_clauses
    )

    # 3️⃣ Generate PDF (REMOTE SERVICE)
    try:
        pdf_bytes = generate_pdf_remote(html)
    except PDFServiceError as e:
        # 🔁 Rollback credit if PDF failed
        if mode == "limited":
            rollback_contract_credit(user_id)

        current_app.logger.error(f"PDF service failed: {e}")
        abort(503, description="Unable to generate PDF. Please try again.")

    filename, object_key = save_pdf_to_r2(
        user_id,
        pdf_bytes,
        user_name
    )

    # 5️⃣ Save metadata in Mongo
    document_history.insert_one({
        "user_id": user_id,
        "email": email,
        "user_name": user_name,

        "document_type": "EMP_NDA",
        "file_name": filename,
        "file_path": object_key,

        "created_at": datetime.now(),
        "expires_at": datetime.now() + timedelta(days=30),
        "status": "active"
    })

    # 6️⃣ Return PDF
    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=filename
    )



@nda_bp.route("/my-documents")
def my_documents():
    if not g.user:
        abort(401)

    user_id = ObjectId(g.user["_id"])

    docs_cursor = document_history.find(
        {"user_id": user_id}
    ).sort("created_at", -1)

    documents = list(docs_cursor)  # ✅ FIX

    return render_template(
        "my_documents.html",
        documents=documents
    )

def cleanup_expired_documents():
    now = datetime.now()

    expired_docs = document_history.find({
        "expires_at": {"$lte": now}
    })

    for doc in expired_docs:
        path = os.path.join(current_app.root_path, doc["file_path"])

        if os.path.exists(path):
            os.remove(path)

        document_history.delete_one({"_id": doc["_id"]})

def generate_r2_signed_url(
    object_key: str,
    expires_in: int = 300,
    download: bool = False,
    filename: str | None = None,
):
    params = {
        "Bucket": R2_BUCKET_NAME,
        "Key": object_key,
    }

    if download:
        safe_name = filename or object_key.split("/")[-1]
        params["ResponseContentDisposition"] = (
            f'attachment; filename="{safe_name}"'
        )
        # 👇 CRITICAL FIX
        params["ResponseContentType"] = "application/octet-stream"

    return r2_client.generate_presigned_url(
        ClientMethod="get_object",
        Params=params,
        ExpiresIn=expires_in,
    )


@nda_bp.route("/document/<document_id>")
@audit_log("document view/download")
def open_document(document_id):
    if not g.user:
        abort(401)

    user_id = ObjectId(g.user["_id"])

    doc = document_history.find_one({
        "_id": ObjectId(document_id),
        "user_id": user_id,
        "status": "active"
    })

    if not doc:
        abort(404)

    file_path = doc.get("file_path")
    if not file_path:
        abort(404)

    action = request.args.get("action", "view")
    is_download = action == "download"

    # 🔐 SIGNED URL (preferred & secure)
    if not file_path.startswith("http"):
        signed_url = generate_r2_signed_url(
            object_key=file_path,
            expires_in=300,
            download=is_download,
            filename=doc.get("file_name")
        )
        return redirect(signed_url)

    # 🌐 Legacy public URLs (view-only)
    if is_download:
        abort(400, description="Download not supported for legacy documents")

    return redirect(file_path)


@nda_bp.route("/document/<doc_id>/delete", methods=["POST"])
@audit_log("document_deleted")
def delete_document(doc_id):
    if not g.user:
        abort(401)

    doc = document_history.find_one({
        "_id": ObjectId(doc_id),
        "user_id": ObjectId(g.user["_id"])
    })

    if not doc:
        abort(404)

    path = doc.get("file_path")
    if path and os.path.exists(path):
        os.remove(path)

    document_history.delete_one({"_id": doc["_id"]})

    flash("Document deleted successfully", "success")
    return redirect(url_for("nda.my_documents"))

