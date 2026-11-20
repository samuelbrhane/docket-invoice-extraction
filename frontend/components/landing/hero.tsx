import { ButtonLink } from "@/components/ui";

import { HeroDemo } from "./hero-demo";

export function Hero() {
  return (
    <section className="mx-auto grid max-w-6xl items-center gap-12 px-6 pt-16 pb-20 lg:grid-cols-[1fr_1.05fr] lg:pt-24 lg:pb-28">
      <div>
        <h1 className="font-display text-[2.6rem] leading-[1.08] sm:text-6xl">
          Supplier invoices, read and checked before anyone types a number.
        </h1>
        <p className="mt-6 max-w-xl text-lg text-ink-soft">
          Docket reads each PDF or phone photo while you watch, checks the math, the IBAN and the history, and only
          updates stock and spending once a person approves it.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <ButtonLink href="/app" className="px-5 py-3 text-base">
            Process a sample invoice
          </ButtonLink>
          <ButtonLink href="#how-it-works" variant="secondary" className="px-5 py-3 text-base">
            See how it works
          </ButtonLink>
        </div>
        <p className="mt-6 text-sm text-ink-soft">No sign-up. Your invoices stay private to your browser.</p>
      </div>
      <HeroDemo />
    </section>
  );
}