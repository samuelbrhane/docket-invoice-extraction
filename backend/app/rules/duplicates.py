"""Spot an invoice that was already processed."""

from app.rules.flags import Flag
from app.rules.normalize import code


def duplicate_key(supplier_vat: str | None, invoice_number: str | None) -> str | None:
    """Same supplier VAT number and same invoice number means the same invoice."""
    vat, number = code(supplier_vat), code(invoice_number)
    if not vat or not number:
        return None
    return f"{vat}|{number}"


def duplicate_flag(earlier: str) -> Flag:
    return Flag(
        "invoice.number", "low", "check",
        f"Possible duplicate of {earlier}, which has the same supplier VAT number and invoice number",
    )