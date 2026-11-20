"use client";

import { useEffect, useState } from "react";

import { listSamples, type Sample } from "@/lib/api";

import { SampleCard } from "./sample-card";

export function SampleGrid({ onPick, disabled }: { onPick: (sample: Sample) => void; disabled?: boolean }) {
  const [samples, setSamples] = useState<Sample[] | null>(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    listSamples().then(setSamples).catch(() => setError(true));
  }, []);

  if (error) return <p className="text-stamp">The sample invoices couldn&apos;t be loaded. Is the API running?</p>;

  return (
    <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">
      {samples
        ? samples.map((sample) => (
            <SampleCard key={sample.key} sample={sample} onPick={() => onPick(sample)} disabled={disabled} />
          ))
        : Array.from({ length: 9 }, (_, i) => <div key={i} className="h-32 animate-shimmer rounded-lg bg-rule/50" />)}
    </div>
  );
}