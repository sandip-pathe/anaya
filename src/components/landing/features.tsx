import FeatureSection from "../FeatureSection";

export default function Features() {
  return (
    <>
      <FeatureSection
        id="intelligence-hub"
        title="Your Firm's Private Intelligence Hub"
        description="Stop hunting through folders and relying on institutional memory. Anaya indexes your firm's entire knowledge base—every brief, case, and note—into a single, searchable intelligence hub. Ask complex questions in plain English and get immediate, cited answers, surfacing insights that would normally take weeks to uncover."
        features={[
          "Unified hub for all your internal knowledge.",
          "Ask questions in plain English, get sources instantly.",
          "Live updates as cases evolve—your intelligence never goes stale.",
          "Spot patterns, risks, and opportunities across all matters.",
        ]}
        image="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/IMG_20250925_234344.png"
      />

      <FeatureSection
        id="agents"
        title="An Army of AI Agents, Custom-Built for You"
        description="Why settle for off-the-shelf features? With Anaya, you can design and deploy an unlimited number of AI agents for any task: contract review, litigation triage, compliance monitoring, e-discovery, and more. These agents are built on your data and fine-tuned to your firm's exact specifications."
        features={[
          "Templates for the most common legal workflows.",
          "Run multiple agents in parallel on a single matter.",
          "Adapted to the way your firm actually works.",
          "Improve continuously as they learn from your cases.",
        ]}
        image="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/IMG_20250925_234542.png"
        reverse
      />

      <FeatureSection
        id="byoc"
        title="Workflow Intelligence & Business Insights"
        description="Anaya does more than just automate tasks; it creates a virtuous cycle of intelligence. Every workflow, from document summarization to risk detection, generates actionable insights. This data feeds back into the system, continuously refining your agents and revealing firm-wide trends that drive smarter business decisions."
        features={[
          "Build multiple workflows across every department.",
          "Feedback loops continuously refine each workflow.",
          "Full audit trails for transparency and compliance.",
          "No lock-in — take your data with you anytime.",
        ]}
        image="https://raw.githubusercontent.com/sandip-pathe/projects/refs/heads/main/IMG_20250926_163046.png"
      />
    </>
  );
}
