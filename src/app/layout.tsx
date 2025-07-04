import type { Metadata } from 'next';
import './globals.css';
import { Toaster } from "@/components/ui/toaster";
import { ThemeProvider } from '@/components/theme-provider';

const title = 'Arin | AI Legal Summarizer';
const description = 'AI-Powered Legal Summaries in Seconds. Save hours on document review with Arin, the AI assistant designed for legal professionals. Get clear, concise summaries of contracts, case files, and more.';
const url = 'https://arin.ai';

export const metadata: Metadata = {
  metadataBase: new URL(url),
  title: {
    default: title,
    template: `%s | Arin`,
  },
  description,
  keywords: [
    'legal tech', 
    'ai summarizer', 
    'legal documents', 
    'contract analysis', 
    'legal ai',
    'document review automation',
    'ai for lawyers'
  ],
  authors: [{ name: 'The Arin Team', url: url }],
  creator: 'The Arin Team',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url,
    title,
    description,
    siteName: title,
    images: [
      {
        url: 'https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/demo.png',
        width: 1200,
        height: 630,
        alt: 'An illustration of the Arin application interface for legal document summarization.',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title,
    description,
    images: ['https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/demo.png'],
    creator: '@arin_ai',
  },
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=League+Spartan:wght@700&family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600;700&display=swap" rel="stylesheet" />
      </head>
      <body className="font-body antialiased">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          {children}
          <Toaster />
        </ThemeProvider>
      </body>
    </html>
  );
}
