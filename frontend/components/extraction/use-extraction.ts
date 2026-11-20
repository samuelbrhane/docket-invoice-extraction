"use client";

import { useEffect, useRef, useState } from "react";

import { ApiError, extractDocument, type InvoiceDetail, type Stage } from "@/lib/api";
import { notifyChanged } from "@/lib/events";
import { EMPTY_VIEW, fromDetail, fromPartial, type InvoiceView } from "@/lib/invoice-view";

export type ExtractionState = {
  stage: Stage | null;
  view: InvoiceView;
  result: InvoiceDetail | null;
  error: string | null;
};

export function useExtraction(documentId: string): ExtractionState {
  const [state, setState] = useState<ExtractionState>({ stage: null, view: EMPTY_VIEW, result: null, error: null });
  const started = useRef(false);

  useEffect(() => {
    // React runs effects twice in development. One extraction per document, never two.
    if (started.current) return;
    started.current = true;

    extractDocument(documentId, {
      onStage: (stage) => setState((s) => ({ ...s, stage })),
      onPartial: (partial) => setState((s) => ({ ...s, view: fromPartial(partial) })),
      onResult: (result) => {
        setState((s) => ({ ...s, result, view: fromDetail(result) }));
        notifyChanged();
      },
      onError: (error) => setState((s) => ({ ...s, error })),
    }).catch((caught) => {
      const error = caught instanceof ApiError ? caught.message : "The connection to the server was lost.";
      setState((s) => ({ ...s, error }));
    });
  }, [documentId]);

  return state;
}