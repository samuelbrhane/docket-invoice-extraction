def italian_iban(cin: str, abi: str, cab: str, account: str) -> str:
    """Build an Italian IBAN with a valid mod 97 check number."""
    bban = f"{cin}{abi}{cab}{account.zfill(12)}"
    digits = "".join(str(int(ch, 36)) for ch in f"{bban}IT00")
    check = 98 - int(digits) % 97
    return f"IT{check:02d}{bban}"