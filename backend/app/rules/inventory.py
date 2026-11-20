"""Check each line's inventory match and warn about price jumps."""

from decimal import Decimal

from app.rules.flags import Flag
from app.rules.normalize import CENT, Invoice

PRICE_ALERT_PCT = Decimal("10")


def _price(value: Decimal) -> str:
    decimals = max(2, -value.normalize().as_tuple().exponent)
    return f"{value:.{decimals}f}"


def check_lines(inv: Invoice, last_prices: dict[str, Decimal | None]) -> list[Flag]:
    """last_prices maps every inventory SKU to its last unit price (None if never bought)."""
    flags = []
    for i, line in enumerate(inv.lines):
        if line.kind == "unmatched":
            flags.append(Flag(f"lines[{i}].match", "medium", "check", "Pick an inventory item or an expense category"))
            continue
        if line.kind != "stock":
            continue
        if line.sku not in last_prices:
            flags.append(Flag(f"lines[{i}].match", "medium", "check", f"Suggested item {line.sku} isn't in the inventory"))
            line.kind, line.sku = "unmatched", None
            continue

        last = last_prices[line.sku]
        line.price_change_pct = None
        if last and line.unit_price is not None:
            pct = ((line.unit_price - last) / last * 100).quantize(CENT)
            line.price_change_pct = pct
            if pct > PRICE_ALERT_PCT:
                flags.append(Flag(
                    f"lines[{i}].unit_price", "medium", "check",
                    f"Price up {pct:.0f}% since the last invoice ({_price(last)} to {_price(line.unit_price)})",
                ))
    return flags