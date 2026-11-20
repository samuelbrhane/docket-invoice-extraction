"""SpeedLine Logistics: modern layout with a navy side strip and zebra rows."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

from scripts.make_samples.draw import H, W, fmt_date, fmt_money, line_rows, new_canvas, stamp, text_lines
from scripts.make_samples.suppliers import BUYER

NAVY = HexColor("#1b2a4a")
ORANGE = HexColor("#f28c28")
ZEBRA = HexColor("#f2f4f8")
LEFT = 34 * mm
RIGHT = W - 16 * mm


def render(spec, path):
    s = spec.supplier
    c = new_canvas(path, spec)

    # Side strip with the company name running up it
    c.setFillColor(NAVY)
    c.rect(0, 0, 22 * mm, H, stroke=0, fill=1)
    c.setFillColor(ORANGE)
    c.rect(0, H - 22 * mm, 22 * mm, 22 * mm, stroke=0, fill=1)
    c.saveState()
    c.translate(14 * mm, 30 * mm)
    c.rotate(90)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 22)
    c.drawString(0, 0, "SPEEDLINE")
    c.restoreState()

    # Title and supplier
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 28)
    c.drawString(LEFT, H - 30 * mm, "Invoice")
    c.setFont("Helvetica", 9)
    text_lines(c, RIGHT - 62 * mm, H - 22 * mm, [s.name, *s.address, f"VAT no. {s.vat}"], "Helvetica", 8.5, 4.3 * mm)

    # Detail grid
    y = H - 50 * mm
    grid = [
        ("Invoice number", spec.number),
        ("Issued", fmt_date(spec.issue_date, "iso")),
        ("Payment due", fmt_date(spec.due_date, "iso")),
        ("Account", "SRC-0042"),
    ]
    for i, (label, value) in enumerate(grid):
        x = LEFT + i * 40 * mm
        c.setFillColor(HexColor("#7a869a"))
        c.setFont("Helvetica", 7.5)
        c.drawString(x, y, label.upper())
        c.setFillColor(NAVY)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y - 5.5 * mm, value)

    c.setFillColor(HexColor("#7a869a"))
    c.setFont("Helvetica", 7.5)
    c.drawString(LEFT, y - 17 * mm, "BILLED TO")
    c.setFillColor(NAVY)
    text_lines(c, LEFT, y - 23 * mm, BUYER, "Helvetica", 9, 4.5 * mm)

    # Zebra table
    y = H - 108 * mm
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(LEFT, y, "SERVICE")
    c.drawRightString(LEFT + 112 * mm, y, "QTY")
    c.drawRightString(RIGHT - 32 * mm, y, "RATE")
    c.drawRightString(RIGHT, y, "AMOUNT")
    c.setStrokeColor(NAVY)
    c.setLineWidth(1.2)
    c.line(LEFT, y - 2.5 * mm, RIGHT, y - 2.5 * mm)
    for i, (desc, qty, unit, price, total) in enumerate(line_rows(spec)):
        y -= 9 * mm
        if i % 2 == 0:
            c.setFillColor(ZEBRA)
            c.rect(LEFT, y - 3 * mm, RIGHT - LEFT, 9 * mm, stroke=0, fill=1)
        c.setFillColor(NAVY)
        c.setFont("Helvetica", 9)
        c.drawString(LEFT + 1.5 * mm, y, desc)
        c.drawRightString(LEFT + 112 * mm, y, f"{qty} {unit}".strip())
        c.drawRightString(RIGHT - 32 * mm, y, price)
        c.drawRightString(RIGHT - 1.5 * mm, y, total)

    # Totals
    y -= 16 * mm
    for label, value in [("Net amount", spec.subtotal), (f"VAT ({spec.vat_rate}%)", spec.vat_amount)]:
        c.setFont("Helvetica", 9.5)
        c.drawRightString(RIGHT - 40 * mm, y, label)
        c.drawRightString(RIGHT - 1.5 * mm, y, fmt_money(value))
        y -= 6.5 * mm
    c.setFillColor(NAVY)
    c.rect(RIGHT - 80 * mm, y - 7 * mm, 80 * mm, 10 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(RIGHT - 40 * mm, y - 3.2 * mm, "Total EUR")
    c.drawRightString(RIGHT - 3 * mm, y - 3.2 * mm, fmt_money(spec.total))

    # Footer
    c.setFillColor(NAVY)
    lines = [spec.terms, f"Pay to IBAN {s.iban}", "Questions about this invoice? billing@speedline.example"]
    text_lines(c, LEFT, 36 * mm, lines, "Helvetica", 8.5, 4.5 * mm)

    if spec.stamp:
        stamp(c, spec.stamp)
    c.save()