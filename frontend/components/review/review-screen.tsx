"use client";

import { useParams } from "next/navigation";
import { useMemo } from "react";

import { DocumentViewer } from "@/components/extraction";
import { flagIndex } from "@/lib/flags";
import { shortDate } from "@/lib/format";

import { DecisionPanel } from "./decision-panel";
import { DuplicateBanner } from "./duplicate-banner";
import { HeaderFields } from "./header-fields";
import { LinesEditor } from "./lines-editor";
import { ReviewHeader } from "./review-header";
import { useInvoice } from "./use-invoice";

export function ReviewSkeleton() {
  return (
    <div className="grid gap-6 lg:grid-cols-2">
      <div className="h-[70vh] animate-shimmer rounded-xl bg-rule/50" />
      <div className="space-y-4">
        <div className="h-24 animate-shimmer rounded-xl bg-rule/50" />
        <div className="h-[50vh] animate-shimmer rounded-xl bg-rule/50" />
      </div>
    </div>
  );
}

export function ReviewScreen() {
  const { id } = useParams<{ id: string }>();
  const { invoice, inventory, loadError, saveState, actionError, save, approve, reject } = useInvoice(id);
  const flags = useMemo(() => flagIndex(invoice?.flags), [invoice]);

  if (loadError) return <p className="rounded-lg border border-stamp/40 bg-sheet px-4 py-3 font-bold text-stamp">{loadError}</p>;
  if (!invoice) return <ReviewSkeleton />;

  const readOnly = invoice.status === "approved" || invoice.status === "rejected";
  const confirm = (path: string) => save({ confirm_fields: [path] });

  return (
    <div className="space-y-6">
      <ReviewHeader invoice={invoice} saveState={saveState} />

      <div className="grid gap-6 lg:grid-cols-[minmax(0,5fr)_minmax(0,6fr)]">
        <div className="lg:sticky lg:top-24 lg:h-[calc(100vh-8rem)]">
          <div className="h-[65vh] lg:h-full">
            <DocumentViewer documentId={invoice.document_id} filename={invoice.filename} />
          </div>
        </div>

        <div className="space-y-5">
          {actionError && <p className="rounded-lg border border-stamp/40 bg-sheet px-4 py-3 font-bold text-stamp">{actionError}</p>}

          <DuplicateBanner
            invoice={invoice}
            onNotDuplicate={() => save({ not_duplicate: true })}
            onRejectDuplicate={() => reject(`Duplicate of ${invoice.duplicate_of?.label}`)}
          />

          {invoice.status === "approved" && (
            <div className="relative overflow-hidden rounded-xl border border-approved/40 bg-sheet p-5">
              <p className="font-display text-lg text-approved">Approved {shortDate(invoice.approved_at)}</p>
              <p className="mt-1 text-sm text-ink-soft">Stock lines were added to inventory and the totals count towards spending.</p>
              <span className="pointer-events-none absolute -top-1 right-6 rotate-[-8deg] rounded-md border-[3px] border-approved/70 px-3 py-1 font-display text-2xl text-approved/80">
                Approved
              </span>
            </div>
          )}
          {invoice.status === "rejected" && (
            <div className="rounded-xl border border-stamp/40 bg-sheet p-5">
              <p className="font-display text-lg text-stamp">Rejected</p>
              <p className="mt-1 text-sm">{invoice.rejection_reason}</p>
            </div>
          )}
          {!readOnly && <DecisionPanel invoice={invoice} onApprove={approve} onReject={reject} />}

          <div className="rounded-xl border border-rule bg-sheet p-6">
            {(flags.get("document") ?? []).map((flag) => (
              <p key={flag.id} className="mb-5 font-bold text-stamp">
                {flag.reason}
              </p>
            ))}
            <HeaderFields invoice={invoice} flags={flags} readOnly={readOnly} onSave={save} onConfirm={confirm}>
              <LinesEditor
                invoice={invoice}
                inventory={inventory}
                flags={flags}
                readOnly={readOnly}
                onSave={(lines) => save({ lines })}
                onConfirm={confirm}
              />
            </HeaderFields>
          </div>
        </div>
      </div>
    </div>
  );
}