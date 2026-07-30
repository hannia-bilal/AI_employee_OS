import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Employee OS — Your Digital Workforce",
  description:
    "AI-powered business operating system. Replace repetitive office work with intelligent AI agents that handle emails, CRM, quotations, invoices, and more.",
  keywords:
    "AI, business automation, CRM, email assistant, quotation generator, invoice, digital workforce",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" data-scroll-behavior="smooth">
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}
