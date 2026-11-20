"""Approve an invoice into stock, or reject it."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import InventoryItem, Invoice, InvoiceStatus, LineKind, StockMovement


class ReviewError(Exception):
    pass


def approve(db: Session, invoice: Invoice, items: dict[str, InventoryItem]) -> None:
    if invoice.status == InvoiceStatus.NEEDS_REVIEW:
        raise ReviewError("Fix or confirm every red field before approving")
    if invoice.status != InvoiceStatus.READY:
        raise ReviewError("Only invoices waiting for review can be approved")

    items_by_id = {item.id: item for item in items.values()}
    for line in invoice.lines:
        item = items_by_id.get(line.inventory_item_id)
        if line.kind != LineKind.STOCK or item is None or not line.quantity:
            continue
        item.stock_qty += line.quantity
        if line.unit_price is not None:
            item.last_unit_price = line.unit_price
        db.add(StockMovement(
            inventory_item_id=item.id, invoice_line_id=line.id, quantity=line.quantity, unit_price=line.unit_price
        ))

    invoice.status = InvoiceStatus.APPROVED
    invoice.approved_at = datetime.now(timezone.utc)


def reject(invoice: Invoice, reason: str) -> None:
    if invoice.status in (InvoiceStatus.APPROVED, InvoiceStatus.REJECTED):
        raise ReviewError("This invoice was already approved or rejected")
    invoice.status = InvoiceStatus.REJECTED
    invoice.rejection_reason = reason.strip()