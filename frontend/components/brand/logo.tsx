/** A receipt spike holding two slips: the docket of invoices waiting to be processed. */
export function LogoMark({ className = "size-7" }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" fill="none" aria-hidden="true" className={className}>
      <rect x="6" y="27" width="20" height="3" rx="1.5" fill="currentColor" />
      <path d="M16 27V4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
      <path d="M8 12.5 23 9.5l1.4 6.8-15 3z" fill="var(--color-sheet)" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M9.5 18.6 24 20.4l-.8 6-14.5-1.8z" fill="var(--color-marker)" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round" />
      <path d="M11 13.4l7-1.4M11.6 15.6l4.6-.9" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
    </svg>
  );
}

export function Logo() {
  return (
    <span className="flex items-center gap-2 text-ink">
      <LogoMark />
      <span className="font-display text-2xl leading-none">Docket</span>
    </span>
  );
}