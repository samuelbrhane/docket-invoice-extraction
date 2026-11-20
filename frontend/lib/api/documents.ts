import { request } from "./client";
import type { DocumentInfo, Sample } from "./types";

export function listSamples(): Promise<Sample[]> {
  return request("/samples");
}

export function uploadDocument(file: File): Promise<DocumentInfo> {
  const form = new FormData();
  form.append("file", file);
  return request("/documents", { method: "POST", body: form });
}

export function pickSample(key: string): Promise<DocumentInfo> {
  const form = new FormData();
  form.append("sample", key);
  return request("/documents", { method: "POST", body: form });
}

/** For the document viewer's src. */
export function documentFileUrl(documentId: string): string {
  return `/api/documents/${documentId}/file`;
}