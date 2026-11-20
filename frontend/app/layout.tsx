import type { Metadata } from "next";
import { Atkinson_Hyperlegible, Courier_Prime, Young_Serif } from "next/font/google";

import "./globals.css";

const display = Young_Serif({
  subsets: ["latin"],
  weight: "400",
  variable: "--font-young-serif",
});

const sans = Atkinson_Hyperlegible({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-atkinson",
});

const figures = Courier_Prime({
  subsets: ["latin"],
  weight: ["400", "700"],
  variable: "--font-courier-prime",
});

export const metadata: Metadata = {
  title: "Docket · AI invoice processing for Sila Roasting Co.",
  description:
    "Upload a supplier invoice, watch the fields fill in, fix what the checks flag, and approve it into inventory.",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${display.variable} ${sans.variable} ${figures.variable}`}>
      <body>{children}</body>
    </html>
  );
}