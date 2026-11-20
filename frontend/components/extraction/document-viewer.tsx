import { documentFileUrl } from "@/lib/api";

type Props = { documentId: string; filename: string; contentType?: string };

/** The original invoice, shown next to the extracted fields. */
export function DocumentViewer({ documentId, filename, contentType }: Props) {
  const url = documentFileUrl(documentId);
  const isPdf = contentType ? contentType === "application/pdf" : filename.toLowerCase().endsWith(".pdf");

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-xl border border-rule bg-sheet shadow-[0_18px_40px_-28px_rgb(28_42_66/0.5)]">
      <div className="flex items-center justify-between border-b border-rule px-4 py-2.5 text-sm">
        <span className="figures truncate">{filename}</span>
        <a href={url} target="_blank" rel="noreferrer" className="shrink-0 text-ink-soft underline underline-offset-4 hover:text-ink">
          Open original
        </a>
      </div>
      <div className="min-h-0 flex-1 bg-[#e4e9e0]">
        {isPdf ? (
          <iframe src={`${url}#toolbar=0&navpanes=0&view=FitH`} title={filename} className="h-full w-full" />
        ) : (
          // eslint-disable-next-line @next/next/no-img-element
          <img src={url} alt={`Scan of ${filename}`} className="h-full w-full object-contain p-4" />
        )}
      </div>
    </div>
  );
}