// DataExtraction.tsx
import Image from "next/image";

const features = [
  "Automatically extract names, dates, amounts, and jurisdictions.",
  "Visualize key data points in easy-to-understand charts.",
  "Export extracted data for further analysis or reporting.",
];

export default function DataExtraction() {
  return (
    <section id="data-extraction" className="py-12 sm:py-16 md:py-24 bg-background dark:from-gray-800 dark:to-gray-900">
      <div className="container mx-auto px-4 sm:px-6">
        <div className="grid items-center gap-12 md:gap-12 md:grid-cols-2">
          <div className="order-1 md:order-1">
            <div className="relative max-w-lg mx-auto">
            <div className="absolute -inset-4 rounded-2xl"></div>
            <div className="relative rounded-2xl border-2 border-black bg-white overflow-hidden ring-1 ring-gray-200 dark:border-gray-700 dark:bg-gray-800 dark:shadow-gray-900/30 dark:ring-gray-700">
                <Image
                  src="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/data-demo.png"
                  alt="Data extraction feature illustration"
                  width={600}
                  height={400}
                  className="w-full h-auto"
                  data-ai-hint="data visualization chart"
                />
              </div>
            </div>
          </div>
          <div className="order-2 md:order-2">
            <div className="max-w-xl mx-auto">
              <h2 className="font-headline text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-gray-900 dark:text-white">
                Essential Insights Fast
              </h2>
              <p className="my-16 md:my-8 lg:my-12 text-lg sm:text-xl text-gray-700 dark:text-gray-300">
                Go beyond summaries. Arin identifies and extracts critical data points from your documents, presenting them in a structured and visual format. Never miss a deadline or key piece of information again.
              </p>
              <ul className="space-y-4 sm:space-y-6">
                {features.map((feature, index) => (
                  <li key={index} className="flex items-start border-b-2 border-black">
                    <span className="ml-1 text-md sm:text-xl md:text-2xl text-gray-700 dark:text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}