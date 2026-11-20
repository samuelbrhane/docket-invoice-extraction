"use client";

import { useInView } from "./use-in-view";

/** A highlighter swipe that is drawn when the value scrolls into view. */
export function MarkerOnView({ children, tone, delay = 0 }: { children: React.ReactNode; tone: "marker" | "marker-red"; delay?: number }) {
  const [ref, inView] = useInView<HTMLSpanElement>(0.8);
  return (
    <span
      ref={ref}
      className={inView ? `${tone} animate-marker-swipe` : "px-[0.15em]"}
      style={{ animationDelay: `${delay}ms` }}
    >
      {children}
    </span>
  );
}