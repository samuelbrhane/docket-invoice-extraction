"""Stock levels and the deliveries behind them."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import InventoryItem, Invoice, InvoiceLine, StockMovement
from app.rules.normalize import CENT
from app.schemas import InventoryItemOut, MovementOut
from app.services.invoices import invoice_label


def list_inventory(db: Session, visitor_id: uuid.UUID) -> list[InventoryItemOut]:
    last_delivery = (
        select(StockMovement.inventory_item_id, func.max(StockMovement.created_at).label("at"))
        .group_by(StockMovement.inventory_item_id)
        .subquery()
    )
    rows = db.execute(
        select(InventoryItem, last_delivery.c.at)
        .outerjoin(last_delivery, last_delivery.c.inventory_item_id == InventoryItem.id)
        .where(InventoryItem.visitor_id == visitor_id)
        .order_by(InventoryItem.sku)
    ).all()
    return [
        InventoryItemOut(
            sku=item.sku,
            name=item.name,
            unit=item.unit,
            stock_qty=item.stock_qty,
            last_unit_price=item.last_unit_price,
            stock_value=(item.stock_qty * item.last_unit_price).quantize(CENT) if item.last_unit_price else None,
            last_delivery=at,
        )
        for item, at in rows
    ]


def find_item(db: Session, visitor_id: uuid.UUID, sku: str) -> InventoryItem | None:
    return db.scalar(select(InventoryItem).where(InventoryItem.visitor_id == visitor_id, InventoryItem.sku == sku))


def list_movements(db: Session, item: InventoryItem) -> list[MovementOut]:
    rows = db.execute(
        select(StockMovement, Invoice)
        .outerjoin(InvoiceLine, InvoiceLine.id == StockMovement.invoice_line_id)
        .outerjoin(Invoice, Invoice.id == InvoiceLine.invoice_id)
        .where(StockMovement.inventory_item_id == item.id)
        .order_by(StockMovement.created_at.desc())
    ).all()
    return [
        MovementOut(
            id=movement.id,
            quantity=movement.quantity,
            unit_price=movement.unit_price,
            created_at=movement.created_at,
            invoice_id=invoice.id if invoice else None,
            invoice_label=invoice_label(invoice) if invoice else None,
            issue_date=invoice.issue_date if invoice else None,
        )
        for movement, invoice in rows
    ]