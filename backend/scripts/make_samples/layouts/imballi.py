"""Imballi Calabri: Italian invoice in a serif face with a fully boxed table."""

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

from scripts.make_samples.draw import H, MARGIN, W, fmt_date, fmt_money, line_rows, new_canvas, text_lines

INK = HexColor("#222222")
RED = HexColor("#9b2226")

SPETT = ["Spett.le", "Sila Roasting Co.", "Via Rossini 18", "87036 Rende (CS)", "P.IVA IT03817450789"]


def render(spec, path):
    s = spec.supplier
    c = new_canvas(path, spec)
    c.setFillColor(INK)

    # Supplier block
    c.setFillColor(RED)
    c.setFont("Times-Bold", 20)
    c.drawString(MARGIN, H - 26 * mm, s.name.upper())
    c.setFillColor(INK)
    lines = ["Imballaggi per alimenti e caffè", *s.address, f"P.IVA {s.vat}"]
    text_lines(c, MARGIN, H - 33 * mm, lines, "Times-Roman", 10, 4.8 * mm)

    # Document title
    c.setFont("Times-Bold", 15)
    c.drawRightString(W - MARGIN, H - 26 * mm, "FATTURA")
    c.setFont("Times-Roman", 11)
    c.drawRightString(W - MARGIN, H - 33 * mm, f"N. {spec.number}")
    c.drawRightString(W - MARGIN, H - 38.5 * mm, f"del {fmt_date(spec.issue_date, 'it')}")

    # Customer box
    bx, by = W - MARGIN - 75 * mm, H - 82 * mm
    c.setStrokeColor(INK)
    c.setLineWidth(0.8)
    c.rect(bx, by, 75 * mm, 30 * mm)
    text_lines(c, bx + 4 * mm, by + 24 * mm, SPETT, "Times-Roman", 10.5, 5 * mm)

    # Boxed table
    cols = [MARGIN, MARGIN + 88 * mm, MARGIN + 108 * mm, MARGIN + 122 * mm, MARGIN + 148 * mm, W - MARGIN]
    top = H - 96 * mm
    row_h = 9 * mm
    rows = line_rows(spec, "it")
    bottom = top - row_h * (len(rows) + 1)
    c.setFillColor(HexColor("#f1e9e0"))
    c.rect(MARGIN, top - row_h, W - 2 * MARGIN, row_h, stroke=0, fill=1)
    c.setFillColor(INK)
    c.rect(MARGIN, bottom, W - 2 * MARGIN, top - bottom)
    for x in cols[1:-1]:
        c.line(x, top, x, bottom)
    for i in range(1, len(rows) + 1):
        c.line(MARGIN, top - i * row_h, W - MARGIN, top - i * row_h)
    headers = ["Descrizione", "Q.tà", "U.M.", "Prezzo unit.", "Importo"]
    c.setFont("Times-Bold", 10)
    for i, label in enumerate(headers):
        c.drawString(cols[i] + 2 * mm, top - 6 * mm, label)
    c.setFont("Times-Roman", 10)
    for r, (desc, qty, unit, price, total) in enumerate(rows, start=1):
        y = top - r * row_h - 6 * mm
        c.drawString(cols[0] + 2 * mm, y, desc)
        c.drawRightString(cols[2] - 2 * mm, y, qty)
        c.drawString(cols[2] + 2 * mm, y, unit)
        c.drawRightString(cols[4] - 2 * mm, y, price)
        c.drawRightString(cols[5] - 2 * mm, y, total)

    # Totals box
    tx, ty = W - MARGIN - 70 * mm, bottom - 30 * mm
    c.rect(tx, ty, 70 * mm, 24 * mm)
    totals = [("Imponibile", spec.subtotal), (f"IVA {spec.vat_rate}%", spec.vat_amount), ("Totale fattura", spec.total)]
    for i, (label, value) in enumerate(totals):
        y = ty + 18 * mm - i * 7 * mm
        c.setFont("Times-Bold" if i == 2 else "Times-Roman", 11 if i == 2 else 10)
        c.drawString(tx + 3 * mm, y, label)
        c.drawRightString(tx + 67 * mm, y, fmt_money(value, "it"))

    # Payment
    info = [
        f"Pagamento: {spec.terms}",
        f"Scadenza: {fmt_date(spec.due_date, 'it')}",
        f"IBAN: {s.iban}",
    ]
    text_lines(c, MARGIN, 40 * mm, info, "Times-Roman", 10, 5 * mm)
    c.setFont("Times-Italic", 8.5)
    c.drawString(MARGIN, 18 * mm, "Contributo CONAI assolto ove dovuto. Documento emesso ai sensi del DPR 633/72.")
    c.save()