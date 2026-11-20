import type { InvoiceDetail } from "@/lib/api";

export type HeaderColumn =
  | "supplier_name"
  | "supplier_vat"
  | "supplier_address"
  | "invoice_number"
  | "issue_date"
  | "due_date"
  | "currency"
  | "subtotal"
  | "vat_rate"
  | "vat_amount"
  | "total"
  | "payment_terms"
  | "iban";

export type FieldKind = "text" | "code" | "date" | "money" | "percent";

export type FieldDef = { column: HeaderColumn; path: string; label: string; kind: FieldKind; wide?: boolean };

/** Every header field, with the flag path the backend uses for it. */
export const SECTIONS: { title: string; fields: FieldDef[] }[] = [
  {
    title: "Supplier",
    fields: [
      { column: "supplier_name", path: "supplier.name", label: "Name", kind: "text" },
      { column: "supplier_vat", path: "supplier.vat", label: "VAT number", kind: "code" },
      { column: "supplier_address", path: "supplier.address", label: "Address", kind: "text", wide: true },
    ],
  },
  {
    title: "Invoice",
    fields: [
      { column: "invoice_number", path: "invoice.number", label: "Number", kind: "code" },
      { column: "currency", path: "invoice.currency", label: "Currency", kind: "code" },
      { column: "issue_date", path: "invoice.issue_date", label: "Issued", kind: "date" },
      { column: "due_date", path: "invoice.due_date", label: "Due", kind: "date" },
    ],
  },
  {
    title: "Totals",
    fields: [
      { column: "subtotal", path: "totals.subtotal", label: "Subtotal", kind: "money" },
      { column: "vat_rate", path: "totals.vat_rate", label: "VAT rate (%)", kind: "percent" },
      { column: "vat_amount", path: "totals.vat_amount", label: "VAT", kind: "money" },
      { column: "total", path: "totals.total", label: "Total", kind: "money" },
    ],
  },
  {
    title: "Payment",
    fields: [
      { column: "payment_terms", path: "payment.terms", label: "Terms", kind: "text" },
      { column: "iban", path: "payment.iban", label: "IBAN", kind: "code" },
    ],
  },
];

/** The value as the input should show it: decimals without trailing zeros. */
export function inputValue(invoice: InvoiceDetail, column: HeaderColumn): string {
  const value = invoice[column];
  if (value === null || value === undefined) return "";
  return trimDecimal(String(value));
}

export function trimDecimal(value: string): string {
  return /^-?\d+\.\d+$/.test(value) ? value.replace(/\.?0+$/, "") : value;
}

export const EXPENSE_CATEGORIES = ["shipping", "repairs", "utilities", "cleaning", "other"] as const;