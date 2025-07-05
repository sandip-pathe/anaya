// components/WishlistOutlineButton.tsx
"use client"
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

interface WishlistOutlineButtonProps {
  className?: string;
}

export default function WishlistOutlineButton({ className }: WishlistOutlineButtonProps) {
  const router = useRouter();

  return (
    <Button
      variant="outline"
      size="lg"
      onClick={() => router.push("/subscribe")}
      className={`hover:bg-black hover:text-white gap-2 hover:gap-4 text-base ${className}`}
    >
      <p>Join the Wishlist</p>
      <p>➔</p>
    </Button>
  );
}
