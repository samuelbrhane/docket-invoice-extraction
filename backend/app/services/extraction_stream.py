"""Run an extraction as a stream of Server-Sent Events and save the result."""

import json
import logging
import uuid
from collections.abc import Iterator
from datetime import datetime, timezone

from app.config import EXTRACTION_MODEL
from app.db import SessionLocal
from app.extraction import extract
from app.models import Document, Extraction, ExtractionStatus
from app.rules import normalize, review_extraction
from app.services.invoices import create_invoice, find_duplicate, inventory_by_sku, invoice_label, last_prices, to_detail

logger = logging.getLogger(__name__)


def sse(event: str, data) -> str:
    return f"event: {event}\ndata: {json.dumps(data, default=str)}\n\n"


def stream_extraction(document_id: uuid.UUID, visitor_id: uuid.UUID) -> Iterator[str]:
    """Events: stage (reading, extracting, checking, ready), partial, result, error."""
    db = SessionLocal()  # its own session, because the stream outlives the request handler
    extraction = None
    try:
        document = db.get(Document, document_id)
        items = inventory_by_sku(db, visitor_id)
        inventory = [{"sku": item.sku, "name": item.name, "unit": item.unit} for item in items.values()]

        extraction = Extraction(document_id=document_id, visitor_id=visitor_id, model=EXTRACTION_MODEL)
        db.add(extraction)
        db.commit()

        final = None
        for event in extract(document.file.content, document.file.content_type, document.filename, inventory):
            if event["type"] == "stage":
                yield sse("stage", {"stage": event["stage"]})
            elif event["type"] == "partial":
                yield sse("partial", event["data"])
            else:
                final = event

        yield sse("stage", {"stage": "checking"})
        extracted, usage = final["invoice"], final["usage"]
        normalized = normalize(extracted)
        duplicate = find_duplicate(db, visitor_id, normalized.supplier_vat, normalized.invoice_number)
        result = review_extraction(extracted, last_prices(items), invoice_label(duplicate) if duplicate else None)

        extraction.status = ExtractionStatus.SUCCEEDED
        extraction.model = usage.model[:50]
        extraction.input_tokens = usage.input_tokens
        extraction.output_tokens = usage.output_tokens
        extraction.cost_usd = usage.cost_usd
        extraction.duration_ms = usage.duration_ms
        extraction.raw_output = extracted.model_dump()
        extraction.finished_at = datetime.now(timezone.utc)

        invoice = create_invoice(db, visitor_id, document_id, result, items, extraction.id, duplicate)
        db.commit()
        yield sse("result", to_detail(db, invoice).model_dump(mode="json"))
        yield sse("stage", {"stage": "ready"})
    except Exception as error:
        logger.exception("Extraction failed for document %s", document_id)
        db.rollback()
        if extraction is not None:
            extraction.status = ExtractionStatus.FAILED
            extraction.error = str(error)[:2000]
            extraction.finished_at = datetime.now(timezone.utc)
            db.commit()
        yield sse("error", {"message": "The extraction failed. Please try again."})
    finally:
        db.close()