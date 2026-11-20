"""Anonymous visitors, told apart by a cookie, each with their own copy of the data."""

import json
import uuid
from decimal import Decimal

from fastapi import Depends, Request, Response
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.config import DEMO_MODE, SAMPLE_DATA_DIR, VISITOR_COOKIE, VISITOR_COOKIE_DAYS
from app.db import get_db
from app.models import Document, DocumentFile, InventoryItem, Visitor
from app.services.history import seed_history


def _starting_inventory() -> list[dict]:
    return json.loads((SAMPLE_DATA_DIR / "inventory.json").read_text(encoding="utf-8"))


def create_visitor(db: Session) -> Visitor:
    visitor = Visitor()
    db.add(visitor)
    db.flush()
    for item in _starting_inventory():
        db.add(InventoryItem(
            visitor_id=visitor.id,
            sku=item["sku"],
            name=item["name"],
            unit=item["unit"],
            stock_qty=Decimal(item["stock_qty"]),
            last_unit_price=Decimal(item["last_unit_price"]),
        ))
    db.flush()
    seed_history(db, visitor)
    db.commit()
    return visitor


def _find(db: Session, raw_id: str | None) -> Visitor | None:
    try:
        return db.get(Visitor, uuid.UUID(raw_id)) if raw_id else None
    except ValueError:
        return None


def set_visitor_cookie(response: Response, visitor: Visitor) -> None:
    response.set_cookie(
        VISITOR_COOKIE,
        str(visitor.id),
        max_age=VISITOR_COOKIE_DAYS * 24 * 3600,
        httponly=True,
        samesite="lax",
        secure=DEMO_MODE,
    )


def get_visitor(request: Request, response: Response, db: Session = Depends(get_db)) -> Visitor:
    """FastAPI dependency: the current visitor, created on the first request."""
    visitor = _find(db, request.cookies.get(VISITOR_COOKIE))
    if visitor is None:
        visitor = create_visitor(db)
        set_visitor_cookie(response, visitor)
    return visitor


def reset_visitor(db: Session, visitor: Visitor) -> Visitor:
    """Delete everything the visitor did and start a fresh visitor with the example history."""
    upload_ids = list(db.scalars(
        select(Document.file_id)
        .join(DocumentFile, DocumentFile.id == Document.file_id)
        .where(Document.visitor_id == visitor.id, DocumentFile.sample_key.is_(None))
    ))
    db.delete(visitor)  # the database cascades to documents, invoices, inventory and the rest
    db.flush()
    if upload_ids:
        db.execute(delete(DocumentFile).where(DocumentFile.id.in_(upload_ids)))
    return create_visitor(db)