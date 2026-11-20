import uuid
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.mixins import CreatedAtMixin, UuidPkMixin


class InventoryItem(UuidPkMixin, CreatedAtMixin, Base):
    """Each visitor's own copy of the roaster's stock items."""

    __tablename__ = "inventory_items"
    __table_args__ = (UniqueConstraint("visitor_id", "sku"),)

    visitor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visitors.id", ondelete="CASCADE"), index=True
    )
    sku: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(20))
    stock_qty: Mapped[Decimal] = mapped_column(Numeric(12, 3), default=Decimal("0"))
    last_unit_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))


class StockMovement(UuidPkMixin, CreatedAtMixin, Base):
    """Stock added to an item by an approved invoice line."""

    __tablename__ = "stock_movements"

    inventory_item_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("inventory_items.id", ondelete="CASCADE"), index=True
    )
    invoice_line_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("invoice_lines.id", ondelete="SET NULL")
    )
    quantity: Mapped[Decimal] = mapped_column(Numeric(12, 3))
    unit_price: Mapped[Decimal | None] = mapped_column(Numeric(12, 4))