"""Shared drawing helpers for the invoice layouts."""

from datetime import date
from decimal import Decimal

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from scripts.make_samples.specs import InvoiceSpec

W, H = A4
MARGIN = 18 * mm


def new_canvas(path: str, spec: InvoiceSpec) -> Canvas:
    c = Canvas(path, pagesize=A4)
    c.setTitle(f"{spec.supplier.name} {spec.number}")
    c.setAuthor(spec.supplier.name)
    return c


def _group(text: str, lang: str) -> str:
    return text.replace(",", "X").replace(".", ",").replace("X", ".") if lang == "it" else text


def fmt_money(value: Decimal, lang: str = "en") -> str:
    text = _group(f"{value:,.2f}", lang)
    return f"{text} €" if lang == "it" else f"€{text}"


def fmt_number(value: Decimal, lang: str = "en", min_decimals: int = 0) -> str:
    """Show as many decimals as the value needs, at least min_decimals."""
    exponent = -value.normalize().as_tuple().exponent
    decimals = max(min_decimals, exponent if exponent > 0 else 0)
    return _group(f"{value:,.{decimals}f}", lang)


def fmt_date(value: date, style: str) -> str:
    if style == "it":
        return value.strftime("%d/%m/%Y")
    if style == "iso":
        return value.isoformat()
    return f"{value.day} {value.strftime('%b %Y')}"


def line_rows(spec: InvoiceSpec, lang: str = "en") -> list[tuple[str, str, str, str, str]]:
    return [
        (
            line.description,
            fmt_number(line.quantity, lang),
            line.unit,
            fmt_number(line.unit_price, lang, min_decimals=2),
            fmt_money(line.total, lang),
        )
        for line in spec.lines
    ]


def text_lines(c: Canvas, x: float, y: float, lines: list[str], font: str, size: float, leading: float) -> float:
    c.setFont(font, size)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def logo(c: Canvas, x: float, y: float, size: float, color: str, initials: str, shape: str) -> None:
    c.saveState()
    c.setFillColor(HexColor(color))
    if shape == "circle":
        c.circle(x + size / 2, y + size / 2, size / 2, stroke=0, fill=1)
    elif shape == "diamond":
        p = c.beginPath()
        p.moveTo(x + size / 2, y + size)
        p.lineTo(x + size, y + size / 2)
        p.lineTo(x + size / 2, y)
        p.lineTo(x, y + size / 2)
        p.close()
        c.drawPath(p, stroke=0, fill=1)
    else:
        c.roundRect(x, y, size, size, size * 0.18, stroke=0, fill=1)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", size * 0.36)
    c.drawCentredString(x + size / 2, y + size * 0.36, initials)
    c.restoreState()


def stamp(c: Canvas, text: str) -> None:
    """A red rubber stamp in the empty space beside the customer block."""
    c.saveState()
    c.translate(W - 62 * mm, H - 76 * mm)
    c.rotate(14)
    c.setStrokeColor(HexColor("#c0392b"))
    c.setFillColor(HexColor("#c0392b"))
    c.setLineWidth(2.2)
    width = c.stringWidth(text, "Helvetica-Bold", 20) + 14 * mm
    c.roundRect(-width / 2, -7 * mm, width, 14 * mm, 3 * mm, stroke=1, fill=0)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(0, -2.6 * mm, text)
    c.restoreState()