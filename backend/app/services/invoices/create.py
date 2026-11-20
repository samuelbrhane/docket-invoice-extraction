"""Save a reviewed extraction as an invoice with its lines and flags."""

import uuid

from sqlalchemy.orm import Session

from app.models import InventoryItem, Invoice, InvoiceLine, InvoiceStatus, LineKind
from app.rules import ReviewResult
from app.services.invoices.flags import add_flags


def clip(value: str | None, length: int) -> str | None:
    return value[:length] if value else value


def create_invoice(
    db: Session,
    visitor_id: uuid.UUID,
    document_id: uuid.UUID,
    result: ReviewResult,
    items: dict[str, InventoryItem],
    extraction_id: uuid.UUID | None = None,
    duplicate: Invoice | None = None,
) -> Invoice:
    inv = result.invoice
    invoice = Invoice(
        visitor_id=visitor_id,
        document_id=document_id,
        extraction_id=extraction_id,
        status=InvoiceStatus(result.status),
        supplier_name=clip(inv.supplier_name, 200),
        supplier_vat=clip(inv.supplier_vat, 30),
        supplier_address=inv.supplier_address,
        invoice_number=clip(inv.invoice_number, 50),
        issue_date=inv.issue_date,
        due_date=inv.due_date,
        currency=clip(inv.currency, 3),
        subtotal=inv.subtotal,
        vat_rate=inv.vat_rate,
        vat_amount=inv.vat_amount,
        total=inv.total,
        payment_terms=clip(inv.payment_terms, 200),
        iban=clip(inv.iban, 34),
        duplicate_of_id=duplicate.id if duplicate else None,
        lines=[
            InvoiceLine(
                position=i,
                description=line.description,
                quantity=line.quantity,
                unit=clip(line.unit, 20),
                unit_price=line.unit_price,
                line_total=line.line_total,
                kind=LineKind(line.kind),
                inventory_item_id=items[line.sku].id if line.sku in items else None,
                expense_category=clip(line.category, 50),
                price_change_pct=line.price_change_pct,
            )
            for i, line in enumerate(inv.lines)
        ],
    )
    db.add(invoice)
    db.flush()
    add_flags(db, invoice, result.flags)
    return invoice