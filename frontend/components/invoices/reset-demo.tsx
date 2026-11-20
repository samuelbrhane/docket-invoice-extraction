"use client";

import { useState } from "react";

import { Button } from "@/components/ui";
import { resetDemo } from "@/lib/api";
import { notifyChanged } from "@/lib/events";

/** Clears this visitor's invoices and stock, after a second click to confirm. */
export function ResetDemo() {
  const [confirming, setConfirming] = useState(false);
  const [busy, setBusy] = useState(false);

  async function reset() {
    setBusy(true);
    await resetDemo().catch(() => undefined);
    notifyChanged();
    setBusy(false);
    setConfirming(false);
  }

  if (!confirming) {
    return (
      <Button variant="quiet" onClick={() => setConfirming(true)}>
        Start over
      </Button>
    );
  }
  return (
    <span className="flex items-center gap-2 text-sm">
      <span className="text-ink-soft">Clear your invoices and stock?</span>
      <Button variant="secondary" disabled={busy} onClick={reset} className="border-stamp/50 text-stamp">
        {busy ? "Clearing…" : "Yes, start over"}
      </Button>
      <Button variant="quiet" onClick={() => setConfirming(false)}>
        Keep
      </Button>
    </span>
  );
}