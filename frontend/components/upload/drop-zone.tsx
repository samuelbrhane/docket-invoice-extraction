"use client";

import { useRef, useState } from "react";

const MAX_BYTES = 4 * 1024 * 1024;
const TYPES = ["application/pdf", "image/jpeg", "image/png"];

function checkFile(file: File): string | null {
  if (!TYPES.includes(file.type)) return "Only PDF, JPG and PNG files are supported";
  if (file.size > MAX_BYTES) return "The file is larger than 4 MB";
  return null;
}

export function DropZone({ onFile, disabled }: { onFile: (file: File) => void; disabled?: boolean }) {
  const input = useRef<HTMLInputElement>(null);
  const [dragging, setDragging] = useState(false);
  const [problem, setProblem] = useState<string | null>(null);

  function take(file: File | undefined) {
    if (!file) return;
    const issue = checkFile(file);
    setProblem(issue);
    if (!issue) onFile(file);
  }

  return (
    <div>
      <label
        onDragOver={(event) => {
          event.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault();
          setDragging(false);
          if (!disabled) take(event.dataTransfer.files[0]);
        }}
        className={`group relative flex min-h-80 cursor-pointer flex-col items-center justify-center overflow-hidden rounded-2xl border-2 border-dashed px-8 text-center transition-colors ${
          dragging ? "border-ink bg-sheet" : "border-ink/25 bg-sheet/70 hover:border-ink/50"
        } ${disabled ? "pointer-events-none opacity-60" : ""}`}
      >
        <input
          ref={input}
          type="file"
          accept="application/pdf,image/jpeg,image/png"
          className="sr-only"
          disabled={disabled}
          onChange={(event) => {
            take(event.target.files?.[0]);
            event.target.value = "";
          }}
        />
        <div className="ruled pointer-events-none absolute inset-0 opacity-50" />

        <svg viewBox="0 0 64 64" className="relative size-16 text-ink" fill="none" aria-hidden="true">
          <path d="M18 8h22l10 10v32a3 3 0 0 1-3 3H18a3 3 0 0 1-3-3V11a3 3 0 0 1 3-3z" fill="var(--color-sheet)" stroke="currentColor" strokeWidth="2.5" strokeLinejoin="round" />
          <path d="M40 8v10h10" stroke="currentColor" strokeWidth="2.5" strokeLinejoin="round" />
          <path d="M22 28h18M22 34h12M22 40h16" stroke="currentColor" strokeWidth="2" strokeLinecap="round" opacity="0.45" />
          <path d="M32 58V45m0 0-5 5m5-5 5 5" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" className="transition-transform group-hover:-translate-y-0.5" />
        </svg>

        <p className="relative mt-5 font-display text-2xl">{dragging ? "Let go to upload" : "Drop an invoice here"}</p>
        <p className="relative mt-2 text-ink-soft">
          or <span className="font-bold text-ink underline decoration-ink/30 underline-offset-4">choose a file</span> from your computer
        </p>
        <p className="relative mt-6 text-sm text-ink-soft">PDF, JPG or PNG, up to 4 MB</p>
      </label>
      {problem && <p className="mt-3 text-sm font-bold text-stamp">{problem}</p>}
    </div>
  );
}