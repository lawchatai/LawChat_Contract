from datetime import datetime
import os
import tempfile
from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import Error as PlaywrightError
import requests
from datetime import datetime
import boto3
import os

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_PUBLIC_BASE_URL = os.getenv("R2_PUBLIC_BASE_URL")  # optional

r2_client = boto3.client(
    "s3",
    endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
)

class PDFGenerationError(Exception):
    """Custom exception for PDF generation failures"""
    pass


PDF_SERVICE_URL = os.getenv("PDF_SERVICE_URL")
PDF_SERVICE_TOKEN = os.getenv("PDF_SERVICE_TOKEN")

class PDFServiceError(Exception):
    pass

def generate_pdf_remote(html: str) -> bytes:
    if not PDF_SERVICE_URL or not PDF_SERVICE_TOKEN:
        raise PDFServiceError("PDF service not configured")

    try:
        resp = requests.post(
            PDF_SERVICE_URL,
            json={"html": html},
            headers={
                "X-INTERNAL-TOKEN": PDF_SERVICE_TOKEN,
                "Content-Type": "application/json"
            },
            timeout=60
        )
        resp.raise_for_status()
        return resp.content

    except requests.exceptions.Timeout:
        raise PDFServiceError("PDF service timeout")

    except requests.exceptions.RequestException as e:
        raise PDFServiceError(str(e))


BASE_PDF_PATH = "storage/nda_pdfs"

def save_pdf_to_disk(user_id, pdf_bytes, user_name):
    user_dir = os.path.join(BASE_PDF_PATH, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    filename = f"NDA_{user_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf"
    file_path = os.path.join(user_dir, filename)

    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    return filename, file_path


def save_pdf_to_r2(user_id, pdf_bytes, user_name):
    """
    Uploads PDF to Cloudflare R2.
    Returns: (filename, object_key, public_url)
    """

    if not pdf_bytes:
        raise ValueError("Empty PDF bytes")

    filename = f"NDA_{user_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf"

    object_key = f"nda/{user_id}/{filename}"

    r2_client.put_object(
        Bucket=R2_BUCKET_NAME,
        Key=object_key,
        Body=pdf_bytes,
        ContentType="application/pdf",
        Metadata={
            "user_id": str(user_id),
            "document_type": "EMP_NDA"
        }
    )

    public_url = None
    if R2_PUBLIC_BASE_URL:
        public_url = f"{R2_PUBLIC_BASE_URL}/{object_key}"

    return filename, object_key, public_url
