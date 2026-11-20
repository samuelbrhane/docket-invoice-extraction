import uuid
from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class InventoryItemOut(BaseModel):
    sku: str
    name: str
    unit: str
    stock_qty: Decimal
    last_unit_price: Decimal | None
    stock_value: Decimal | None
    last_delivery: datetime | None


class MovementOut(BaseModel):
    id: uuid.UUID
    quantity: Decimal
    unit_price: Decimal | None
    created_at: datetime
    invoice_id: uuid.UUID | None
    invoice_label: str | None
    issue_date: date | None


class SpendingMonth(BaseModel):
    month: str  # YYYY-MM
    total: Decimal
    by_category: dict[str, Decimal]


class SpendingSupplier(BaseModel):
    name: str
    total: Decimal
    invoice_count: int


class SpendingCategory(BaseModel):
    category: str
    total: Decimal


class SpendingOut(BaseModel):
    """Approved invoices, net of VAT. Stock lines count as stock, expense lines by category."""

    currency: str
    total: Decimal
    months: list[SpendingMonth]
    suppliers: list[SpendingSupplier]
    categories: list[SpendingCategory]


class StatsOut(BaseModel):
    invoices_by_status: dict[str, int]
    extractions: int
    fields_reviewed: int
    fields_corrected: int
    accuracy_pct: Decimal | None
    corrections_this_week: int
    issues_caught: int
    total_cost_usd: Decimal
    average_cost_usd: Decimal | None
    average_duration_ms: int | None