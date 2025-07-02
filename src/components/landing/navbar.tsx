import { Button } from "@/components/ui/button";
import Logo from "@/components/landing/logo";

export default function Navbar() {
  return (
    <header className="py-4">
      <div className="container mx-auto flex items-center justify-between px-4">
        <Logo />
        <Button>Get Early Access</Button>
      </div>
    </header>
  );
}
