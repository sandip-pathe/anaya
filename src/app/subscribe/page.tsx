"use client";

import * as React from "react";
import { useToast } from "@/hooks/use-toast";
import Logo from "@/components/landing/logo";
import CalendlyEmbed from "@/components/calendly";

export default function EarlyAccessPage() {
  const { toast } = useToast();

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col lg:flex-row">
      {/* Left Side: Form + Calendly */}
      <div className="flex-1 flex flex-col justify-center px-6 py-12 lg:py-24 bg-white">
        <div className="max-w-lg w-full mx-auto space-y-6">
          {/* Logo */}
          <div className="flex justify-center">
            <Logo />
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
            <div className="overflow-hidden">
              <CalendlyEmbed />
            </div>
          </div>
        </div>
      </div>

      {/* Right Side: Testimonial / Image */}
      <div className="hidden lg:flex flex-1 flex-col justify-center items-center relative bg-gradient-to-b from-black to-black text-white p-12">
        <div className="max-w-md text-center space-y-6 z-10">
          <h2 className="text-4xl font-bold tracking-tight">
            Join the Innovation Wave
          </h2>
          <p className="text-lg text-blue-200">
            "Being an early adopter gave us a competitive edge we couldn't have
            gotten anywhere else."
          </p>
          <p className="text-blue-100 italic font-medium">
            - Sarah K., Product Director at TechCorp
          </p>
        </div>

        {/* Optional: subtle background decoration */}
        <div className="absolute inset-0 bg-gradient-to-tr from-purple-800 via-blue-900 to-black opacity-20"></div>
      </div>
    </div>
  );
}
