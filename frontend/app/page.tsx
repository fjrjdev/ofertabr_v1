"use client";

import { Hero, Features, CallToAction, Footer } from "@/app/components";

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Features />
      <CallToAction />
      <Footer />
    </main>
  );
}
