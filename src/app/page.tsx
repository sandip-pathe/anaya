import Navbar from "@/components/landing/navbar";
import Header from "@/components/landing/header";
import Benefits from "@/components/landing/benefits";
import HowItWorks from "@/components/landing/how-it-works";
import Cta from "@/components/landing/cta";
import Faq from "@/components/landing/faq";
import Footer from "@/components/landing/footer";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Header />
        <Benefits />
        <HowItWorks />
        <Cta />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}
