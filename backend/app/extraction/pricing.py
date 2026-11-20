"""Token prices in USD per million tokens, from the OpenAI pricing page."""

from decimal import Decimal

PRICES = {
    "gpt-5.4-mini": {"input": Decimal("0.75"), "cached": Decimal("0.075"), "output": Decimal("4.50")},
    "gpt-5.4": {"input": Decimal("2.50"), "cached": Decimal("0.25"), "output": Decimal("15.00")},
}

MILLION = Decimal(1_000_000)


def _prices_for(model: str) -> dict | None:
    # The API returns snapshot names like gpt-5.4-mini-2026-03-17, so match the longest prefix
    matches = [name for name in PRICES if model.startswith(name)]
    return PRICES[max(matches, key=len)] if matches else None


def cost_usd(model: str, input_tokens: int, cached_tokens: int, output_tokens: int) -> Decimal:
    prices = _prices_for(model)
    if prices is None:
        return Decimal("0")
    uncached = input_tokens - cached_tokens
    total = uncached * prices["input"] + cached_tokens * prices["cached"] + output_tokens * prices["output"]
    return (total / MILLION).quantize(Decimal("0.000001"))