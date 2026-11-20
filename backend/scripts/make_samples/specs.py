from dataclasses import dataclass, field
from datetime import date
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(CENT, rounding=ROUND_HALF_UP)


@dataclass
class Supplier:
    key: str
    name: str
    vat: str
    address: list[str]
    iban: str
    layout: str
    lang: str = "en"


@dataclass
class Line:
    description: str
    quantity: Decimal
    unit: str
    unit_price: Decimal
    sku: str | None = None  # expected inventory match
    expense: str | None = None  # expected expense category

    @property
    def total(self) -> Decimal:
        return money(self.quantity * self.unit_price)


@dataclass
class InvoiceSpec:
    file: str
    supplier: Supplier
    number: str
    issue_date: date
    due_date: date
    lines: list[Line]
    vat_rate: Decimal
    terms: str
    printed_subtotal: Decimal | None = None  # set to print a wrong subtotal
    stamp: str | None = None
    scan: bool = False
    issues: list[str] = field(default_factory=list)

    @property
    def subtotal(self) -> Decimal:
        if self.printed_subtotal is not None:
            return self.printed_subtotal
        return money(sum((line.total for line in self.lines), Decimal("0")))

    @property
    def vat_amount(self) -> Decimal:
        return money(self.subtotal * self.vat_rate / 100)

    @property
    def total(self) -> Decimal:
        return self.subtotal + self.vat_amount