"""Turn a saved invoice back into the rules' plain dataclasses so the checks can run again."""

from app.models import InventoryItem, Invoice
from app.rules import Invoice as RulesInvoice
from app.rules import Line as RulesLine


def to_rules(invoice: Invoice, items_by_id: dict) -> RulesInvoice:
    return RulesInvoice(
        is_invoice=True,
        supplier_name=invoice.supplier_name,
        supplier_vat=invoice.supplier_vat,
        supplier_address=invoice.supplier_address,
        invoice_number=invoice.invoice_number,
        issue_date=invoice.issue_date,
        due_date=invoice.due_date,
        currency=invoice.currency,
        subtotal=invoice.subtotal,
        vat_rate=invoice.vat_rate,
        vat_amount=invoice.vat_amount,
        total=invoice.total,
        payment_terms=invoice.payment_terms,
        iban=invoice.iban,
        lines=[
            RulesLine(
                description=line.description,
                quantity=line.quantity,
                unit=line.unit,
                unit_price=line.unit_price,
                line_total=line.line_total,
                kind=line.kind.value,
                sku=_sku(items_by_id.get(line.inventory_item_id)),
                category=line.expense_category,
            )
            for line in invoice.lines
        ],
    )


def _sku(item: InventoryItem | None) -> str | None:
    return item.sku if item else None