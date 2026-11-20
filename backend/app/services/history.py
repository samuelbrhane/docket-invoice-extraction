"""Give each new visitor a few approved invoices, so the app looks used from the first visit."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import Document, InvoiceStatus, Visitor
from app.rules import review_extraction
from app.services.invoices import create_invoice, inventory_by_sku, last_prices
from app.services.samples import HISTORY_KEYS, answer_to_extracted, get_sample, sample_file
from app.services.uploads import page_count


def seed_history(db: Session, visitor: Visitor) -> None:
    """Built from the answer files, so no tokens are spent. Stock already includes these deliveries."""
    items = inventory_by_sku(db, visitor.id)
    for key in HISTORY_KEYS:
        sample = get_sample(key)
        file = sample_file(db, key)
        document = Document(
            visitor_id=visitor.id,
            file_id=file.id,
            filename=sample["filename"],
            page_count=page_count(file.content, file.content_type),
        )
        db.add(document)
        db.flush()

        result = review_extraction(answer_to_extracted(sample["answer"]), last_prices(items))
        invoice = create_invoice(db, visitor.id, document.id, result, items)
        invoice.status = InvoiceStatus.APPROVED
        invoice.approved_at = datetime.now(timezone.utc)