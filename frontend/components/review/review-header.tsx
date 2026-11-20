import Link from "next/link";

import { Stamp } from "@/components/ui";
import { invoiceExportUrl, type InvoiceDetail } from "@/lib/api";
import { money, shortDate, usd } from "@/lib/format";

import type { SaveState } from "./use-invoice";

const STATUS = {
  needs_review: { label: "Needs review", tone: "stamp" as const },
  ready: { label: "Ready to approve", tone: "ink" as const },
  approved: { label: "Approved", tone: "approved" as const },
  rejected: { label: "Rejected", tone: "stamp" as const },
};

const SAVE_TEXT: Record<SaveState, string> = { idle: "", saving: "Saving…", saved: "Saved, checks re-run", error: "Not saved" };

export function ReviewHeader({ invoice, saveState }: { invoice: InvoiceDetail; saveState: SaveState }) {
  const status = STATUS[invoice.status];
  const done = invoice.status === "approved" || invoice.status === "rejected";

  return (
    <div className="flex flex-wrap items-end justify-between gap-4">
      <div className="min-w-0">
        <Link href="/app/invoices" className="text-sm text-ink-soft hover:text-ink">
          All invoices
        </Link>
        <div className="mt-2 flex flex-wrap items-center gap-3">
          <h1 className="font-display text-3xl leading-tight sm:text-4xl">{invoice.supplier_name ?? "Unknown supplier"}</h1>
          <Stamp tone={status.tone}>{status.label}</Stamp>
        </div>
        <p className="mt-2 text-ink-soft">
          <span className="figures text-ink">{invoice.invoice_number ?? "No number"}</span>
          {" "}issued {shortDate(invoice.issue_date)}, total{" "}
          <span className="figures font-bold text-ink">{money(invoice.total, invoice.currency)}</span>
          {invoice.extraction && <>, read for {usd(invoice.cost_usd)}</>}
        </p>
      </div>
      <div className="flex items-center gap-4 text-sm">
        <span className={saveState === "error" ? "font-bold text-stamp" : "text-ink-soft"} aria-live="polite">
          {SAVE_TEXT[saveState]}
        </span>
        {done && (
          <>
            <a href={invoiceExportUrl(invoice.id, "json")} className="font-bold underline underline-offset-4">
              Export JSON
            </a>
            <a href={invoiceExportUrl(invoice.id, "csv")} className="font-bold underline underline-offset-4">
              Export CSV
            </a>
          </>
        )}
      </div>
    </div>
  );
}