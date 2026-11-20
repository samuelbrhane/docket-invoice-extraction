import { Button, ButtonLink, Stamp } from "@/components/ui";
import type { InvoiceDetail } from "@/lib/api";
import { usd } from "@/lib/format";

export function ResultBanner({ invoice, onAnother }: { invoice: InvoiceDetail; onAnother: () => void }) {
  const red = invoice.open_red_flags;
  const yellow = invoice.open_flags - red;
  const seconds = invoice.extraction?.duration_ms ? (invoice.extraction.duration_ms / 1000).toFixed(1) : null;

  let title = "Everything checks out";
  if (red) title = `${red} ${red === 1 ? "field needs" : "fields need"} a look before approval`;
  else if (yellow) title = `Ready, with ${yellow} ${yellow === 1 ? "warning" : "warnings"} to glance at`;

  return (
    <div className="animate-rise rounded-xl border border-rule bg-sheet p-5">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            {red ? <Stamp>Needs review</Stamp> : <Stamp tone="approved">Ready</Stamp>}
            {invoice.duplicate_of && <Stamp tilt={2}>Possible duplicate</Stamp>}
          </div>
          <p className="mt-3 font-display text-xl">{title}</p>
          <p className="mt-1 text-sm text-ink-soft">
            Read in {seconds ?? "a few"} seconds for {usd(invoice.cost_usd)}
            {invoice.extraction && `, ${invoice.extraction.input_tokens + invoice.extraction.output_tokens} tokens`}
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="secondary" onClick={onAnother}>
            Process another
          </Button>
          <ButtonLink href={`/app/invoices/${invoice.id}`}>Open review</ButtonLink>
        </div>
      </div>
    </div>
  );
}