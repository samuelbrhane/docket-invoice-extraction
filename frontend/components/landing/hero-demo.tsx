"use client";

import { useEffect, useState } from "react";

const LINES = [
  { description: "Grinder burr set, 98 mm", qty: "1", total: "€118.00" },
  { description: "Technician labour", qty: "2 h", total: "€90.00" },
  { description: "Call-out fee", qty: "1", total: "€35.00" },
];

// Each step reveals one more value. The last steps run the checks and stamp the result.
const FIELD_STEPS = 9;
const CHECK_STEP = FIELD_STEPS + 1;
const STAMP_STEP = FIELD_STEPS + 2;
const LAST_STEP = FIELD_STEPS + 6;

function Value({ show, children, className = "" }: { show: boolean; children: React.ReactNode; className?: string }) {
  return show ? (
    <span className={`animate-ink-in ${className}`}>{children}</span>
  ) : (
    <span className="inline-block h-3 w-16 translate-y-0.5 animate-shimmer rounded-sm bg-rule" />
  );
}

/** The hero loop: a paper invoice is read top to bottom while its values fill a form, then a check catches the subtotal. */
export function HeroDemo() {
  const [step, setStep] = useState(0);

  useEffect(() => {
    // With reduced motion, jump straight to the finished state instead of looping
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      const timer = window.setTimeout(() => setStep(LAST_STEP), 0);
      return () => window.clearTimeout(timer);
    }
    const timer = window.setInterval(() => setStep((s) => (s >= LAST_STEP ? 0 : s + 1)), 700);
    return () => window.clearInterval(timer);
  }, []);

  const scan = Math.min(step, FIELD_STEPS) / FIELD_STEPS;
  const checked = step >= CHECK_STEP;

  return (
    <div className="relative grid gap-4 sm:grid-cols-[0.9fr_1fr]" aria-hidden="true">
      {/* The paper invoice */}
      <div className="relative flex flex-col overflow-hidden rounded-md border border-rule bg-white p-5 font-[family-name:var(--font-figures)] text-[11px] leading-relaxed text-ink shadow-[0_24px_50px_-30px_rgb(28_42_66/0.6)] sm:rotate-[-1.5deg]">
        <p className="text-sm font-bold">BRUNO ESPRESSO SERVICE</p>
        <p className="text-ink-soft">Corso Mazzini 140, Cosenza</p>
        <div className="my-3 border-t border-dashed border-ink/40" />
        <div className="flex justify-between">
          <span className="font-bold">INVOICE BES-0977</span>
          <span>24/10/2026</span>
        </div>
        <div className="my-3 border-t border-dashed border-ink/40" />
        {LINES.map((line) => (
          <div key={line.description} className="flex justify-between gap-2">
            <span className="truncate">{line.description}</span>
            <span>{line.total.replace("€", "")}</span>
          </div>
        ))}
        <div className="my-3 border-t border-dashed border-ink/40" />
        <div className="flex justify-between">
          <span>SUBTOTAL</span>
          <span>€263.00</span>
        </div>
        <div className="flex justify-between">
          <span>IVA 22%</span>
          <span>€57.86</span>
        </div>
        <div className="flex justify-between text-[13px] font-bold">
          <span>TOTAL</span>
          <span>€320.86</span>
        </div>
        <div className="mt-auto pt-4 text-ink-soft">
          <p>PAYMENT: due on receipt, 14 days</p>
          <p>Grazie! Keep the roaster running.</p>
        </div>
        {/* The reading line moves down the page */}
        {step <= FIELD_STEPS && (
          <div
            className="pointer-events-none absolute inset-x-0 h-10 bg-gradient-to-b from-transparent via-marker/45 to-transparent transition-[top] duration-700 ease-linear"
            style={{ top: `calc(${scan * 100}% - 1.25rem)` }}
          />
        )}
      </div>

      {/* The form it fills */}
      <div className="relative rounded-xl border border-rule bg-sheet p-5 text-[13px] shadow-[0_24px_50px_-34px_rgb(28_42_66/0.55)]">
        <dl className="grid grid-cols-2 gap-x-4 gap-y-3">
          <div className="col-span-2">
            <dt className="text-[11px] text-ink-soft">Supplier</dt>
            <dd className="font-bold">
              <Value show={step >= 1}>Bruno Espresso Service</Value>
            </dd>
          </div>
          <div>
            <dt className="text-[11px] text-ink-soft">Invoice</dt>
            <dd className="figures">
              <Value show={step >= 2}>BES-0977</Value>
            </dd>
          </div>
          <div>
            <dt className="text-[11px] text-ink-soft">Issued</dt>
            <dd>
              <Value show={step >= 3}>24 Oct 2026</Value>
            </dd>
          </div>
        </dl>
        <div className="mt-4 space-y-1.5 border-t border-rule pt-3">
          {LINES.map((line, i) => (
            <div key={line.description} className="flex justify-between gap-2">
              <span className="truncate">
                <Value show={step >= 4 + i}>{line.description}</Value>
              </span>
              <span className="figures shrink-0">
                <Value show={step >= 4 + i}>{line.total}</Value>
              </span>
            </div>
          ))}
        </div>
        <div className="mt-3 space-y-1.5 border-t border-rule pt-3">
          <div className="flex justify-between">
            <span className="text-ink-soft">Subtotal</span>
            <span className="figures">
              <Value show={step >= 7} className={checked ? "marker-red animate-marker-swipe" : ""}>
                €263.00
              </Value>
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-ink-soft">VAT 22%</span>
            <span className="figures">
              <Value show={step >= 8}>€57.86</Value>
            </span>
          </div>
          <div className="flex justify-between text-[15px] font-bold">
            <span>Total</span>
            <span className="figures">
              <Value show={step >= 9}>€320.86</Value>
            </span>
          </div>
        </div>
        <p className={`mt-3 min-h-9 text-[12px] leading-snug text-stamp transition-opacity ${checked ? "opacity-100" : "opacity-0"}`}>
          Line totals add up to €243.00, but the subtotal says €263.00
        </p>
        {step >= STAMP_STEP && (
          <span className="absolute -top-3 right-4 rotate-[-6deg] animate-rise rounded-[4px] border-2 border-stamp bg-sheet px-2 py-0.5 text-xs font-bold text-stamp">
            Needs review
          </span>
        )}
      </div>
    </div>
  );
}