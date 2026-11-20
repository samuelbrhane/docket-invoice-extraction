from app.rules.checks.formats import check_formats
from app.rules.checks.math import check_math
from app.rules.checks.required import check_required
from app.rules.flags import Flag
from app.rules.normalize import Invoice


def run_checks(inv: Invoice) -> list[Flag]:
    return [*check_required(inv), *check_math(inv), *check_formats(inv)]


__all__ = ["run_checks"]