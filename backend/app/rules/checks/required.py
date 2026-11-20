"""Is anything important missing?"""

from app.rules.flags import Flag
from app.rules.normalize import Invoice

REQUIRED = {
    "supplier.name": ("supplier_name", "Supplier name is missing"),
    "invoice.number": ("invoice_number", "Invoice number is missing"),
    "invoice.issue_date": ("issue_date", "Invoice date is missing or not a valid date"),
    "totals.total": ("total", "Total is missing"),
}


def check_required(inv: Invoice) -> list[Flag]:
    if not inv.is_invoice:
        return [Flag("document", "low", "check", "This doesn't look like a supplier invoice")]

    flags = [
        Flag(path, "low", "check", reason)
        for path, (attr, reason) in REQUIRED.items()
        if getattr(inv, attr) is None
    ]
    if not inv.lines:
        flags.append(Flag("lines", "low", "check", "No line items were found"))
    for i, line in enumerate(inv.lines):
        if line.quantity is None or line.unit_price is None:
            flags.append(Flag(f"lines[{i}].quantity", "medium", "check", "Quantity or unit price is missing"))
    return flags