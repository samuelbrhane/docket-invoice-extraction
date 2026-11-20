"use client";

import { useEffect } from "react";

const EVENT = "docket:changed";

/** Tell the rest of the app that invoices changed, so stats and lists refresh. */
export function notifyChanged(): void {
  window.dispatchEvent(new Event(EVENT));
}

export function useOnChanged(callback: () => void): void {
  useEffect(() => {
    window.addEventListener(EVENT, callback);
    return () => window.removeEventListener(EVENT, callback);
  }, [callback]);
}