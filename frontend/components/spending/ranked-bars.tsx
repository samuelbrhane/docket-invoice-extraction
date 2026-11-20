import { money } from "@/lib/format";

export type Row = { key: string; label: string; value: string; note?: string };

/** A ranked list where each row's bar shows its share of the largest. */
export function RankedBars({ rows }: { rows: Row[] }) {
  const max = Math.max(...rows.map((row) => Number(row.value)), 1);
  if (rows.length === 0) return <p className="text-ink-soft">Nothing yet.</p>;

  return (
    <ul className="space-y-3.5">
      {rows.map((row) => (
        <li key={row.key} title={`${row.label}: ${money(row.value)}`}>
          <div className="flex items-baseline justify-between gap-3 text-[15px]">
            <span className="truncate">
              {row.label}
              {row.note && <span className="ml-2 text-sm text-ink-soft">{row.note}</span>}
            </span>
            <span className="figures shrink-0 font-bold">{money(row.value)}</span>
          </div>
          <div className="mt-1.5 h-2 rounded-full bg-rule/60">
            <div className="h-full rounded-full bg-ink/75" style={{ width: `${(Number(row.value) / max) * 100}%` }} />
          </div>
        </li>
      ))}
    </ul>
  );
}