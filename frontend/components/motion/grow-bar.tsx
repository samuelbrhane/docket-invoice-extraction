"use client";

import { useInView } from "./use-in-view";

/** A bar that fills to its share when it scrolls into view. */
export function GrowBar({ share, delay = 0, className = "bg-ink/75" }: { share: number; delay?: number; className?: string }) {
  const [ref, inView] = useInView<HTMLDivElement>(0.5);
  return (
    <div ref={ref} className="h-full">
      <div
        className={`h-full rounded-full transition-[width] duration-1000 ease-out ${className}`}
        style={{ width: inView ? `${share}%` : "0%", transitionDelay: `${delay}ms` }}
      />
    </div>
  );
}