"""Save flags and keep them in step with the latest checks."""

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Confidence, FieldFlag, FlagSource, Invoice
from app.rules import Flag


def _line_id(invoice: Invoice, flag: Flag):
    index = flag.line_index
    if index is None or index >= len(invoice.lines):
        return None
    return invoice.lines[index].id


def add_flags(db: Session, invoice: Invoice, flags: list[Flag]) -> None:
    for flag in flags:
        db.add(FieldFlag(
            invoice_id=invoice.id,
            line_id=_line_id(invoice, flag),
            field=flag.field,
            level=Confidence(flag.level),
            source=FlagSource(flag.source),
            reason=flag.reason,
        ))


def open_flags(db: Session, invoice: Invoice) -> list[FieldFlag]:
    return list(db.scalars(
        select(FieldFlag).where(FieldFlag.invoice_id == invoice.id, FieldFlag.resolved_at.is_(None))
    ))


def sync_check_flags(db: Session, invoice: Invoice, fresh: list[Flag]) -> None:
    """Replace check flags with the latest results, keeping ones the user already confirmed."""
    existing = list(db.scalars(
        select(FieldFlag).where(FieldFlag.invoice_id == invoice.id, FieldFlag.source == FlagSource.CHECK)
    ))
    kept = {(flag.field, flag.reason): flag for flag in existing}
    fresh_keys = {(flag.field, flag.reason) for flag in fresh}

    for key, flag in kept.items():
        if key not in fresh_keys:
            db.delete(flag)
    add_flags(db, invoice, [flag for flag in fresh if (flag.field, flag.reason) not in kept])


def resolve_fields(db: Session, invoice: Invoice, fields: set[str], source: FlagSource | None = None) -> None:
    now = datetime.now(timezone.utc)
    for flag in open_flags(db, invoice):
        if flag.field in fields and (source is None or flag.source == source):
            flag.resolved_at = now