export const APP_LINKS = [
  { href: "/app", label: "Process" },
  { href: "/app/invoices", label: "Invoices" },
  { href: "/app/inventory", label: "Inventory" },
  { href: "/app/spending", label: "Spending" },
];

export function isActive(pathname: string, href: string): boolean {
  return href === "/app" ? pathname === "/app" : pathname.startsWith(href);
}