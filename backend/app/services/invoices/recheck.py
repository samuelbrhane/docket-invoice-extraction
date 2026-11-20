"""Run the checks again on a saved invoice and update its flags and status."""

from sqlalchemy.orm import Session

from app.models import Confidence, InventoryItem, Invoice, InvoiceStatus, LineKind
from app.rules import recheck
from app.services.invoices.convert import to_rules
from app.services.invoices.flags import open_flags, sync_check_flags
from app.services.invoices.queries import find_duplicate, invoice_label, last_prices


def refresh_status(db: Session, invoice: Invoice) -> None:
    db.flush()
    has_red = any(flag.level == Confidence.LOW for flag in open_flags(db, invoice))
    invoice.status = InvoiceStatus.NEEDS_REVIEW if has_red else InvoiceStatus.READY


def recheck_invoice(db: Session, invoice: Invoice, items: dict[str, InventoryItem]) -> None:
    items_by_id = {item.id: item for item in items.values()}
    rules_invoice = to_rules(invoice, items_by_id)

    duplicate = find_duplicate(db, invoice.visitor_id, invoice.supplier_vat, invoice.invoice_number, before=invoice)
    invoice.duplicate_of_id = duplicate.id if duplicate else None
    duplicate_label = invoice_label(duplicate) if duplicate and not invoice.duplicate_confirmed else None

    fresh = recheck(rules_invoice, last_prices(items), duplicate_label)

    # The checks may unmatch a line or compute a new price change
    for line, checked in zip(invoice.lines, rules_invoice.lines):
        line.price_change_pct = checked.price_change_pct
        if checked.kind == "unmatched" and line.kind == LineKind.STOCK:
            line.kind, line.inventory_item_id = LineKind.UNMATCHED, None

    sync_check_flags(db, invoice, fresh)
    refresh_status(db, invoice)