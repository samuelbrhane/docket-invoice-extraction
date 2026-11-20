import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.enums import InvoiceStatus, LineKind
from app.models.mixins import CreatedAtMixin, UuidPkMixin, str_enum

MONEY = Numeric(12, 2)
UNIT_PRICE = Numeric(12, 4)
QUANTITY = Numeric(12, 3)


class Invoice(UuidPkMixin, CreatedAtMixin, Base):
    __tablename__ = "invoices"

    visitor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visitors.id", ondelete="CASCADE"), index=True
    )
    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), unique=True
    )
    extraction_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("extractions.id", ondelete="SET NULL")
    )
    status: Mapped[InvoiceStatus] = mapped_column(
        str_enum(InvoiceStatus), default=InvoiceStatus.NEEDS_REVIEW, index=True
    )

    # Supplier
    supplier_name: Mapped[str | None] = mapped_column(String(200))
    supplier_vat: Mapped[str | None] = mapped_column(String(30))
    supplier_address: Mapped[str | None] = mapped_column(Text)

    # Invoice
    invoice_number: Mapped[str | None] = mapped_column(String(50))
    issue_date: Mapped[date | None] = mapped_column(Date)
    due_date: Mapped[date | None] = mapped_column(Date)
    currency: Mapped[str | None] = mapped_column(String(3))

    # Totals
    subtotal: Mapped[Decimal | None] = mapped_column(MONEY)
    vat_rate: Mapped[Decimal | None] = mapped_column(Numeric(5, 2))
    vat_amount: Mapped[Decimal | None] = mapped_column(MONEY)
    total: Mapped[Decimal | None] = mapped_column(MONEY)

    # Payment
    payment_terms: Mapped[str | None] = mapped_column(String(200))
    iban: Mapped[str | None] = mapped_column(String(34))

    # Review
    duplicate_of_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("invoices.id", ondelete="SET NULL")
    )
    duplicate_confirmed: Mapped[bool] = mapped_column(default=False)
    rejection_reason: Mapped[str | None] = mapped_column(Text)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    lines: Mapped[list["InvoiceLine"]] = relationship(
        back_populates="invoice",
        order_by="InvoiceLine.position",
        cascade="all, delete-orphan",
    )


class InvoiceLine(UuidPkMixin, Base):
    __tablename__ = "invoice_lines"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"), index=True
    )
    position: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    quantity: Mapped[Decimal | None] = mapped_column(QUANTITY)
    unit: Mapped[str | None] = mapped_column(String(20))
    unit_price: Mapped[Decimal | None] = mapped_column(UNIT_PRICE)
    line_total: Mapped[Decimal | None] = mapped_column(MONEY)

    # Where an approved line goes: stock, an expense, or nowhere yet
    kind: Mapped[LineKind] = mapped_column(str_enum(LineKind), default=LineKind.UNMATCHED)
    inventory_item_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("inventory_items.id", ondelete="SET NULL")
    )
    expense_category: Mapped[str | None] = mapped_column(String(50))
    price_change_pct: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))

    invoice: Mapped[Invoice] = relationship(back_populates="lines")