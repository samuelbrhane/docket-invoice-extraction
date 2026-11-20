"use client";

import { useMemo } from "react";

import { Button } from "@/components/ui";
import type { DocumentInfo } from "@/lib/api";
import { flagIndex } from "@/lib/flags";

import { DocumentViewer } from "./document-viewer";
import { LiveForm } from "./live-form";
import { ResultBanner } from "./result-banner";
import { StageTrack } from "./stage-track";
import { useExtraction } from "./use-extraction";

export function ExtractionView({ document, onAnother }: { document: DocumentInfo; onAnother: () => void }) {
  const { stage, view, result, error } = useExtraction(document.id);
  const flags = useMemo(() => flagIndex(result?.flags), [result]);

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_minmax(0,1fr)]">
      <div className="lg:sticky lg:top-24 lg:h-[calc(100vh-8rem)]">
        <div className="h-[70vh] lg:h-full">
          <DocumentViewer documentId={document.id} filename={document.filename} contentType={document.content_type} />
        </div>
      </div>

      <div className="space-y-5">
        <div className="rounded-xl border border-rule bg-sheet p-5">
          <StageTrack stage={stage} failed={Boolean(error)} />
        </div>

        {error && (
          <div className="animate-rise rounded-xl border border-stamp/40 bg-sheet p-5">
            <p className="font-bold text-stamp">{error}</p>
            <Button variant="secondary" className="mt-4" onClick={onAnother}>
              Try another invoice
            </Button>
          </div>
        )}

        {result && <ResultBanner invoice={result} onAnother={onAnother} />}

        <div className="rounded-xl border border-rule bg-sheet p-6">
          <LiveForm view={view} flags={flags} />
        </div>
      </div>
    </div>
  );
}