"use client";

import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import { FaWhatsapp } from "react-icons/fa";
import { Button } from "../ui/button";
import { useRouter } from "next/navigation";

const faqs = [
  {
    question: "How is this different from other legal AI tools?",
    answer:
      "Most legal AI products are SaaS tools that require you to upload your sensitive data to their servers. Anaya is different. We provide a secure AI layer that operates on top of your firm's existing data, wherever it resides. You get the power of custom-built AI without compromising on security or control.",
  },
  {
    question: "Do we need a technical team to build agents and workflows?",
    answer:
      "No. Anaya is designed for legal professionals. We provide templates for common legal workflows, and our intuitive interface allows you to create and customize AI agents with no coding required. Our team will also work with you during onboarding to set up your initial workflows. Having a technical team can be beneficial for more complex integrations, but it's not a requirement.",
  },
  {
    question: "What kind of data can Anaya work with?",
    answer:
      "Anaya can connect to a wide range of data sources, including popular document management systems, email archives, and internal databases. It supports various file formats, including PDF, Word, and more. If you have specific data sources in mind, we can discuss integration options during our consultation.",
  },
];

export default function Faq() {
  const router = useRouter();
  return (
    <section id="faq" className="py-16 sm:py-24 bg-background">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center mb-6">
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
                className="border-b-2 hover:border-black border-transparent hover:border-b-2"
              >
                <AccordionTrigger className="text-left text-lg md:text-xl md:font-semibold text-gray-900 hover:no-underline">
                  <div className="flex justify-between items-center w-full">
                    <span>{faq.question}</span>
                  </div>
                </AccordionTrigger>
                <AccordionContent className="mt-2 text-base text-gray-600">
                  {faq.answer}
                </AccordionContent>
              </AccordionItem>
            ))}

            <AccordionItem value="item-button" className="border-0">
              <AccordionTrigger className="text-left text-lg md:text-xl md:font-semibold text-gray-900 hover:no-underline">
                <div className="flex justify-between items-center w-full">
                  <span>Ask Your Own Question</span>
                </div>
              </AccordionTrigger>
              <AccordionContent>
                <div className="flex items-center justify-start mr-4 space-x-4 mt-4">
                  {/* Contact Us Button */}
                  <Button
                    variant="outline"
                    size="lg"
                    onClick={() => {
                      router.push("/subscribe");
                    }}
                    className="hover:bg-black hover:text-white gap-2 mt-4 text-base flex-1"
                  >
                    Contact Us
                  </Button>

                  {/* WhatsApp Button */}
                  <Button
                    variant="outline"
                    size="lg"
                    onClick={() => {
                      window.open("https://wa.me/+918767394523", "_blank");
                    }}
                    className="hover:bg-green-600 hover:text-white gap-2 mt-4 text-base flex-1 text-green-600"
                  >
                    <FaWhatsapp size={20} />
                    WhatsApp
                  </Button>
                </div>
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
    </section>
  );
}
