"""Pulito Pro: friendly layout with rounded cards and a teal accent."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

from scripts.make_samples.draw import H, MARGIN, W, fmt_date, fmt_money, line_rows, logo, new_canvas, text_lines
from scripts.make_samples.suppliers import BUYER

TEAL = HexColor("#0f8b8d")
MINT = HexColor("#e6f4f4")
INK = HexColor("#1f3b3c")


def render(spec, path):
    s = spec.supplier
    c = new_canvas(path, spec)

    logo(c, W - MARGIN - 22 * mm, H - 36 * mm, 22 * mm, "#0f8b8d", "PP", "circle")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(MARGIN, H - 24 * mm, s.name)
    c.setFillColor(INK)
    text_lines(c, MARGIN, H - 31 * mm, ["Professional cleaning for food businesses", *s.address, f"P.IVA {s.vat}"], "Helvetica", 9, 4.4 * mm)

    # Cards
    card_y, card_h = H - 92 * mm, 34 * mm
    card_w = (W - 2 * MARGIN - 8 * mm) / 2
    for i in range(2):
        c.setFillColor(MINT)
        c.roundRect(MARGIN + i * (card_w + 8 * mm), card_y, card_w, card_h, 4 * mm, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN + 5 * mm, card_y + card_h - 7 * mm, "Invoice for")
    c.drawString(MARGIN + card_w + 13 * mm, card_y + card_h - 7 * mm, "Invoice details")
    c.setFillColor(INK)
    text_lines(c, MARGIN + 5 * mm, card_y + card_h - 13 * mm, BUYER, "Helvetica", 9, 4.5 * mm)
    details = [("Number", spec.number), ("Date", fmt_date(spec.issue_date, "en")), ("Due", fmt_date(spec.due_date, "en"))]
    for i, (label, value) in enumerate(details):
        y = card_y + card_h - 13 * mm - i * 6 * mm
        x = MARGIN + card_w + 13 * mm
        c.setFont("Helvetica", 9)
        c.drawString(x, y, label)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(x + 20 * mm, y, value)

    # Table
    y = H - 108 * mm
    c.setFillColor(TEAL)
    c.roundRect(MARGIN, y - 3 * mm, W - 2 * MARGIN, 9 * mm, 2.5 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN + 4 * mm, y, "What we did")
    c.drawRightString(MARGIN + 115 * mm, y, "Qty")
    c.drawRightString(W - MARGIN - 32 * mm, y, "Price")
    c.drawRightString(W - MARGIN - 4 * mm, y, "Total")
    c.setFillColor(INK)
    for desc, qty, unit, price, total in line_rows(spec):
        y -= 10 * mm
        c.setFont("Helvetica", 9.5)
        c.drawString(MARGIN + 4 * mm, y, desc)
        c.drawRightString(MARGIN + 115 * mm, y, f"{qty} {unit}".strip())
        c.drawRightString(W - MARGIN - 32 * mm, y, price)
        c.drawRightString(W - MARGIN - 4 * mm, y, total)

    # Totals card
    y -= 12 * mm
    tw = 78 * mm
    c.setFillColor(MINT)
    c.roundRect(W - MARGIN - tw, y - 22 * mm, tw, 27 * mm, 4 * mm, stroke=0, fill=1)
    rows = [("Subtotal", spec.subtotal), (f"VAT {spec.vat_rate}%", spec.vat_amount), ("Total", spec.total)]
    for i, (label, value) in enumerate(rows):
        bold = i == 2
        c.setFillColor(TEAL if bold else INK)
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 12 if bold else 9.5)
        c.drawString(W - MARGIN - tw + 5 * mm, y - i * 7.5 * mm, label)
        c.drawRightString(W - MARGIN - 5 * mm, y - i * 7.5 * mm, fmt_money(value))

    c.setFillColor(INK)
    text_lines(c, MARGIN, 38 * mm, [spec.terms, f"IBAN {s.iban}", "Thank you for keeping a clean roastery!"], "Helvetica", 9, 4.6 * mm)
    c.save()