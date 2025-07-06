"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { Button } from "../ui/button";
import { MoveRight } from "lucide-react";
import WishlistOutlineButton from "../WishlistOutlineButton";

const faqs = [
  {
    question: "Is this only for lawyers?",
    answer:
      "Yes — we’ve designed this tool specifically for legal documents. It’s not for general-purpose summarization.",
  },
  {
    question: "What documents does it support?",
    answer:
      "Currently PDF and Word files — contracts, agreements, memos, case files.",
  },
  {
    question: "How secure is this?",
    answer:
      "We never store your documents. They’re processed instantly and securely.",
  },
];

export default function Faq() {
  return (
    <section id="faq" className="py-16 sm:py-24 bg-[#fef9f4]">
      <div className="container mx-auto px-4">
      <div className="mx-auto max-w-3xl text-center mb-6">
          <h2 className="font-headline text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            Frequently Asked Questions
          </h2>
      </div>

        {/* Accordion */}
        <div className="mx-auto max-w-3xl">
          <Accordion type="single" collapsible className="w-full space-y-4">
            {faqs.map((faq, index) => (
              <AccordionItem
                key={index}
                value={`item-${index}`}
                className="border-b-2 hover:border-b hover:border-black border-transparent hover:border-b-2"
              >
                <AccordionTrigger className="text-left text-xl font-semibold text-gray-900 hover:no-underline">
                  <div className="flex justify-between items-center w-full">
                    <span>{faq.question}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="mt-2 text-base text-gray-600">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}

            <AccordionItem
              value="item-button"
              className="border-0"
            >
              <AccordionTrigger className="text-left text-xl font-semibold text-gray-900 hover:no-underline">
                  <div className="flex justify-between items-center w-full">
                    <span>Ask A Question</span>
                </div>
              </AccordionTrigger>
              <AccordionContent className="mt-2 text-base text-gray-600">
              <WishlistOutlineButton className="mt-4"/>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </section>
  );
}
