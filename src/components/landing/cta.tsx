"use client";

import { useRouter } from "next/navigation";
import { Button } from "../ui/button";

export default function Cta() {
  const router = useRouter();
  return (
    <section id="cta" className="bg-secondary py-6 sm:py-24">
      <div className="container mx-auto px-4 text-center">
        <div className="mx-auto max-w-3xl">
          <h2 className="font-headline text-3xl sm:text-4xl font-bold tracking-tight text-foreground">
            Stop Buying Software. Start Building Intelligence.
          </h2>
          <Button
            size="lg"
            onClick={() => router.push(`https://app.anaya.legal`)}
            className={`bg-blue-950 hover:bg-black gap-2 hover:gap-4 text-base mt-6`}
          >
            <p>Talk to us</p>
            <p>➔</p>
          </Button>
        </div>
      </div>
    </section>
  );
}
