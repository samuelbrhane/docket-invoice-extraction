import { ButtonLink } from "@/components/ui";

export function ClosingCta() {
  return (
    <section className="border-t border-rule">
      <div className="ruled mx-auto max-w-6xl px-6 py-20 text-center">
        <h2 className="mx-auto max-w-2xl font-display text-4xl leading-tight">Try it on the invoice with the wrong subtotal</h2>
        <p className="mx-auto mt-4 max-w-xl text-lg text-ink-soft">
          Nine sample invoices are ready, each one testing something: a phone photo, an Italian invoice, a duplicate, a
          price jump. Or drop in your own.
        </p>
        <ButtonLink href="/app" className="mt-8 px-6 py-3 text-base">
          Open Docket
        </ButtonLink>
      </div>
    </section>
  );
}