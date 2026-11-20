import type { Stage } from "@/lib/api";

const STAGES: { key: Stage; label: string }[] = [
  { key: "reading", label: "Reading the document" },
  { key: "extracting", label: "Extracting fields" },
  { key: "checking", label: "Running checks" },
  { key: "ready", label: "Ready for review" },
];

export function StageTrack({ stage, failed }: { stage: Stage | null; failed?: boolean }) {
  const current = stage ? STAGES.findIndex((s) => s.key === stage) : -1;

  return (
    <ol className="grid grid-cols-4 gap-2">
      {STAGES.map((s, i) => {
        const done = i < current || stage === "ready";
        const active = i === current && stage !== "ready" && !failed;
        return (
          <li key={s.key} className="flex flex-col gap-2">
            <div className="flex items-center gap-2">
              <span
                className={`grid size-5 shrink-0 place-items-center rounded-full border-2 transition-colors ${
                  done ? "border-ink bg-ink text-sheet" : active ? "animate-dot-pulse border-ink bg-sheet" : "border-rule bg-sheet"
                }`}
              >
                {done && (
                  <svg viewBox="0 0 12 12" className="size-3" fill="none" aria-hidden="true">
                    <path d="m2.5 6.2 2.3 2.3 4.7-5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  </svg>
                )}
                {active && <span className="size-1.5 rounded-full bg-ink" />}
              </span>
              {i < STAGES.length - 1 && (
                <span className="h-0.5 flex-1 overflow-hidden rounded-full bg-rule">
                  <span className={`block h-full bg-ink transition-[width] duration-500 ${done ? "w-full" : "w-0"}`} />
                </span>
              )}
            </div>
            <span className={`text-sm leading-tight ${done || active ? "text-ink" : "text-ink-soft"} ${active ? "font-bold" : ""}`}>
              {s.label}
            </span>
          </li>
        );
      })}
    </ol>
  );
}