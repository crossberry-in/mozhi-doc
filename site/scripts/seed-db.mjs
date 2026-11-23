// seed-db.mjs — sync the mz-docs site index into the NxDB cloud database.
//
// The NxDB database is the "db ↔ site files" connection point:
//   mz_releases  → one row per allowed release (latest flag)
//   mz_files     → one row per distributable binary (sha256, bytes, site url)
//   mz_docs      → docs index (guides, titles, summaries) powering /api/docs
//
// Credentials NEVER live in this repository. They are read from the
// environment (set them in the Netlify UI: Site configuration → Environment
// variables, or export them locally before running):
//   NXDB_ID        the database id (nxdb-...)
//   NXDB_PASSWORD  the database password (trusted server environments only)
//
// The script is deliberately non-fatal: when the variables are absent or the
// database is unreachable the build continues and the API functions fall back
// to their bundled data files.
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

const databaseId = process.env.NXDB_ID;
const password = process.env.NXDB_PASSWORD;

if (!databaseId || !password) {
  console.log("seed-db: NXDB_ID / NXDB_PASSWORD not set — skipping db sync (APIs will use bundled data)");
  process.exit(0);
}

let NxDB;
try {
  NxDB = (await import("nxmirror-db")).default;
} catch (e) {
  console.log(`seed-db: nxmirror-db SDK unavailable (${e.message}) — skipping db sync`);
  process.exit(0);
}

try {
  const db = await NxDB.connect({ databaseId, password });

  await db.exec(`CREATE TABLE IF NOT EXISTS mz_releases (
    version TEXT PRIMARY KEY,
    published_at TEXT,
    is_latest INTEGER,
    is_allowed INTEGER,
    notes TEXT
  )`);
  await db.exec(`CREATE TABLE IF NOT EXISTS mz_files (
    version TEXT,
    filename TEXT,
    flavor TEXT,
    arch TEXT,
    bytes INTEGER,
    sha256 TEXT,
    url TEXT,
    PRIMARY KEY (version, filename)
  )`);
  await db.exec(`CREATE TABLE IF NOT EXISTS mz_docs (
    slug TEXT PRIMARY KEY,
    guide TEXT,
    title TEXT,
    sort INTEGER,
    description TEXT,
    words INTEGER,
    updated_at TEXT
  )`);

  const manifestPath = join(ROOT, "public", "dist", "manifest.json");
  if (existsSync(manifestPath)) {
    const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
    for (const [version, info] of Object.entries(manifest.versions)) {
      await db.query(
        `INSERT INTO mz_releases (version, published_at, is_latest, is_allowed, notes)
         VALUES (?, ?, ?, ?, ?)
         ON CONFLICT(version) DO UPDATE SET published_at=excluded.published_at,
           is_latest=excluded.is_latest, is_allowed=excluded.is_allowed, notes=excluded.notes`,
        [version, info.published_at, info.latest ? 1 : 0, 1, info.notes || ""]
      );
      for (const f of Object.values(info.files)) {
        await db.query(
          `INSERT INTO mz_files (version, filename, flavor, arch, bytes, sha256, url)
           VALUES (?, ?, ?, ?, ?, ?, ?)
           ON CONFLICT(version, filename) DO UPDATE SET bytes=excluded.bytes,
             sha256=excluded.sha256, url=excluded.url`,
          [version, f.filename, f.flavor, f.arch, f.bytes, f.sha256, f.url]
        );
      }
    }
    console.log(`seed-db: synced ${Object.keys(manifest.versions).length} releases into mz_releases/mz_files`);
  } else {
    console.log("seed-db: public/dist/manifest.json not found — run fetch-dist first (releases skipped)");
  }

  const indexPath = join(ROOT, "lib", "content-index.json");
  if (existsSync(indexPath)) {
    const index = JSON.parse(readFileSync(indexPath, "utf8"));
    for (const d of index.docs) {
      await db.query(
        `INSERT INTO mz_docs (slug, guide, title, sort, description, words, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(slug) DO UPDATE SET guide=excluded.guide, title=excluded.title,
           sort=excluded.sort, description=excluded.description, words=excluded.words,
           updated_at=excluded.updated_at`,
        [d.slug, d.guide, d.title, d.order, d.description, d.words,
         new Date().toISOString().slice(0, 10)]
      );
    }
    const c = await db.query("SELECT COUNT(*) AS n FROM mz_docs");
    console.log(`seed-db: docs index synced — mz_docs now has ${c.rows?.[0]?.n ?? "?"} pages`);
  } else {
    console.log("seed-db: lib/content-index.json not found — run build-content first (docs skipped)");
  }

  process.exit(0);
} catch (err) {
  console.log(`seed-db: database sync failed (${err.message}) — build continues, APIs fall back to bundled data`);
  process.exit(0);
}
