import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { UploadCloud, BrainCircuit, DownloadCloud } from "lucide-react";

const steps = [
  {
    icon: <UploadCloud className="h-10 w-10 text-primary" />,
    title: "Upload Document",
    description: "Upload your PDF or Word document.",
  },
  {
    icon: <BrainCircuit className="h-10 w-10 text-primary" />,
    title: "AI Summarization",
    description: "Our AI extracts and summarizes the key information.",
  },
  {
    icon: <DownloadCloud className="h-10 w-10 text-primary" />,
    title: "Get Your Summary",
    description: "Download your summary or copy it directly.",
  },
];

export default function HowItWorks() {
  return (
    <section id="how-it-works" className="py-16 sm:py-24">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-3xl text-center">
          <h2 className="font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            How It Works
          </h2>
          <p className="mt-4 text-lg text-foreground/80">
            Three simple steps to get your legal summaries.
          </p>
        </div>
        <div className="mt-16 grid grid-cols-1 gap-8 md:grid-cols-3">
          {steps.map((step, index) => (
            <Card key={index} className="text-center shadow-lg">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <span className="flex h-16 w-16 items-center justify-center rounded-full bg-secondary">
                    {step.icon}
                  </span>
                </div>
                <CardTitle className="font-headline text-xl">
                  <span className="text-muted-foreground mr-2">{index + 1}.</span>{step.title}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground/80">{step.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
