import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

Status = Literal["needs_review", "ready", "approved", "rejected"]
Kind = Literal["stock", "expense", "unmatched"]


class FlagOut(BaseModel):
    id: uuid.UUID
    field: str
    level: Literal["medium", "low"]
    source: Literal["model", "check"]
    reason: str
    resolved: bool


class LineOut(BaseModel):
    id: uuid.UUID
    position: int
    description: str
    quantity: Decimal | None
    unit: str | None
    unit_price: Decimal | None
    line_total: Decimal | None
    kind: Kind
    sku: str | None
    expense_category: str | None
    price_change_pct: Decimal | None


class ExtractionOut(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: Decimal
    duration_ms: int | None


class DuplicateOut(BaseModel):
    id: uuid.UUID
    label: str


class InvoiceSummary(BaseModel):
    id: uuid.UUID
    document_id: uuid.UUID
    filename: str
    status: Status
    supplier_name: str | None
    invoice_number: str | None
    issue_date: date | None
    total: Decimal | None
    currency: str | None
    open_red_flags: int
    open_flags: int
    cost_usd: Decimal | None
    created_at: datetime


class InvoiceDetail(InvoiceSummary):
    supplier_vat: str | None
    supplier_address: str | None
    due_date: date | None
    subtotal: Decimal | None
    vat_rate: Decimal | None
    vat_amount: Decimal | None
    payment_terms: str | None
    iban: str | None
    duplicate_of: DuplicateOut | None
    duplicate_confirmed: bool
    rejection_reason: str | None
    approved_at: datetime | None
    lines: list[LineOut]
    flags: list[FlagOut]
    extraction: ExtractionOut | None


class LineIn(BaseModel):
    id: uuid.UUID | None = Field(None, description="Existing line id, empty for a new line")
    description: str
    quantity: Decimal | None = None
    unit: str | None = None
    unit_price: Decimal | None = None
    line_total: Decimal | None = None
    kind: Kind = "unmatched"
    sku: str | None = None
    expense_category: str | None = None


class InvoiceUpdate(BaseModel):
    """Send only the fields that changed. Lines, when sent, replace the whole list in the new order."""

    supplier_name: str | None = None
    supplier_vat: str | None = None
    supplier_address: str | None = None
    invoice_number: str | None = None
    issue_date: date | None = None
    due_date: date | None = None
    currency: str | None = None
    subtotal: Decimal | None = None
    vat_rate: Decimal | None = None
    vat_amount: Decimal | None = None
    total: Decimal | None = None
    payment_terms: str | None = None
    iban: str | None = None
    lines: list[LineIn] | None = None
    confirm_fields: list[str] = Field(default_factory=list, description="Flagged fields the user checked and confirms as correct")
    not_duplicate: bool | None = Field(None, description="True when the user confirms this is not a duplicate")


class RejectIn(BaseModel):
    reason: str = Field(min_length=3, max_length=500)