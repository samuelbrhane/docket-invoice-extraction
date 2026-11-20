"use client";

import { useCallback, useEffect, useMemo, useState } from "react";

import { ButtonLink } from "@/components/ui";
import { exportUrl, listInvoices, type InvoiceSummary } from "@/lib/api";
import { useOnChanged } from "@/lib/events";

import { InvoiceCard, InvoiceRow } from "./invoice-row";
import { ResetDemo } from "./reset-demo";
import { FILTERS, StatusFilter, type Filter } from "./status-filter";

export function InvoiceList() {
  const [invoices, setInvoices] = useState<InvoiceSummary[] | null>(null);
  const [error, setError] = useState(false);
  const [filter, setFilter] = useState<Filter>("all");

  const load = useCallback(() => {
    listInvoices().then(setInvoices).catch(() => setError(true));
  }, []);
  useEffect(load, [load]);
  useOnChanged(load);

  const counts = useMemo(() => {
    const result = Object.fromEntries(FILTERS.map((f) => [f.key, 0])) as Record<Filter, number>;
    for (const invoice of invoices ?? []) {
      result.all += 1;
      result[invoice.status] += 1;
    }
    return result;
  }, [invoices]);

  const shown = (invoices ?? []).filter((invoice) => filter === "all" || invoice.status === filter);
  const waiting = counts.needs_review + counts.ready;

  return (
    <div>
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <h1 className="font-display text-4xl leading-tight">Invoices</h1>
          <p className="mt-2 text-ink-soft">
            {invoices === null
              ? "Loading…"
              : waiting
                ? `${waiting} waiting for review, ${counts.approved} approved`
                : `Nothing waiting for review, ${counts.approved} approved`}
          </p>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <ResetDemo />
          <a href={exportUrl("csv")} className="rounded-lg border border-ink/25 bg-sheet px-4 py-2.5 text-[15px] font-bold hover:border-ink/60">
            Export CSV
          </a>
          <a href={exportUrl("json")} className="rounded-lg border border-ink/25 bg-sheet px-4 py-2.5 text-[15px] font-bold hover:border-ink/60">
            Export JSON
          </a>
          <ButtonLink href="/app">Process an invoice</ButtonLink>
        </div>
      </div>

      <div className="mt-8">
        <StatusFilter value={filter} counts={counts} onChange={setFilter} />
      </div>

      {error && <p className="mt-6 font-bold text-stamp">The invoices couldn&apos;t be loaded. Is the API running?</p>}

      {invoices === null && !error ? (
        <div className="mt-4 space-y-2">
          {Array.from({ length: 4 }, (_, i) => (
            <div key={i} className="h-16 animate-shimmer rounded-lg bg-rule/50" />
          ))}
        </div>
      ) : shown.length === 0 ? (
        <div className="mt-4 rounded-xl border border-dashed border-ink/25 bg-sheet/70 px-6 py-12 text-center">
          <p className="font-display text-xl">No invoices here</p>
          <p className="mt-2 text-ink-soft">Process an invoice and it will show up in this list.</p>
        </div>
      ) : (
        <>
          <div className="mt-4 hidden overflow-hidden rounded-xl border border-rule bg-sheet md:block">
            <table className="w-full">
              <thead>
                <tr className="text-left text-[13px] text-ink-soft">
                  <th className="py-3 pl-5 pr-3 font-normal">Supplier</th>
                  <th className="px-3 py-3 font-normal">Issued</th>
                  <th className="px-3 py-3 text-right font-normal">Total</th>
                  <th className="px-3 py-3 font-normal">Status</th>
                  <th className="px-3 py-3 font-normal">Needs a look</th>
                  <th className="py-3 pr-5 pl-3 text-right font-normal">AI cost</th>
                </tr>
              </thead>
              <tbody>
                {shown.map((invoice) => (
                  <InvoiceRow key={invoice.id} invoice={invoice} />
                ))}
              </tbody>
            </table>
          </div>
          <div className="mt-4 space-y-2 md:hidden">
            {shown.map((invoice) => (
              <InvoiceCard key={invoice.id} invoice={invoice} />
            ))}
          </div>
        </>
      )}
      <p className="mt-4 text-sm text-ink-soft">Exports include approved invoices, one CSV row per line item.</p>
    </div>
  );
}