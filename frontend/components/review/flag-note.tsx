import type { Flag } from "@/lib/api";

/** Why a field is flagged, with a way to say it was checked and is right. */
export function FlagNote({ flag, onConfirm, readOnly }: { flag: Flag; onConfirm: () => void; readOnly?: boolean }) {
  const red = flag.level === "low";
  return (
    <div className="mt-1.5 flex animate-rise items-start gap-2 text-[13px] leading-snug">
      <span className={`mt-1 size-2 shrink-0 rounded-full ${red ? "bg-stamp" : "bg-[#d9b200]"}`} />
      <p className={red ? "text-stamp" : "text-ink-soft"}>
        {flag.reason}
        {flag.source === "model" && <span className="text-ink-soft"> (the AI wasn&apos;t sure)</span>}
      </p>
      {!readOnly && (
        <button onClick={onConfirm} className="ml-auto shrink-0 font-bold text-ink underline decoration-ink/30 underline-offset-4 hover:decoration-ink">
          Looks right
        </button>
      )}
    </div>
  );
}