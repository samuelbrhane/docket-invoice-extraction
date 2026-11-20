import type { Flag } from "@/lib/api";

export type Highlight = "low" | "medium" | null;

/** Open flags grouped by field path, for quick lookups while rendering. */
export function flagIndex(flags: Flag[] | undefined): Map<string, Flag[]> {
  const index = new Map<string, Flag[]>();
  for (const flag of flags ?? []) {
    if (flag.resolved) continue;
    index.set(flag.field, [...(index.get(flag.field) ?? []), flag]);
  }
  return index;
}

export function highlightFor(index: Map<string, Flag[]>, path: string): Highlight {
  const flags = index.get(path);
  if (!flags?.length) return null;
  return flags.some((flag) => flag.level === "low") ? "low" : "medium";
}

export function markerClass(highlight: Highlight): string {
  if (highlight === "low") return "marker-red animate-marker-swipe";
  if (highlight === "medium") return "marker animate-marker-swipe";
  return "";
}