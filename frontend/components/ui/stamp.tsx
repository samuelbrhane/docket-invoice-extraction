type Tone = "stamp" | "ink" | "approved";

const TONES: Record<Tone, string> = {
  stamp: "border-stamp text-stamp",
  ink: "border-ink/50 text-ink/70",
  approved: "border-approved text-approved",
};

/** A small rubber stamp mark, for labels like "Phone photo" or "Approved". */
export function Stamp({ children, tone = "stamp", tilt = -2 }: { children: React.ReactNode; tone?: Tone; tilt?: number }) {
  return (
    <span
      className={`inline-block whitespace-nowrap rounded-[3px] border-[1.5px] px-1.5 py-px text-xs font-bold tracking-wide ${TONES[tone]}`}
      style={{ transform: `rotate(${tilt}deg)` }}
    >
      {children}
    </span>
  );
}