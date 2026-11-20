"""Do the codes look like real VAT numbers, IBANs and currencies?"""

import re

from app.rules.flags import Flag
from app.rules.normalize import Invoice

IBAN_LENGTHS = {"AT": 20, "BE": 16, "CH": 21, "DE": 22, "ES": 24, "FR": 27, "GB": 22, "IT": 27, "NL": 18, "PT": 25}
VAT_PATTERNS = {"IT": r"IT\d{11}", "DE": r"DE\d{9}", "FR": r"FR[0-9A-Z]{2}\d{9}", "ES": r"ES[0-9A-Z]\d{7}[0-9A-Z]", "NL": r"NL\d{9}B\d{2}"}
CURRENCIES = {"EUR", "USD", "GBP", "CHF"}


def iban_checksum_ok(iban: str) -> bool:
    rearranged = iban[4:] + iban[:4]
    try:
        return int("".join(str(int(ch, 36)) for ch in rearranged)) % 97 == 1
    except ValueError:
        return False


def iban_problem(iban: str) -> str | None:
    country = iban[:2]
    expected = IBAN_LENGTHS.get(country)
    if expected and len(iban) != expected:
        return f"{country} IBANs have {expected} characters, this one has {len(iban)}. A character was probably misread"
    if not iban_checksum_ok(iban):
        return "The IBAN check digits don't match. A character was probably misread"
    return None


def vat_problem(vat: str) -> str | None:
    pattern = VAT_PATTERNS.get(vat[:2], r"[A-Z]{2}[0-9A-Z]{8,12}")
    if not re.fullmatch(pattern, vat):
        return "This doesn't look like a valid VAT number"
    return None


def check_formats(inv: Invoice) -> list[Flag]:
    flags = []
    if inv.iban and (problem := iban_problem(inv.iban)):
        flags.append(Flag("payment.iban", "low", "check", problem))
    if inv.supplier_vat and (problem := vat_problem(inv.supplier_vat)):
        flags.append(Flag("supplier.vat", "medium", "check", problem))
    if inv.currency and inv.currency not in CURRENCIES:
        flags.append(Flag("invoice.currency", "medium", "check", f"{inv.currency} isn't a currency we expect"))
    return flags