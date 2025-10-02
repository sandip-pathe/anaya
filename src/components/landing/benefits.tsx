"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { BsDatabaseFillLock, BsLightningFill } from "react-icons/bs";
import { RiFunctionAddLine } from "react-icons/ri";
import { LiaNetworkWiredSolid } from "react-icons/lia";
import { MdAutoGraph } from "react-icons/md";
import { IoShieldCheckmark } from "react-icons/io5";
import { SiGitconnected } from "react-icons/si";

const benefits = [
  {
    icon: <LiaNetworkWiredSolid className="h-8 w-8 text-blue-600" />,
    title: "Smarter Workflows",
    description:
      "Stop repetitive tasks. Let your lawyers focus on strategy, argumentation, and client value.",
  },
  {
    icon: <MdAutoGraph className="h-8 w-8 text-blue-600" />,
    title: "Scalable Intelligence",
    description:
      "Unlimited AI agents running in parallel on your firm’s data. Grow capabilities without limits.",
  },
  {
    icon: <RiFunctionAddLine className="h-8 w-8 text-blue-600" />,
    title: "Your own Agents",
    description:
      "Design agents that reflect your workflows, culture, and priorities. Your AI works your way.",
  },
  {
    icon: <SiGitconnected className="h-8 w-8 text-blue-600" />,
    title: "Seamless Integration",
    description:
      "Connect to DMS, email, and workflow systems. Anaya agents operate within your tools without disruption.",
  },
  {
    icon: <IoShieldCheckmark className="h-8 w-8 text-blue-600" />,
    title: "Future-Proof Your Firm",
    description:
      "Flexible deployment, modular agents, and model choices ensure your firm evolves with AI securely.",
  },
  {
    icon: <BsLightningFill className="h-8 w-8 text-blue-600" />,
    title: "Business Intelligence",
    description:
      "Turn raw legal data into actionable dashboards, reports, and firm-wide insights.",
  },
];

export default function Benefits() {
  return (
    <section className="py-16 sm:py-24 bg-gray-100 dark:bg-black">
      <div className="container mx-auto px-4 max-w-5xl">
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8 lg:gap-12">
          {benefits.map((benefit, index) => (
            <Card
              key={index}
              className="text-center border-none bg-background shadow-sm p-0 hover:shadow-md transition-shadow duration-300"
            >
              <CardHeader>
                <div className="flex justify-center">{benefit.icon}</div>
                <CardTitle className="text-lg sm:text-xl font-semibold text-gray-800 dark:text-gray-200">
                  {benefit.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-sm sm:text-base text-gray-600 dark:text-gray-400">
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
