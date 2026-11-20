"use client";

import { useCallback, useEffect, useState } from "react";

import { getStats, type Stats } from "@/lib/api";
import { useOnChanged } from "@/lib/events";
import { percent, usd } from "@/lib/format";

function Stat({ value, label }: { value: string; label: string }) {
  return (
    <div className="flex items-baseline gap-1.5">
      <span className="figures text-[15px] font-bold text-ink">{value}</span>
      <span className="text-sm text-ink-soft">{label}</span>
    </div>
  );
}

export function StatsStrip() {
  const [stats, setStats] = useState<Stats | null>(null);
  const load = useCallback(() => {
    getStats().then(setStats).catch(() => setStats(null));
  }, []);

  useEffect(load, [load]);
  useOnChanged(load);

  if (!stats) return <div className="h-5 w-64 animate-shimmer rounded bg-rule/60" />;

  return (
    <div className="flex items-center gap-4">
      <Stat value={stats.accuracy_pct ? percent(stats.accuracy_pct) : "—"} label="AI accuracy" />
      <span className="h-4 w-px bg-rule" />
      <Stat value={String(stats.invoices_by_status.approved ?? 0)} label="approved" />
      <span className="h-4 w-px bg-rule" />
      <Stat value={usd(stats.total_cost_usd)} label="spent on AI" />
    </div>
  );
}