"use client";

import { useEffect, useRef } from "react";

interface CalendlyEmbedProps {
  onLoad?: () => void;
  onEventScheduled?: () => void;
}

export default function CalendlyEmbed({
  onLoad,
  onEventScheduled,
}: CalendlyEmbedProps) {
  const widgetRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    // Load Calendly script
    const script = document.createElement("script");
    script.src = "https://assets.calendly.com/assets/external/widget.js";
    script.async = true;
    script.onload = () => {
      if (onLoad) onLoad();
    };
    document.body.appendChild(script);

    // Listen for Calendly events
    const handler = (e: MessageEvent) => {
      if (e.data?.event === "calendly.event_scheduled") {
        if (onEventScheduled) onEventScheduled();
      }
    };
    window.addEventListener("message", handler);

    return () => {
      document.body.removeChild(script);
      window.removeEventListener("message", handler);
    };
  }, [onLoad, onEventScheduled]);

  return (
    <div
      ref={widgetRef}
      className="calendly-inline-widget"
      data-url="https://calendly.com/sandippathe/anaya-ai-factory-demo?hide_event_type_details=1&hide_gdpr_banner=1"
      style={{ minWidth: "320px", height: "700px" }}
    />
  );
}
