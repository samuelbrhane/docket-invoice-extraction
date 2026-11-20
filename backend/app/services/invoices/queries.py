"""Lookups shared by extraction, editing and approval."""

import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import InventoryItem, Invoice, InvoiceStatus
from app.rules import duplicate_key


def inventory_by_sku(db: Session, visitor_id: uuid.UUID) -> dict[str, InventoryItem]:
    items = db.scalars(select(InventoryItem).where(InventoryItem.visitor_id == visitor_id))
    return {item.sku: item for item in items}


def last_prices(items: dict[str, InventoryItem]) -> dict[str, Decimal | None]:
    return {sku: item.last_unit_price for sku, item in items.items()}


def invoice_label(invoice: Invoice) -> str:
    return f"{invoice.supplier_name or 'Unknown supplier'} {invoice.invoice_number or ''}".strip()


def find_duplicate(
    db: Session,
    visitor_id: uuid.UUID,
    supplier_vat: str | None,
    invoice_number: str | None,
    before: Invoice | None = None,
) -> Invoice | None:
    """The earliest invoice of this visitor with the same supplier VAT and invoice number.

    When checking an invoice that is already saved, pass it as before so only older ones count.
    """
    key = duplicate_key(supplier_vat, invoice_number)
    if key is None:
        return None
    candidates = db.scalars(
        select(Invoice)
        .where(
            Invoice.visitor_id == visitor_id,
            Invoice.supplier_vat == supplier_vat,
            Invoice.status != InvoiceStatus.REJECTED,
        )
        .order_by(Invoice.created_at)
    )
    for candidate in candidates:
        if before is not None and (candidate.id == before.id or candidate.created_at >= before.created_at):
            continue
        if duplicate_key(candidate.supplier_vat, candidate.invoice_number) == key:
            return candidate
    return None