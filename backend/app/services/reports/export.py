"""Export invoices as CSV (one row per line item) or JSON, ready for accounting software.

This is where an integration with QuickBooks, Xero or an ERP would plug in.
"""

import csv
import io

from sqlalchemy.orm import Session

from app.models import Invoice
from app.services.invoices import to_detail

CSV_COLUMNS = [
    "invoice_number", "supplier_name", "supplier_vat", "issue_date", "due_date", "currency",
    "line", "description", "quantity", "unit", "unit_price", "line_total", "kind", "sku", "expense_category",
    "subtotal", "vat_rate", "vat_amount", "total", "iban", "status",
]

INVOICE_FIELDS = [
    "id", "status", "supplier_name", "supplier_vat", "supplier_address", "invoice_number", "issue_date",
    "due_date", "currency", "subtotal", "vat_rate", "vat_amount", "total", "payment_terms", "iban", "approved_at",
]
LINE_FIELDS = ["description", "quantity", "unit", "unit_price", "line_total", "kind", "sku", "expense_category"]


def to_json(db: Session, invoices: list[Invoice]) -> list[dict]:
    exported = []
    for invoice in invoices:
        detail = to_detail(db, invoice).model_dump(mode="json")
        exported.append({
            **{field: detail[field] for field in INVOICE_FIELDS},
            "lines": [{field: line[field] for field in LINE_FIELDS} for line in detail["lines"]],
        })
    return exported


def to_csv(db: Session, invoices: list[Invoice]) -> str:
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    for invoice in to_json(db, invoices):
        for number, line in enumerate(invoice["lines"], start=1):
            writer.writerow({
                **{column: invoice.get(column) for column in CSV_COLUMNS if column in invoice},
                **{column: line.get(column) for column in LINE_FIELDS},
                "line": number,
            })
    return buffer.getvalue()