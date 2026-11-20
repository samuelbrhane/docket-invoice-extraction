"use client";

import { useState } from "react";

import { Button } from "@/components/ui";
import type { InvoiceDetail } from "@/lib/api";

type Props = { invoice: InvoiceDetail; onApprove: () => void; onReject: (reason: string) => void };

export function DecisionPanel({ invoice, onApprove, onReject }: Props) {
  const [rejecting, setRejecting] = useState(false);
  const [reason, setReason] = useState("");
  const red = invoice.open_red_flags;
  const stockLines = invoice.lines.filter((line) => line.kind === "stock").length;

  if (rejecting) {
    return (
      <div className="animate-rise rounded-xl border border-rule bg-sheet p-5">
        <label htmlFor="reject-reason" className="font-display text-lg">
          Why are you rejecting it?
        </label>
        <textarea
          id="reject-reason"
          autoFocus
          rows={2}
          value={reason}
          onChange={(event) => setReason(event.target.value)}
          placeholder="For example: wrong company, already paid, or a quote rather than an invoice"
          className="mt-2 w-full rounded-md border border-rule bg-sheet px-3 py-2 outline-none focus:border-ink"
        />
        <div className="mt-3 flex gap-2">
          <Button disabled={reason.trim().length < 3} onClick={() => onReject(reason.trim())} className="bg-stamp hover:bg-stamp/90">
            Reject invoice
          </Button>
          <Button variant="quiet" onClick={() => setRejecting(false)}>
            Cancel
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-rule bg-sheet p-5">
      <div className="flex flex-wrap items-center gap-3">
        <Button disabled={red > 0} onClick={onApprove}>
          Approve invoice
        </Button>
        <Button variant="secondary" onClick={() => setRejecting(true)}>
          Reject
        </Button>
        <p className={`text-sm ${red ? "font-bold text-stamp" : "text-ink-soft"}`}>
          {red
            ? `Fix or confirm ${red} red ${red === 1 ? "field" : "fields"} to approve`
            : stockLines
              ? `Approving adds ${stockLines} ${stockLines === 1 ? "line" : "lines"} to inventory`
              : "No stock lines, so approving records it as spending only"}
        </p>
      </div>
    </div>
  );
}