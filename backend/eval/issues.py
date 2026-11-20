"""Did the checks catch the problems planted in the samples, and nothing else?"""

from dataclasses import dataclass

from app.rules import Flag

# How each planted problem shows up as a flag
EXPECTED = {
    "subtotal_mismatch": lambda f: f.field == "totals.subtotal",
    "duplicate": lambda f: f.field == "invoice.number" and "duplicate" in f.reason.lower(),
    "price_jump": lambda f: f.field.startswith("lines[") and f.field.endswith(".unit_price") and "price up" in f.reason.lower(),
}


@dataclass
class IssueResult:
    caught: list[str]  # planted problems the checks flagged
    missed: list[str]  # planted problems nobody flagged
    mistakes_flagged: list[str]  # fields the AI got wrong that were flagged for review
    mistakes_silent: list[str]  # fields the AI got wrong with no flag: the dangerous kind
    false_alarms: list[Flag]  # red flags on fields that were actually right


def check_issues(flags: list[Flag], expected_issues: list[str], misses: dict[str, str]) -> IssueResult:
    planted = [issue for issue in expected_issues if issue in EXPECTED]
    caught = [issue for issue in planted if any(EXPECTED[issue](flag) for flag in flags)]
    explained = [flag for flag in flags if any(EXPECTED[issue](flag) for issue in planted)]
    flagged_fields = {flag.field for flag in flags}

    return IssueResult(
        caught=caught,
        missed=[issue for issue in planted if issue not in caught],
        mistakes_flagged=[path for path in misses if path in flagged_fields],
        mistakes_silent=[path for path in misses if path not in flagged_fields],
        false_alarms=[f for f in flags if f.level == "low" and f not in explained and f.field not in misses],
    )