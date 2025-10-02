"use client";

import { Button } from "../ui/button";

export default function Header() {
  return (
    <section className="min-h-screen flex items-center justify-center bg-background">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="font-headline text-4xl sm:text-6xl lg:text-[4.75rem] lg:leading-tight font-bold tracking-tight text-foreground">
            Your Firm’s Private Intelligent Agents
          </h1>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-4 my-8 text-xl sm:text-2xl font-body leading-8 text-gray-600">
            <p>Your Data.</p>
            <p>Your Workflows.</p>
            <p>Your Competitive Edge.</p>
          </div>

          <div className="text-base p-6 bg-secondary rounded-2xl shadow-sm sm:text-lg text-foreground/60 sm:px-12 sm:py-8">
            Anaya is a secure AI layer that integrates directly with your firm's
            existing data. Transform decades of case files, contracts, and
            internal knowledge into a powerful, proprietary intelligence engine.
            Build and deploy unlimited AI agents to automate any workflow—from
            litigation prep to contract analysis—without ever sending sensitive
            data outside your walls
          </div>

          <div className="mt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              size="lg"
              className="bg-blue-950 hover:bg-black gap-2 hover:gap-4 text-base w-full sm:w-auto"
            >
              <span>See how it works</span>
              <span>➔</span>
            </Button>
            <Button
              size="lg"
              className="bg-black hover:bg-black gap-2 hover:gap-4 text-base w-full sm:w-auto"
            >
              <span>Request Demo</span>
              <span>➔</span>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
