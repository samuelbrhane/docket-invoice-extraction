"""Do the numbers on the invoice add up?"""

from decimal import Decimal

from app.rules.flags import Flag
from app.rules.normalize import CENT, Invoice

TOLERANCE = Decimal("0.01")
VAT_TOLERANCE = Decimal("0.02")


def _fmt(value: Decimal) -> str:
    return f"{value:,.2f}"


def check_math(inv: Invoice) -> list[Flag]:
    flags = []

    for i, line in enumerate(inv.lines):
        if None in (line.quantity, line.unit_price, line.line_total):
            continue
        expected = (line.quantity * line.unit_price).quantize(CENT)
        if abs(expected - line.line_total) > TOLERANCE:
            flags.append(Flag(
                f"lines[{i}].line_total", "low", "check",
                f"{line.quantity.normalize()} x {line.unit_price.normalize()} = {_fmt(expected)}, but the line says {_fmt(line.line_total)}",
            ))

    totals = [line.line_total for line in inv.lines]
    if inv.subtotal is not None and totals and None not in totals:
        lines_sum = sum(totals, Decimal("0"))
        if abs(lines_sum - inv.subtotal) > TOLERANCE:
            flags.append(Flag(
                "totals.subtotal", "low", "check",
                f"Line totals add up to {_fmt(lines_sum)}, but the subtotal says {_fmt(inv.subtotal)}",
            ))

    if None not in (inv.subtotal, inv.vat_rate, inv.vat_amount):
        expected_vat = (inv.subtotal * inv.vat_rate / 100).quantize(CENT)
        if abs(expected_vat - inv.vat_amount) > VAT_TOLERANCE:
            flags.append(Flag(
                "totals.vat_amount", "medium", "check",
                f"{inv.vat_rate.normalize()}% of {_fmt(inv.subtotal)} is {_fmt(expected_vat)}, but the VAT says {_fmt(inv.vat_amount)}",
            ))

    if None not in (inv.subtotal, inv.vat_amount, inv.total):
        expected_total = inv.subtotal + inv.vat_amount
        if abs(expected_total - inv.total) > TOLERANCE:
            flags.append(Flag(
                "totals.total", "low", "check",
                f"Subtotal plus VAT is {_fmt(expected_total)}, but the total says {_fmt(inv.total)}",
            ))

    if inv.issue_date and inv.due_date and inv.due_date < inv.issue_date:
        flags.append(Flag("invoice.due_date", "low", "check", "The due date is before the invoice date"))

    return flags