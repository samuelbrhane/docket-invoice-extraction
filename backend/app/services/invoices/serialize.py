"""Build API responses from saved invoices."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Confidence, Document, Extraction, FieldFlag, InventoryItem, Invoice
from app.schemas import DuplicateOut, ExtractionOut, FlagOut, InvoiceDetail, InvoiceSummary, LineOut
from app.services.invoices.queries import invoice_label


def flag_counts(db: Session, invoice_ids: list[uuid.UUID]) -> dict[uuid.UUID, tuple[int, int]]:
    """Open flags per invoice as (red, all)."""
    if not invoice_ids:
        return {}
    rows = db.execute(
        select(
            FieldFlag.invoice_id,
            func.count().filter(FieldFlag.level == Confidence.LOW),
            func.count(),
        )
        .where(FieldFlag.invoice_id.in_(invoice_ids), FieldFlag.resolved_at.is_(None))
        .group_by(FieldFlag.invoice_id)
    )
    return {invoice_id: (red, total) for invoice_id, red, total in rows}


def _summary_fields(invoice: Invoice, filename: str, counts: tuple[int, int], extraction: Extraction | None) -> dict:
    return {
        "id": invoice.id,
        "document_id": invoice.document_id,
        "filename": filename,
        "status": invoice.status.value,
        "supplier_name": invoice.supplier_name,
        "invoice_number": invoice.invoice_number,
        "issue_date": invoice.issue_date,
        "total": invoice.total,
        "currency": invoice.currency,
        "open_red_flags": counts[0],
        "open_flags": counts[1],
        "cost_usd": extraction.cost_usd if extraction else None,
        "created_at": invoice.created_at,
    }


def list_summaries(db: Session, visitor_id: uuid.UUID) -> list[InvoiceSummary]:
    rows = db.execute(
        select(Invoice, Document.filename, Extraction)
        .join(Document, Document.id == Invoice.document_id)
        .outerjoin(Extraction, Extraction.id == Invoice.extraction_id)
        .where(Invoice.visitor_id == visitor_id)
        .order_by(Invoice.created_at.desc())
    ).all()
    counts = flag_counts(db, [invoice.id for invoice, _, _ in rows])
    return [
        InvoiceSummary(**_summary_fields(invoice, filename, counts.get(invoice.id, (0, 0)), extraction))
        for invoice, filename, extraction in rows
    ]


def to_detail(db: Session, invoice: Invoice) -> InvoiceDetail:
    document = db.get(Document, invoice.document_id)
    extraction = db.get(Extraction, invoice.extraction_id) if invoice.extraction_id else None
    duplicate = db.get(Invoice, invoice.duplicate_of_id) if invoice.duplicate_of_id else None
    sku_by_id = dict(db.execute(
        select(InventoryItem.id, InventoryItem.sku).where(InventoryItem.visitor_id == invoice.visitor_id)
    ).all())
    flags = db.scalars(select(FieldFlag).where(FieldFlag.invoice_id == invoice.id).order_by(FieldFlag.created_at)).all()
    counts = flag_counts(db, [invoice.id]).get(invoice.id, (0, 0))

    return InvoiceDetail(
        **_summary_fields(invoice, document.filename, counts, extraction),
        supplier_vat=invoice.supplier_vat,
        supplier_address=invoice.supplier_address,
        due_date=invoice.due_date,
        subtotal=invoice.subtotal,
        vat_rate=invoice.vat_rate,
        vat_amount=invoice.vat_amount,
        payment_terms=invoice.payment_terms,
        iban=invoice.iban,
        duplicate_of=DuplicateOut(id=duplicate.id, label=invoice_label(duplicate)) if duplicate else None,
        duplicate_confirmed=invoice.duplicate_confirmed,
        rejection_reason=invoice.rejection_reason,
        approved_at=invoice.approved_at,
        lines=[
            LineOut(
                id=line.id,
                position=line.position,
                description=line.description,
                quantity=line.quantity,
                unit=line.unit,
                unit_price=line.unit_price,
                line_total=line.line_total,
                kind=line.kind.value,
                sku=sku_by_id.get(line.inventory_item_id),
                expense_category=line.expense_category,
                price_change_pct=line.price_change_pct,
            )
            for line in invoice.lines
        ],
        flags=[
            FlagOut(
                id=flag.id,
                field=flag.field,
                level=flag.level.value,
                source=flag.source.value,
                reason=flag.reason,
                resolved=flag.resolved_at is not None,
            )
            for flag in flags
        ],
        extraction=ExtractionOut(
            model=extraction.model,
            input_tokens=extraction.input_tokens,
            output_tokens=extraction.output_tokens,
            cost_usd=extraction.cost_usd,
            duration_ms=extraction.duration_ms,
        ) if extraction else None,
    )