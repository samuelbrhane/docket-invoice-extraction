import { AfterApproval, Checks, ClosingCta, Hero, HowItWorks, SiteFooter, SiteHeader, UnderTheHood } from "@/components/landing";

export default function LandingPage() {
  return (
    <>
      <SiteHeader />
      <main>
        <Hero />
        <HowItWorks />
        <Checks />
        <AfterApproval />
        <UnderTheHood />
        <ClosingCta />
      </main>
      <SiteFooter />
    </>
  );
}