import Link from "next/link";

import { Logo } from "@/components/brand";

import { NavLink } from "./nav-link";
import { StatsStrip } from "./stats-strip";

const LINKS = [
  { href: "/app", label: "Process" },
  { href: "/app/invoices", label: "Invoices" },
  { href: "/app/inventory", label: "Inventory" },
  { href: "/app/spending", label: "Spending" },
];

export function AppHeader() {
  return (
    <header className="sticky top-0 z-20 border-b border-rule bg-ledger/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center gap-10 px-6">
        <Link href="/" aria-label="Docket home">
          <Logo />
        </Link>
        <nav className="flex gap-7">
          {LINKS.map((link) => (
            <NavLink key={link.href} href={link.href}>
              {link.label}
            </NavLink>
          ))}
        </nav>
        <div className="ml-auto hidden lg:block">
          <StatsStrip />
        </div>
      </div>
    </header>
  );
}