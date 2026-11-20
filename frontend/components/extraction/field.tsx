import type { Flag } from "@/lib/api";
import { highlightFor, markerClass } from "@/lib/flags";
import type { Value } from "@/lib/invoice-view";

type Props = {
  label: string;
  value: Value;
  path?: string;
  flags?: Map<string, Flag[]>;
  format?: (value: string) => string;
  figures?: boolean;
  className?: string;
};

/** One extracted value: a waiting line while unread, then the value inked in, then a highlighter if flagged. */
export function Field({ label, value, path, flags, format, figures, className = "" }: Props) {
  const reasons = path && flags ? flags.get(path) ?? [] : [];
  const highlight = path && flags ? highlightFor(flags, path) : null;

  return (
    <div className={`min-w-0 ${className}`}>
      <dt className="text-[13px] text-ink-soft">{label}</dt>
      <dd className="mt-1 min-h-6 leading-6">
        {value === undefined ? (
          <span className="block h-[0.9rem] w-3/4 translate-y-1 animate-shimmer rounded-sm bg-rule" />
        ) : value === null ? (
          <span className="text-sm text-ink-soft italic">Not on the invoice</span>
        ) : (
          <span key={value} className={`animate-ink-in break-words ${figures ? "figures" : ""} ${markerClass(highlight)}`}>
            {format ? format(value) : value}
          </span>
        )}
      </dd>
      {reasons.map((flag) => (
        <p key={flag.id} className={`mt-1 animate-rise text-[13px] leading-snug ${flag.level === "low" ? "text-stamp" : "text-ink-soft"}`}>
          {flag.reason}
        </p>
      ))}
    </div>
  );
}