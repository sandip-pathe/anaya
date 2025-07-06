import Logo from "@/components/landing/logo";
import Link from "next/link";
import WishlistOutlineButton from "../WishlistOutlineButton";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const navLinks = [
    { label: "Demo", href: "#demo" },
    { label: "Benefits", href: "#benefits" },
    { label: "Features", href: "#summarization" },
    { label: "About", href: "#" },
  ];

  return (
    <footer className="relative overflow-hidden bg-blue-950">
      <div className="relative container max-w-5xl mx-auto px-4 pt-16 flex justify-center">
        <div className="rounded-2xl text-foreground rounded-b-none bg-white backdrop-blur-md shadow-2xl shadow-blue-500/20 transform transition-transform duration-500 hover:scale-[1.02] p-8 w-full flex-wrap items-center gap-8">
          {/* Left: Heading & CTA */}
          <div className="flex-1 border-b-2 pb-8 border-black flex w-full flex-row justify-between items-center">
            <div>
              <h2 className="font-headline text-3xl sm:text-3xl font-bold tracking-tight">
                Save Hours
              </h2>
              <WishlistOutlineButton className="mt-6"/>
            </div>

            {/* Right: Logo & Links */}
            <div className="flex flex-col items-center gap-4">
              <Logo />
              <nav className="flex flex-col justify-center gap-x-6 gap-y-2 mt-4">
                {navLinks.map((link) => (
                  <Link
                    key={link.label}
                    href={link.href}
                    className="font-body text-sm text-muted-foreground transition-colors hover:text-foreground"
                  >
                    {link.label}
                  </Link>
                ))}
              </nav>
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
