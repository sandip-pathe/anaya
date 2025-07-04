import Logo from "@/components/landing/logo";
import Link from "next/link";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t border-border bg-secondary">
      <div className="container mx-auto px-4 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
        
        {/* Left: Logo */}
        <Logo />

        {/* Center: Copyright */}
        <p className="text-sm text-foreground/60">
          &copy; {currentYear} Arin. All rights reserved.
        </p>

        {/* Right: Links */}
        <div className="flex items-center gap-4">
          <Link
            href="https://linkedin.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:opacity-80"
          >
            <svg className="h-5 w-5 fill-foreground" viewBox="0 0 24 24">
              <path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V24h-4V8zm7.5 0h4v2.59h.06c.56-1.06 1.93-2.17 3.97-2.17C21.23 8.42 22 11 22 15.1V24h-4v-8.18c0-1.95-.03-4.47-2.72-4.47-2.72 0-3.13 2.12-3.13 4.32V24h-4V8z" />
            </svg>
          </Link>

          <Link
            href="https://x.com"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:opacity-80"
          >
            <svg className="h-5 w-5 fill-foreground" viewBox="0 0 24 24">
              <path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.3 4.3 0 001.88-2.37c-.82.5-1.73.86-2.7 1.06A4.27 4.27 0 0016.11 4c-2.36 0-4.27 1.91-4.27 4.27 0 .33.04.65.11.96A12.13 12.13 0 013 5.16a4.26 4.26 0 001.32 5.7c-.67-.02-1.3-.2-1.85-.5v.05c0 2.1 1.5 3.86 3.5 4.27a4.3 4.3 0 01-1.84.07 4.27 4.27 0 004 2.97A8.58 8.58 0 012 19.54a12.07 12.07 0 006.55 1.92c7.87 0 12.18-6.52 12.18-12.18 0-.19-.01-.39-.02-.58A8.73 8.73 0 0024 5.1a8.45 8.45 0 01-2.54.7z" />
            </svg>
          </Link>
        </div>
      </div>

      {/* Bottom links */}
      <div className="container mx-auto px-4 pb-6 flex flex-col md:flex-row items-center justify-between gap-4 border-t border-border pt-4">
        <div className="flex items-center gap-4 text-sm">
          <Link href="/privacy-policy" className="hover:underline">
            Privacy Policy
          </Link>
          <Link href="/terms-of-service" className="hover:underline">
            Terms of Service
          </Link>
        </div>
      </div>
    </footer>
  );
}
