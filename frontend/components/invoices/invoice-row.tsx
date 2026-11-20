import Link from "next/link";

import { Stamp } from "@/components/ui";
import type { InvoiceSummary } from "@/lib/api";
import { money, shortDate, usd } from "@/lib/format";

export const STATUS_STAMP = {
  needs_review: { label: "Needs review", tone: "stamp" as const },
  ready: { label: "Ready", tone: "ink" as const },
  approved: { label: "Approved", tone: "approved" as const },
  rejected: { label: "Rejected", tone: "stamp" as const },
};

function Attention({ invoice }: { invoice: InvoiceSummary }) {
  const yellow = invoice.open_flags - invoice.open_red_flags;
  if (invoice.status === "approved" || invoice.status === "rejected") return <span className="text-ink-soft">—</span>;
  if (!invoice.open_flags) return <span className="text-sm text-ink-soft">All clear</span>;
  return (
    <span className="flex items-center gap-2 text-sm">
      {invoice.open_red_flags > 0 && <span className="marker-red figures font-bold">{invoice.open_red_flags} red</span>}
      {yellow > 0 && <span className="marker figures">{yellow} yellow</span>}
    </span>
  );
}

export function InvoiceRow({ invoice }: { invoice: InvoiceSummary }) {
  const status = STATUS_STAMP[invoice.status];
  const href = `/app/invoices/${invoice.id}`;

  return (
    <tr className="group relative border-t border-rule transition-colors hover:bg-ledger/60">
      <td className="py-3.5 pl-5 pr-3">
        {/* The link covers the whole row, so any click opens the review */}
        <Link href={href} className="font-bold after:absolute after:inset-0">
          {invoice.supplier_name ?? "Unknown supplier"}
        </Link>
        <p className="figures mt-0.5 text-sm text-ink-soft">{invoice.invoice_number ?? invoice.filename}</p>
      </td>
      <td className="px-3 py-3.5 text-[15px] whitespace-nowrap">{shortDate(invoice.issue_date)}</td>
      <td className="figures px-3 py-3.5 text-right font-bold whitespace-nowrap">{money(invoice.total, invoice.currency)}</td>
      <td className="px-3 py-3.5">
        <Stamp tone={status.tone}>{status.label}</Stamp>
      </td>
      <td className="px-3 py-3.5">
        <Attention invoice={invoice} />
      </td>
      <td className="figures py-3.5 pr-5 pl-3 text-right text-sm text-ink-soft">
        {invoice.cost_usd === null ? "Example" : usd(invoice.cost_usd)}
      </td>
    </tr>
  );
}

/** The same invoice as a card, for narrow screens. */
export function InvoiceCard({ invoice }: { invoice: InvoiceSummary }) {
  const status = STATUS_STAMP[invoice.status];
  return (
    <Link href={`/app/invoices/${invoice.id}`} className="block rounded-lg border border-rule bg-sheet p-4 active:bg-ledger">
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <p className="truncate font-bold">{invoice.supplier_name ?? "Unknown supplier"}</p>
          <p className="figures text-sm text-ink-soft">{invoice.invoice_number ?? invoice.filename}</p>
        </div>
        <Stamp tone={status.tone}>{status.label}</Stamp>
      </div>
      <div className="mt-3 flex items-end justify-between gap-3">
        <div className="text-sm text-ink-soft">
          {shortDate(invoice.issue_date)}
          <div className="mt-1">
            <Attention invoice={invoice} />
          </div>
        </div>
        <p className="figures text-lg font-bold">{money(invoice.total, invoice.currency)}</p>
      </div>
    </Link>
  );
}