"use client"

import { Button } from "@/components/ui/button";
import { EarlyAccessDialog } from "@/components/landing/early-access-dialog";

export default function Header() {
  return (
    <section className="py-20 text-center sm:py-32">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl">
          <h1 className="font-headline text-4xl font-bold tracking-tight text-foreground sm:text-5xl lg:text-6xl">
            Tired of Wasting Hours Reading Legal Docs?
          </h1>
          <p className="mt-6 text-lg leading-8 text-foreground/80 sm:text-xl">
            Get AI-Powered Legal Summaries in Seconds.
          </p>
          <p className="mt-4 text-base text-foreground/60">
            Summarize contracts, case files, and legal documents — clear, concise, no legal jargon.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <EarlyAccessDialog>
              <Button size="lg">Get Early Access</Button>
            </EarlyAccessDialog>
          </div>
        </div>
      </div>
    </section>
  );
}
