"""Write the correct values for each invoice, used by the eval."""

import json
from pathlib import Path

from scripts.make_samples.specs import InvoiceSpec


def _match(line) -> dict:
    if line.sku:
        return {"kind": "stock", "sku": line.sku}
    if line.expense:
        return {"kind": "expense", "category": line.expense}
    return {"kind": "unmatched"}


def answer_for(spec: InvoiceSpec) -> dict:
    s = spec.supplier
    return {
        "file": spec.file,
        "supplier": {"name": s.name, "vat": s.vat, "address": ", ".join(s.address)},
        "invoice": {
            "number": spec.number,
            "issue_date": spec.issue_date.isoformat(),
            "due_date": spec.due_date.isoformat(),
            "currency": "EUR",
        },
        "lines": [
            {
                "description": line.description,
                "quantity": str(line.quantity),
                "unit": line.unit or None,
                "unit_price": str(line.unit_price),
                "line_total": str(line.total),
                "match": _match(line),
            }
            for line in spec.lines
        ],
        "totals": {
            "subtotal": str(spec.subtotal),
            "vat_rate": str(spec.vat_rate),
            "vat_amount": str(spec.vat_amount),
            "total": str(spec.total),
        },
        "payment": {"terms": spec.terms, "iban": s.iban},
        "expected_issues": spec.issues,
    }


def write_answer(spec: InvoiceSpec, folder: Path) -> None:
    path = folder / f"{Path(spec.file).stem}.json"
    path.write_text(json.dumps(answer_for(spec), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")