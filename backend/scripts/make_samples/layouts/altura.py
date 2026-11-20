"""Altura Green Coffee: classic layout with a green header band and a ruled table."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

from scripts.make_samples.draw import H, MARGIN, W, fmt_date, fmt_money, line_rows, logo, new_canvas, text_lines
from scripts.make_samples.suppliers import BUYER

GREEN = HexColor("#2e5e3e")
PALE = HexColor("#e8f0ea")
INK = HexColor("#1d2a22")


def render(spec, path):
    s = spec.supplier
    c = new_canvas(path, spec)

    # Header band
    c.setFillColor(GREEN)
    c.rect(0, H - 38 * mm, W, 38 * mm, stroke=0, fill=1)
    logo(c, MARGIN, H - 30 * mm, 20 * mm, "#8fbf6a", "AG", "square")
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 17)
    c.drawString(MARGIN + 25 * mm, H - 19 * mm, s.name)
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN + 25 * mm, H - 25 * mm, "Specialty green coffee importers since 1998")
    c.setFont("Helvetica-Bold", 26)
    c.drawRightString(W - MARGIN, H - 22 * mm, "INVOICE")

    # Addresses and details
    c.setFillColor(INK)
    y = H - 52 * mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "FROM")
    c.drawString(MARGIN + 62 * mm, y, "BILL TO")
    text_lines(c, MARGIN, y - 6 * mm, [s.name, *s.address, f"VAT {s.vat}"], "Helvetica", 9, 4.6 * mm)
    text_lines(c, MARGIN + 62 * mm, y - 6 * mm, BUYER, "Helvetica", 9, 4.6 * mm)

    bx = W - MARGIN - 52 * mm
    c.setFillColor(PALE)
    c.rect(bx, y - 20 * mm, 52 * mm, 25 * mm, stroke=0, fill=1)
    c.setFillColor(INK)
    details = [("Invoice no.", spec.number), ("Invoice date", fmt_date(spec.issue_date, "en")), ("Due date", fmt_date(spec.due_date, "en"))]
    for i, (label, value) in enumerate(details):
        row_y = y - i * 7 * mm
        c.setFont("Helvetica", 8.5)
        c.drawString(bx + 3 * mm, row_y, label)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawRightString(bx + 49 * mm, row_y, value)

    # Table
    cols = [MARGIN, MARGIN + 92 * mm, MARGIN + 108 * mm, MARGIN + 128 * mm, W - MARGIN]
    y = H - 92 * mm
    c.setFillColor(GREEN)
    c.rect(MARGIN, y - 2.5 * mm, W - 2 * MARGIN, 8 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(cols[0] + 2 * mm, y, "Description")
    c.drawRightString(cols[2] - 2 * mm, y, "Qty")
    c.drawString(cols[2] + 2 * mm, y, "Unit")
    c.drawRightString(cols[4] - 30 * mm, y, "Unit price")
    c.drawRightString(cols[4] - 2 * mm, y, "Amount")
    c.setFillColor(INK)
    c.setStrokeColor(HexColor("#c9d6cc"))
    for desc, qty, unit, price, total in line_rows(spec):
        y -= 9 * mm
        c.setFont("Helvetica", 9)
        c.drawString(cols[0] + 2 * mm, y, desc)
        c.drawRightString(cols[2] - 2 * mm, y, qty)
        c.drawString(cols[2] + 2 * mm, y, unit)
        c.drawRightString(cols[4] - 30 * mm, y, price)
        c.drawRightString(cols[4] - 2 * mm, y, total)
        c.line(MARGIN, y - 3.5 * mm, W - MARGIN, y - 3.5 * mm)

    # Totals
    y -= 14 * mm
    totals = [("Subtotal", spec.subtotal), (f"VAT {spec.vat_rate}%", spec.vat_amount)]
    for label, value in totals:
        c.setFont("Helvetica", 9.5)
        c.drawRightString(W - MARGIN - 32 * mm, y, label)
        c.drawRightString(W - MARGIN - 2 * mm, y, fmt_money(value))
        y -= 6.5 * mm
    c.setFillColor(PALE)
    c.rect(W - MARGIN - 70 * mm, y - 3.5 * mm, 70 * mm, 10 * mm, stroke=0, fill=1)
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(W - MARGIN - 32 * mm, y, "Total due")
    c.drawRightString(W - MARGIN - 2 * mm, y, fmt_money(spec.total))

    # Payment
    y = 42 * mm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "Payment")
    text_lines(c, MARGIN, y - 5.5 * mm, [spec.terms, f"IBAN {s.iban}", f"Reference {spec.number}"], "Helvetica", 9, 4.6 * mm)
    c.save()