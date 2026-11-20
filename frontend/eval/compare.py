"""Compare an extraction with the answer file, field by field."""

import re
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation

from app.rules import Invoice

# Keyed by the same field paths the flags use. Free text like the address and
# payment terms is left out: the wording can differ and still be right.
HEADER_FIELDS = {
    "supplier.name": ("supplier_name", lambda a: a["supplier"]["name"], "name"),
    "supplier.vat": ("supplier_vat", lambda a: a["supplier"]["vat"], "code"),
    "invoice.number": ("invoice_number", lambda a: a["invoice"]["number"], "code"),
    "invoice.issue_date": ("issue_date", lambda a: a["invoice"]["issue_date"], "date"),
    "invoice.due_date": ("due_date", lambda a: a["invoice"]["due_date"], "date"),
    "invoice.currency": ("currency", lambda a: a["invoice"]["currency"], "code"),
    "totals.subtotal": ("subtotal", lambda a: a["totals"]["subtotal"], "number"),
    "totals.vat_rate": ("vat_rate", lambda a: a["totals"]["vat_rate"], "number"),
    "totals.vat_amount": ("vat_amount", lambda a: a["totals"]["vat_amount"], "number"),
    "totals.total": ("total", lambda a: a["totals"]["total"], "number"),
    "payment.iban": ("iban", lambda a: a["payment"]["iban"], "code"),
}
LINE_FIELDS = ("quantity", "unit_price", "line_total", "match")


@dataclass
class Score:
    fields_right: int = 0
    fields_total: int = 0
    lines_right: int = 0
    lines_total: int = 0
    misses: dict[str, str] = field(default_factory=dict)  # field path: what was wrong


def _number(value) -> Decimal | None:
    try:
        return Decimal(str(value)) if value is not None else None
    except InvalidOperation:
        return None


def same(kind: str, got, expected) -> bool:
    if expected is None:
        return got is None
    if got is None:
        return False
    if kind == "number":
        a, b = _number(got), _number(expected)
        return a is not None and b is not None and abs(a - b) <= Decimal("0.01")
    if kind == "date":
        return str(got) == str(expected)
    if kind == "code":
        return re.sub(r"[\s.\-]", "", str(got)).upper() == re.sub(r"[\s.\-]", "", str(expected)).upper()
    # Names: same letters and digits, ignoring case and punctuation
    return re.sub(r"[^a-z0-9]", "", str(got).lower()) == re.sub(r"[^a-z0-9]", "", str(expected).lower())


def _match_text(kind: str, sku: str | None, category: str | None) -> str:
    return f"{kind}:{sku or category or ''}"


def score(inv: Invoice, answer: dict) -> Score:
    result = Score()

    for path, (attr, expected_of, kind) in HEADER_FIELDS.items():
        result.fields_total += 1
        got, expected = getattr(inv, attr), expected_of(answer)
        if same(kind, got, expected):
            result.fields_right += 1
        else:
            result.misses[path] = f"got {got!r}, expected {expected!r}"

    expected_lines = answer["lines"]
    if len(inv.lines) != len(expected_lines):
        result.misses["lines"] = f"got {len(inv.lines)} lines, expected {len(expected_lines)}"

    for i, expected in enumerate(expected_lines):
        got = inv.lines[i] if i < len(inv.lines) else None
        for name in LINE_FIELDS:
            result.lines_total += 1
            if got is None:
                continue
            if name == "match":
                m = expected["match"]
                ok = _match_text(got.kind, got.sku, got.category) == _match_text(m["kind"], m.get("sku"), m.get("category"))
                shown = (_match_text(got.kind, got.sku, got.category), _match_text(m["kind"], m.get("sku"), m.get("category")))
            else:
                ok = same("number", getattr(got, name), expected[name])
                shown = (getattr(got, name), expected[name])
            if ok:
                result.lines_right += 1
            else:
                result.misses[f"lines[{i}].{name}"] = f"got {shown[0]!r}, expected {shown[1]!r}"

    return result