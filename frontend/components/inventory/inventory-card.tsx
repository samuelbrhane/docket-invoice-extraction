"use client";

import { useState } from "react";

import type { InventoryItem } from "@/lib/api";
import { money, quantity, shortDate, unitPrice } from "@/lib/format";

import { Movements } from "./movements";

/** One stock item as a card, for narrow screens. Tap to see its deliveries. */
export function InventoryCard({ item }: { item: InventoryItem }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="rounded-lg border border-rule bg-sheet">
      <button onClick={() => setOpen((value) => !value)} aria-expanded={open} className="block w-full p-4 text-left">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <p className="font-bold">{item.name}</p>
            <p className="figures text-sm text-ink-soft">{item.sku}</p>
          </div>
          <p className="figures shrink-0 text-right">
            <span className="text-lg font-bold">{quantity(item.stock_qty)}</span> <span className="text-ink-soft">{item.unit}</span>
          </p>
        </div>
        <dl className="mt-3 grid grid-cols-3 gap-2 text-sm">
          <div>
            <dt className="text-ink-soft">Last price</dt>
            <dd className="figures">{unitPrice(item.last_unit_price)}</dd>
          </div>
          <div>
            <dt className="text-ink-soft">Value</dt>
            <dd className="figures">{money(item.stock_value)}</dd>
          </div>
          <div>
            <dt className="text-ink-soft">Last delivery</dt>
            <dd>{item.last_delivery ? shortDate(item.last_delivery) : "Opening stock"}</dd>
          </div>
        </dl>
      </button>
      {open && (
        <div className="animate-rise border-t border-rule bg-ledger/50 px-4 py-3">
          <Movements item={item} />
        </div>
      )}
    </div>
  );
}