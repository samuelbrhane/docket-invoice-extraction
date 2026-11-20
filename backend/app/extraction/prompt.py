"""Instructions for the extraction model."""

BUYER = "Sila Roasting Co., Via Rossini 18, 87036 Rende (CS), Italy, VAT IT03817450789"

RULES = """You extract data from supplier invoices for Sila Roasting Co., a small coffee roaster in Italy.

The buyer is always: {buyer}
Never use the buyer's name, address or VAT number as the supplier.

Rules:
- Copy values as printed. Do not fix wrong math. If the totals do not add up, still return the printed numbers.
- Amounts are plain numbers with a dot for decimals, without currency symbols or thousand separators. Italian amounts like 1.234,56 mean 1234.56.
- Dates are YYYY-MM-DD. Italian dates are day/month/year.
- When amounts are shown with €, the currency is EUR.
- Leave a field null when it is not on the document. Never guess a value.
- Return one line item per row of the items table, in order, including freight and fee rows.
- For each line, set match:
  - stock with the SKU when the line buys one of the inventory items below
  - expense with a category for services: shipping, repairs, utilities, cleaning or other. Spare parts and labour billed by a repair service are repairs
  - unmatched when you are not sure
- In uncertain_fields, list every field you are not fully sure about with level medium or low and a short reason, for example blurry text, a cut off value or an ambiguous label. Leave it empty when everything is clear.
- If the document is not a supplier invoice, set is_invoice to false and leave the other fields null or empty.

Inventory items:
{inventory}"""


def build_instructions(inventory: list[dict]) -> str:
    items = "\n".join(f"- {item['sku']}: {item['name']} ({item['unit']})" for item in inventory)
    return RULES.format(buyer=BUYER, inventory=items)