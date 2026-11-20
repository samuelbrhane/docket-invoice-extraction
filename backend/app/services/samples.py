"""The sample invoices visitors can try without their own file."""

import json
from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import SAMPLE_DATA_DIR
from app.models import DocumentFile
from app.services import storage
from app.services.uploads import detect_type

ISSUE_LABELS = {
    "italian": "Italian",
    "scan": "Phone photo",
    "price_jump": "Price jump",
    "subtotal_mismatch": "Wrong subtotal",
    "duplicate": "Resent copy",
}

# Already in every visitor's history, so they are left out of the picker
HISTORY_KEYS = ("01-altura-green-coffee", "04-bruno-espresso-service", "05-energia-sud")


@lru_cache
def catalog() -> list[dict]:
    samples = []
    for path in sorted((SAMPLE_DATA_DIR / "answers").glob("*.json")):
        answer = json.loads(path.read_text(encoding="utf-8"))
        samples.append({
            "key": path.stem,
            "filename": answer["file"],
            "supplier": answer["supplier"]["name"],
            "invoice_number": answer["invoice"]["number"],
            "total": answer["totals"]["total"],
            "currency": answer["invoice"]["currency"],
            "labels": [ISSUE_LABELS[issue] for issue in answer["expected_issues"]],
            "answer": answer,
        })
    return samples


def get_sample(key: str) -> dict | None:
    return next((sample for sample in catalog() if sample["key"] == key), None)


def picker_samples() -> list[dict]:
    return [sample for sample in catalog() if sample["key"] not in HISTORY_KEYS]


def sample_file(db: Session, key: str) -> DocumentFile:
    """Each sample file is stored once and shared by every visitor's documents."""
    existing = db.scalar(select(DocumentFile).where(DocumentFile.sample_key == key))
    if existing is not None:
        return existing
    sample = get_sample(key)
    content = (SAMPLE_DATA_DIR / "invoices" / sample["filename"]).read_bytes()
    return storage.save(db, content, detect_type(content), sample_key=key)