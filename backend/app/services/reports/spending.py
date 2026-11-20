"""Where the money went, from approved invoices."""

import uuid
from collections import defaultdict
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Invoice, InvoiceStatus, LineKind
from app.schemas import SpendingCategory, SpendingMonth, SpendingOut, SpendingSupplier

ZERO = Decimal("0")


def _category(line) -> str:
    if line.kind == LineKind.STOCK:
        return "stock"
    if line.kind == LineKind.EXPENSE and line.expense_category:
        return line.expense_category
    return "other"


def spending(db: Session, visitor_id: uuid.UUID) -> SpendingOut:
    invoices = db.scalars(
        select(Invoice)
        .options(selectinload(Invoice.lines))
        .where(Invoice.visitor_id == visitor_id, Invoice.status == InvoiceStatus.APPROVED)
    ).all()

    months: dict[str, dict[str, Decimal]] = defaultdict(lambda: defaultdict(lambda: ZERO))
    suppliers: dict[str, list] = defaultdict(lambda: [ZERO, 0])
    categories: dict[str, Decimal] = defaultdict(lambda: ZERO)

    for invoice in invoices:
        when = invoice.issue_date or invoice.approved_at.date()
        month = when.strftime("%Y-%m")
        supplier = suppliers[invoice.supplier_name or "Unknown supplier"]
        supplier[1] += 1
        for line in invoice.lines:
            amount = line.line_total or ZERO
            category = _category(line)
            months[month][category] += amount
            categories[category] += amount
            supplier[0] += amount

    return SpendingOut(
        currency="EUR",
        total=sum(categories.values(), ZERO),
        months=[
            SpendingMonth(month=month, total=sum(values.values(), ZERO), by_category=dict(values))
            for month, values in sorted(months.items())
        ],
        suppliers=[
            SpendingSupplier(name=name, total=total, invoice_count=count)
            for name, (total, count) in sorted(suppliers.items(), key=lambda item: item[1][0], reverse=True)
        ],
        categories=[
            SpendingCategory(category=category, total=total)
            for category, total in sorted(categories.items(), key=lambda item: item[1], reverse=True)
        ],
    )