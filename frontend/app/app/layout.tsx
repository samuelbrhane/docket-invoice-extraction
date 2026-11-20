import { AppHeader } from "@/components/app";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <AppHeader />
      <main className="mx-auto max-w-7xl px-6 py-10">{children}</main>
    </>
  );
}