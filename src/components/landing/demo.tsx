import Image from "next/image";

export default function Demo() {
  return (
    <section id="demo" className="py-16 sm:py-24">
      <div className="container mx-auto px-4">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="font-headline text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
            See Arin in Action
          </h2>
          <p className="mt-4 text-lg text-foreground/80">
            A quick walkthrough of how Arin summarizes your legal documents in seconds.
          </p>
        </div>
        <div className="mt-12">
          <div className="aspect-video overflow-hidden rounded-lg border bg-card shadow-lg">
            <Image
              src="https://placehold.co/1200x800.png"
              alt="Arin App Demo"
              width={1200}
              height={800}
              className="h-full w-full object-cover"
              data-ai-hint="app interface"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
