"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { isActive } from "./links";

export function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  const active = isActive(usePathname(), href);

  return (
    <Link
      href={href}
      aria-current={active ? "page" : undefined}
      className={`relative py-5 text-[15px] transition-colors ${
        active ? "font-bold text-ink" : "text-ink-soft hover:text-ink"
      }`}
    >
      {children}
      {active && <span className="absolute inset-x-0 bottom-0 h-0.5 rounded-full bg-ink" />}
    </Link>
  );
}