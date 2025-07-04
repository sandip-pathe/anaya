import Navbar from "@/components/landing/navbar";
import Header from "@/components/landing/header";
import Demo from "@/components/landing/demo";
import Benefits from "@/components/landing/benefits";
import Summarization from "@/components/landing/summarization";
import DataExtraction from "@/components/landing/data-extraction";
import Cta from "@/components/landing/cta";
import Faq from "@/components/landing/faq";
import Footer from "@/components/landing/footer";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col">
      <Navbar />
      <main className="flex-1">
        <Header />
        <Demo />
        <Benefits />
        <Summarization />
        <DataExtraction />
        <Cta />
        <Faq />
      </main>
      <Footer />
    </div>
  );
}
