// GET /api/registry — the Mozhi library registry, mirrored from NxDB (mz_packages).
//
//   /api/registry            → the official registry shape: { registry, version,
//                              updated, packages: [...] }
//   /api/registry?name=strings → one package detail
//   /api/registry?q=http     → filter by name/description/keywords
//
// Source: the mz_packages table in NxDB when NXDB_ID/NXDB_PASSWORD are present
// (synced by scripts/seed-db.mjs from the repository's mozhi-registry.json);
// otherwise the bundled snapshot generated at build time. Shape-compatible
// with the official mozhi-registry.json so consumers can swap the URL.
import { REGISTRY } from "./_data/registry-data.mjs";

const json = (status, body) => new Response(JSON.stringify(body, null, 2), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=300" }
});

async function fromDatabase() {
  const databaseId = process.env.NXDB_ID;
  const password = process.env.NXDB_PASSWORD;
  if (!databaseId || !password) return null;
  try {
    const NxDB = (await import("nxmirror-db")).default;
    const db = await NxDB.connect({ databaseId, password });
    const rows = await db.query("SELECT * FROM mz_packages ORDER BY name");
    if (!rows.rows?.length) return null;
    return rows.rows.map(p => ({
      name: p.name,
      version: p.version,
      description: p.description,
      author: p.author,
      license: p.license,
      category: p.category,
      keywords: p.keywords ? JSON.parse(p.keywords) : [],
      source: p.source || undefined,
      install: p.install || undefined,
      repo: p.repo || undefined,
      dist: p.dist || undefined,
      asset: p.asset || undefined,
      import_as: p.import_as || undefined,
      official: !!p.official
    }));
  } catch {
    return null;
  }
}

export default async (req) => {
  const url = new URL(req.url);
  const name = (url.searchParams.get("name") || "").trim().toLowerCase();
  const q = (url.searchParams.get("q") || "").trim().toLowerCase();

  let packages = await fromDatabase();
  let source = "nxdb";
  if (!packages) {
    packages = REGISTRY.packages;
    source = "bundled";
  }

  if (name) {
    const hit = packages.find(p => (p.name || "").toLowerCase() === name || (p.import_as || "").toLowerCase() === name);
    if (!hit) {
      return json(404, { ok: false, error: `no package named ${name}`, total: packages.length });
    }
    return json(200, { ok: true, source, package: hit });
  }

  if (q) {
    const filtered = packages.filter(p =>
      [p.name, p.description, ...(p.keywords || [])].join(" ").toLowerCase().includes(q));
    return json(200, { ok: true, source, query: q, total: filtered.length, packages: filtered });
  }

  return json(200, {
    ok: true,
    registry: "mozhi",
    version: REGISTRY.version,
    updated: REGISTRY.updated,
    source,
    total: packages.length,
    packages
  });
};

export const config = { path: "/api/registry" };
