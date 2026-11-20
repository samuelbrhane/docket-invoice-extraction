"""Apply the user's edits, log corrections against the AI's values and re-run the checks."""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Correction, FlagSource, InventoryItem, Invoice, InvoiceLine, InvoiceStatus, LineKind
from app.rules.normalize import code, text
from app.schemas import InvoiceUpdate, LineIn
from app.services.invoices.create import clip
from app.services.invoices.fields import HEADER_FIELDS, line_path
from app.services.invoices.flags import resolve_fields
from app.services.invoices.recheck import recheck_invoice, refresh_status

CODE_COLUMNS = {"supplier_vat", "iban", "currency"}
LENGTHS = {"supplier_name": 200, "supplier_vat": 30, "invoice_number": 50, "currency": 3, "payment_terms": 200, "iban": 34}


class EditError(Exception):
    pass


def _as_text(value) -> str | None:
    if value is None:
        return None
    return format(value.normalize(), "f") if isinstance(value, Decimal) else str(value)


def _clean(column: str, value):
    if isinstance(value, str):
        value = code(value) if column in CODE_COLUMNS else text(value)
        return clip(value, LENGTHS[column]) if column in LENGTHS else value
    return value


def _correct(db: Session, invoice: Invoice, field: str, old, new, line_id=None) -> None:
    """Keep the AI's first value and the user's latest one. Drop the row if they match again."""
    row = db.scalar(select(Correction).where(
        Correction.invoice_id == invoice.id, Correction.field == field, Correction.line_id == line_id
    ))
    if row is None:
        db.add(Correction(invoice_id=invoice.id, line_id=line_id, field=field, ai_value=_as_text(old), user_value=_as_text(new)))
    elif row.ai_value == _as_text(new):
        db.delete(row)
    else:
        row.user_value = _as_text(new)


def _match_text(kind, sku, category) -> str:
    return " ".join(part for part in (kind, sku, category) if part)


def _apply_lines(db: Session, invoice: Invoice, lines: list[LineIn], items: dict[str, InventoryItem], changed: set[str]) -> None:
    existing = {line.id: line for line in invoice.lines}
    sku_by_id = {item.id: sku for sku, item in items.items()}
    ordered = []

    for position, incoming in enumerate(lines):
        kind = LineKind(incoming.kind)
        item = items.get(incoming.sku) if kind == LineKind.STOCK else None
        if kind == LineKind.STOCK and item is None:
            kind = LineKind.UNMATCHED
        category = clip(text(incoming.expense_category), 50) if kind == LineKind.EXPENSE else None
        values = {
            "description": text(incoming.description) or "",
            "quantity": incoming.quantity,
            "unit": clip(text(incoming.unit), 20),
            "unit_price": incoming.unit_price,
            "line_total": incoming.line_total,
        }

        line = existing.pop(incoming.id, None) if incoming.id else None
        if line is None:
            line = InvoiceLine(invoice_id=invoice.id, **values, kind=kind,
                               inventory_item_id=item.id if item else None, expense_category=category)
            changed.add("lines")
        else:
            for column, new in values.items():
                if getattr(line, column) != new:
                    path = line_path(position, column)
                    _correct(db, invoice, path, getattr(line, column), new, line.id)
                    setattr(line, column, new)
                    changed.add(path)
            old_match = _match_text(line.kind.value, sku_by_id.get(line.inventory_item_id), line.expense_category)
            new_match = _match_text(kind.value, item.sku if item else None, category)
            if old_match != new_match:
                path = line_path(position, "kind")
                _correct(db, invoice, path, old_match, new_match, line.id)
                line.kind, line.inventory_item_id, line.expense_category = kind, item.id if item else None, category
                changed.add(path)
        line.position = position
        ordered.append(line)

    if existing:
        changed.add("lines")
    invoice.lines = ordered  # lines left out are deleted


def apply_update(db: Session, invoice: Invoice, update: InvoiceUpdate, items: dict[str, InventoryItem]) -> None:
    if invoice.status in (InvoiceStatus.APPROVED, InvoiceStatus.REJECTED):
        raise EditError("Approved and rejected invoices can't be edited")

    sent = update.model_fields_set
    changed: set[str] = set()

    for column, path in HEADER_FIELDS.items():
        if column not in sent:
            continue
        new, old = _clean(column, getattr(update, column)), getattr(invoice, column)
        if new != old:
            _correct(db, invoice, path, old, new)
            setattr(invoice, column, new)
            changed.add(path)

    if "lines" in sent and update.lines is not None:
        _apply_lines(db, invoice, update.lines, items, changed)

    if update.not_duplicate:
        invoice.duplicate_confirmed = True

    db.flush()
    resolve_fields(db, invoice, changed, source=FlagSource.MODEL)  # an edited value replaces the model's guess
    recheck_invoice(db, invoice, items)
    if update.confirm_fields:
        resolve_fields(db, invoice, set(update.confirm_fields))
        refresh_status(db, invoice)