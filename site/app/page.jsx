"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

// The site root hands off immediately to the docs — there is no separate
// marketing page and no nav bar.
export default function Home() {
  const router = useRouter();
  useEffect(() => { router.replace("/docs/"); }, [router]);
  return (
    <div className="notfound">
      <h1><span style={{ color: "var(--accent)" }}>mz</span> docs</h1>
      <p>Taking you to the documentation… <a href="/docs/">open it here</a>.</p>
    </div>
  );
}
