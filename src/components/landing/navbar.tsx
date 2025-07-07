"use client"

import * as React from "react"
import { Button } from "@/components/ui/button";
import Logo from "@/components/landing/logo";
import WishlistOutlineButton from "../WishlistOutlineButton";
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
  { label: "Try", href: "/subscribe" },
  { label: "Demo", href: "#demo" },
  { label: "Features", href: "#summarization" },
  { label: "FAQ", href: "#faq" },
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
                className="text-base font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </Link>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <WishlistOutlineButton/>
          </div>
        </div>

        <div className="md:hidden">
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon">
                <Menu className="h-6 w-6" />
                <span className="sr-only">Open menu</span>
              </Button>
            </SheetTrigger>
            {/* Fixed SheetContent structure */}
            <SheetContent side="right" className="w-[300px] flex flex-col">
              <SheetHeader className="text-left">
                <Logo />
                <SheetTitle className="sr-only">Menu</SheetTitle>
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
              
              {/* Buttons container moved to bottom */}
              <div className="mt-auto flex flex-col gap-2 border-t pt-6">
                <WishlistOutlineButton/>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}