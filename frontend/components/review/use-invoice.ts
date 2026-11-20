"use client";

import { useCallback, useEffect, useRef, useState } from "react";

import {
  ApiError,
  approveInvoice,
  getInventory,
  getInvoice,
  rejectInvoice,
  updateInvoice,
  type InventoryItem,
  type InvoiceDetail,
  type InvoiceUpdate,
} from "@/lib/api";
import { notifyChanged } from "@/lib/events";

export type SaveState = "idle" | "saving" | "saved" | "error";

export function useInvoice(invoiceId: string) {
  const [invoice, setInvoice] = useState<InvoiceDetail | null>(null);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [saveState, setSaveState] = useState<SaveState>("idle");
  const [actionError, setActionError] = useState<string | null>(null);
  // Saves run one after another, so a quick second edit never overtakes the first
  const queue = useRef<Promise<unknown>>(Promise.resolve());

  useEffect(() => {
    Promise.all([getInvoice(invoiceId), getInventory()])
      .then(([detail, items]) => {
        setInvoice(detail);
        setInventory(items);
      })
      .catch((caught) => setLoadError(caught instanceof ApiError ? caught.message : "The invoice couldn't be loaded."));
  }, [invoiceId]);

  const run = useCallback((task: () => Promise<InvoiceDetail>, isSave: boolean) => {
    const next = queue.current.then(async () => {
      if (isSave) setSaveState("saving");
      setActionError(null);
      try {
        const detail = await task();
        setInvoice(detail);
        if (isSave) setSaveState("saved");
        notifyChanged();
      } catch (caught) {
        if (isSave) setSaveState("error");
        setActionError(caught instanceof ApiError ? caught.message : "Something went wrong. Please try again.");
      }
    });
    queue.current = next;
    return next;
  }, []);

  return {
    invoice,
    inventory,
    loadError,
    saveState,
    actionError,
    save: (update: InvoiceUpdate) => run(() => updateInvoice(invoiceId, update), true),
    approve: () => run(() => approveInvoice(invoiceId), false),
    reject: (reason: string) => run(() => rejectInvoice(invoiceId, reason), false),
  };
}