"""Run one extraction and stream progress, partial fields and the final result."""

import time
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal

from jiter import from_json
from openai import OpenAI

from app.config import EXTRACTION_MODEL, EXTRACTION_REASONING
from app.extraction.files import document_input
from app.extraction.pricing import cost_usd
from app.extraction.prompt import build_instructions
from app.extraction.schema import ExtractedInvoice

PARTIAL_INTERVAL = 0.15  # seconds between partial updates

client = OpenAI()


class ExtractionError(Exception):
    pass


@dataclass
class Usage:
    model: str
    input_tokens: int
    cached_tokens: int
    output_tokens: int
    cost_usd: Decimal
    duration_ms: int


def _partial(text: str) -> dict | None:
    try:
        return from_json(text.encode(), partial_mode="trailing-strings")
    except ValueError:
        return None


def extract(content: bytes, content_type: str, filename: str, inventory: list[dict]) -> Iterator[dict]:
    """Yield stage, partial and result events for one document."""
    started = time.monotonic()
    yield {"type": "stage", "stage": "reading"}

    options = {"reasoning": {"effort": EXTRACTION_REASONING}} if EXTRACTION_REASONING else {}
    text = ""
    last_sent = 0.0
    extracting = False

    with client.responses.stream(
        model=EXTRACTION_MODEL,
        instructions=build_instructions(inventory),
        input=[
            {
                "role": "user",
                "content": [
                    document_input(content, content_type, filename),
                    {"type": "input_text", "text": "Extract this invoice."},
                ],
            }
        ],
        text_format=ExtractedInvoice,
        **options,
    ) as stream:
        for event in stream:
            if event.type != "response.output_text.delta":
                continue
            if not extracting:
                extracting = True
                yield {"type": "stage", "stage": "extracting"}
            text += event.delta
            now = time.monotonic()
            if now - last_sent >= PARTIAL_INTERVAL:
                data = _partial(text)
                if data:
                    last_sent = now
                    yield {"type": "partial", "data": data}
        response = stream.get_final_response()

    invoice = response.output_parsed
    if invoice is None:
        raise ExtractionError("The model returned no structured result")

    usage = response.usage
    cached = usage.input_tokens_details.cached_tokens if usage.input_tokens_details else 0
    yield {
        "type": "result",
        "invoice": invoice,
        "usage": Usage(
            model=response.model,
            input_tokens=usage.input_tokens,
            cached_tokens=cached,
            output_tokens=usage.output_tokens,
            cost_usd=cost_usd(response.model, usage.input_tokens, cached, usage.output_tokens),
            duration_ms=int((time.monotonic() - started) * 1000),
        ),
    }