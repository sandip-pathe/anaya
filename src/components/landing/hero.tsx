"use client";

import { useRouter } from "next/navigation";
import { Button } from "../ui/button";

export default function Header() {
  const router = useRouter();
  return (
    <section className="flex min-h-screen items-center justify-center bg-background px-4 py-20 sm:px-6 lg:px-8">
      <div className="container mx-auto">
        <div className="mx-auto max-w-5xl text-center">
          <h1 className="font-headline text-4xl font-bold tracking-tight text-foreground sm:text-6xl lg:text-[4.75rem] lg:leading-tight">
            Your Firm’s Private Intelligent Agents
          </h1>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-2 sm:gap-4 my-8 text-xl sm:text-2xl font-body leading-8 text-gray-600">
            <p>Your Data.</p>
            <p>Your Workflows.</p>
            <p>Your Competitive Edge.</p>
          </div>

          <div className="text-base hidden md:flex p-6 bg-secondary hover:shadow-lg rounded-2xl shadow-sm sm:text-lg text-foreground/60 sm:px-12 sm:py-8">
            Anaya is a secure AI layer that integrates directly with your firm's
            existing data. Transform decades of case files, contracts, and
            internal knowledge into a powerful, proprietary intelligence engine.
            Build and deploy unlimited AI agents to automate any workflow—from
            litigation prep to contract analysis—without ever sending sensitive
            data outside your walls
          </div>

          <div className="mt-6 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Button
              variant="default"
              size="lg"
              onClick={() => router.push("/subscribe")}
              className={`hover:bg-black bg-primary hover:text-white gap-2 hover:gap-4 text-base mt-0`}
            >
              <p>Request Demo</p>
              <p>➔</p>
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => router.push("/subscribe")}
              className={`hover:bg-black hover:text-white gap-2 hover:gap-4 text-base mt-0`}
            >
              <p>Contact Us</p>
              <p>➔</p>
            </Button>
          </div>
        </div>
      </div>
    </section>
  );
}
