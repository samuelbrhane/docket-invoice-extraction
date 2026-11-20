"""How well the AI did and what it cost, for this visitor."""

import uuid
from datetime import datetime, timedelta, timezone
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Correction, Extraction, ExtractionStatus, FieldFlag, FlagSource, Invoice, InvoiceLine, InvoiceStatus
from app.schemas import StatsOut
from app.services.invoices.fields import HEADER_FIELDS

FIELDS_PER_LINE = 6  # description, quantity, unit, unit price, line total, match


def stats(db: Session, visitor_id: uuid.UUID) -> StatsOut:
    by_status = dict(db.execute(
        select(Invoice.status, func.count()).where(Invoice.visitor_id == visitor_id).group_by(Invoice.status)
    ).all())

    # Accuracy counts only AI-extracted invoices the user finished reviewing
    reviewed = select(Invoice.id).where(
        Invoice.visitor_id == visitor_id,
        Invoice.extraction_id.is_not(None),
        Invoice.status.in_([InvoiceStatus.APPROVED, InvoiceStatus.REJECTED]),
    )
    reviewed_count = db.scalar(select(func.count()).select_from(reviewed.subquery()))
    line_count = db.scalar(select(func.count()).select_from(InvoiceLine).where(InvoiceLine.invoice_id.in_(reviewed)))
    fields_reviewed = reviewed_count * len(HEADER_FIELDS) + line_count * FIELDS_PER_LINE
    fields_corrected = db.scalar(select(func.count()).select_from(Correction).where(Correction.invoice_id.in_(reviewed)))
    accuracy = (
        (Decimal(100) * (fields_reviewed - fields_corrected) / fields_reviewed).quantize(Decimal("0.1"))
        if fields_reviewed else None
    )

    mine = select(Invoice.id).where(Invoice.visitor_id == visitor_id)
    week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    corrections_this_week = db.scalar(
        select(func.count()).select_from(Correction).where(Correction.invoice_id.in_(mine), Correction.created_at >= week_ago)
    )
    issues_caught = db.scalar(
        select(func.count()).select_from(FieldFlag).where(FieldFlag.invoice_id.in_(mine), FieldFlag.source == FlagSource.CHECK)
    )

    count, total_cost, average_cost, average_ms = db.execute(
        select(
            func.count(),
            func.coalesce(func.sum(Extraction.cost_usd), 0),
            func.avg(Extraction.cost_usd),
            func.avg(Extraction.duration_ms),
        ).where(Extraction.visitor_id == visitor_id, Extraction.status == ExtractionStatus.SUCCEEDED)
    ).one()

    return StatsOut(
        invoices_by_status={status.value: by_status.get(status, 0) for status in InvoiceStatus},
        extractions=count,
        fields_reviewed=fields_reviewed,
        fields_corrected=fields_corrected,
        accuracy_pct=accuracy,
        corrections_this_week=corrections_this_week,
        issues_caught=issues_caught,
        total_cost_usd=Decimal(total_cost).quantize(Decimal("0.000001")),
        average_cost_usd=Decimal(average_cost).quantize(Decimal("0.000001")) if average_cost is not None else None,
        average_duration_ms=int(average_ms) if average_ms is not None else None,
    )