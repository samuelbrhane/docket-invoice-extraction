"""Map database columns to the field paths used by flags and corrections."""

HEADER_FIELDS = {
    "supplier_name": "supplier.name",
    "supplier_vat": "supplier.vat",
    "supplier_address": "supplier.address",
    "invoice_number": "invoice.number",
    "issue_date": "invoice.issue_date",
    "due_date": "invoice.due_date",
    "currency": "invoice.currency",
    "subtotal": "totals.subtotal",
    "vat_rate": "totals.vat_rate",
    "vat_amount": "totals.vat_amount",
    "total": "totals.total",
    "payment_terms": "payment.terms",
    "iban": "payment.iban",
}

LINE_FIELDS = {
    "description": "description",
    "quantity": "quantity",
    "unit": "unit",
    "unit_price": "unit_price",
    "line_total": "line_total",
    "kind": "match",
    "sku": "match",
    "expense_category": "match",
}


def line_path(position: int, column: str) -> str:
    return f"lines[{position}].{LINE_FIELDS[column]}"