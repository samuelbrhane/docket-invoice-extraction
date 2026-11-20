"""Run every sample invoice through the AI and score it against its answer file.

Run from the backend folder:
    python -m eval.run_eval
    python -m eval.run_eval --model gpt-5.4
"""

import argparse
import json
import mimetypes
import time
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from pathlib import Path

from app.config import EXTRACTION_MODEL, SAMPLE_DATA_DIR
from app.extraction import extract
from app.rules import duplicate_key, normalize, review_extraction
from eval.compare import score
from eval.issues import check_issues

RESULTS_DIR = Path(__file__).parent / "results"


def run_one(path: Path, inventory: list[dict], model: str) -> dict:
    """Extract one invoice. Runs in parallel with the others."""
    answer = json.loads(path.read_text(encoding="utf-8"))
    file = SAMPLE_DATA_DIR / "invoices" / answer["file"]
    content_type = mimetypes.guess_type(file.name)[0]
    started = time.monotonic()
    for event in extract(file.read_bytes(), content_type, file.name, inventory, model=model):
        if event["type"] == "result":
            return {"name": path.stem, "answer": answer, "extracted": event["invoice"], "usage": event["usage"],
                    "seconds": time.monotonic() - started}
    raise RuntimeError(f"No result for {path.stem}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=EXTRACTION_MODEL)
    model = parser.parse_args().model

    inventory = json.loads((SAMPLE_DATA_DIR / "inventory.json").read_text(encoding="utf-8"))
    last_prices = {item["sku"]: Decimal(item["last_unit_price"]) for item in inventory}
    answers = sorted((SAMPLE_DATA_DIR / "answers").glob("*.json"))

    print(f"Running {len(answers)} invoices with {model}...\n")
    with ThreadPoolExecutor(max_workers=4) as pool:
        runs = list(pool.map(lambda path: run_one(path, inventory, model), answers))

    # The checks run in invoice order, so the resent copy is compared with the one before it
    seen: dict[str, str] = {}
    rows = []
    totals = {"fields_right": 0, "fields_total": 0, "lines_right": 0, "lines_total": 0, "caught": 0, "planted": 0,
              "flagged": 0, "silent": 0, "false_alarms": 0, "cost": Decimal("0"), "seconds": 0.0, "tokens": 0}

    print(f"{'invoice':34} {'fields':>7} {'lines':>7} {'planted':>8} {'alarms':>7} {'cost':>9} {'time':>6}")
    for run in runs:
        inv = normalize(run["extracted"])
        key = duplicate_key(inv.supplier_vat, inv.invoice_number)
        review = review_extraction(run["extracted"], last_prices, duplicate_of=seen.get(key))
        if key and key not in seen:
            seen[key] = run["name"]

        result = score(review.invoice, run["answer"])
        issues = check_issues(review.flags, run["answer"]["expected_issues"], result.misses)
        usage = run["usage"]

        planted = len(issues.caught) + len(issues.missed)
        print(
            f"{run['name']:34} {result.fields_right:>3}/{result.fields_total:<3} {result.lines_right:>3}/{result.lines_total:<3}"
            f" {(f'{len(issues.caught)}/{planted}' if planted else '-'):>8} {len(issues.false_alarms):>7}"
            f" ${usage.cost_usd:>8.4f} {run['seconds']:>5.1f}s"
        )
        for path, text in result.misses.items():
            note = "flagged for review" if path in issues.mistakes_flagged else "NOT flagged"
            print(f"    AI mistake  {path}: {text} ({note})")
        for issue in issues.missed:
            print(f"    planted problem not caught  {issue}")
        for flag in issues.false_alarms:
            print(f"    false alarm  {flag.field}: {flag.reason}")

        totals["fields_right"] += result.fields_right
        totals["fields_total"] += result.fields_total
        totals["lines_right"] += result.lines_right
        totals["lines_total"] += result.lines_total
        totals["caught"] += len(issues.caught)
        totals["planted"] += planted
        totals["flagged"] += len(issues.mistakes_flagged)
        totals["silent"] += len(issues.mistakes_silent)
        totals["false_alarms"] += len(issues.false_alarms)
        totals["cost"] += usage.cost_usd
        totals["seconds"] += run["seconds"]
        totals["tokens"] += usage.input_tokens + usage.output_tokens
        rows.append({"invoice": run["name"], "fields": [result.fields_right, result.fields_total],
                     "lines": [result.lines_right, result.lines_total], "caught": issues.caught, "missed": issues.missed,
                     "false_alarms": [f"{f.field}: {f.reason}" for f in issues.false_alarms], "mistakes": result.misses,
                     "mistakes_flagged": issues.mistakes_flagged,
                     "cost_usd": str(usage.cost_usd), "seconds": round(run["seconds"], 1)})

    count = len(runs)
    summary = {
        "model": model,
        "invoices": count,
        "field_accuracy_pct": round(100 * totals["fields_right"] / totals["fields_total"], 1),
        "line_accuracy_pct": round(100 * totals["lines_right"] / totals["lines_total"], 1),
        "planted_caught": f"{totals['caught']}/{totals['planted']}",
        "ai_mistakes": totals["flagged"] + totals["silent"],
        "ai_mistakes_flagged": totals["flagged"],
        "false_alarms": totals["false_alarms"],
        "cost_per_invoice_usd": str((totals["cost"] / count).quantize(Decimal("0.0001"))),
        "total_cost_usd": str(totals["cost"].quantize(Decimal("0.0001"))),
        "seconds_per_invoice": round(totals["seconds"] / count, 1),
        "tokens_per_invoice": totals["tokens"] // count,
    }

    print(
        f"\nField accuracy {summary['field_accuracy_pct']}% | line items {summary['line_accuracy_pct']}% | "
        f"planted problems caught {summary['planted_caught']} | false alarms {summary['false_alarms']}\n"
        f"AI mistakes {summary['ai_mistakes']}, of which {summary['ai_mistakes_flagged']} were flagged for review\n"
        f"${summary['cost_per_invoice_usd']} and {summary['seconds_per_invoice']}s per invoice, "
        f"{summary['tokens_per_invoice']} tokens, ${summary['total_cost_usd']} in total"
    )

    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"{model}.json"
    out.write_text(json.dumps({"summary": summary, "invoices": rows}, indent=2) + "\n", encoding="utf-8")
    print(f"Saved to {out.relative_to(Path.cwd())}")


if __name__ == "__main__":
    main()