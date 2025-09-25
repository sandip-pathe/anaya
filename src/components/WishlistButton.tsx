// components/WishlistButton.tsx
"use client";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

interface WishlistButtonProps {
  className?: string;
}

export default function WishlistButton({ className }: WishlistButtonProps) {
  const router = useRouter();

  return (
    <Button
      size="lg"
      onClick={() => router.push(`https://app.anaya.legal`)}
      className={`bg-blue-950 hover:bg-black gap-2 hover:gap-4 text-base ${className}`}
    >
      <p>⚡ Try Anaya Now (Free Demo)</p>
      <p>➔</p>
    </Button>
  );
}
