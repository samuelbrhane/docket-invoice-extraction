import { GrowBar, Reveal } from "@/components/motion";

const STEPS = [
  {
    title: "Drop in an invoice",
    body: "A PDF from email or a photo taken on a phone, in English or Italian. Docket stores the original next to everything read from it.",
  },
  {
    title: "Watch it being read",
    body: "Supplier, dates, every line item and the totals fill in as the AI writes them, in a fixed shape that always matches the form.",
  },
  {
    title: "Fix what's flagged",
    body: "Code checks every value. Anything doubtful is highlighted with the reason, and you either correct it or confirm it's right.",
  },
  {
    title: "Approve it into the books",
    body: "Stock lines raise inventory at the new price, services land in spending, and nothing changes until you click approve.",
  },
];

export function HowItWorks() {
  return (
    <section id="how-it-works" className="scroll-mt-20 border-t border-rule bg-sheet/60">
      <div className="mx-auto max-w-6xl px-6 py-20">
        <h2 className="max-w-2xl font-display text-4xl leading-tight">From the inbox to the stock count in four steps</h2>
        <ol className="mt-12 grid gap-10 sm:grid-cols-2 lg:grid-cols-4 lg:gap-8">
          {STEPS.map((step, i) => (
            <li key={step.title}>
              <Reveal delay={i * 150}>
                <span className="figures text-sm font-bold text-ink-soft">Step {i + 1}</span>
                <div className="mt-3 h-0.5 bg-rule">
                  <GrowBar share={((i + 1) / STEPS.length) * 100} delay={300 + i * 150} className="bg-ink" />
                </div>
                <h3 className="mt-5 font-display text-xl">{step.title}</h3>
                <p className="mt-2 text-ink-soft">{step.body}</p>
              </Reveal>
            </li>
          ))}
        </ol>
      </div>
    </section>
  );
}