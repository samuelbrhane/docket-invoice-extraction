import { HealthCheck, StreamCheck } from "@/components/setup";

const SWATCHES = ["ledger", "sheet", "rule", "ink", "ink-soft", "stamp", "approved", "marker", "marker-red"];

export default function SetupPage() {
  return (
    <main className="mx-auto max-w-3xl px-6 py-16">
      <h1 className="font-display text-5xl">Docket</h1>
      <p className="mt-3 text-lg text-ink-soft">Invoice processing for Sila Roasting Co.</p>

      <section className="mt-10 rounded-lg border border-rule bg-sheet p-6">
        <HealthCheck />
      </section>

      <section className="mt-6 rounded-lg border border-rule bg-sheet p-6">
        <StreamCheck />
      </section>

      <section className="ruled mt-10 rounded-lg border border-rule bg-sheet px-6 py-[0.4rem] text-lg leading-8">
        <p>
          Supplier <span className="font-bold">Altura Green Coffee S.r.l.</span>
        </p>
        <p>
          Invoice <span className="figures">AGC-2026-0496</span>
        </p>
        <p>
          Unit price <span className="figures marker">8.05</span> was 6.80
        </p>
        <p>
          Subtotal <span className="figures marker-red">€263.00</span> lines add up to €243.00
        </p>
      </section>

      <section className="mt-10 grid grid-cols-3 gap-3">
        {SWATCHES.map((name) => (
          <div key={name} className="rounded-lg border border-rule bg-sheet p-3">
            <div className="h-10 rounded" style={{ background: `var(--color-${name})` }} />
            <p className="figures mt-2 text-sm">{name}</p>
          </div>
        ))}
      </section>
    </main>
  );
}