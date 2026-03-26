import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Algo Platform",
  description: "Algo trading platform V1"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
