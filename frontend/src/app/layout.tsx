import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NewsAI — AI-Native Business Intelligence",
  description: "AI-powered news platform with personalized briefings, interactive story arcs, and intelligent concierge. Transform how you consume business news.",
  keywords: "AI news, business intelligence, personalized newsroom, news navigator, story arc tracker",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
