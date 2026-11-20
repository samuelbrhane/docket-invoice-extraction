"""Run one extraction on a file without the database and print what streams back.

Run from the backend folder:
    python -m scripts.try_extraction sample_data/invoices/01-altura-green-coffee.pdf
"""

import json
import mimetypes
import sys
from pathlib import Path

from app.extraction import extract

INVENTORY = json.loads(Path("sample_data/inventory.json").read_text(encoding="utf-8"))


def main(path: str) -> None:
    file = Path(path)
    content_type = mimetypes.guess_type(file.name)[0] or "application/octet-stream"
    partials = 0
    last_partial = {}

    for event in extract(file.read_bytes(), content_type, file.name, INVENTORY):
        if event["type"] == "stage":
            print(f"stage: {event['stage']}")
        elif event["type"] == "partial":
            partials += 1
            last_partial = event["data"]
        elif event["type"] == "result":
            invoice, usage = event["invoice"], event["usage"]

    print(f"partials: {partials} (last one had keys {list(last_partial)})")
    print(json.dumps(invoice.model_dump(), indent=2, ensure_ascii=False))
    print(
        f"model {usage.model} | tokens in {usage.input_tokens} out {usage.output_tokens} | "
        f"cost ${usage.cost_usd} | {usage.duration_ms} ms"
    )


if __name__ == "__main__":
    main(sys.argv[1])