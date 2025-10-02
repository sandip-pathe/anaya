"use client";

import * as React from "react";
import Logo from "@/components/landing/logo";
import CalendlyEmbed from "@/components/calendly";
import { useRouter } from "next/navigation";

export default function EarlyAccessPage() {
  const router = useRouter();

  const [loading, setLoading] = React.useState(true);
  const [showSuccessButton, setShowSuccessButton] = React.useState(false);

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col lg:flex-row">
      {/* Left Side: Form + Calendly */}
      <div className="flex-1 flex flex-col justify-center px-6 py-12 lg:py-24 bg-white">
        <div className="max-w-lg w-full mx-auto space-y-6">
          {/* Logo */}
          <div className="flex justify-between items-center">
            <Logo />
            {/* Back Button */}
            <button
              onClick={() => router.push("/")}
              className="text-md text-gray-600 hover:text-gray-900 underline"
            >
              ← Back
            </button>
          </div>

          {/* Heading */}
          <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 text-center">
            Book a Demo & Join Early Access
          </h1>
          <p className="text-gray-600 text-center">
            Get priority access to our AI Factory platform and see it in action.
          </p>

          {/* Calendly Widget */}
          <div className="mt-6 w-full">
            <div className="relative w-full min-h-[600px]">
              {/* Custom Loader */}
              {loading && (
                <div className="absolute inset-0 flex items-center justify-center bg-white z-10">
                  <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent"></div>
                </div>
              )}
              <div className="overflow-hidden">
                <CalendlyEmbed
                  onLoad={() => setLoading(false)}
                  onEventScheduled={() => setShowSuccessButton(true)}
                />

                {showSuccessButton && (
                  <div className="mt-6 flex justify-center">
                    <button
                      onClick={() => router.push("/")}
                      className="px-6 py-3 bg-primary text-white font-semibold rounded-lg shadow hover:bg-primary/90"
                    >
                      🎉 Thanks for booking! Go Back Home
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side: Testimonial / Image */}
      <div className="hidden lg:flex flex-1 flex-col justify-center items-center relative bg-gradient-to-b from-black to-black text-white p-12">
        <div className="max-w-md text-center space-y-8 z-10">
          <h2 className="text-4xl font-bold select-none font-headline tracking-tight">
            Join the Innovation Wave
          </h2>
          <p className="text-7xl text-blue-200">
            ❝Innovation distinguishes between a leader and a follower.❞
          </p>
          <p className="text-blue-100 italic font-medium">– Steve Jobs</p>
        </div>
        {/* Optional: subtle background decoration */}
        <div className="absolute inset-0 bg-gradient-to-tr from-purple-800 via-blue-900 to-black opacity-20"></div>
      </div>
    </div>
  );
}
