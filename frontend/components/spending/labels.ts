const CATEGORY_LABELS: Record<string, string> = {
  stock: "Stock purchases",
  shipping: "Shipping",
  repairs: "Repairs",
  utilities: "Utilities",
  cleaning: "Cleaning",
  other: "Other",
};

export function categoryLabel(key: string): string {
  return CATEGORY_LABELS[key] ?? key[0].toUpperCase() + key.slice(1);
}

export function monthLabel(month: string): string {
  const [year, number] = month.split("-").map(Number);
  return new Intl.DateTimeFormat("en-IE", { month: "short", year: "numeric" }).format(new Date(year, number - 1, 1));
}