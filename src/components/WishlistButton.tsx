// components/WishlistButton.tsx
"use client"
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

interface WishlistButtonProps {
  className?: string; // Allows adding extra styles if needed
}

export default function WishlistButton({ className }: WishlistButtonProps) {
  const router = useRouter();

  return (
    <Button
      size="lg"
      onClick={() => router.push("/subscribe")}
      className={`bg-blue-950 hover:bg-black gap-2 hover:gap-4 text-base ${className}`}
    >
      <p>Join the Wishlist</p>
      <p>➔</p>
    </Button>
  );
}
