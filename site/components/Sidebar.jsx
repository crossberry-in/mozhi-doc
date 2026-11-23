"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

// Sidebar — the only navigation of the standalone docs site (there is no top
// nav bar by design). Shows the guides and their page titles; typing in the
// search box filters pages live using the build-time search index.
export default function Sidebar({ docs, guides }) {
  const pathname = usePathname();
  const [query, setQuery] = useState("");
  const [texts, setTexts] = useState(null);

  // Lazy-load the search index (title + plain text per page) on first keystroke.
  useEffect(() => {
    if (!query || texts) return;
    let alive = true;
    fetch("/docs-content.json")
      .then(r => (r.ok ? r.json() : { docs: [] }))
      .then(data => { if (alive) setTexts(data.docs || []); })
      .catch(() => { if (alive) setTexts([]); });
    return () => { alive = false; };
  }, [query, texts]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return null;
    const source = texts || docs.map(d => ({ slug: d.slug, title: d.title, description: d.description, text: "" }));
    return source
      .map(d => {
        const t = (d.title || "").toLowerCase().includes(q) ? 3 : 0;
        const ds = (d.description || "").toLowerCase().includes(q) ? 2 : 0;
        const hits = d.text ? d.text.toLowerCase().split(q).length - 1 : 0;
        const at = d.text ? d.text.toLowerCase().indexOf(q) : -1;
        const excerpt = at >= 0 ? "…" + d.text.slice(Math.max(0, at - 40), at + 90) + "…" : (d.description || "");
        return { slug: d.slug, title: d.title, score: t + ds + (hits ? 1 : 0), hits, excerpt };
      })
      .filter(r => r.score > 0 || r.hits > 0)
      .sort((a, b) => b.score - a.score || b.hits - a.hits)
      .slice(0, 8);
  }, [query, texts, docs]);

  return (
    <aside className="sidebar">
      <Link href="/docs/" className="brand">
        <span className="logo"><span className="mz">mz</span> docs</span>
        <div className="tagline">Mozhi language · mz.netlify.app</div>
      </Link>

      <div className="searchbox">
        <input
          type="search"
          placeholder="Search docs…"
          value={query}
          onChange={e => setQuery(e.target.value)}
          aria-label="Search docs"
        />
        {query && !results && <div className="hint">loading index…</div>}
        {results && results.length === 0 && <div className="search-results"><div className="none">No matches for “{query}”</div></div>}
        {results && results.length > 0 && (
          <div className="search-results">
            {results.map(r => (
              <Link key={r.slug} href={`/docs/${r.slug}/`} className="sr" onClick={() => setQuery("")}>
                <div className="t">{r.title}</div>
                <div className="x">{r.excerpt}</div>
              </Link>
            ))}
          </div>
        )}
        {!query && <div className="hint">Search pages, commands and errors — or browse below.</div>}
      </div>

      {guides.map(g => (
        <nav className="nav-group" key={g}>
          <h4>{g} guide</h4>
          {docs.filter(d => d.guide === g).map(d => (
            <Link key={d.slug} href={`/docs/${d.slug}/`}
              className={pathname === `/docs/${d.slug}/` ? "active" : ""}>
              {d.title}
            </Link>
          ))}
        </nav>
      ))}
    </aside>
  );
}
