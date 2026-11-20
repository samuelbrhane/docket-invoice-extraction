"use client";

import { useState } from "react";

import type { Flag, InventoryItem, InvoiceDetail, LineInput } from "@/lib/api";
import { EXPENSE_CATEGORIES, trimDecimal } from "@/lib/fields";

import { FlagNote } from "./flag-note";

type Props = {
  invoice: InvoiceDetail;
  inventory: InventoryItem[];
  flags: Map<string, Flag[]>;
  readOnly: boolean;
  onSave: (lines: LineInput[]) => void;
  onConfirm: (path: string) => void;
};

type NumberKey = "quantity" | "unit_price" | "line_total";

function fromInvoice(invoice: InvoiceDetail): LineInput[] {
  return invoice.lines.map((line) => ({
    id: line.id,
    description: line.description,
    quantity: line.quantity === null ? null : trimDecimal(line.quantity),
    unit: line.unit,
    unit_price: line.unit_price === null ? null : trimDecimal(line.unit_price),
    line_total: line.line_total === null ? null : trimDecimal(line.line_total),
    kind: line.kind,
    sku: line.sku,
    expense_category: line.expense_category,
  }));
}

function matchValue(line: LineInput): string {
  if (line.kind === "stock" && line.sku) return `stock:${line.sku}`;
  if (line.kind === "expense" && line.expense_category) return `expense:${line.expense_category}`;
  return "unmatched";
}

function withMatch(line: LineInput, value: string): LineInput {
  const [kind, key] = value.split(":");
  if (kind === "stock") return { ...line, kind: "stock", sku: key, expense_category: null };
  if (kind === "expense") return { ...line, kind: "expense", sku: null, expense_category: key };
  return { ...line, kind: "unmatched", sku: null, expense_category: null };
}

function toneClass(flags: Map<string, Flag[]>, path: string): string {
  const list = flags.get(path) ?? [];
  if (list.some((f) => f.level === "low")) return "border-stamp/60 bg-marker-red/45";
  if (list.length) return "border-[#d9b200]/70 bg-marker/40";
  return "border-rule";
}

export function LinesEditor({ invoice, inventory, flags, readOnly, onSave, onConfirm }: Props) {
  const serverLines = fromInvoice(invoice);
  const serverKey = JSON.stringify(serverLines);
  const [draft, setDraft] = useState(serverLines);
  const [synced, setSynced] = useState(serverKey);

  if (serverKey !== synced) {
    setSynced(serverKey);
    setDraft(serverLines);
  }

  function update(index: number, change: Partial<LineInput>) {
    setDraft((lines) => lines.map((line, i) => (i === index ? { ...line, ...change } : line)));
  }

  function commit(lines = draft) {
    if (JSON.stringify(lines) !== serverKey) onSave(lines);
  }

  const cellInput =
    "w-full rounded-md border bg-sheet px-2 py-1.5 outline-none focus:border-ink disabled:border-transparent disabled:bg-transparent disabled:px-0";

  const numberCell = (index: number, line: LineInput, key: NumberKey, label: string) => (
    <label className="block min-w-0">
      <span className="text-[12px] text-ink-soft">{label}</span>
      <input
        inputMode="decimal"
        value={line[key] ?? ""}
        disabled={readOnly}
        onChange={(event) => update(index, { [key]: event.target.value === "" ? null : event.target.value })}
        onBlur={() => commit()}
        className={`${cellInput} figures mt-0.5 text-right disabled:text-left ${toneClass(flags, `lines[${index}].${key}`)}`}
      />
    </label>
  );

  return (
    <section>
      <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
        <h3 className="font-display text-lg">Line items</h3>
        <p className="text-[13px] text-ink-soft">Stock lines are added to inventory when you approve</p>
      </div>
      <ol className="space-y-3">
        {draft.map((line, i) => {
          const lineFlags = [...flags.entries()].filter(([path]) => path.startsWith(`lines[${i}].`)).flatMap(([, list]) => list);
          return (
            <li key={line.id ?? `new-${i}`} className="rounded-lg border border-rule/80 bg-ledger/40 p-3">
              <div className="flex items-center gap-2">
                <span className="figures w-5 shrink-0 text-sm text-ink-soft">{i + 1}</span>
                <input
                  aria-label={`Line ${i + 1} description`}
                  value={line.description}
                  placeholder="Description"
                  disabled={readOnly}
                  onChange={(event) => update(i, { description: event.target.value })}
                  onBlur={() => commit()}
                  className={`${cellInput} border-rule font-bold`}
                />
                {!readOnly && (
                  <button
                    aria-label={`Remove line ${i + 1}`}
                    onClick={() => {
                      const lines = draft.filter((_, index) => index !== i);
                      setDraft(lines);
                      commit(lines);
                    }}
                    className="grid size-8 shrink-0 place-items-center rounded-md text-ink-soft hover:bg-rule/60 hover:text-stamp"
                  >
                    <svg viewBox="0 0 16 16" className="size-3.5" fill="none" aria-hidden="true">
                      <path d="M4 4l8 8M12 4l-8 8" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" />
                    </svg>
                  </button>
                )}
              </div>

              <div className="mt-2 grid grid-cols-2 gap-x-3 gap-y-2 pl-7 sm:grid-cols-[1fr_0.7fr_1fr_1fr_1.7fr]">
                {numberCell(i, line, "quantity", "Qty")}
                <label className="block min-w-0">
                  <span className="text-[12px] text-ink-soft">Unit</span>
                  <input
                    value={line.unit ?? ""}
                    disabled={readOnly}
                    onChange={(event) => update(i, { unit: event.target.value || null })}
                    onBlur={() => commit()}
                    className={`${cellInput} mt-0.5 border-rule`}
                  />
                </label>
                {numberCell(i, line, "unit_price", "Unit price")}
                {numberCell(i, line, "line_total", "Total")}
                <label className="col-span-2 block min-w-0 sm:col-span-1">
                  <span className="text-[12px] text-ink-soft">Goes to</span>
                  <select
                    value={matchValue(line)}
                    disabled={readOnly}
                    onChange={(event) => {
                      const lines = draft.map((l, index) => (index === i ? withMatch(l, event.target.value) : l));
                      setDraft(lines);
                      commit(lines);
                    }}
                    className={`${cellInput} mt-0.5 py-[7px] text-sm disabled:appearance-none ${toneClass(flags, `lines[${i}].match`)}`}
                  >
                    <optgroup label="Inventory">
                      {inventory.map((item) => (
                        <option key={item.sku} value={`stock:${item.sku}`}>
                          {item.name}
                        </option>
                      ))}
                    </optgroup>
                    <optgroup label="Expense">
                      {EXPENSE_CATEGORIES.map((category) => (
                        <option key={category} value={`expense:${category}`}>
                          {category[0].toUpperCase() + category.slice(1)}
                        </option>
                      ))}
                    </optgroup>
                    <option value="unmatched">Not matched yet</option>
                  </select>
                </label>
              </div>

              {lineFlags.length > 0 && (
                <div className="mt-1 pl-7">
                  {lineFlags.map((flag) => (
                    <FlagNote key={flag.id} flag={flag} readOnly={readOnly} onConfirm={() => onConfirm(flag.field)} />
                  ))}
                </div>
              )}
            </li>
          );
        })}
      </ol>
      {!readOnly && (
        <button
          onClick={() => setDraft((lines) => [...lines, { description: "", kind: "unmatched" }])}
          className="mt-3 text-sm font-bold text-ink underline decoration-ink/30 underline-offset-4 hover:decoration-ink"
        >
          Add a line
        </button>
      )}
      {(flags.get("lines") ?? []).map((flag) => (
        <FlagNote key={flag.id} flag={flag} readOnly={readOnly} onConfirm={() => onConfirm(flag.field)} />
      ))}
    </section>
  );
}