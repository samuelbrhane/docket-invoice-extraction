import Link from "next/link";

import { Logo } from "@/components/brand";
import { ButtonLink } from "@/components/ui";

const LINKS = [
  { href: "#how-it-works", label: "How it works" },
  { href: "#checks", label: "The checks" },
  { href: "#after-approval", label: "After approval" },
];

export function SiteHeader() {
  return (
    <header className="sticky top-0 z-20 border-b border-rule/70 bg-ledger/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center gap-8 px-6">
        <Link href="/" aria-label="Docket home">
          <Logo />
        </Link>
        <nav className="hidden gap-7 text-[15px] text-ink-soft md:flex">
          {LINKS.map((link) => (
            <a key={link.href} href={link.href} className="hover:text-ink">
              {link.label}
            </a>
          ))}
        </nav>
        <ButtonLink href="/app" className="ml-auto">
          Open the app
        </ButtonLink>
      </div>
    </header>
  );
}