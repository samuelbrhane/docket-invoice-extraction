"""The shape the model must return. One schema drives the API, the review form and the eval."""

from typing import Literal

from pydantic import BaseModel, Field

Level = Literal["medium", "low"]
ExpenseCategory = Literal["shipping", "repairs", "utilities", "cleaning", "other"]


class SupplierFields(BaseModel):
    name: str | None = Field(description="Company that issued the invoice. Never the buyer.")
    vat: str | None = Field(description="Supplier VAT number with country prefix, for example IT02294710325")
    address: str | None = Field(description="Supplier address on one line, parts separated by commas")


class InvoiceFields(BaseModel):
    number: str | None = Field(description="Invoice number exactly as printed")
    issue_date: str | None = Field(description="Invoice date as YYYY-MM-DD")
    due_date: str | None = Field(description="Due date as YYYY-MM-DD, null if no date is printed")
    currency: str | None = Field(description="ISO 4217 code, for example EUR")


class LineMatch(BaseModel):
    kind: Literal["stock", "expense", "unmatched"]
    sku: str | None = Field(description="Inventory SKU when kind is stock, otherwise null")
    category: ExpenseCategory | None = Field(description="Expense category when kind is expense, otherwise null")


class LineItem(BaseModel):
    description: str
    quantity: float | None
    unit: str | None = Field(description="Unit as printed, for example kg, pcs, hours. Null if none")
    unit_price: float | None
    line_total: float | None
    match: LineMatch


class Totals(BaseModel):
    subtotal: float | None = Field(description="Total before VAT as printed")
    vat_rate: float | None = Field(description="VAT percent as a number, for example 22")
    vat_amount: float | None
    total: float | None = Field(description="Total including VAT as printed")


class Payment(BaseModel):
    terms: str | None = Field(description="Payment terms as printed")
    iban: str | None = Field(description="IBAN without spaces")


class UncertainField(BaseModel):
    field: str = Field(description="Path like supplier.vat, totals.total or lines[2].quantity (lines count from 0)")
    level: Level
    reason: str = Field(description="Short reason, for example blurry, cut off, ambiguous label")


class ExtractedInvoice(BaseModel):
    is_invoice: bool = Field(description="False if the document is not a supplier invoice")
    supplier: SupplierFields
    invoice: InvoiceFields
    lines: list[LineItem]
    totals: Totals
    payment: Payment
    uncertain_fields: list[UncertainField]