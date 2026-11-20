import { Stamp } from "@/components/ui";
import type { Sample } from "@/lib/api";
import { money } from "@/lib/format";

/** A sample invoice drawn as a small paper slip with a perforated tear line. */
export function SampleCard({ sample, onPick, disabled }: { sample: Sample; onPick: () => void; disabled?: boolean }) {
  return (
    <button
      onClick={onPick}
      disabled={disabled}
      className="group flex h-full flex-col rounded-lg border border-rule bg-sheet text-left shadow-[0_1px_0_var(--color-rule),0_6px_14px_-10px_rgb(28_42_66/0.35)] transition-[border-color,transform] hover:-translate-y-0.5 hover:border-ink/40 disabled:pointer-events-none disabled:opacity-60"
    >
      <div className="px-4 pt-4 pb-3">
        <p className="line-clamp-1 font-bold">{sample.supplier}</p>
        <p className="figures mt-0.5 text-sm text-ink-soft">{sample.invoice_number}</p>
      </div>
      <div className="mx-3 border-t-2 border-dotted border-rule" />
      <div className="flex flex-1 items-end justify-between gap-2 px-4 pt-3 pb-4">
        <div className="flex flex-wrap gap-1.5">
          {sample.labels.map((label, i) => (
            <Stamp key={label} tilt={i % 2 ? 2 : -2}>
              {label}
            </Stamp>
          ))}
        </div>
        <p className="figures shrink-0 text-lg font-bold">{money(sample.total, sample.currency)}</p>
      </div>
    </button>
  );
}