import { Reveal } from "@/components/motion";

const POINTS = [
  { title: "One schema, end to end", body: "A Pydantic model drives the AI's structured output, the API and the TypeScript types, so the form can never drift from the data." },
  { title: "Streamed, not spinning", body: "Server-Sent Events carry each field to the screen as the model writes it, through a Next.js proxy on one domain." },
  { title: "Corrections are measured", body: "Every edit logs the AI's value next to yours, which turns into an accuracy figure and a cost per invoice." },
  { title: "Swappable pieces", body: "File storage, the model and the export are each behind one small module, ready for S3, another model or an ERP." },
];

export function UnderTheHood() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-20">
      <h2 className="font-display text-3xl">Under the hood</h2>
      <p className="mt-3 text-ink-soft">
        Next.js and TypeScript on the front, FastAPI and Postgres behind it, OpenAI structured outputs in the middle.
      </p>
      <dl className="mt-10 grid gap-x-10 gap-y-8 sm:grid-cols-2">
        {POINTS.map((point, i) => (
          <Reveal key={point.title} delay={i * 120} className="border-l-2 border-ink/20 pl-5">
            <dt className="font-bold">{point.title}</dt>
            <dd className="mt-1.5 text-ink-soft">{point.body}</dd>
          </Reveal>
        ))}
      </dl>
    </section>
  );
}