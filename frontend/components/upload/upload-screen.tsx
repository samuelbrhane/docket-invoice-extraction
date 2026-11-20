"use client";

import { useState } from "react";

import { ExtractionView } from "@/components/extraction";
import { ApiError, pickSample, uploadDocument, type DocumentInfo, type Sample } from "@/lib/api";

import { DropZone } from "./drop-zone";
import { SampleGrid } from "./sample-grid";

export function UploadScreen() {
  const [document, setDocument] = useState<DocumentInfo | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function start(create: () => Promise<DocumentInfo>) {
    setBusy(true);
    setError(null);
    try {
      setDocument(await create());
      window.scrollTo({ top: 0 });
    } catch (caught) {
      setError(caught instanceof ApiError ? caught.message : "Something went wrong. Please try again.");
    } finally {
      setBusy(false);
    }
  }

  if (document) return <ExtractionView key={document.id} document={document} onAnother={() => setDocument(null)} />;

  return (
    <div>
      <div className="max-w-2xl">
        <h1 className="font-display text-4xl leading-tight sm:text-5xl">Process a supplier invoice</h1>
        <p className="mt-4 text-lg text-ink-soft">
          Drop in a PDF or a phone photo, or pick one of Sila Roasting Co.&apos;s invoices below. The AI reads it while
          you watch, the checks catch what&apos;s off, and nothing is saved to stock until you approve it.
        </p>
      </div>

      {error && <p className="mt-6 rounded-lg border border-stamp/40 bg-sheet px-4 py-3 font-bold text-stamp">{error}</p>}

      <div className="mt-10 grid gap-10 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)]">
        <section>
          <h2 className="mb-4 font-display text-xl">Your own invoice</h2>
          <DropZone disabled={busy} onFile={(file) => start(() => uploadDocument(file))} />
        </section>
        <section>
          <div className="mb-4 flex items-baseline justify-between gap-4">
            <h2 className="font-display text-xl">Or try a sample</h2>
            <p className="text-sm text-ink-soft">Stamps show what each one tests</p>
          </div>
          <SampleGrid disabled={busy} onPick={(sample: Sample) => start(() => pickSample(sample.key))} />
        </section>
      </div>
    </div>
  );
}