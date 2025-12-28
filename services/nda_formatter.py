import re
import html

MAX_LINE_LENGTH = 500       # Prevent extremely long lines
MAX_LINES = 200             # Prevent extremely large PDFs

def clean_text(text: str) -> str:
    """
    Normalize newlines, remove excessive blank lines, strip spaces.
    """
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)  # max 2 newlines
    return text.strip()

def sanitize_line(line: str) -> str:
    """
    Escape HTML, remove non-printable chars, and truncate to MAX_LINE_LENGTH.
    """
    # Escape HTML special chars
    line = html.escape(line)
    # Remove non-printable characters
    line = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", line)
    # Truncate to MAX_LINE_LENGTH
    if len(line) > MAX_LINE_LENGTH:
        line = line[:MAX_LINE_LENGTH] + "…"
    return line

def format_nda_text(nda_text: str, include_watermark: bool = False) -> str:
    """
    Convert NDA text to safe HTML for PDF generation.
    """
    nda_text = clean_text(nda_text)
    lines = nda_text.split("\n")
    html_lines = []

    for i, line in enumerate(lines):
        if i >= MAX_LINES:
            html_lines.append("<p class='text-sm leading-7'>…Document truncated…</p>")
            break

        line = line.strip()
        safe_line = sanitize_line(line)

        # Header pattern: e.g., "1. CONFIDENTIAL INFORMATION"
        if re.match(r"^\d+\.\s+[A-Z ]+$", safe_line):
            html_lines.append(f"<h2 class='font-semibold mt-6 mb-2'>{safe_line}</h2>")
        elif safe_line == "":
            html_lines.append("<br>")
        else:
            html_lines.append(f"<p class='text-sm leading-7'>{safe_line}</p>")

    # Optional watermark overlay
    if include_watermark:
        watermark_html = """
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-30deg);
            font-size: 5rem;
            color: rgba(0,0,0,0.05);
            pointer-events: none;
            user-select: none;
            z-index: 0;">
            DRAFT · LawChatAI
        </div>
        """
        html_lines.insert(0, watermark_html)

    return "\n".join(html_lines)
