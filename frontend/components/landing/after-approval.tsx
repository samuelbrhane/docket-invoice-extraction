const BARS = [
  { label: "Stock purchases", value: "€2,747.00", share: 100 },
  { label: "Utilities", value: "€538.35", share: 20 },
  { label: "Repairs", value: "€563.50", share: 21 },
  { label: "Shipping", value: "€170.00", share: 6 },
];

export function AfterApproval() {
  return (
    <section id="after-approval" className="scroll-mt-20 border-t border-rule bg-sheet/60">
      <div className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="max-w-2xl font-display text-4xl leading-tight">An approved invoice updates the books by itself</h2>
        <p className="mt-4 max-w-2xl text-lg text-ink-soft">
          Each line is matched to a stock item or an expense category while it&apos;s read. Approving it does the
          bookkeeping nobody wants to do by hand.
        </p>

        <div className="mt-12 grid gap-6 md:grid-cols-2">
          <div className="rounded-xl border border-rule bg-sheet p-6">
            <h3 className="font-display text-xl">Inventory</h3>
            <div className="mt-5 flex items-end justify-between gap-3 border-b border-rule pb-4">
              <div>
                <p className="font-bold">Ethiopia Yirgacheffe green beans</p>
                <p className="figures text-sm text-ink-soft">GB-ETH</p>
              </div>
              <p className="figures text-right">
                <span className="text-sm text-ink-soft line-through">120 kg</span>
                <span className="ml-2 text-xl font-bold">240 kg</span>
              </p>
            </div>
            <p className="mt-4 text-[15px]">
              <span className="figures font-bold text-approved">+120 kg</span>
              <span className="text-ink-soft"> at </span>
              <span className="figures marker">8.05</span>
              <span className="text-ink-soft"> from Altura Green Coffee AGC-2026-0496</span>
            </p>
            <p className="mt-2 text-sm text-ink-soft">The last price paid updates too, so the next price jump is caught.</p>
          </div>

          <div className="rounded-xl border border-rule bg-sheet p-6">
            <h3 className="font-display text-xl">Spending</h3>
            <ul className="mt-5 space-y-3">
              {BARS.map((bar) => (
                <li key={bar.label}>
                  <div className="flex justify-between text-[15px]">
                    <span>{bar.label}</span>
                    <span className="figures font-bold">{bar.value}</span>
                  </div>
                  <div className="mt-1.5 h-2 rounded-full bg-rule/60">
                    <div className="h-full rounded-full bg-ink/75" style={{ width: `${bar.share}%` }} />
                  </div>
                </li>
              ))}
            </ul>
            <p className="mt-4 text-sm text-ink-soft">By month, category and supplier, with CSV and JSON exports for accounting software.</p>
          </div>
        </div>
      </div>
    </section>
  );
}