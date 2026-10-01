from io import BytesIO

from pypdf import PdfReader


def extract_resume_text(pdf_bytes: bytes) -> str:
    """Convert PDF bytes into plain text."""
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    reader = PdfReader(BytesIO(pdf_bytes))
    if not reader.pages:
        raise ValueError("The PDF contains no pages.")

    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text.strip())

    return "\n\n".join(pages).strip()
