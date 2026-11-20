import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Response, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Document, Visitor
from app.schemas import DocumentOut, SampleOut
from app.services import storage
from app.services.samples import get_sample, picker_samples, sample_file
from app.services.uploads import MAX_BYTES, UploadError, page_count, validate
from app.services.visitors import get_visitor

router = APIRouter(prefix="/api", tags=["documents"])


def to_out(doc: Document) -> DocumentOut:
    return DocumentOut(
        id=doc.id,
        filename=doc.filename,
        content_type=doc.file.content_type,
        size_bytes=doc.file.size_bytes,
        page_count=doc.page_count,
        sample_key=doc.file.sample_key,
        created_at=doc.created_at,
    )


def visitor_document(db: Session, visitor: Visitor, document_id: uuid.UUID) -> Document:
    doc = db.get(Document, document_id)
    if doc is None or doc.visitor_id != visitor.id:
        raise HTTPException(404, "Document not found")
    return doc


@router.get("/samples", response_model=list[SampleOut], summary="List the sample invoices for the picker")
def list_samples():
    return [SampleOut(**sample) for sample in picker_samples()]


@router.post("/documents", response_model=DocumentOut, status_code=201, summary="Upload an invoice or pick a sample")
def create_document(
    file: UploadFile | None = File(None, description="PDF, JPG or PNG up to 4 MB"),
    sample: str | None = Form(None, description="Sample key from GET /api/samples, instead of a file"),
    visitor: Visitor = Depends(get_visitor),
    db: Session = Depends(get_db),
):
    if (file is None) == (sample is None):
        raise HTTPException(422, "Send either a file or a sample key")

    if sample is not None:
        found = get_sample(sample)
        if found is None:
            raise HTTPException(404, "Sample not found")
        stored = sample_file(db, sample)
        filename = found["filename"]
        pages = page_count(stored.content, stored.content_type)
    else:
        content = file.file.read(MAX_BYTES + 1)
        try:
            content_type, pages = validate(content)
        except UploadError as error:
            raise HTTPException(422, str(error)) from error
        stored = storage.save(db, content, content_type)
        filename = Path(file.filename or "invoice").name[:255]

    doc = Document(visitor_id=visitor.id, file_id=stored.id, filename=filename, page_count=pages)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return to_out(doc)


@router.get(
    "/documents/{document_id}/file",
    summary="Get the original file for the document viewer",
    response_class=Response,
    responses={200: {"content": {"application/pdf": {}, "image/jpeg": {}, "image/png": {}}}},
)
def get_document_file(document_id: uuid.UUID, visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    doc = visitor_document(db, visitor, document_id)
    return Response(
        content=doc.file.content,
        media_type=doc.file.content_type,
        headers={"Content-Disposition": f'inline; filename="{doc.filename}"', "Cache-Control": "private, max-age=3600"},
    )