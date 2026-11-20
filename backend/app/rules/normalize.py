"""Turn the model's output into clean values the checks and the database can use."""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from app.extraction.schema import ExtractedInvoice

CENT = Decimal("0.01")
UNIT_PRICE_STEP = Decimal("0.0001")
QUANTITY_STEP = Decimal("0.001")


@dataclass
class Line:
    description: str
    quantity: Decimal | None
    unit: str | None
    unit_price: Decimal | None
    line_total: Decimal | None
    kind: str = "unmatched"  # stock, expense or unmatched
    sku: str | None = None
    category: str | None = None
    price_change_pct: Decimal | None = None


@dataclass
class Invoice:
    is_invoice: bool = True
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
    lines: list[Line] = field(default_factory=list)


def text(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


def code(value: str | None) -> str | None:
    """Uppercase with spaces, dots and dashes removed, for VAT numbers and IBANs."""
    value = text(value)
    if value is None:
        return None
    return "".join(ch for ch in value.upper() if ch not in " .-") or None


def number(value: float | None, step: Decimal) -> Decimal | None:
    if value is None:
        return None
    return Decimal(str(value)).quantize(step)


def iso_date(value: str | None) -> date | None:
    try:
        return date.fromisoformat(value) if value else None
    except ValueError:
        return None


def normalize(extracted: ExtractedInvoice) -> Invoice:
    s, inv, t, p = extracted.supplier, extracted.invoice, extracted.totals, extracted.payment
    return Invoice(
        is_invoice=extracted.is_invoice,
        supplier_name=text(s.name),
        supplier_vat=code(s.vat),
        supplier_address=text(s.address),
        invoice_number=text(inv.number),
        issue_date=iso_date(inv.issue_date),
        due_date=iso_date(inv.due_date),
        currency=code(inv.currency),
        subtotal=number(t.subtotal, CENT),
        vat_rate=number(t.vat_rate, CENT),
        vat_amount=number(t.vat_amount, CENT),
        total=number(t.total, CENT),
        payment_terms=text(p.terms),
        iban=code(p.iban),
        lines=[
            Line(
                description=text(line.description) or "",
                quantity=number(line.quantity, QUANTITY_STEP),
                unit=text(line.unit),
                unit_price=number(line.unit_price, UNIT_PRICE_STEP),
                line_total=number(line.line_total, CENT),
                kind=line.match.kind,
                sku=line.match.sku if line.match.kind == "stock" else None,
                category=line.match.category if line.match.kind == "expense" else None,
            )
            for line in extracted.lines
        ],
    )