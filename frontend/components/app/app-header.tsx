import Link from "next/link";
import { Suspense } from "react";

import { Logo } from "@/components/brand";

import { APP_LINKS } from "./links";
import { MobileMenu } from "./mobile-menu";
import { NavLink } from "./nav-link";
import { StatsStrip } from "./stats-strip";

export function AppHeader() {
  return (
    <header className="sticky top-0 z-20 border-b border-rule bg-ledger/85 backdrop-blur">
      <div className="relative mx-auto flex h-16 max-w-7xl items-center gap-10 px-6">
        <Link href="/" aria-label="Docket home">
          <Logo />
        </Link>
        <nav className="hidden gap-7 md:flex">
          {APP_LINKS.map((link) => (
            // The active tab depends on the URL, so each link waits in Suspense on dynamic pages
            <Suspense key={link.href} fallback={<span className="py-5 text-[15px] text-ink-soft">{link.label}</span>}>
              <NavLink href={link.href}>{link.label}</NavLink>
            </Suspense>
          ))}
        </nav>
        <div className="ml-auto hidden lg:block">
          <StatsStrip />
        </div>
        <div className="ml-auto md:hidden">
          <Suspense fallback={<div className="size-10 rounded-lg border border-rule bg-sheet" />}>
            <MobileMenu />
          </Suspense>
        </div>
      </div>
    </header>
  );
}