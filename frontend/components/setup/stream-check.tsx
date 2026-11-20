"use client";

import { useState } from "react";

import { ApiError, extractDocument, pickSample, type Stage } from "@/lib/api";

export function StreamCheck() {
  const [stages, setStages] = useState<Stage[]>([]);
  const [partials, setPartials] = useState(0);
  const [supplier, setSupplier] = useState<string | null>(null);
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [running, setRunning] = useState(false);

  async function run() {
    setStages([]);
    setPartials(0);
    setSupplier(null);
    setResult(null);
    setError(null);
    setRunning(true);
    try {
      const document = await pickSample("12-pulito-pro");
      await extractDocument(document.id, {
        onStage: (stage) => setStages((previous) => [...previous, stage]),
        onPartial: (partial) => {
          setPartials((count) => count + 1);
          if (partial.supplier?.name) setSupplier(partial.supplier.name);
        },
        onResult: (invoice) => setResult(`${invoice.status}, ${invoice.lines.length} lines, $${invoice.cost_usd}`),
        onError: setError,
      });
    } catch (caught) {
      setError(caught instanceof ApiError ? caught.message : String(caught));
    } finally {
      setRunning(false);
    }
  }

  return (
    <div className="space-y-2">
      <button
        onClick={run}
        disabled={running}
        className="rounded-md bg-ink px-4 py-2 font-bold text-sheet disabled:opacity-50"
      >
        {running ? "Extracting…" : "Run a test extraction (sample 12)"}
      </button>
      <p className="figures text-sm">Stages: {stages.join(" → ") || "none yet"}</p>
      <p className="figures text-sm">
        Partials: {partials} {supplier && `· supplier so far: ${supplier}`}
      </p>
      {result && <p className="font-bold text-approved">Result: {result}</p>}
      {error && <p className="font-bold text-stamp">{error}</p>}
    </div>
  );
}