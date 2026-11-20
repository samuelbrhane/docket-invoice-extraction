import type { InvoiceStatus } from "@/lib/api";

export type Filter = "all" | InvoiceStatus;

export const FILTERS: { key: Filter; label: string }[] = [
  { key: "all", label: "All" },
  { key: "needs_review", label: "Needs review" },
  { key: "ready", label: "Ready" },
  { key: "approved", label: "Approved" },
  { key: "rejected", label: "Rejected" },
];

type Props = { value: Filter; counts: Record<Filter, number>; onChange: (filter: Filter) => void };

export function StatusFilter({ value, counts, onChange }: Props) {
  return (
    <div role="tablist" aria-label="Filter by status" className="flex gap-1 overflow-x-auto rounded-lg border border-rule bg-sheet p-1">
      {FILTERS.map((filter) => {
        const active = filter.key === value;
        return (
          <button
            key={filter.key}
            role="tab"
            aria-selected={active}
            onClick={() => onChange(filter.key)}
            className={`flex shrink-0 items-center gap-2 rounded-md px-3 py-1.5 text-sm transition-colors ${
              active ? "bg-ink font-bold text-sheet" : "text-ink-soft hover:text-ink"
            }`}
          >
            {filter.label}
            <span className={`figures text-xs ${active ? "text-sheet/70" : "text-ink-soft"}`}>{counts[filter.key]}</span>
          </button>
        );
      })}
    </div>
  );
}