import Link from "next/link";

export default function Logo() {
  return (
    <Link href="/" className="flex items-center hover:opacity-80 transition">
      <span className="font-headline text-5xl font-bold text-primary">
        Anaya
      </span>
    </Link>
  );
}
