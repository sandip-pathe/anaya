"use client";

import Image from "next/image";
import { Button } from "../ui/button";

export default function Demo() {
  return (
    <section
      id="demo"
      className="sm:py-16 py-8 bg-white dark:from-gray-900 dark:to-blue-900/20"
    >
      <div className="container mx-auto px-4">
        {/* Section Heading */}
        <div className="mx-auto max-w-3xl text-center mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-foreground dark:text-gray-100">
            Inside the AI Factory
          </h2>
          <p className="mt-2 text-sm sm:text-base text-muted-foreground dark:text-gray-300">
            Watch a live workflow — highlight risks, extract key data, and
            generate actionable insights in seconds.
          </p>
        </div>

        {/* Live Demo Badge */}
        <div className="mb-6 flex justify-center">
          <div className="inline-flex items-center space-x-2 px-3 py-1.5 sm:px-4 sm:py-2 bg-white rounded-full shadow-md">
            <div className="h-2.5 w-2.5 sm:h-3 sm:w-3 rounded-full bg-red-200 animate-pulse"></div>
            <span className="text-xs sm:text-sm font-medium text-foreground dark:text-gray-300">
              Live Demo
            </span>
          </div>
        </div>

        {/* Demo Window */}
        <div className="relative max-w-4xl mx-auto overflow-hidden rounded-xl sm:rounded-2xl border-2 sm:border-4 border-black/80 dark:border-gray-800 shadow-md sm:shadow-none">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 dark:from-blue-700/10 dark:to-purple-700/10"></div>
          <div className="relative bg-black dark:bg-gray-800">
            {/* Top Bar */}
            <div className="flex justify-center items-center p-1.5 sm:p-2 bg-gradient-to-r from-blue-600 to-purple-600">
              <div className="flex space-x-1 sm:space-x-1.5">
                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-red-400"></div>
                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-yellow-400"></div>
                <div className="w-2.5 h-2.5 sm:w-3 sm:h-3 rounded-full bg-green-400"></div>
              </div>
            </div>
            {/* Demo Image */}
            <Image
              src="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/0.png"
              alt="Anaya Agent Demo"
              width={1366}
              height={694}
              className="w-full h-auto object-contain cursor-pointer"
              data-ai-hint="app interface"
              onClick={() => window.open("https://app.anaya.legal", "_blank")}
            />
          </div>
        </div>

        {/* Demo Description / CTA */}
        <div className="mt-6 text-center max-w-2xl mx-auto">
          {/* Hidden on small screens */}
          <p className="hidden sm:block text-sm sm:text-md text-muted-foreground dark:text-gray-300 mb-4">
            Watch how a single workflow in the Anaya AI Factory can automate
            complex tasks. In this example, multiple AI agents collaborate on a
            set of documents. Imagine scaling this across dozens of workflows,
            all running in parallel, all tailored to your firm's unique
            processes.
          </p>
          <Button
            size="lg"
            variant="outline"
            onClick={() => window.open("https://app.anaya.legal", "_blank")}
            className="w-full sm:w-auto hover:bg-black hover:text-white gap-2 hover:gap-4 text-sm sm:text-base"
          >
            <span>⚡ Try it now</span>
            <span>➔</span>
          </Button>
        </div>
      </div>
    </section>
  );
}
