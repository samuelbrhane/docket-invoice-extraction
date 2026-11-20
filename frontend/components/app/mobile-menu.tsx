"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

import { APP_LINKS, isActive } from "./links";
import { StatsStrip } from "./stats-strip";

/** On small screens the tabs fold into a menu under the header. */
export function MobileMenu() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <div className="md:hidden">
      <button
        onClick={() => setOpen((value) => !value)}
        aria-expanded={open}
        aria-controls="mobile-menu"
        aria-label={open ? "Close menu" : "Open menu"}
        className="grid size-10 place-items-center rounded-lg border border-rule bg-sheet text-ink"
      >
        <svg viewBox="0 0 24 24" className="size-5" fill="none" aria-hidden="true">
          {open ? (
            <path d="M6 6l12 12M18 6 6 18" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          ) : (
            <path d="M4 7h16M4 12h16M4 17h10" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          )}
        </svg>
      </button>

      {open && (
        <div id="mobile-menu" className="absolute inset-x-0 top-16 animate-rise border-b border-rule bg-ledger px-6 pt-2 pb-6 shadow-[0_16px_30px_-20px_rgb(28_42_66/0.4)]">
          <nav className="flex flex-col">
            {APP_LINKS.map((link) => {
              const active = isActive(pathname, link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  onClick={() => setOpen(false)}
                  aria-current={active ? "page" : undefined}
                  className={`flex items-center justify-between border-b border-rule py-3.5 text-lg ${
                    active ? "font-bold text-ink" : "text-ink-soft"
                  }`}
                >
                  {link.label}
                  {active && <span className="size-2 rounded-full bg-ink" />}
                </Link>
              );
            })}
          </nav>
          <div className="mt-5 [&>div]:flex-wrap [&>div]:gap-y-2">
            <StatsStrip />
          </div>
        </div>
      )}
    </div>
  );
}