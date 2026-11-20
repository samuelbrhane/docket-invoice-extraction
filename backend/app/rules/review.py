"""Run every rule on an extraction and decide whether it needs review."""

from dataclasses import dataclass
from decimal import Decimal

from app.extraction.schema import ExtractedInvoice
from app.rules.checks import run_checks
from app.rules.duplicates import duplicate_flag
from app.rules.flags import Flag
from app.rules.inventory import check_lines
from app.rules.normalize import Invoice, normalize


@dataclass
class ReviewResult:
    invoice: Invoice
    flags: list[Flag]
    status: str  # needs_review or ready


def status_for(flags: list[Flag]) -> str:
    return "needs_review" if any(flag.level == "low" for flag in flags) else "ready"


def recheck(inv: Invoice, last_prices: dict[str, Decimal | None], duplicate_of: str | None = None) -> list[Flag]:
    """Code checks only. Also used again after the user edits a field."""
    flags = [*run_checks(inv), *check_lines(inv, last_prices)]
    if duplicate_of:
        flags.append(duplicate_flag(duplicate_of))
    return flags


def review_extraction(
    extracted: ExtractedInvoice,
    last_prices: dict[str, Decimal | None],
    duplicate_of: str | None = None,
) -> ReviewResult:
    inv = normalize(extracted)
    model_flags = [Flag(u.field, u.level, "model", u.reason) for u in extracted.uncertain_fields]
    flags = [*model_flags, *recheck(inv, last_prices, duplicate_of)]
    return ReviewResult(invoice=inv, flags=flags, status=status_for(flags))