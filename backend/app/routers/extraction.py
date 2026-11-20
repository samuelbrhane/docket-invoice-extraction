import uuid

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Invoice, Visitor
from app.routers.documents import visitor_document
from app.services.extraction_stream import stream_extraction
from app.services.limits import check_limits
from app.services.visitors import get_visitor

router = APIRouter(prefix="/api", tags=["extraction"])

STREAM_DESCRIPTION = """Server-Sent Events, in order:

- `stage` with `reading`, `extracting`, `checking`, then `ready`
- `partial` with the fields read so far, several times while the model writes
- `result` with the saved invoice, the same shape as `GET /api/invoices/{id}`
- `error` with a message if anything fails
"""


@router.post(
    "/documents/{document_id}/extract",
    summary="Extract the invoice and stream progress",
    description=STREAM_DESCRIPTION,
    response_class=StreamingResponse,
    responses={200: {"content": {"text/event-stream": {}}}, 409: {"description": "Already extracted"}, 429: {"description": "Daily limit reached"}},
)
def extract_document(document_id: uuid.UUID, visitor: Visitor = Depends(get_visitor), db: Session = Depends(get_db)):
    document = visitor_document(db, visitor, document_id)
    if db.scalar(select(Invoice.id).where(Invoice.document_id == document.id)):
        raise HTTPException(409, "This document was already extracted")
    check_limits(db, visitor)
    return StreamingResponse(
        stream_extraction(document.id, visitor.id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache, no-transform", "X-Accel-Buffering": "no"},
    )