import Image from "next/image";
import { Check } from "lucide-react";

const features = [
    "Identify key clauses and obligations instantly.",
    "Understand complex legal jargon in plain English.",
    "Accelerate your document review process by up to 80%.",
];

export default function Summarization() {
  return (
    <section id="summarization" className="py-16 sm:py-24">
      <div className="container mx-auto px-4">
        <div className="grid items-center gap-12 md:grid-cols-2">
          <div className="order-2 md:order-1">
            <div className="mx-auto max-w-xl">
              <h2 className="font-headline text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
                AI Document Summarization
              </h2>
              <p className="mt-6 text-xl text-foreground/80">
                Stop drowning in paperwork. Arin’s advanced AI reads your legal documents and delivers a clear, concise summary in seconds. Focus on what matters, not on manual reading.
              </p>
              <ul className="mt-8 space-y-4">
                {features.map((feature, index) => (
                  <li key={index} className="flex items-start">
                    <Check className="h-6 w-6 shrink-0 text-primary mr-3 mt-1" />
                    <span className="text-lg text-foreground/80">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="order-1 md:order-2">
            <Image
              src="https://placehold.co/600x400.png"
              alt="Summarization feature illustration"
              width={600}
              height={400}
              className="rounded-lg shadow-xl"
              data-ai-hint="document summary"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
