import { request, sendJson } from "./client";
import type { ExportFormat, InventoryItem, InvoiceStatus, Movement, Spending, Stats } from "./types";

export function getInventory(): Promise<InventoryItem[]> {
  return request("/inventory");
}

export function getMovements(sku: string): Promise<Movement[]> {
  return request(`/inventory/${encodeURIComponent(sku)}/movements`);
}

export function getSpending(): Promise<Spending> {
  return request("/spending");
}

export function getStats(): Promise<Stats> {
  return request("/stats");
}

export function exportUrl(format: ExportFormat = "csv", status: InvoiceStatus = "approved"): string {
  return `/api/export?format=${format}&status=${status}`;
}

/** Clears this visitor's data and starts again with the example history. */
export function resetDemo(): Promise<void> {
  return sendJson("/demo/reset", "POST");
}