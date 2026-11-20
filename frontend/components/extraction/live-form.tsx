import type { Flag } from "@/lib/api";
import { highlightFor, markerClass } from "@/lib/flags";
import { money, percent, quantity, shortDate, unitPrice } from "@/lib/format";
import type { InvoiceView, Value } from "@/lib/invoice-view";

import { Field } from "./field";

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section className="border-t border-rule pt-5 first:border-t-0 first:pt-0">
      <h3 className="mb-3 font-display text-lg">{title}</h3>
      {children}
    </section>
  );
}

function Cell({ value, format, path, flags, align = "right" }: { value: Value; format: (v: string) => string; path: string; flags: Map<string, Flag[]>; align?: "left" | "right" }) {
  if (value === undefined) return <span className={`inline-block h-3 w-12 animate-shimmer rounded-sm bg-rule ${align === "right" ? "ml-auto" : ""}`} />;
  if (value === null) return <span className="text-ink-soft">—</span>;
  return <span key={value} className={`figures animate-ink-in ${markerClass(highlightFor(flags, path))}`}>{format(value)}</span>;
}

export function LiveForm({ view, flags }: { view: InvoiceView; flags: Map<string, Flag[]> }) {
  const currency = view.currency ?? "EUR";
  const asMoney = (v: string) => money(v, currency);
  const lineReasons = [...flags.entries()].filter(([path]) => path.startsWith("lines[")).flatMap(([, list]) => list);

  return (
    <div className="space-y-6">
      <Section title="Supplier">
        <dl className="grid grid-cols-2 gap-x-6 gap-y-4">
          <Field label="Name" value={view.supplierName} path="supplier.name" flags={flags} />
          <Field label="VAT number" value={view.supplierVat} path="supplier.vat" flags={flags} figures />
          <Field label="Address" value={view.supplierAddress} path="supplier.address" flags={flags} className="col-span-2" />
        </dl>
      </Section>

      <Section title="Invoice">
        <dl className="grid grid-cols-4 gap-x-6 gap-y-4">
          <Field label="Number" value={view.number} path="invoice.number" flags={flags} figures className="col-span-2" />
          <Field label="Currency" value={view.currency} path="invoice.currency" flags={flags} figures className="col-span-2" />
          <Field label="Issued" value={view.issueDate} path="invoice.issue_date" flags={flags} format={shortDate} className="col-span-2" />
          <Field label="Due" value={view.dueDate} path="invoice.due_date" flags={flags} format={shortDate} className="col-span-2" />
        </dl>
      </Section>

      <Section title="Line items">
        <table className="w-full text-[15px]">
          <thead>
            <tr className="text-left text-[13px] text-ink-soft">
              <th className="pb-2 font-normal">Description</th>
              <th className="pb-2 text-right font-normal">Qty</th>
              <th className="pb-2 text-right font-normal">Unit price</th>
              <th className="pb-2 text-right font-normal">Total</th>
            </tr>
          </thead>
          <tbody>
            {view.lines.map((line, i) => (
              <tr key={i} className="animate-rise border-t border-rule/70 align-top">
                <td className="py-2 pr-3">{line.description ?? <span className="inline-block h-3 w-32 animate-shimmer rounded-sm bg-rule" />}</td>
                <td className="py-2 text-right whitespace-nowrap">
                  <Cell value={line.quantity} format={quantity} path={`lines[${i}].quantity`} flags={flags} />
                  {line.unit && <span className="ml-1 text-sm text-ink-soft">{line.unit}</span>}
                </td>
                <td className="py-2 pl-3 text-right"><Cell value={line.unitPrice} format={unitPrice} path={`lines[${i}].unit_price`} flags={flags} /></td>
                <td className="py-2 pl-3 text-right"><Cell value={line.lineTotal} format={asMoney} path={`lines[${i}].line_total`} flags={flags} /></td>
              </tr>
            ))}
            {view.lines.length === 0 && (
              <tr className="border-t border-rule/70">
                <td colSpan={4} className="py-3"><span className="block h-3 w-2/3 animate-shimmer rounded-sm bg-rule" /></td>
              </tr>
            )}
          </tbody>
        </table>
        {lineReasons.map((flag) => (
          <p key={flag.id} className={`mt-2 animate-rise text-[13px] ${flag.level === "low" ? "text-stamp" : "text-ink-soft"}`}>
            {flag.reason}
          </p>
        ))}
      </Section>

      <Section title="Totals">
        <dl className="grid grid-cols-4 gap-x-6 gap-y-4">
          <Field label="Subtotal" value={view.subtotal} path="totals.subtotal" flags={flags} format={asMoney} figures className="col-span-2" />
          <Field label="VAT rate" value={view.vatRate} path="totals.vat_rate" flags={flags} format={percent} figures />
          <Field label="VAT" value={view.vatAmount} path="totals.vat_amount" flags={flags} format={asMoney} figures />
          <Field label="Total" value={view.total} path="totals.total" flags={flags} format={asMoney} figures className="col-span-4 [&_dd]:text-2xl [&_dd]:font-bold" />
        </dl>
      </Section>

      <Section title="Payment">
        <dl className="grid grid-cols-2 gap-x-6 gap-y-4">
          <Field label="Terms" value={view.terms} path="payment.terms" flags={flags} />
          <Field label="IBAN" value={view.iban} path="payment.iban" flags={flags} figures />
        </dl>
      </Section>
    </div>
  );
}