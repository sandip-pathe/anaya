import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "@/components/ui/toaster";
import { ThemeProvider } from "@/components/theme-provider";

const title = "Anaya";
const description = `Anaya provides an AI-powered platform for legal professionals to 
automate document review, streamline contract analysis, and build custom legal workflows. 
Our secure, on-premise solution turns your firm's data into a private intelligence hub.`;
const url = "https://anaya.legal";
const imageUrl =
  "https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/demo.png";

export const metadata: Metadata = {
  metadataBase: new URL(url),
  title: {
    default: title,
    template: `%s | Anaya`,
  },
  description,
  keywords: [
    "AI for law firms",
    "legal tech software",
    "contract lifecycle management",
    "legal workflow automation",
    "e-discovery solutions",
    "legal document analysis",
    "AI-powered legal research",
    "AI Layer",
    "Ai factory",
    "Legal tech",
    "Automate high-volume tasks",
    "Anaya is a secure AI layer",
  ],
  authors: [{ name: "The Anaya Team", url }],
  creator: "The Anaya Team",
  openGraph: {
    type: "website",
    locale: "en_US",
    url,
    title,
    description,
    siteName: title,
    images: [
      {
        url: imageUrl,
        width: 1200,
        height: 630,
        alt: "An illustration of the Anaya application interface for summarization head",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title,
    description,
    images: [imageUrl],
    creator: "@Anaya_ai",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  // ✅ Reuse metadata values for Schema
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: title,
    applicationCategory: "LegalTech",
    description,
    operatingSystem: "Web",
    offers: {
      "@type": "Offer",
      price: "0",
      priceCurrency: "USD",
    },
    url,
    publisher: {
      "@type": "Organization",
      name: title,
    },
  };

  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@700&family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600;700&display=swap"
          rel="stylesheet"
        />

        {/* ✅ JSON-LD Schema injected safely */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
        />
      </head>
      <body className="font-body antialiased">
        <ThemeProvider
          attribute="class"
          forcedTheme="light"
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
