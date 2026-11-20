import type { Flag, InvoiceDetail, InvoiceUpdate } from "@/lib/api";
import { inputValue, SECTIONS } from "@/lib/fields";

import { EditableField } from "./editable-field";

type Props = {
  invoice: InvoiceDetail;
  flags: Map<string, Flag[]>;
  readOnly: boolean;
  onSave: (update: InvoiceUpdate) => void;
  onConfirm: (path: string) => void;
  children?: React.ReactNode; // the line items, placed between Invoice and Totals
};

export function HeaderFields({ invoice, flags, readOnly, onSave, onConfirm, children }: Props) {
  return (
    <div className="space-y-7">
      {SECTIONS.map((section) => (
        <div key={section.title} className="space-y-7">
          {section.title === "Totals" && children}
          <section>
            <h3 className="mb-3 font-display text-lg">{section.title}</h3>
            <div className="grid grid-cols-2 gap-x-5 gap-y-4">
              {section.fields.map((def) => (
                <EditableField
                  key={def.column}
                  def={def}
                  value={inputValue(invoice, def.column)}
                  flags={flags.get(def.path) ?? []}
                  readOnly={readOnly}
                  onSave={(value) => onSave({ [def.column]: value })}
                  onConfirm={onConfirm}
                />
              ))}
            </div>
          </section>
        </div>
      ))}
    </div>
  );
}