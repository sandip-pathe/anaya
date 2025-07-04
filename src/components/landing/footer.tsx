import Logo from "@/components/landing/logo";
import Link from "next/link";
import { EarlyAccessDialog } from "./early-access-dialog";
import { Button } from "../ui/button";
import { MoveRight } from "lucide-react";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="relative overflow-hidden bg-blue-950">
      <div className="relative container max-w-5xl mx-auto px-4 pt-16 flex justify-center">
        <div className="rounded-2xl text-foreground rounded-b-none bg-white backdrop-blur-md shadow-2xl shadow-blue-500/20 transform transition-transform duration-500 hover:scale-[1.02] p-8 w-full flex-wrap items-center gap-8">
          {/* Left: Heading & CTA */}
          <div className="flex-1 border-b-2 pb-8 border-black flex width-full flex-row justify-between">
          <div>
            <h2 className="font-headline text-2xl sm:text-3xl font-bold tracking-tight">
              Build the best product experiences.
            </h2>
            <div className="mt-6">
            <EarlyAccessDialog>
              <Button variant="outline" className="border-2 border-foreground">
                <p className="text-base">Join The Wishlist</p>
                <MoveRight className="h-8 w-8 text-foreground" />
                </Button>
            </EarlyAccessDialog>
            </div>
          </div>

          {/* Right: Logo & Social */}
          <div className="flex flex-col items-center gap-4">
            <Logo />
            <div className="flex items-center gap-3">
              <Link
                href="https://linkedin.com"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:opacity-80"
              >
                <svg className="h-6 w-6 fill-foreground" viewBox="0 0 24 24">
                  <path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.5 8h4V24h-4V8zm7.5 0h4v2.59h.06c.56-1.06 1.93-2.17 3.97-2.17C21.23 8.42 22 11 22 15.1V24h-4v-8.18c0-1.95-.03-4.47-2.72-4.47-2.72 0-3.13 2.12-3.13 4.32V24h-4V8z" />
                </svg>
              </Link>

              <Link
                href="https://x.com"
                target="_blank"
                rel="noopener noreferrer"
                className="hover:opacity-80"
              >
                <svg className="h-6 w-6 fill-foreground" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.3 4.3 0 001.88-2.37c-.82.5-1.73.86-2.7 1.06A4.27 4.27 0 0016.11 4c-2.36 0-4.27 1.91-4.27 4.27 0 .33.04.65.11.96A12.13 12.13 0 013 5.16a4.26 4.26 0 001.32 5.7c-.67-.02-1.3-.2-1.85-.5v.05c0 2.1 1.5 3.86 3.5 4.27a4.3 4.3 0 01-1.84.07 4.27 4.27 0 004 2.97A8.58 8.58 0 012 19.54a12.07 12.07 0 006.55 1.92c7.87 0 12.18-6.52 12.18-12.18 0-.19-.01-.39-.02-.58A8.73 8.73 0 0024 5.1a8.45 8.45 0 01-2.54.7z" />
                </svg>
              </Link>
            </div>
          </div>
          </div>
          {/* Bottom: Links */}
          <div className="flex flex-col md:flex-row justify-between items-center w-full text-sm mt-4">
            <p className="text-foreground/60">&copy; {currentYear} Spur. All rights reserved.</p>
            <div className="flex items-center gap-4">
              <Link href="/privacy-policy" className="hover:underline">Privacy Policy</Link>
              <Link href="/terms-of-service" className="hover:underline">Terms of Service</Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
