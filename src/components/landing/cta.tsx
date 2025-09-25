"use client";

import WishlistButton from "../WishlistButton";

export default function Cta() {
  return (
    <section id="cta" className="bg-secondary py-6 sm:py-24">
      <div className="container mx-auto px-4 text-center">
        <div className="mx-auto max-w-3xl">
          <h2 className="font-headline text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            Get Extra Time for Strategies & Sharpening Your Thinking.
          </h2>
          <WishlistButton className="mt-8" />
        </div>
      </div>
    </section>
  );
}
