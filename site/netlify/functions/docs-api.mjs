// GET /api/docs — public, keyless docs API for humans, agents and LLMs.
//
//   /api/docs                      → list every docs page (slug, guide, title, description)
//   /api/docs?q=install            → search across titles, descriptions and page text
//   /api/docs?path=developers/01-install-mz → full markdown of one page
//   /api/docs?guide=users          → list only one guide
//
// Data source: the NxDB database when NXDB_ID/NXDB_PASSWORD are present —
// the docs index lives in mz_docs and the page CONTENT (markdown files) lives
// in NxDB file storage (mz_doc_files → storage download). When the database is
// unavailable the bundled build data is served instead, so the endpoint never
// goes down. No credentials are exposed by this endpoint.
import { DOCS } from "./_data/docs-data.mjs";

const json = (status, body) => new Response(JSON.stringify(body, null, 2), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=60" }
});

function excerpt(text, query, radius = 120) {
  const lower = text.toLowerCase();
  const at = lower.indexOf(query.toLowerCase());
  if (at === -1) return text.slice(0, radius) + (text.length > radius ? "…" : "");
  const start = Math.max(0, at - radius / 2);
  return (start > 0 ? "…" : "") + text.slice(start, at + query.length + radius / 2).replace(/\s+/g, " ") + "…";
}

// Docs file storage — resolve a page's markdown from NxDB file storage.
async function contentFromDb(slug) {
  const databaseId = process.env.NXDB_ID;
  const password = process.env.NXDB_PASSWORD;
  if (!databaseId || !password) return null;
  try {
    const NxDB = (await import("nxmirror-db")).default;
    const db = await NxDB.connect({ databaseId, password });
    const row = await db.query("SELECT file_id FROM mz_doc_files WHERE slug = ?", [slug]);
    const fileId = row.rows?.[0]?.file_id;
    if (!fileId) return null;
    const buf = await db.storage.download(fileId);
    const text = buf.toString("utf8");
    return text.length > 0 ? text : null;
  } catch {
    return null;
  }
}

export default async (req) => {
  const url = new URL(req.url);
  const q = (url.searchParams.get("q") || "").trim();
  const path = (url.searchParams.get("path") || "").trim().replace(/^\/+|\.md$/g, "");
  const guide = (url.searchParams.get("guide") || "").trim().toLowerCase();

  // Full document read. The lookup is tolerant: exact slug, slug with the
  // numeric sidebar prefix (developers/01-install-mz → developers/install-mz),
  // or the bare page name (install-mz).
  if (path) {
    const norm = path.replace(/\/\d{1,3}-/g, "/").replace(/^\d{1,3}-/, "");
    const bare = norm.split("/").pop();
    const found =
      DOCS.find(d => d.slug === path) ||
      DOCS.find(d => d.slug === norm) ||
      DOCS.find(d => d.slug.endsWith("/" + bare));
    if (!found) {
      return json(404, { ok: false, error: "no docs page for path " + path, hint: "GET /api/docs for the list of slugs" });
    }
    const fromDb = await contentFromDb(found.slug);
    return json(200, {
      ok: true,
      doc: {
        slug: found.slug, guide: found.guide, title: found.title,
        description: found.description, words: found.words,
        url: `https://mz.netlify.app/docs/${found.slug}/`,
        source: fromDb ? "nxdb" : "bundled",
        content_markdown: fromDb || found.content
      }
    });
  }

  // Index (optionally filtered by guide)
  let list = DOCS;
  if (guide) list = list.filter(d => d.guide === guide);
  const index = list.map(d => ({
    slug: d.slug, guide: d.guide, title: d.title,
    description: d.description, words: d.words,
    url: `https://mz.netlify.app/docs/${d.slug}/`
  }));

  // Search
  if (q) {
    const needle = q.toLowerCase();
    const scored = list.map(d => {
      const title = d.title.toLowerCase().includes(needle) ? 3 : 0;
      const desc = d.description.toLowerCase().includes(needle) ? 2 : 0;
      const bodyHits = d.content.toLowerCase().split(needle).length - 1;
      return { d, score: title + desc + (bodyHits > 0 ? 1 : 0), bodyHits };
    }).filter(r => r.score > 0 || r.bodyHits > 0)
      .sort((a, b) => b.score - a.score || b.bodyHits - a.bodyHits);
    return json(200, {
      ok: true, query: q, total: scored.length,
      results: scored.slice(0, 20).map(r => ({
        slug: r.d.slug, guide: r.d.guide, title: r.d.title,
        description: r.d.description,
        matches: r.bodyHits,
        excerpt: excerpt(r.d.content, q),
        url: `https://mz.netlify.app/docs/${r.d.slug}/`,
        read: `https://mz.netlify.app/api/docs?path=${r.d.slug}`
      }))
    });
  }

  return json(200, {
    ok: true, total: index.length, guides: [...new Set(DOCS.map(d => d.guide))],
    usage: {
      list: "/api/docs",
      byGuide: "/api/docs?guide=users",
      search: "/api/docs?q=install",
      read: "/api/docs?path=developers/01-install-mz"
    },
    docs: index
  });
};

export const config = { path: "/api/docs" };
