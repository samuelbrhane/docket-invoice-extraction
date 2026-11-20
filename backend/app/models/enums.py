from enum import StrEnum


class ExtractionStatus(StrEnum):
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class InvoiceStatus(StrEnum):
    NEEDS_REVIEW = "needs_review"
    READY = "ready"
    APPROVED = "approved"
    REJECTED = "rejected"


class Confidence(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class FlagSource(StrEnum):
    MODEL = "model"
    CHECK = "check"


class LineKind(StrEnum):
    STOCK = "stock"
    EXPENSE = "expense"
    UNMATCHED = "unmatched"