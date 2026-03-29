import type { Metadata } from "next";
import "./globals.css";
import NavbarWrapper from "@/components/layout/NavbarWrapper";
import { ModalProvider } from "@/context/ModalContext";

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
      <body>
        <ModalProvider>
          <NavbarWrapper />
          {children}
        </ModalProvider>
      </body>
    </html>
  );
}
