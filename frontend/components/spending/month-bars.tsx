"use client";

import { useState } from "react";

import type { Spending } from "@/lib/api";
import { money } from "@/lib/format";

import { categoryLabel, monthLabel } from "./labels";

const HEIGHT = 320;

/** Net spending per month: one ink bar each, with the split by category on hover. */
export function MonthBars({ months }: { months: Spending["months"] }) {
  const [hovered, setHovered] = useState<string | null>(null);
  // Headroom above the tallest bar for its label and the tooltip
  const max = Math.max(...months.map((m) => Number(m.total)), 1) * 1.25;

  if (months.length === 0) return <p className="text-ink-soft">No approved invoices yet.</p>;

  return (
    <div className="relative">
      <div className="relative" style={{ height: HEIGHT }}>
        <div className="absolute inset-0 flex items-end justify-around gap-4 border-b border-ink/40">
          {months.map((month) => {
            const height = Math.max(4, (Number(month.total) / max) * HEIGHT);
            const active = hovered === month.month;
            return (
              <div
                key={month.month}
                className="relative flex h-full w-full max-w-24 cursor-default items-end justify-center"
                onMouseEnter={() => setHovered(month.month)}
                onMouseLeave={() => setHovered(null)}
                onFocus={() => setHovered(month.month)}
                onBlur={() => setHovered(null)}
                tabIndex={0}
                aria-label={`${monthLabel(month.month)}: ${money(month.total)}`}
              >
                <span className="figures absolute text-sm font-bold" style={{ bottom: height + 6 }}>
                  {money(month.total)}
                </span>
                <div
                  className={`w-full max-w-14 rounded-t-[4px] transition-colors ${active ? "bg-ink" : "bg-ink/75"}`}
                  style={{ height }}
                />
                {active && (
                  <div
                    role="tooltip"
                    className="absolute left-1/2 z-10 w-64 -translate-x-1/2 animate-rise rounded-lg border border-rule bg-sheet p-3 text-sm shadow-[0_12px_30px_-16px_rgb(28_42_66/0.5)]"
                    style={{ bottom: Math.min(height + 32, HEIGHT - 150) }}
                  >
                    <p className="font-bold">{monthLabel(month.month)}</p>
                    <ul className="mt-2 space-y-1">
                      {Object.entries(month.by_category)
                        .sort((a, b) => Number(b[1]) - Number(a[1]))
                        .map(([category, amount]) => (
                          <li key={category} className="flex justify-between gap-3">
                            <span className="whitespace-nowrap text-ink-soft">{categoryLabel(category)}</span>
                            <span className="figures">{money(amount)}</span>
                          </li>
                        ))}
                    </ul>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
      <div className="mt-2 flex justify-around gap-4">
        {months.map((month) => (
          <span key={month.month} className="w-full max-w-24 text-center text-sm text-ink-soft">
            {monthLabel(month.month)}
          </span>
        ))}
      </div>
    </div>
  );
}