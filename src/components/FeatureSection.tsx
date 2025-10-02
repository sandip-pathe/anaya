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
    // Adjusted padding
    <section id={id} className={`py-16 dark:bg-black sm:py-24 ${ reverse ? "bg-gray-100":""}`}>
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div
          // Added lg:gap-24 for more space between columns on large screens
          className={`grid items-center gap-12 md:grid-cols-2 lg:gap-24 ${
            reverse ? "md:[&>*:first-child]:order-last" : ""
          }`}
        >
          {/* Text Column */}
          <div className="text-left">
            <h2 className="font-headline text-3xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              {title}
            </h2>
            <p className="mt-6 text-base text-gray-700 dark:text-gray-300 sm:text-lg">
              {description}
            </p>
            <ul className="mt-8 space-y-4">
              {features.map((feature, index) => (
                <li
                  key={index}
                  // Added padding-bottom for a subtle visual touch
                  className="flex items-start border-b border-gray-400/50 pb-2 text-gray-700 hover:text-black dark:border-gray-700 dark:text-gray-300"
                >
                  <span className="ml-1 text-sm sm:text-base">
                    {feature}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          {/* Image Column */}
          <div className="flex justify-center">
            <Image
              src={image}
              alt={title}
              width={700}
              height={500}
              // Ensured the image scales properly and doesn't exceed its container
              className="h-auto w-full max-w-md object-contain md:max-w-lg lg:max-w-xl"
              priority
            />
          </div>
        </div>
      </div>
    </section>
  );
}