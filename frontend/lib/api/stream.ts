import { ensureOk, ensureSession } from "./client";
import type { InvoiceDetail } from "./types";

export type Stage = "reading" | "extracting" | "checking" | "ready";

/** The fields read so far. Any part can still be missing while the model writes. */
export type PartialInvoice = {
  supplier?: { name?: string | null; vat?: string | null; address?: string | null };
  invoice?: { number?: string | null; issue_date?: string | null; due_date?: string | null; currency?: string | null };
  lines?: {
    description?: string;
    quantity?: number | null;
    unit?: string | null;
    unit_price?: number | null;
    line_total?: number | null;
  }[];
  totals?: { subtotal?: number | null; vat_rate?: number | null; vat_amount?: number | null; total?: number | null };
  payment?: { terms?: string | null; iban?: string | null };
};

export type ExtractionHandlers = {
  onStage?: (stage: Stage) => void;
  onPartial?: (partial: PartialInvoice) => void;
  onResult?: (invoice: InvoiceDetail) => void;
  onError?: (message: string) => void;
};

function dispatch(block: string, handlers: ExtractionHandlers): void {
  let event = "message";
  const data: string[] = [];
  for (const line of block.split("\n")) {
    if (line.startsWith("event:")) event = line.slice(6).trim();
    else if (line.startsWith("data:")) data.push(line.slice(5).trimStart());
  }
  if (!data.length) return;
  const payload = JSON.parse(data.join("\n"));

  if (event === "stage") handlers.onStage?.(payload.stage);
  else if (event === "partial") handlers.onPartial?.(payload);
  else if (event === "result") handlers.onResult?.(payload);
  else if (event === "error") handlers.onError?.(payload.message);
}

/**
 * Start the extraction and call the handlers as events arrive.
 * Uses fetch because EventSource can't send a POST. Throws ApiError for a 409 or 429 before streaming.
 */
export async function extractDocument(
  documentId: string,
  handlers: ExtractionHandlers,
  signal?: AbortSignal,
): Promise<void> {
  await ensureSession();
  const response = await ensureOk(
    await fetch(`/api/documents/${documentId}/extract`, { method: "POST", credentials: "same-origin", signal }),
  );
  const reader = response.body!.pipeThrough(new TextDecoderStream()).getReader();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += value.replace(/\r\n/g, "\n");
    let boundary = buffer.indexOf("\n\n");
    while (boundary !== -1) {
      dispatch(buffer.slice(0, boundary), handlers);
      buffer = buffer.slice(boundary + 2);
      boundary = buffer.indexOf("\n\n");
    }
  }
  if (buffer.trim()) dispatch(buffer, handlers);
}