"""Daily cleanup: delete idle visitors and the upload files nobody uses anymore."""

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete, exists, select
from sqlalchemy.orm import Session

from app.config import UPLOAD_RETENTION_DAYS
from app.models import Document, DocumentFile, Invoice, Visitor


def _idle_visitor_ids(db: Session, cutoff: datetime) -> list:
    """Visitors older than the cutoff with no upload or invoice change since then."""
    recent_document = exists().where(Document.visitor_id == Visitor.id, Document.created_at >= cutoff)
    recent_invoice = exists().where(Invoice.visitor_id == Visitor.id, Invoice.updated_at >= cutoff)
    return list(db.scalars(
        select(Visitor.id).where(Visitor.created_at < cutoff, ~recent_document, ~recent_invoice)
    ))


def run_cleanup(db: Session) -> dict:
    cutoff = datetime.now(timezone.utc) - timedelta(days=UPLOAD_RETENTION_DAYS)

    visitor_ids = _idle_visitor_ids(db, cutoff)
    if visitor_ids:
        # The database cascades to documents, invoices, inventory and the rest
        db.execute(
            delete(Visitor).where(Visitor.id.in_(visitor_ids)),
            execution_options={"synchronize_session": False},
        )

    # Upload files left without a document; sample files are shared and always kept
    in_use = exists().where(Document.file_id == DocumentFile.id)
    files = db.execute(
        delete(DocumentFile).where(DocumentFile.sample_key.is_(None), ~in_use),
        execution_options={"synchronize_session": False},
    )

    return {"visitors_deleted": len(visitor_ids), "files_deleted": files.rowcount}