"use client";

import { useInView } from "./use-in-view";

/** Rises into place when scrolled into view. Without JavaScript the content simply shows. */
export function Reveal({ children, delay = 0, className = "" }: { children: React.ReactNode; delay?: number; className?: string }) {
  const [ref, inView] = useInView<HTMLDivElement>(0.2);
  return (
    <div
      ref={ref}
      className={`transition-[opacity,transform] duration-700 ease-out ${inView ? "translate-y-0 opacity-100" : "translate-y-4 opacity-0"} ${className}`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      {children}
    </div>
  );
}