// Summarization.tsx
import Image from "next/image";

const features = [
  "Identify key clauses and obligations instantly.",
  "Understand complex legal jargon in plain English.",
  "Accelerate your document review process by up to 80%.",
];

export default function Summarization() {
  return (
    <section id="summarization" className="py-16 sm:py-24 bg-secondary to-white dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 sm:px-6">
        <div className="grid items-center gap-12 md:grid-cols-2">
          <div className="order-2 md:order-1">
            <div className="relative mx-auto max-w-xl">
              <h2 className="font-headline text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-gray-900 dark:text-white">
              Summarize Your Documents
              </h2>
              <p className="my-16 text-xl text-gray-700 dark:text-gray-300">
                Stop drowning in paperwork. Arin's advanced AI reads your legal documents and delivers a clear, concise summary in seconds. Focus on what matters, not on manual reading.
              </p>
              <ul className="space-y-4">
                {features.map((feature, index) => (
                  <li key={index} className="flex items-start border-b-2 border-black">
                    <span className="ml-1 text-2xl text-gray-700 dark:text-gray-300">{feature}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          <div className="order-1 md:order-2">
            <div className="relative max-w-lg">
              <div className="absolute -inset-4 rounded-2xl"></div>
              <div className="relative rounded-2xl border-2 border-black bg-white overflow-hidden ring-1 ring-gray-200 dark:border-gray-700 dark:bg-gray-800 dark:shadow-gray-900/30 dark:ring-gray-700">
                <Image
                  src="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/summary_demo.png"
                  alt="Summarization feature illustration"
                  width={600}
                  height={400}
                  className="w-full h-auto"
                  data-ai-hint="document summary"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}