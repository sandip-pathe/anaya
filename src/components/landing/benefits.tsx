"use client"

import { useState, useEffect, useRef, useCallback } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, ShieldCheck, UserCheck, ChevronLeft, ChevronRight } from "lucide-react";

const benefits = [
  {
    icon: <CheckCircle2 className="h-8 w-8 text-black-300" />,
    title: "Save Hours Every Week",
    description: "AI highlights key points, deadlines, and risks — no more manual skimming.",
  },
  {
    icon: <UserCheck className="h-8 w-8 text-black-300" />,
    title: "Built for Legal Professionals",
    description: "Clear, professional summaries — not generic AI fluff.",
  },
  {
    icon: <ShieldCheck className="h-8 w-8 text-black-300" />,
    title: "Secure & Private",
    description: "Your documents are never stored — instant processing, instant results.",
  },
  {
    icon: <CheckCircle2 className="h-8 w-8 text-black-300" />,
    title: "Intelligent Analysis",
    description: "Context-aware insights tailored to your specific legal domain.",
  },
  {
    icon: <UserCheck className="h-8 w-8 text-black-300" />,
    title: "Seamless Integration",
    description: "Works with your existing tools and document management systems.",
  },
];

export default function Benefits() {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const sliderRef = useRef<HTMLDivElement>(null);
  const touchStartX = useRef(0);
  const touchEndX = useRef(0);

  const nextSlide = useCallback(() => {
    setCurrentIndex((prev) => (prev === benefits.length - 1 ? 0 : prev + 1));
  }, []);

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev === 0 ? benefits.length - 1 : prev - 1));
  };

  // Auto slide functionality
  useEffect(() => {
    if (isPaused) return;
    
    const interval = setInterval(() => {
      nextSlide();
    }, 5000);
    
    return () => clearInterval(interval);
  }, [isPaused, nextSlide]);

  // Touch handling for mobile
  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX;
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    touchEndX.current = e.touches[0].clientX;
  };

  const handleTouchEnd = () => {
    if (touchStartX.current - touchEndX.current > 75) {
      nextSlide();
    } else if (touchEndX.current - touchStartX.current > 75) {
      prevSlide();
    }
  };

  // Calculate card offset for sliding effect
  const calculateOffset = () => {
    if (!sliderRef.current) return 0;
    const cardWidth = sliderRef.current.children[0]?.clientWidth || 0;
    return cardWidth * currentIndex;
  };

  return (
    <section id="benefits" className="py-16 sm:py-24 bg-blue-950 relative overflow-hidden">
      <div className="container mx-auto px-4 relative z-10">
        <div 
          ref={sliderRef}
          className="flex transition-transform duration-500 ease-in-out"
          style={{ transform: `translateX(-${calculateOffset()}px)` }}
          onTouchStart={handleTouchStart}
          onTouchMove={handleTouchMove}
          onTouchEnd={handleTouchEnd}
          onMouseEnter={() => setIsPaused(true)}
          onMouseLeave={() => setIsPaused(false)}
        >
          {benefits.map((benefit, index) => (
            <div 
              key={index} 
              className="flex-shrink-0 w-full sm:w-2/3 md:w-1/2 lg:w-1/3 px-4"
            >
              <Card 
                className={`text-center rounded-2xl border-4 border-white bg-white transition-all duration-300 ease-in-out transform hover:-translate-y-2 hover:shadow-xl ${
                  index === currentIndex ? "ring-4 ring-blue-400 scale-[1.02]" : "opacity-90 border-black"
                }`}
              >
                <CardHeader>
                  <div className="flex justify-center mb-4">{benefit.icon}</div>
                  <CardTitle className="font-headline text-black text-2xl md:text-3xl">
                    {benefit.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-md text-black">{benefit.description}</p>
                </CardContent>
              </Card>
            </div>
          ))}
        </div>
      </div>

      {/* Navigation arrows */}
      <button 
        onClick={prevSlide}
        className="absolute left-4 top-1/2 -translate-y-1/2 z-20 bg-white/80 hover:bg-white rounded-full p-2 shadow-lg transition-all duration-300 hover:scale-110 focus:outline-none"
        aria-label="Previous slide"
      >
        <ChevronLeft className="h-6 w-6 text-blue-900" />
      </button>
      
      <button 
        onClick={nextSlide}
        className="absolute right-4 top-1/2 -translate-y-1/2 z-20 bg-white/80 hover:bg-white rounded-full p-2 shadow-lg transition-all duration-300 hover:scale-110 focus:outline-none"
        aria-label="Next slide"
      >
        <ChevronRight className="h-6 w-6 text-blue-900" />
      </button>

      {/* Pagination indicators */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 flex space-x-2 z-20">
        {benefits.map((_, index) => (
          <button
            key={index}
            onClick={() => setCurrentIndex(index)}
            className={`w-3 h-3 rounded-full transition-all duration-300 ${
              index === currentIndex 
                ? "bg-white scale-125" 
                : "bg-white/50 hover:bg-white/80"
            }`}
            aria-label={`Go to slide ${index + 1}`}
          />
        ))}
      </div>

      {/* Decorative gradient elements */}
      <div className="absolute inset-y-0 left-0 w-24 bg-gradient-to-r from-blue-950 to-transparent z-10 pointer-events-none" />
      <div className="absolute inset-y-0 right-0 w-24 bg-gradient-to-l from-blue-950 to-transparent z-10 pointer-events-none" />
    </section>
  );
}