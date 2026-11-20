const CHECKS = [
  {
    title: "Totals that don't add up",
    label: "Subtotal",
    value: "€263.00",
    tone: "marker-red",
    reason: "Line totals add up to €243.00, but the subtotal says €263.00",
    red: true,
  },
  {
    title: "A digit lost on a blurry photo",
    label: "IBAN",
    value: "IT34K05387428400000331892",
    tone: "marker-red",
    reason: "Italian IBANs have 27 characters, this one has 26",
    red: true,
  },
  {
    title: "The same bill sent twice",
    label: "Invoice number",
    value: "SL-55821",
    tone: "marker-red",
    reason: "Same supplier and number as an invoice already processed",
    red: true,
  },
  {
    title: "A supplier raising prices",
    label: "Unit price",
    value: "8.05 / kg",
    tone: "marker",
    reason: "Price up 18% since the last invoice (6.80 to 8.05)",
    red: false,
  },
];

export function Checks() {
  return (
    <section id="checks" className="scroll-mt-20">
      <div className="mx-auto max-w-6xl px-6 py-20">
        <div className="grid gap-6 lg:grid-cols-[1fr_1.4fr] lg:gap-16">
          <div>
            <h2 className="font-display text-4xl leading-tight">The AI makes the first guess. The rules decide what&apos;s trusted.</h2>
            <p className="mt-5 text-lg text-ink-soft">
              Every value goes through plain code checks after the AI reads it. Red needs a person before the invoice can
              be approved. Yellow is worth a glance.
            </p>
            <p className="mt-4 text-ink-soft">These four are real catches from the sample invoices you can try.</p>
          </div>
          <ul className="grid gap-4 sm:grid-cols-2">
            {CHECKS.map((check) => (
              <li key={check.title} className="rounded-xl border border-rule bg-sheet p-5">
                <h3 className="font-display text-lg">{check.title}</h3>
                <div className="mt-4 rounded-lg border border-rule/80 bg-ledger/50 p-3">
                  <p className="text-[12px] text-ink-soft">{check.label}</p>
                  <p className="figures mt-0.5 break-all text-[15px]">
                    <span className={check.tone}>{check.value}</span>
                  </p>
                </div>
                <p className={`mt-3 text-sm leading-snug ${check.red ? "text-stamp" : "text-ink-soft"}`}>{check.reason}</p>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}