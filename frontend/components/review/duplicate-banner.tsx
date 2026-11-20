import Link from "next/link";

import { Button } from "@/components/ui";
import type { InvoiceDetail } from "@/lib/api";

type Props = { invoice: InvoiceDetail; onNotDuplicate: () => void; onRejectDuplicate: () => void };

export function DuplicateBanner({ invoice, onNotDuplicate, onRejectDuplicate }: Props) {
  const earlier = invoice.duplicate_of;
  if (!earlier || invoice.duplicate_confirmed) return null;
  const open = invoice.status === "needs_review" || invoice.status === "ready";

  return (
    <div className="animate-rise rounded-xl border-2 border-stamp/50 bg-marker-red/25 p-5">
      <p className="font-display text-lg text-stamp">This looks like an invoice you already have</p>
      <p className="mt-1 text-[15px]">
        Same supplier VAT number and invoice number as{" "}
        <Link href={`/app/invoices/${earlier.id}`} className="font-bold underline underline-offset-4">
          {earlier.label}
        </Link>
        . Paying it twice is the mistake this check is here to stop.
      </p>
      {open && (
        <div className="mt-4 flex flex-wrap gap-2">
          <Button onClick={onRejectDuplicate}>Reject as duplicate</Button>
          <Button variant="secondary" onClick={onNotDuplicate}>
            It&apos;s a different invoice
          </Button>
        </div>
      )}
    </div>
  );
}