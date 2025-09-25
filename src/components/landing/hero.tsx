"use client";

import WishlistButton from "../WishlistButton";

export default function Header() {
  return (
    <section className="py-20 text-center sm:py-32 bg-background">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl">
          <h1 className="font-headline text-5xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-[4.75rem] lg:leading-tight">
            Tired of Wasting Hours Reading Legal Docs?
          </h1>
          <div className="flex flex-row items-center justify-center space-x-3 mt-6 text-2xl font-semibold leading-8 text-gray-600">
            <p>Don’t Read.</p>
            <p>Understand.</p>
            <p>Anaya.</p>
          </div>
          <p className="mt-6 text-lg text-foreground/60">
            From contracts to case files — accurate, secure, and shareable
            important information in seconds.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <WishlistButton className="mt-8" />
          </div>
        </div>
      </div>
    </section>
  );
}

// Your Firm’s Private Intelligent Agents
// Your Data.
// Your Agents.
// Your AI.
// Deploy secure, firm-specific AI agents on your own cloud. Build and
// run agents tailored to your workflows, keep full control of your
// data, and leverage AI without ever sharing sensitive information
// outside your firm.
