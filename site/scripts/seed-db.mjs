// seed-db.mjs — sync the mz-docs site index into the NxDB cloud database.
//
// The NxDB database is the "db ↔ site files" connection point:
//   mz_releases   → one row per allowed release (latest flag)
//   mz_files      → one row per distributable binary (sha256, bytes, site url)
//   mz_docs       → docs index (guides, titles, summaries) powering /api/docs
//   mz_doc_files  → docs page CONTENT in NxDB file storage (slug → file_id)
//   mz_packages   → the Mozhi library registry mirrored from mozhi-registry.json
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
import { createHash } from "node:crypto";
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

    // Docs FILE storage — upload every page's markdown into NxDB file storage
    // (mz-docs/<slug>.md) and record the file_id so /api/docs can serve page
    // content straight from the database ("db connects the site to files").
    await db.exec(`CREATE TABLE IF NOT EXISTS mz_doc_files (
      slug TEXT PRIMARY KEY,
      file_id TEXT,
      path TEXT,
      sha256 TEXT,
      bytes INTEGER,
      updated_at TEXT
    )`);
    let docsUploaded = 0;
    for (const d of index.docs) {
      const body = Buffer.from(d.content || "", "utf8");
      if (!body.length) continue;
      const path = `mz-docs/${d.slug}.md`;
      const rec = await db.storage.upload({
        path,
        file: body,
        mime: "text/markdown",
        public: false
      });
      const file = rec.file || rec;
      const fileId = file.file_id || file.id || file.fileId || null;
      await db.query(
        `INSERT INTO mz_doc_files (slug, file_id, path, sha256, bytes, updated_at)
         VALUES (?, ?, ?, ?, ?, ?)
         ON CONFLICT(slug) DO UPDATE SET file_id=excluded.file_id, path=excluded.path,
           sha256=excluded.sha256, bytes=excluded.bytes, updated_at=excluded.updated_at`,
        [d.slug, fileId, path, createHash("sha256").update(body).digest("hex"),
         body.length, new Date().toISOString().slice(0, 10)]
      );
      docsUploaded++;
    }
    const dfc = await db.query("SELECT COUNT(*) AS n FROM mz_doc_files");
    console.log(`seed-db: docs content uploaded — ${docsUploaded} pages into file storage (mz_doc_files=${dfc.rows?.[0]?.n ?? "?"})`);
  } else {
    console.log("seed-db: lib/content-index.json not found — run build-content first (docs skipped)");
  }

  // Pkg registry metadata — mirror the Mozhi library registry (mozhi-registry.json
  // at the repository root) into mz_packages so /api/registry serves it from NxDB.
  await db.exec(`CREATE TABLE IF NOT EXISTS mz_packages (
    name TEXT PRIMARY KEY,
    version TEXT,
    description TEXT,
    author TEXT,
    license TEXT,
    category TEXT,
    keywords TEXT,
    source TEXT,
    install TEXT,
    repo TEXT,
    dist TEXT,
    asset TEXT,
    import_as TEXT,
    official INTEGER,
    updated_at TEXT
  )`);
  const registryCandidates = [
    join(ROOT, "..", "mozhi-registry.json"),
    join(ROOT, "mozhi-registry.json")
  ];
  const registryPath = registryCandidates.find(p => existsSync(p));
  if (registryPath) {
    const registry = JSON.parse(readFileSync(registryPath, "utf8"));
    let pkgs = 0;
    for (const p of registry.packages || []) {
      await db.query(
        `INSERT INTO mz_packages (name, version, description, author, license, category, keywords,
           source, install, repo, dist, asset, import_as, official, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
         ON CONFLICT(name) DO UPDATE SET version=excluded.version, description=excluded.description,
           author=excluded.author, license=excluded.license, category=excluded.category,
           keywords=excluded.keywords, source=excluded.source, install=excluded.install,
           repo=excluded.repo, dist=excluded.dist, asset=excluded.asset,
           import_as=excluded.import_as, official=excluded.official, updated_at=excluded.updated_at`,
        [p.name, p.version || "0.0.0", p.description || "", p.author || "", p.license || "",
         p.category || "", JSON.stringify(p.keywords || []), p.source || null, p.install || null,
         p.repo || null, p.dist || null, p.asset || null, p.import_as || null,
         p.official ? 1 : 0, registry.updated || new Date().toISOString().slice(0, 10)]
      );
      pkgs++;
    }
    const pc = await db.query("SELECT COUNT(*) AS n FROM mz_packages");
    console.log(`seed-db: registry metadata synced — ${pkgs} packages (mz_packages=${pc.rows?.[0]?.n ?? "?"})`);
  } else {
    console.log("seed-db: mozhi-registry.json not found — registry mirror skipped");
  }

  process.exit(0);
} catch (err) {
  console.log(`seed-db: database sync failed (${err.message}) — build continues, APIs fall back to bundled data`);
  process.exit(0);
}
