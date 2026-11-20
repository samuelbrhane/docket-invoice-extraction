import { Logo } from "@/components/brand";

export function SiteFooter() {
  return (
    <footer className="border-t border-rule bg-sheet/60">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center justify-between gap-4 px-6 py-8 text-sm text-ink-soft">
        <Logo />
        <p>Sila Roasting Co. and its suppliers are fictional, and the sample invoices are generated.</p>
      </div>
    </footer>
  );
}