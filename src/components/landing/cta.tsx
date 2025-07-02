"use client"

import { Button } from "@/components/ui/button";
import { EarlyAccessDialog } from "@/components/landing/early-access-dialog";

export default function Cta() {
  return (
    <section id="cta" className="bg-secondary py-16 sm:py-24">
      <div className="container mx-auto px-4 text-center">
        <h2 className="font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
          Join Our Early Access Program
        </h2>
        <p className="mt-4 text-lg leading-6 text-foreground/80">
          Be among the first to test CLAIR and save hours every week.
        </p>
        <div className="mt-8">
          <EarlyAccessDialog>
            <Button size="lg">Request Early Access</Button>
          </EarlyAccessDialog>
        </div>
        <p className="mt-4 text-sm text-foreground/60">
          Spaces are limited — priority given to practicing legal professionals.
        </p>
      </div>
    </section>
  );
}
