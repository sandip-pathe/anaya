import Logo from "@/components/landing/logo";

export default function Footer() {
  const currentYear = new Date().getFullYear();
  return (
    <footer className="bg-white">
      <div className="container mx-auto px-4 py-8">
        <div className="flex flex-col items-center justify-between gap-4 md:flex-row">
          <Logo />
          <p className="text-sm text-foreground/60">
            &copy; {currentYear} CLAIR. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
