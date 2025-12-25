import re

def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)  # max 2 newlines
    return text.strip()

def format_nda_text(nda_text: str):
    nda_text = clean_text(nda_text)

    lines = nda_text.split("\n")
    html = []

    for line in lines:
        line = line.strip()

        if re.match(r"^\d+\.\s+[A-Z ]+$", line):
            html.append(f"<h2 class='font-semibold mt-6 mb-2'>{line}</h2>")
        elif line == "":
            html.append("<br>")
        else:
            html.append(f"<p class='text-sm leading-7'>{line}</p>")

    return "\n".join(html)
