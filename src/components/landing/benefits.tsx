import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, ShieldCheck, UserCheck } from "lucide-react";

const benefits = [
  {
    icon: <CheckCircle2 className="h-8 w-8 text-accent" />,
    title: "Save Hours Every Week",
    description: "AI highlights key points, deadlines, and risks — no more manual skimming.",
  },
  {
    icon: <UserCheck className="h-8 w-8 text-accent" />,
    title: "Built for Legal Professionals",
    description: "Clear, professional summaries — not generic AI fluff.",
  },
  {
    icon: <ShieldCheck className="h-8 w-8 text-accent" />,
    title: "Secure & Private",
    description: "Your documents are never stored — instant processing, instant results.",
  },
];

export default function Benefits() {
  return (
    <section id="benefits" className="py-16 sm:py-24 bg-white">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {benefits.map((benefit, index) => (
            <Card key={index} className="text-center border-0 shadow-none bg-transparent">
              <CardHeader>
                <div className="flex justify-center mb-4">{benefit.icon}</div>
                <CardTitle className="font-headline text-xl">{benefit.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-foreground/80">{benefit.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
