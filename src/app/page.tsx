import Navbar from "@/components/landing/navbar";
import Header from "@/components/landing/hero";
import Demo from "@/components/landing/demo";
import Benefits from "@/components/landing/benefits";
import Cta from "@/components/landing/cta";
import Faq from "@/components/landing/faq";
import Footer from "@/components/landing/footer";
import Features from "@/components/landing/features";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Header />
        <Demo />
        <Benefits />
        <Features />
        <Faq />
        <Cta />
      </main>
      <Footer />
    </div>
  );
}
