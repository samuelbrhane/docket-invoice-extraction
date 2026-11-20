import uuid
from datetime import datetime

from pydantic import BaseModel


class SampleOut(BaseModel):
    key: str
    filename: str
    supplier: str
    invoice_number: str
    total: str
    currency: str
    labels: list[str]


class DocumentOut(BaseModel):
    id: uuid.UUID
    filename: str
    content_type: str
    size_bytes: int
    page_count: int | None
    sample_key: str | None
    created_at: datetime