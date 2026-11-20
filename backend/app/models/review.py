import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.models.enums import Confidence, FlagSource
from app.models.mixins import CreatedAtMixin, UuidPkMixin, str_enum


class FieldFlag(UuidPkMixin, CreatedAtMixin, Base):
    """A field the model or a check marked as medium or low confidence."""

    __tablename__ = "field_flags"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"), index=True
    )
    line_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("invoice_lines.id", ondelete="CASCADE")
    )
    field: Mapped[str] = mapped_column(String(50))
    level: Mapped[Confidence] = mapped_column(str_enum(Confidence))
    source: Mapped[FlagSource] = mapped_column(str_enum(FlagSource))
    reason: Mapped[str] = mapped_column(Text)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class Correction(UuidPkMixin, CreatedAtMixin, Base):
    """The AI's value and the user's value for a field the user changed."""

    __tablename__ = "corrections"

    invoice_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"), index=True
    )
    line_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("invoice_lines.id", ondelete="SET NULL")
    )
    field: Mapped[str] = mapped_column(String(50))
    ai_value: Mapped[str | None] = mapped_column(Text)
    user_value: Mapped[str | None] = mapped_column(Text)