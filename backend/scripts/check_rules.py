"""Run the rules on every answer file, in order, as if each invoice were processed.

Run from the backend folder:  python -m scripts.check_rules
"""

import json
from decimal import Decimal
from pathlib import Path

from app.extraction.schema import ExtractedInvoice
from app.rules import duplicate_key, review_extraction

SAMPLES = Path("sample_data")
SCAN_IBAN_AS_READ = "IT34K053874284000003318920"  # what the model read from the blurry scan


def to_extracted(answer: dict) -> ExtractedInvoice:
    return ExtractedInvoice.model_validate({
        "is_invoice": True,
        "supplier": answer["supplier"],
        "invoice": answer["invoice"],
        "lines": [
            {
                "description": line["description"],
                "quantity": float(line["quantity"]),
                "unit": line["unit"],
                "unit_price": float(line["unit_price"]),
                "line_total": float(line["line_total"]),
                "match": {
                    "kind": line["match"]["kind"],
                    "sku": line["match"].get("sku"),
                    "category": line["match"].get("category"),
                },
            }
            for line in answer["lines"]
        ],
        "totals": {key: float(value) for key, value in answer["totals"].items()},
        "payment": answer["payment"],
        "uncertain_fields": [],
    })


def main() -> None:
    inventory = json.loads((SAMPLES / "inventory.json").read_text(encoding="utf-8"))
    last_prices = {item["sku"]: Decimal(item["last_unit_price"]) for item in inventory}
    seen: dict[str, str] = {}

    answers = sorted((SAMPLES / "answers").glob("*.json"))
    cases = [(path.stem, json.loads(path.read_text(encoding="utf-8")), True) for path in answers]
    scan = json.loads((SAMPLES / "answers" / "08-imballi-calabri-scan.json").read_text(encoding="utf-8"))
    scan["payment"]["iban"] = SCAN_IBAN_AS_READ
    cases.append(("08 scan as the model read it", scan, False))  # same invoice again, so skip the duplicate check

    for name, answer, track_duplicates in cases:
        extracted = to_extracted(answer)
        key = duplicate_key(extracted.supplier.vat, extracted.invoice.number)
        duplicate_of = seen.get(key) if track_duplicates else None
        result = review_extraction(extracted, last_prices, duplicate_of=duplicate_of)
        if track_duplicates and key and key not in seen:
            seen[key] = name

        print(f"\n{name}  ->  {result.status}")
        for flag in result.flags:
            print(f"  [{flag.level}] {flag.field}: {flag.reason}")
        if not result.flags:
            print("  no flags")


if __name__ == "__main__":
    main()