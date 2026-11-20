"""File bytes storage. Postgres for now; swap these three functions for S3 or Vercel Blob."""

import hashlib
import uuid

from sqlalchemy.orm import Session

from app.models import DocumentFile


def save(db: Session, content: bytes, content_type: str, sample_key: str | None = None) -> DocumentFile:
    file = DocumentFile(
        content=content,
        content_type=content_type,
        size_bytes=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
        sample_key=sample_key,
    )
    db.add(file)
    db.flush()
    return file


def get(db: Session, file_id: uuid.UUID) -> DocumentFile | None:
    return db.get(DocumentFile, file_id)


def delete(db: Session, file_id: uuid.UUID) -> None:
    file = db.get(DocumentFile, file_id)
    if file is not None:
        db.delete(file)