import uuid

from sqlalchemy import ForeignKey, LargeBinary, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.models.mixins import CreatedAtMixin, UuidPkMixin


class DocumentFile(UuidPkMixin, CreatedAtMixin, Base):
    """File bytes, kept apart from documents so storage can be swapped."""

    __tablename__ = "document_files"

    content: Mapped[bytes] = mapped_column(LargeBinary)
    content_type: Mapped[str] = mapped_column(String(50))
    size_bytes: Mapped[int]
    sha256: Mapped[str] = mapped_column(String(64), index=True)
    # Set for the shared sample invoices, empty for visitor uploads
    sample_key: Mapped[str | None] = mapped_column(String(50), unique=True)


class Document(UuidPkMixin, CreatedAtMixin, Base):
    __tablename__ = "documents"

    visitor_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("visitors.id", ondelete="CASCADE"), index=True
    )
    file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("document_files.id"))
    filename: Mapped[str] = mapped_column(String(255))
    page_count: Mapped[int | None]

    file: Mapped[DocumentFile] = relationship()