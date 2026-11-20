"""Energia Sud: utility bill with the amount due in a large box at the top."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

from scripts.make_samples.draw import H, MARGIN, W, fmt_date, fmt_money, fmt_number, logo, new_canvas, text_lines

ORANGE = HexColor("#e85d04")
SOFT = HexColor("#fff1e6")
INK = HexColor("#2d2a26")
GREY = HexColor("#8a8580")


def render(spec, path):
    s = spec.supplier
    c = new_canvas(path, spec)

    logo(c, MARGIN, H - 32 * mm, 16 * mm, "#e85d04", "ES", "diamond")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(MARGIN + 20 * mm, H - 22 * mm, s.name)
    text_lines(c, MARGIN + 20 * mm, H - 27.5 * mm, [*s.address, f"VAT {s.vat}"], "Helvetica", 8, 3.8 * mm)

    # Amount due box
    bx, bw = W - MARGIN - 72 * mm, 72 * mm
    c.setFillColor(ORANGE)
    c.roundRect(bx, H - 44 * mm, bw, 30 * mm, 3 * mm, stroke=0, fill=1)
    c.setFillColor(HexColor("#ffffff"))
    c.setFont("Helvetica", 9)
    c.drawString(bx + 5 * mm, H - 21 * mm, "Amount due")
    c.setFont("Helvetica-Bold", 22)
    c.drawString(bx + 5 * mm, H - 31 * mm, fmt_money(spec.total))
    c.setFont("Helvetica", 9)
    c.drawString(bx + 5 * mm, H - 38 * mm, f"by {fmt_date(spec.due_date, 'en')}")

    # Bill details
    c.setFillColor(SOFT)
    c.rect(MARGIN, H - 86 * mm, W - 2 * MARGIN, 30 * mm, stroke=0, fill=1)
    left = [("Customer", "Sila Roasting Co."), ("Supply address", "Via Rossini 18, 87036 Rende (CS)"), ("Customer VAT", "IT03817450789")]
    right = [("Bill number", spec.number), ("Bill date", fmt_date(spec.issue_date, "en")), ("Supply point", "POD IT001E70418836")]
    for col, items in enumerate([left, right]):
        x = MARGIN + 5 * mm + col * 90 * mm
        for i, (label, value) in enumerate(items):
            y = H - 64 * mm - i * 7.5 * mm
            c.setFillColor(GREY)
            c.setFont("Helvetica", 8)
            c.drawString(x, y, label)
            c.setFillColor(INK)
            c.setFont("Helvetica-Bold", 9)
            c.drawString(x + 30 * mm, y, value)

    # Breakdown
    y = H - 102 * mm
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "Charges breakdown")
    y -= 10 * mm
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(GREY)
    c.drawString(MARGIN, y, "Item")
    c.drawRightString(MARGIN + 120 * mm, y, "Quantity x price")
    c.drawRightString(W - MARGIN, y, "Amount")
    c.setStrokeColor(HexColor("#e2ddd8"))
    for line in spec.lines:
        y -= 9 * mm
        c.line(MARGIN, y + 5.5 * mm, W - MARGIN, y + 5.5 * mm)
        c.setFillColor(INK)
        c.setFont("Helvetica", 9.5)
        c.drawString(MARGIN, y, line.description)
        if line.unit:
            detail = f"{fmt_number(line.quantity)} {line.unit} x {fmt_number(line.unit_price, min_decimals=2)}"
        else:
            detail = "flat charge"
        c.setFillColor(GREY)
        c.drawRightString(MARGIN + 120 * mm, y, detail)
        c.setFillColor(INK)
        c.drawRightString(W - MARGIN, y, fmt_money(line.total))

    y -= 14 * mm
    rows = [("Total before VAT", spec.subtotal), (f"VAT at {spec.vat_rate}%", spec.vat_amount), ("Total to pay", spec.total)]
    for i, (label, value) in enumerate(rows):
        bold = i == 2
        c.setFont("Helvetica-Bold" if bold else "Helvetica", 11 if bold else 9.5)
        c.setFillColor(ORANGE if bold else INK)
        c.drawRightString(W - MARGIN - 40 * mm, y, label)
        c.drawRightString(W - MARGIN, y, fmt_money(value))
        y -= 7 * mm

    c.setFillColor(GREY)
    notes = [spec.terms + f" from IBAN on file. Our IBAN {s.iban}.", "Prices per kWh include energy and losses. Thank you for choosing Energia Sud."]
    text_lines(c, MARGIN, 30 * mm, notes, "Helvetica", 8, 4.2 * mm)
    c.save()