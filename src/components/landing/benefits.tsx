"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BsDatabaseFillLock, BsLightningFill } from "react-icons/bs";
import { RiFunctionAddLine } from "react-icons/ri";
import { LiaNetworkWiredSolid } from "react-icons/lia";
import { MdAutoGraph } from "react-icons/md";
import { IoShieldCheckmark } from "react-icons/io5";

// Renamed and updated benefit titles and descriptions for the new messaging
const benefits = [
  {
    icon: <LiaNetworkWiredSolid className="h-8 w-8 text-blue-600" />,
    title: "Smarter Workflows",
    description:
      "Automate high-volume tasks. Free up your legal talent to focus on high-impact strategy and winning cases.",
  },
  {
    icon: <MdAutoGraph className="h-8 w-8 text-blue-600" />,
    title: "Scalable Intelligence",
    description:
      "Your firm's intelligence grows with every case. Our AI agents continuously learn from your data, making your entire firm smarter.",
  },
  {
    icon: <RiFunctionAddLine className="h-8 w-8 text-blue-600" />,
    title: "Your Own Agents",
    description:
      "Move beyond one-size-fits-all software. Build bespoke AI agents that understand your firm's specific language and practice.",
  },
  {
    icon: <IoShieldCheckmark className="h-8 w-8 text-blue-600" />,
    title: "Secure by Design",
    description:
      "Your data stays yours, always. We provide the intelligence layer; you maintain complete control and security.",
  },
  {
    icon: <BsDatabaseFillLock className="h-8 w-8 text-blue-600" />,
    title: "Future-Proof Your Firm",
    description:
      "Build a sustainable competitive advantage with a flexible, ever-evolving platform that keeps you at the forefront of legal innovation.",
  },
  {
    icon: <BsLightningFill className="h-8 w-8 text-blue-600" />,
    title: "Business Intelligence",
    description:
      "Unlock strategic insights hidden in your data. Identify trends, manage risks, and make data-driven decisions.",
  },
];

export default function Benefits() {
  return (
    // Adjusted padding
    <section id="benefits" className="bg-gray-100 py-16 dark:bg-black sm:py-24">
      {/* Increased max-width for larger screens */}
      <div className="container mx-auto max-w-6xl px-4">
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 md:grid-cols-3 sm:gap-8 lg:gap-12">
          {benefits.map((benefit, index) => (
            <Card
              key={index}
              className="border-none bg-background p-4 text-center shadow-sm transition-shadow duration-300 hover:shadow-md"
            >
              <CardHeader>
                <div className="flex justify-center">{benefit.icon}</div>
                <CardTitle className="mt-4 text-lg font-semibold text-gray-800 dark:text-gray-200 sm:text-xl">
                  {benefit.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-600 dark:text-gray-400 sm:text-base">
                  {benefit.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
