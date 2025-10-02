// FeatureSection.tsx
import Image from "next/image";

interface FeatureSectionProps {
  id: string;
  title: string;
  description: string;
  features: string[];
  image: string;
  reverse?: boolean;
}

export default function FeatureSection({
  id,
  title,
  description,
  features,
  image,
  reverse = false,
}: FeatureSectionProps) {
  return (
    <section id={id} className={`py-12 sm:py-16 dark:bg-black`}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div
          className={`grid gap-10 sm:gap-12 md:grid-cols-2 items-center ${
            reverse ? "md:[&>*:first-child]:order-last" : ""
          }`}
        >
          {/* Text */}
          <div className="p-4 sm:p-6">
            <h2 className="font-headline text-2xl sm:text-3xl md:text-4xl font-bold tracking-tight text-gray-900 dark:text-white">
              {title}
            </h2>
            <p className="mt-6 sm:mt-8 md:mt-6 lg:mt-8 text-base sm:text-lg md:text-md text-gray-700 dark:text-gray-300">
              {description}
            </p>
            <ul className="mt-6 sm:mt-8 space-y-3 sm:space-y-4">
              {features.map((feature, index) => (
                <li
                  key={index}
                  className="flex items-start border-b border-gray-400/50 dark:border-gray-700 text-gray-700 hover:text-black dark:text-gray-300"
                >
                  <span className="ml-1 text-sm sm:text-base md:text-lg">
                    {feature}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Image */}
          <div className="flex justify-center">
            <Image
              src={image}
              alt={title}
              width={700}
              height={500}
              className="w-full max-w-md md:max-w-lg lg:max-w-xl h-auto object-contain"
              priority
            />
          </div>
        </div>
      </div>
    </section>
  );
}
