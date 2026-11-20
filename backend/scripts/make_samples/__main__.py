"""Generate the sample invoices, their answer files and the inventory list.

Run from the backend folder:  python -m scripts.make_samples
"""

import json
from pathlib import Path

from scripts.make_samples.answers import write_answer
from scripts.make_samples.inventory import INVENTORY
from scripts.make_samples.invoices import INVOICES
from scripts.make_samples.layouts import RENDERERS
from scripts.make_samples.scan import pdf_to_scan

OUT = Path(__file__).resolve().parents[2] / "sample_data"


def main() -> None:
    invoices_dir = OUT / "invoices"
    answers_dir = OUT / "answers"
    invoices_dir.mkdir(parents=True, exist_ok=True)
    answers_dir.mkdir(parents=True, exist_ok=True)

    for spec in INVOICES:
        render = RENDERERS[spec.supplier.layout]
        target = invoices_dir / spec.file
        if spec.scan:
            temp_pdf = target.with_suffix(".tmp.pdf")
            render(spec, str(temp_pdf))
            pdf_to_scan(temp_pdf, target)
            temp_pdf.unlink()
        else:
            render(spec, str(target))
        write_answer(spec, answers_dir)
        print(f"  {spec.file}  total {spec.total}  issues {spec.issues or '-'}")

    (OUT / "inventory.json").write_text(json.dumps(INVENTORY, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(INVOICES)} invoices, {len(INVOICES)} answer files and inventory.json to {OUT}")


if __name__ == "__main__":
    main()