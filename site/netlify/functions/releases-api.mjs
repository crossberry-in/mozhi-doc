// GET /api/releases — public release + file index for the mz binary distribution.
//
//   /api/releases            → allowed releases, latest flag, every file with
//                              flavor/arch/bytes/sha256/site url
//   /api/releases?version=v3.7.0 → one release
//
// This is the database ↔ site-files connection surface: the NxDB database
// (mz_releases + mz_files) mirrors what the build materialized into public/dist/.
// When the database environment is not configured the bundled manifest
// generated at build time is served instead. No credentials are exposed.
import { RELEASES } from "./_data/releases-data.mjs";

const json = (status, body) => new Response(JSON.stringify(body, null, 2), {
  status,
  headers: { "content-type": "application/json; charset=utf-8", "cache-control": "public, max-age=300" }
});

async function fromDatabase(version) {
  const databaseId = process.env.NXDB_ID;
  const password = process.env.NXDB_PASSWORD;
  if (!databaseId || !password) return null;
  let NxDB;
  try { NxDB = (await import("nxmirror-db")).default; } catch { return null; }
  try {
    const db = await NxDB.connect({ databaseId, password });
    const relRows = version
      ? await db.query("SELECT * FROM mz_releases WHERE version = ?", [version])
      : await db.query("SELECT * FROM mz_releases ORDER BY is_latest DESC, published_at DESC");
    if (!relRows.rows?.length) return null;
    const out = [];
    for (const rel of relRows.rows) {
      const files = await db.query("SELECT filename, flavor, arch, bytes, sha256, url FROM mz_files WHERE version = ?", [rel.version]);
      out.push({
        version: rel.version,
        published_at: rel.published_at,
        latest: !!rel.is_latest,
        allowed: !!rel.is_allowed,
        notes: rel.notes || "",
        files: (files.rows || []).map(f => ({ ...f, url: `https://mz.netlify.app${f.url}` }))
      });
    }
    return out;
  } catch {
    return null;
  }
}

function fromBundle(version) {
  const entries = Object.entries(RELEASES.versions)
    .filter(([v]) => !version || v === version)
    .map(([v, info]) => ({
      version: v,
      published_at: info.published_at,
      latest: !!info.latest,
      allowed: !!info.allowed,
      notes: info.notes || "",
      files: Object.values(info.files).map(f => ({ ...f, url: `https://mz.netlify.app${f.url}` }))
    }));
  return entries;
}

export default async (req) => {
  const url = new URL(req.url);
  const version = (url.searchParams.get("version") || "").trim();

  let releases = await fromDatabase(version || null);
  let source = "nxdb";
  if (!releases) {
    releases = fromBundle(version);
    source = "bundled";
  }

  if (version && !releases.length) {
    return json(404, {
      ok: false, error: `unknown version ${version}`,
      allowed: RELEASES.allowed
    });
  }

  return json(200, {
    ok: true,
    source,
    latest: RELEASES.latest,
    allowed: RELEASES.allowed,
    installer: "curl -fsSL https://mz.netlify.app/install.sh | sh",
    pinned: "curl -fsSL https://mz.netlify.app/install.sh | sh -s -- v3.7.0",
    manifest: "https://mz.netlify.app/dist/manifest.json",
    total: releases.length,
    releases
  });
};

export const config = { path: "/api/releases" };
