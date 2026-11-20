"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { getMovements, type InventoryItem, type Movement } from "@/lib/api";
import { quantity, shortDate, unitPrice } from "@/lib/format";

/** The approved deliveries that added stock to one item. */
export function Movements({ item }: { item: InventoryItem }) {
  const [movements, setMovements] = useState<Movement[] | null>(null);

  useEffect(() => {
    getMovements(item.sku).then(setMovements).catch(() => setMovements([]));
  }, [item.sku]);

  if (movements === null) return <div className="h-10 animate-shimmer rounded bg-rule/50" />;
  if (movements.length === 0) {
    return <p className="text-sm text-ink-soft">No deliveries approved in Docket yet. The opening stock came from before.</p>;
  }

  return (
    <ul className="space-y-2">
      {movements.map((movement) => (
        <li key={movement.id} className="flex flex-wrap items-baseline gap-x-3 gap-y-1 text-[15px]">
          <span className="figures font-bold text-approved">
            +{quantity(movement.quantity)} {item.unit}
          </span>
          {movement.unit_price && <span className="figures text-ink-soft">at {unitPrice(movement.unit_price)}</span>}
          <span className="text-ink-soft">from</span>
          {movement.invoice_id ? (
            <Link href={`/app/invoices/${movement.invoice_id}`} className="underline underline-offset-4">
              {movement.invoice_label}
            </Link>
          ) : (
            <span>an invoice that was removed</span>
          )}
          <span className="text-sm text-ink-soft">{shortDate(movement.issue_date ?? movement.created_at)}</span>
        </li>
      ))}
    </ul>
  );
}