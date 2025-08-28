// FollowUpChat.tsx
import Image from "next/image";

const features = [
  "Ask questions about document instantly.",
  "Brainstorm ideas and get suggestions.",
  "Get interactive explanations tailored to your context.",
];

export default function FollowUpChat() {
  return (
    <section
      id="followup-chat"
      className="py-16 sm:py-24 bg-secondary to-white dark:from-gray-900 dark:to-gray-800"
    >
      <div className="container mx-auto px-4 sm:px-6">
        <div className="grid items-center gap-12 md:grid-cols-2">
          {/* Text section */}
          <div className="order-2 md:order-1">
            <div className="relative mx-auto max-w-xl">
              <h2 className="font-headline text-3xl sm:text-4xl md:text-5xl font-bold tracking-tight text-gray-900 dark:text-white">
                Ask. Clarify. Go Deeper.
              </h2>
              <p className="my-16 text-xl text-gray-700 dark:text-gray-300">
                Don’t stop at summaries. Anaya lets you chat directly with your
                documents — so you can ask follow-up questions, clarify complex
                points, and surface insights on demand.
              </p>
              <ul className="space-y-4">
                {features.map((feature, index) => (
                  <li
                    key={index}
                    className="flex items-start border-b-2 border-black text-gray-700 hover:text-black"
                  >
                    <span className="ml-1 text-2xl dark:text-gray-300">
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Image/Illustration */}
          <div className="order-1 md:order-2">
            <div className="relative max-w-lg">
              <div className="absolute -inset-4 rounded-2xl"></div>
              <div className="relative rounded-2xl border-2 border-black bg-white overflow-hidden ring-1 ring-gray-200 dark:border-gray-700 dark:bg-gray-800 dark:shadow-gray-900/30 dark:ring-gray-700">
                <Image
                  src="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/chat_demo.png"
                  alt="Follow-up chat feature illustration"
                  width={600}
                  height={400}
                  className="w-full h-auto"
                  data-ai-hint="chat with documents"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
