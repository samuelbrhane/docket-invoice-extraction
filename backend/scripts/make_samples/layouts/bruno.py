"""Bruno Espresso Service: typewriter style service invoice with dashed rules."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

from scripts.make_samples.draw import H, W, fmt_date, fmt_money, line_rows, new_canvas
from scripts.make_samples.suppliers import BUYER

INK = HexColor("#2b2b2b")
LEFT = 30 * mm
RIGHT = W - 30 * mm
CENTER = W / 2


def dashed(c, y):
    c.setDash(2, 2)
    c.line(LEFT, y, RIGHT, y)
    c.setDash()


def render(spec, path):
    s = spec.supplier
    c = new_canvas(path, spec)
    c.setFillColor(INK)
    c.setStrokeColor(INK)

    c.setFont("Courier-Bold", 18)
    c.drawCentredString(CENTER, H - 28 * mm, s.name.upper())
    c.setFont("Courier", 9.5)
    for i, line in enumerate(["Espresso machine & roaster repairs", *s.address, f"P.IVA {s.vat}"]):
        c.drawCentredString(CENTER, H - 35 * mm - i * 4.6 * mm, line)

    y = H - 62 * mm
    dashed(c, y)
    c.setFont("Courier-Bold", 11)
    c.drawString(LEFT, y - 7 * mm, f"SERVICE INVOICE  {spec.number}")
    c.setFont("Courier", 9.5)
    c.drawRightString(RIGHT, y - 7 * mm, f"DATE {fmt_date(spec.issue_date, 'it')}")
    c.drawRightString(RIGHT, y - 12 * mm, f"DUE  {fmt_date(spec.due_date, 'it')}")
    c.drawString(LEFT, y - 15 * mm, "CUSTOMER:")
    for i, line in enumerate(BUYER):
        c.drawString(LEFT, y - 20 * mm - i * 4.4 * mm, line)

    y = H - 112 * mm
    dashed(c, y + 6 * mm)
    c.setFont("Courier-Bold", 9.5)
    c.drawString(LEFT, y, "ITEM")
    c.drawRightString(LEFT + 102 * mm, y, "QTY")
    c.drawRightString(RIGHT - 28 * mm, y, "PRICE")
    c.drawRightString(RIGHT, y, "TOTAL")
    dashed(c, y - 3 * mm)
    c.setFont("Courier", 9.5)
    for desc, qty, unit, price, total in line_rows(spec):
        y -= 9 * mm
        c.drawString(LEFT, y, desc[:44])
        c.drawRightString(LEFT + 102 * mm, y, f"{qty} {unit}".strip())
        c.drawRightString(RIGHT - 28 * mm, y, price)
        c.drawRightString(RIGHT, y, total)
    dashed(c, y - 5 * mm)

    y -= 13 * mm
    for label, value in [("SUBTOTAL", spec.subtotal), (f"IVA {spec.vat_rate}%", spec.vat_amount)]:
        c.drawRightString(RIGHT - 34 * mm, y, label)
        c.drawRightString(RIGHT, y, fmt_money(value))
        y -= 5.5 * mm
    c.setFont("Courier-Bold", 12)
    c.drawRightString(RIGHT - 34 * mm, y - 2 * mm, "TOTAL")
    c.drawRightString(RIGHT, y - 2 * mm, fmt_money(spec.total))

    c.setFont("Courier", 9)
    footer = [f"PAYMENT: {spec.terms}", f"IBAN: {s.iban}", "", "Grazie! Keep the roaster running."]
    for i, line in enumerate(footer):
        c.drawString(LEFT, 46 * mm - i * 4.6 * mm, line)
    c.save()