import { request, sendJson } from "./client";
import type { ExportFormat, InvoiceDetail, InvoiceSummary, InvoiceUpdate } from "./types";

export function listInvoices(): Promise<InvoiceSummary[]> {
  return request("/invoices");
}

export function getInvoice(invoiceId: string): Promise<InvoiceDetail> {
  return request(`/invoices/${invoiceId}`);
}

/** Send only what changed. Lines, when sent, replace the whole list. */
export function updateInvoice(invoiceId: string, update: InvoiceUpdate): Promise<InvoiceDetail> {
  return sendJson(`/invoices/${invoiceId}`, "PATCH", update);
}

export function approveInvoice(invoiceId: string): Promise<InvoiceDetail> {
  return sendJson(`/invoices/${invoiceId}/approve`, "POST");
}

export function rejectInvoice(invoiceId: string, reason: string): Promise<InvoiceDetail> {
  return sendJson(`/invoices/${invoiceId}/reject`, "POST", { reason });
}

export function invoiceExportUrl(invoiceId: string, format: ExportFormat = "json"): string {
  return `/api/invoices/${invoiceId}/export?format=${format}`;
}