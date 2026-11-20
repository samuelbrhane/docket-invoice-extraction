import type { InvoiceDetail, PartialInvoice } from "@/lib/api";

/** undefined means not read yet, null means not on the document. */
export type Value = string | null | undefined;

export type LineView = {
  description: Value;
  quantity: Value;
  unit: Value;
  unitPrice: Value;
  lineTotal: Value;
};

export type InvoiceView = {
  supplierName: Value;
  supplierVat: Value;
  supplierAddress: Value;
  number: Value;
  issueDate: Value;
  dueDate: Value;
  currency: Value;
  subtotal: Value;
  vatRate: Value;
  vatAmount: Value;
  total: Value;
  terms: Value;
  iban: Value;
  lines: LineView[];
};

export const EMPTY_VIEW: InvoiceView = {
  supplierName: undefined,
  supplierVat: undefined,
  supplierAddress: undefined,
  number: undefined,
  issueDate: undefined,
  dueDate: undefined,
  currency: undefined,
  subtotal: undefined,
  vatRate: undefined,
  vatAmount: undefined,
  total: undefined,
  terms: undefined,
  iban: undefined,
  lines: [],
};

function read(value: string | number | null | undefined): Value {
  if (value === undefined) return undefined;
  if (value === null) return null;
  return String(value);
}

export function fromPartial(partial: PartialInvoice): InvoiceView {
  const { supplier, invoice, totals, payment } = partial;
  return {
    supplierName: read(supplier?.name),
    supplierVat: read(supplier?.vat),
    supplierAddress: read(supplier?.address),
    number: read(invoice?.number),
    issueDate: read(invoice?.issue_date),
    dueDate: read(invoice?.due_date),
    currency: read(invoice?.currency),
    subtotal: read(totals?.subtotal),
    vatRate: read(totals?.vat_rate),
    vatAmount: read(totals?.vat_amount),
    total: read(totals?.total),
    terms: read(payment?.terms),
    iban: read(payment?.iban),
    lines: (partial.lines ?? []).map((line) => ({
      description: read(line.description),
      quantity: read(line.quantity),
      unit: read(line.unit),
      unitPrice: read(line.unit_price),
      lineTotal: read(line.line_total),
    })),
  };
}

export function fromDetail(detail: InvoiceDetail): InvoiceView {
  return {
    supplierName: detail.supplier_name,
    supplierVat: detail.supplier_vat,
    supplierAddress: detail.supplier_address,
    number: detail.invoice_number,
    issueDate: detail.issue_date,
    dueDate: detail.due_date,
    currency: detail.currency,
    subtotal: detail.subtotal,
    vatRate: detail.vat_rate,
    vatAmount: detail.vat_amount,
    total: detail.total,
    terms: detail.payment_terms,
    iban: detail.iban,
    lines: detail.lines.map((line) => ({
      description: line.description,
      quantity: line.quantity,
      unit: line.unit,
      unitPrice: line.unit_price,
      lineTotal: line.line_total,
    })),
  };
}