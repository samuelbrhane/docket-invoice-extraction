"use client";

import { useState } from "react";

import type { Flag } from "@/lib/api";
import type { FieldDef } from "@/lib/fields";

import { FlagNote } from "./flag-note";

type Props = {
  def: FieldDef;
  value: string;
  flags: Flag[];
  readOnly: boolean;
  onSave: (value: string | null) => void;
  onConfirm: (path: string) => void;
};

const INPUT_TONE = {
  low: "border-stamp/60 bg-marker-red/45",
  medium: "border-[#d9b200]/70 bg-marker/40",
  none: "border-rule bg-sheet",
};

/** An input that saves when you leave it, tinted like a highlighter when its value is flagged. */
export function EditableField({ def, value, flags, readOnly, onSave, onConfirm }: Props) {
  const [draft, setDraft] = useState(value);
  const [synced, setSynced] = useState(value);

  // When the server sends a new value, show it
  if (value !== synced) {
    setSynced(value);
    setDraft(value);
  }

  const tone = flags.some((f) => f.level === "low") ? "low" : flags.length ? "medium" : "none";
  const isNumber = def.kind === "money" || def.kind === "percent";

  function commit() {
    const next = draft.trim();
    if (next === value) return;
    onSave(next === "" ? null : next);
  }

  return (
    <div className={def.wide ? "col-span-2" : ""}>
      <label className="text-[13px] text-ink-soft" htmlFor={def.column}>
        {def.label}
      </label>
      <input
        id={def.column}
        type={def.kind === "date" ? "date" : "text"}
        inputMode={isNumber ? "decimal" : undefined}
        value={draft}
        disabled={readOnly}
        onChange={(event) => setDraft(event.target.value)}
        onBlur={commit}
        onKeyDown={(event) => event.key === "Enter" && event.currentTarget.blur()}
        className={`mt-1 w-full rounded-md border px-3 py-2 text-[15px] transition-colors outline-none focus:border-ink disabled:border-transparent disabled:bg-transparent disabled:px-0 ${
          def.kind === "code" || isNumber ? "figures" : ""
        } ${isNumber ? "text-right disabled:text-left" : ""} ${INPUT_TONE[tone]}`}
      />
      {flags.map((flag) => (
        <FlagNote key={flag.id} flag={flag} readOnly={readOnly} onConfirm={() => onConfirm(flag.field)} />
      ))}
    </div>
  );
}