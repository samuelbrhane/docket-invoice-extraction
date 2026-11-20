"""Check an uploaded file before it is stored."""

import pypdfium2 as pdfium

from app.config import MAX_PDF_PAGES, MAX_UPLOAD_MB

MAX_BYTES = MAX_UPLOAD_MB * 1024 * 1024

# Trust the file's first bytes, not the name or the browser's content type
SIGNATURES = {
    b"%PDF": "application/pdf",
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
}


class UploadError(Exception):
    pass


def detect_type(content: bytes) -> str | None:
    for signature, content_type in SIGNATURES.items():
        if content.startswith(signature):
            return content_type
    return None


def page_count(content: bytes, content_type: str) -> int | None:
    if content_type != "application/pdf":
        return None
    try:
        return len(pdfium.PdfDocument(content))
    except pdfium.PdfiumError as error:
        raise UploadError("This PDF couldn't be opened. It may be damaged or password protected") from error


def validate(content: bytes) -> tuple[str, int | None]:
    """Return the content type and page count, or raise UploadError."""
    if not content:
        raise UploadError("The file is empty")
    if len(content) > MAX_BYTES:
        raise UploadError(f"The file is larger than {MAX_UPLOAD_MB} MB")
    content_type = detect_type(content)
    if content_type is None:
        raise UploadError("Only PDF, JPG and PNG files are supported")
    pages = page_count(content, content_type)
    if pages is not None and pages > MAX_PDF_PAGES:
        raise UploadError(f"Invoices can have at most {MAX_PDF_PAGES} pages")
    return content_type, pages