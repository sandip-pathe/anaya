"use client"

import * as React from "react"
import { Button } from "@/components/ui/button";
import Logo from "@/components/landing/logo";
import { Menu } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";
import Link from "next/link";

const navLinks = [
  { label: "Demo", href: "#demo" },
  { label: "Benefits", href: "#benefits" },
  { label: "Features", href: "#summarization" },
  { label: "FAQ", href: "#faq" },
  { label: "Try", href: "/subscribe" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <header className="sticky top-0 z-50 w-full bg-background/95 backdrop-blur-sm">
      <div className="container mx-auto flex h-14 items-center justify-between px-4">
        <Logo />
        <div className="hidden items-center gap-6 md:flex">
          <nav className="flex items-center gap-6">
            {navLinks.map((link) => (
              <Link
                key={link.label}
                href={link.href}
                className="font-body text-base font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="md:hidden">
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="h-6 w-6" />
                <span className="sr-only">Open menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[300px]">
              <div className="flex h-full flex-col">
                <div className="flex-1">
                  <SheetHeader className="p-0 text-left">
                    <SheetTitle>
                      <Logo />
                    </SheetTitle>
                  </SheetHeader>
                  <nav className="mt-8 flex flex-col gap-6">
                    {navLinks.map((link) => (
                      <Link
                        key={link.label}
                        href={link.href}
                        className="text-lg font-medium text-foreground"
                        onClick={() => setIsOpen(false)}
                      >
                        {link.label}
                      </Link>
                    ))}
                  </nav>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
