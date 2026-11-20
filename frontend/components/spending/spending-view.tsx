"use client";

import { useCallback, useEffect, useState } from "react";

import { getSpending, type Spending } from "@/lib/api";
import { useOnChanged } from "@/lib/events";
import { money } from "@/lib/format";

import { categoryLabel } from "./labels";
import { MonthBars } from "./month-bars";
import { RankedBars } from "./ranked-bars";

function Panel({ title, note, children, className = "" }: { title: string; note?: string; children: React.ReactNode; className?: string }) {
  return (
    <section className={`rounded-xl border border-rule bg-sheet p-6 ${className}`}>
      <div className="mb-5 flex flex-wrap items-baseline justify-between gap-2">
        <h2 className="font-display text-xl">{title}</h2>
        {note && <p className="text-sm text-ink-soft">{note}</p>}
      </div>
      {children}
    </section>
  );
}

export function SpendingView() {
  const [spending, setSpending] = useState<Spending | null>(null);

  const load = useCallback(() => {
    getSpending().then(setSpending).catch(() => setSpending(null));
  }, []);
  useEffect(load, [load]);
  useOnChanged(load);

  if (!spending) {
    return (
      <div className="space-y-4">
        <div className="h-24 w-80 animate-shimmer rounded-lg bg-rule/50" />
        <div className="h-80 animate-shimmer rounded-xl bg-rule/50" />
      </div>
    );
  }

  return (
    <div>
      <h1 className="font-display text-4xl leading-tight">Spending</h1>
      <p className="mt-2 text-ink-soft">From approved invoices, before VAT.</p>
      <p className="figures mt-5 text-5xl font-bold">{money(spending.total, spending.currency)}</p>

      <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-[minmax(0,3fr)_minmax(0,2fr)]">
        <Panel title="By month" note="Hover or tap a bar to see what it was spent on" className="self-start">
          <MonthBars months={spending.months} />
        </Panel>
        <div className="space-y-6">
          <Panel title="By category">
            <RankedBars
              rows={spending.categories.map((c) => ({ key: c.category, label: categoryLabel(c.category), value: c.total }))}
            />
          </Panel>
          <Panel title="By supplier">
            <RankedBars
              rows={spending.suppliers.map((s) => ({
                key: s.name,
                label: s.name,
                value: s.total,
                note: `${s.invoice_count} ${s.invoice_count === 1 ? "invoice" : "invoices"}`,
              }))}
            />
          </Panel>
        </div>
      </div>
    </div>
  );
}