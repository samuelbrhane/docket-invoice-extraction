"use client";

import { Fragment, useCallback, useEffect, useState } from "react";

import { getInventory, type InventoryItem } from "@/lib/api";
import { useOnChanged } from "@/lib/events";
import { money, quantity, shortDate, unitPrice } from "@/lib/format";

import { Movements } from "./movements";

function Chevron({ open }: { open: boolean }) {
  return (
    <svg viewBox="0 0 16 16" className={`size-4 transition-transform ${open ? "rotate-90" : ""}`} fill="none" aria-hidden="true">
      <path d="m6 4 4 4-4 4" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function InventoryTable() {
  const [items, setItems] = useState<InventoryItem[] | null>(null);
  const [open, setOpen] = useState<string | null>(null);

  const load = useCallback(() => {
    getInventory().then(setItems).catch(() => setItems([]));
  }, []);
  useEffect(load, [load]);
  useOnChanged(load);

  const totalValue = (items ?? []).reduce((sum, item) => sum + Number(item.stock_value ?? 0), 0);

  return (
    <div>
      <h1 className="font-display text-4xl leading-tight">Inventory</h1>
      <p className="mt-2 text-ink-soft">
        {items === null ? (
          "Loading…"
        ) : (
          <>
            <span className="figures font-bold text-ink">{money(totalValue)}</span> of stock across {items.length} items, valued at the
            last price paid. Approving an invoice adds its stock lines here.
          </>
        )}
      </p>

      <div className="mt-8 overflow-hidden rounded-xl border border-rule bg-sheet">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[640px]">
            <thead>
              <tr className="text-left text-[13px] text-ink-soft">
                <th className="py-3 pl-5 pr-3 font-normal">Item</th>
                <th className="px-3 py-3 text-right font-normal">On hand</th>
                <th className="px-3 py-3 text-right font-normal">Last price</th>
                <th className="px-3 py-3 text-right font-normal">Value</th>
                <th className="py-3 pr-5 pl-3 font-normal">Last delivery</th>
              </tr>
            </thead>
            <tbody>
              {(items ?? []).map((item) => {
                const expanded = open === item.sku;
                return (
                  <Fragment key={item.sku}>
                    <tr className="border-t border-rule">
                      <td className="py-3.5 pl-5 pr-3">
                        <button
                          onClick={() => setOpen(expanded ? null : item.sku)}
                          aria-expanded={expanded}
                          className="flex items-center gap-2 text-left"
                        >
                          <span className="text-ink-soft">
                            <Chevron open={expanded} />
                          </span>
                          <span>
                            <span className="font-bold">{item.name}</span>
                            <span className="figures block text-sm text-ink-soft">{item.sku}</span>
                          </span>
                        </button>
                      </td>
                      <td className="figures px-3 py-3.5 text-right whitespace-nowrap">
                        <span className="font-bold">{quantity(item.stock_qty)}</span> <span className="text-ink-soft">{item.unit}</span>
                      </td>
                      <td className="figures px-3 py-3.5 text-right">{unitPrice(item.last_unit_price)}</td>
                      <td className="figures px-3 py-3.5 text-right">{money(item.stock_value)}</td>
                      <td className="py-3.5 pr-5 pl-3 text-[15px]">
                        {item.last_delivery ? shortDate(item.last_delivery) : <span className="text-ink-soft">Opening stock</span>}
                      </td>
                    </tr>
                    {expanded && (
                      <tr className="bg-ledger/50">
                        <td colSpan={5} className="animate-rise px-5 py-4 pl-11">
                          <Movements item={item} />
                        </td>
                      </tr>
                    )}
                  </Fragment>
                );
              })}
              {items === null &&
                Array.from({ length: 6 }, (_, i) => (
                  <tr key={i} className="border-t border-rule">
                    <td colSpan={5} className="px-5 py-4">
                      <div className="h-6 animate-shimmer rounded bg-rule/50" />
                    </td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}