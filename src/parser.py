import re
import fitz  # this is PyMuPDF's import name


class ResumeParseError(Exception):
    """Raised when we can't get readable text out of a PDF."""


def clean_text(text: str) -> str:
    # Turn different bullet symbols into a simple "-"
    for bullet in ["\u2022", "\u25cf", "\uf0b7", "\u25aa", "\u2023"]:
        text = text.replace(bullet, "-")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)      # many spaces/tabs -> one space
    text = re.sub(r"\n{3,}", "\n\n", text)   # many blank lines -> one blank line
    return text.strip()


def extract_text(pdf_bytes: bytes) -> str:
    """Take the raw bytes of a PDF and return clean text."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ResumeParseError("Could not open this file as a PDF.") from e

    pages = [page.get_text("text") for page in doc]
    doc.close()

    cleaned = clean_text("\n".join(pages))
    if len(cleaned) < 100:
        raise ResumeParseError(
            "No readable text found. This looks like a scanned PDF. "
            "Please upload a text-based PDF."
        )
    return cleaned