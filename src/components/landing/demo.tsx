"use client";

import Image from "next/image";
import { Button } from "../ui/button";

export default function Demo() {
  return (
    <section
      id="demo"
      className="bg-white py-16 dark:from-gray-900 dark:to-blue-900/20 sm:py-24"
    >
      <div className="container mx-auto px-4">
        {/* Section Heading */}
        <div className="mx-auto mb-12 max-w-3xl text-center">
          <h2 className="font-headline text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
            Inside the AI Factory
          </h2>
          <p className="mt-4 text-base text-muted-foreground dark:text-gray-300 sm:text-lg">
            Watch how a single workflow in the Anaya AI Factory can automate
            complex tasks.
          </p>
        </div>

        {/* Live Demo Badge - No changes needed, it's already responsive */}
        <div className="mb-8 flex justify-center">
          <div className="inline-flex items-center space-x-2 rounded-full bg-white px-3 py-1.5 shadow-md sm:px-4 sm:py-2">
            <div className="h-2.5 w-2.5 animate-pulse rounded-full bg-red-200 sm:h-3 sm:w-3"></div>
            <span className="text-xs font-medium text-foreground dark:text-gray-300 sm:text-sm">
              Live Demo
            </span>
          </div>
        </div>

        {/* Demo Window - Increased max-width on larger screens */}
        <div className="relative mx-auto max-w-4xl overflow-hidden rounded-xl border-2 border-black/80 shadow-md dark:border-gray-800 sm:rounded-2xl sm:border-4 lg:max-w-6xl">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 dark:from-blue-700/10 dark:to-purple-700/10"></div>
          <div className="relative bg-black dark:bg-gray-800">
            {/* Top Bar - No changes needed */}
            <div className="flex items-center justify-center bg-gradient-to-r from-blue-600 to-purple-600 p-1.5 sm:p-2">
              <div className="flex space-x-1 sm:space-x-1.5">
                <div className="h-2.5 w-2.5 rounded-full bg-red-400 sm:h-3 "></div>
                <div className="h-2.5 w-2.5 rounded-full bg-yellow-400 sm:h-3 "></div>
                <div className="h-2.5 w-2.5 rounded-full bg-green-400  sm:h-3"></div>
              </div>
            </div>
            {/* Demo Image */}
            <Image
              src="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/0.png"
              alt="A demonstration of the Anaya AI platform analyzing legal documents."
              width={1366}
              height={694}
              className="h-auto w-full cursor-pointer object-contain"
              data-ai-hint="app interface"
              onClick={() => window.open("https://app.anaya.legal", "_blank")}
            />
          </div>
        </div>

        {/* Demo Description / CTA */}
        <div className="mx-auto mt-8 max-w-3xl text-center lg:mt-12">
          {/* Made this paragraph visible on medium screens and up */}
          <p className="hidden text-base text-muted-foreground dark:text-gray-300 md:block">
            In this example, multiple AI agents—a summarizer, a key-data
            extractor, and a risk-highlighter—collaborate on a set of documents.{" "}
            <span className="hidden md:inline">
              Imagine scaling this across dozens of workflows, all running in
              parallel, all tailored to your firm's unique processes.
            </span>
          </p>
          <Button
            size="lg"
            variant="outline"
            onClick={() => window.open("https://app.anaya.legal", "_blank")}
            className="mt-6 w-full gap-2 text-sm hover:bg-black hover:text-white hover:gap-4 sm:w-auto sm:text-base"
          >
            <span>⚡ See how it works</span>
            <span>➔</span>
          </Button>
        </div>
      </div>
    </section>
  );
}
