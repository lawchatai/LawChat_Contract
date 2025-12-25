from datetime import datetime
import os
import tempfile
from playwright.sync_api import sync_playwright, Playwright
from playwright.sync_api import Error as PlaywrightError


class PDFGenerationError(Exception):
    """Custom exception for PDF generation failures"""
    pass

def generate_pdf_with_playwright(html_content: str) -> bytes:
    html_file = None
    browser = None

    try:
        if not html_content or not html_content.strip():
            raise ValueError("Empty HTML content received")

        # Write HTML to a temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as f:
            f.write(html_content)
            html_file = f.name

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,   #for prod make it TRUE
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )

            page = browser.new_page()

            page.goto(f"file:///{html_file}", wait_until="networkidle")

            pdf_bytes = page.pdf(
                format="A4",
                margin={
                    "top": "30mm",
                    "bottom": "30mm",
                    "left": "25mm",
                    "right": "25mm"
                },
                print_background=True
            )

            if not pdf_bytes:
                raise PDFGenerationError("Playwright returned empty PDF")

            return pdf_bytes  # ✅ BYTES

    except PlaywrightError as e:
        raise PDFGenerationError(f"Playwright error: {str(e)}") from e

    except Exception as e:
        raise PDFGenerationError(f"PDF generation failed: {str(e)}") from e

    finally:
        # 🔐 Cleanup
        try:
            if browser:
                browser.close()
        except Exception:
            pass

        try:
            if html_file and os.path.exists(html_file):
                os.remove(html_file)
        except Exception:
            pass


BASE_PDF_PATH = "storage/nda_pdfs"

def save_pdf_to_disk(user_id, pdf_bytes, user_name):
    user_dir = os.path.join(BASE_PDF_PATH, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    filename = f"NDA_{user_name}_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.pdf"
    file_path = os.path.join(user_dir, filename)

    with open(file_path, "wb") as f:
        f.write(pdf_bytes)

    return filename, file_path
