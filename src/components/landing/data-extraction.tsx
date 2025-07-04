import Image from "next/image";
import { Check } from "lucide-react";

const features = [
    "Automatically extract names, dates, amounts, and jurisdictions.",
    "Visualize key data points in easy-to-understand charts.",
    "Export extracted data for further analysis or reporting.",
];

export default function DataExtraction() {
  return (
    <section id="data-extraction" className="py-16 sm:py-24 bg-secondary">
      <div className="container mx-auto px-4">
        <div className="grid items-center gap-12 md:grid-cols-2">
          <div>
            <Image
              src="https://placehold.co/600x400.png"
              alt="Data extraction feature illustration"
              width={600}
              height={400}
              className="rounded-lg shadow-xl"
              data-ai-hint="data visualization chart"
            />
          </div>
          <div className="mx-auto max-w-xl">
            <h2 className="font-headline text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            Essential Insights Fast
            </h2>
            <p className="mt-6 text-xl text-foreground/80">
              Go beyond summaries. Arin identifies and extracts critical data points from your documents, presenting them in a structured and visual format. Never miss a deadline or key piece of information again.
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
      </div>
    </section>
  );
}
