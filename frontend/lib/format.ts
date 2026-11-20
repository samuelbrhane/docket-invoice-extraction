/** Display helpers. The API sends amounts as decimal strings so nothing is lost to floating point. */

type Amount = string | number | null | undefined;

const EMPTY = "—";
const moneyFormats = new Map<string, Intl.NumberFormat>();

function toNumber(value: Amount): number | null {
  if (value === null || value === undefined || value === "") return null;
  const number = typeof value === "number" ? value : Number(value);
  return Number.isFinite(number) ? number : null;
}

export function money(value: Amount, currency: string | null = "EUR"): string {
  const number = toNumber(value);
  if (number === null) return EMPTY;
  const code = currency || "EUR";
  if (!moneyFormats.has(code)) {
    moneyFormats.set(code, new Intl.NumberFormat("en-IE", { style: "currency", currency: code }));
  }
  return moneyFormats.get(code)!.format(number);
}

/** 120.000 becomes 120, 3.500 becomes 3.5 */
export function quantity(value: Amount): string {
  const number = toNumber(value);
  if (number === null) return EMPTY;
  return new Intl.NumberFormat("en-IE", { maximumFractionDigits: 3 }).format(number);
}

/** At least two decimals, up to four: 0.0350 becomes 0.035 */
export function unitPrice(value: Amount): string {
  const number = toNumber(value);
  if (number === null) return EMPTY;
  return new Intl.NumberFormat("en-IE", { minimumFractionDigits: 2, maximumFractionDigits: 4 }).format(number);
}

export function percent(value: Amount): string {
  const number = toNumber(value);
  return number === null ? EMPTY : `${new Intl.NumberFormat("en-IE", { maximumFractionDigits: 1 }).format(number)}%`;
}

export function usd(value: Amount): string {
  const number = toNumber(value);
  if (number === null) return EMPTY;
  if (number === 0) return "$0.00";
  return `$${number < 0.01 ? number.toFixed(4) : number.toFixed(2)}`;
}

export function shortDate(value: string | null | undefined): string {
  if (!value) return EMPTY;
  const date = new Date(value.length === 10 ? `${value}T00:00:00` : value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat("en-IE", { day: "numeric", month: "short", year: "numeric" }).format(date);
}

export function fileSize(bytes: number): string {
  return bytes < 1024 * 1024 ? `${Math.max(1, Math.round(bytes / 1024))} KB` : `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}