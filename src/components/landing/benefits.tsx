"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, UserCheck } from "lucide-react";
import { RiFlashlightFill } from "react-icons/ri";
import { HiMiniPencilSquare } from "react-icons/hi2";
import { FaListCheck } from "react-icons/fa6";
import { FiShare2 } from "react-icons/fi";

const benefits = [
  {
    icon: <CheckCircle2 className="h-8 w-8 text-blue-600" />,
    title: "Accurate Case Insights",
    description:
      "Get precise, citation-backed summaries of your documents, so you understand key points instantly.",
  },
  {
    icon: <RiFlashlightFill className="h-8 w-8 text-blue-600" />,
    title: "Quick Skim & Review",
    description:
      "Scan contracts, judgments, or filings in minutes without missing critical clauses or obligations.",
  },
  {
    icon: <HiMiniPencilSquare className="h-8 w-8 text-blue-600" />,
    title: "Drafting Support",
    description:
      "Use extracted clauses and obligations to streamline drafting and review, reducing manual work.",
  },
  {
    icon: <FaListCheck className="h-8 w-8 text-blue-600" />,
    title: "Plain English Summaries",
    description:
      "Turn complex legal language into clear explanations, making it easy to act on insights.",
  },
  {
    icon: <FiShare2 className="h-8 w-8 text-blue-600" />,
    title: "Shareable & Collaborative",
    description:
      "Export summaries as PDFs or links, so colleagues or clients can access insights instantly.",
  },
  {
    icon: <UserCheck className="h-8 w-8 text-blue-600" />,
    title: "Secure & Private",
    description:
      "All processing is confidential — documents stay with you unless you choose otherwise.",
  },
];

export default function Benefits() {
  return (
    <section className="py-16 sm:py-24">
      <div className="container mx-auto px-4 max-w-4xl">
        <div className="items-center justify-center grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => (
            <Card
              key={index}
              className="text-center bg-secondary border-none rounded-xl shadow-md hover:shadow-lg transition-all duration-300 "
            >
              <CardHeader>
                <div className="flex justify-center mb-2">{benefit.icon}</div>
                <CardTitle className="text-xl font-semibold text-gray-700">
                  {benefit.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-500">{benefit.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
