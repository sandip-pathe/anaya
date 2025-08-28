import Logo from "@/components/landing/logo";
import Link from "next/link";
import WishlistOutlineButton from "../WishlistOutlineButton";
import React from "react";

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
        <div className="rounded-2xl rounded-b-none bg-white backdrop-blur-md shadow-2xl shadow-blue-500/20 transform transition-transform duration-500 hover:scale-[1.02] p-8 w-full">
          {/* Top Section */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b-2 pb-8 border-black">
            {/* Left: Heading & CTA */}
            <div className="mb-8 md:mb-0">
              <h2 className="font-headline text-3xl sm:text-3xl font-bold tracking-tight">
                Save Hours
              </h2>
              <WishlistOutlineButton className="mt-6" />
            </div>

            {/* Right: Logo & Links */}
            <div className="flex flex-col md:items-end">
              <Logo />
              <nav className="flex flex-wrap justify-center gap-x-4 gap-y-2 md:justify-end">
                {navLinks.map((link, index) => (
                  <React.Fragment key={link.label}>
                    <Link
                      href={link.href}
                      className="font-body text-sm text-muted-foreground transition-colors hover:text-foreground whitespace-nowrap"
                    >
                      {link.label}
                    </Link>
                    {index < navLinks.length - 1 && (
                      <span className="hidden md:inline text-muted-foreground">
                        --
                      </span>
                    )}
                  </React.Fragment>
                ))}
              </nav>
            </div>
          </div>

          {/* Bottom: Copyright & Legal Links */}
          <div className="flex flex-col md:flex-row justify-between items-center w-full text-sm mt-4 gap-4">
            <p className="text-foreground/60 order-2 md:order-1">
              &copy; {currentYear}{" "}
              <a className="hover:underline cursor-pointer" href="#">
                Anaya.
              </a>{" "}
              All rights reserved.
            </p>
            <div className="flex items-center gap-4 order-1 md:order-2">
              <Link
                href="/privacy-policy"
                className="hover:underline whitespace-nowrap"
              >
                Privacy Policy
              </Link>
              <Link
                href="/terms-of-service"
                className="hover:underline whitespace-nowrap"
              >
                Terms of Service
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
