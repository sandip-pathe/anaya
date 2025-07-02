"use client"

import * as React from "react"
import { Button } from "@/components/ui/button";
import Logo from "@/components/landing/logo";
import { Menu } from "lucide-react";
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet";
import { EarlyAccessDialog } from "@/components/landing/early-access-dialog";

const navLinks = [
  { label: "Try", href: "#" },
  { label: "Pricing", href: "#" },
  { label: "Security", href: "#" },
];

export default function Navbar() {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-14 items-center justify-between px-4">
        <Logo />

        <div className="hidden items-center gap-6 md:flex">
          <nav className="flex items-center gap-6">
            {navLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="text-sm font-medium text-muted-foreground transition-colors hover:text-foreground"
              >
                {link.label}
              </a>
            ))}
          </nav>
          <div className="flex items-center gap-2">
            <Button variant="ghost">Login</Button>
            <EarlyAccessDialog>
              <Button>Join The Wishlist</Button>
            </EarlyAccessDialog>
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
            <SheetContent side="right" className="w-[300px]">
              <div className="flex h-full flex-col">
                <div className="flex-1">
                  <Logo />
                  <nav className="mt-8 flex flex-col gap-6">
                    {navLinks.map((link) => (
                      <a
                        key={link.label}
                        href={link.href}
                        className="text-lg font-medium text-foreground"
                        onClick={() => setIsOpen(false)}
                      >
                        {link.label}
                      </a>
                    ))}
                  </nav>
                </div>
                <div className="mt-auto flex flex-col gap-2 border-t pt-6">
                  <Button variant="outline">Login</Button>
                  <EarlyAccessDialog>
                    <Button>Join The Wishlist</Button>
                  </EarlyAccessDialog>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
