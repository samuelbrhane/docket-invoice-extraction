"""Daily extraction limits for the public demo."""

from datetime import datetime, time, timezone

from fastapi import HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.config import DAILY_EXTRACTIONS_PER_VISITOR, DAILY_EXTRACTIONS_TOTAL, DEMO_MODE
from app.models import Extraction, Visitor


def check_limits(db: Session, visitor: Visitor) -> None:
    if not DEMO_MODE:
        return
    today = datetime.combine(datetime.now(timezone.utc).date(), time.min, tzinfo=timezone.utc)
    counted = select(func.count()).select_from(Extraction).where(Extraction.started_at >= today)

    if db.scalar(counted.where(Extraction.visitor_id == visitor.id)) >= DAILY_EXTRACTIONS_PER_VISITOR:
        raise HTTPException(
            429, f"You've used today's {DAILY_EXTRACTIONS_PER_VISITOR} extractions. You can still review and approve invoices."
        )
    if db.scalar(counted) >= DAILY_EXTRACTIONS_TOTAL:
        raise HTTPException(429, "The demo reached today's extraction limit. Please come back tomorrow.")