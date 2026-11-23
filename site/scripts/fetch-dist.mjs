// fetch-dist.mjs — materialize the mz binary distribution into public/dist/.
//
// Download order, per file:
//   1. NxDB file storage (mz_db_files → storage download) — the durable host
//      that keeps working after this repository goes private. Requires the
//      NXDB_ID / NXDB_PASSWORD env vars (set in Netlify → Environment).
//   2. GitHub releases of crossberry-in/mozhi-doc (public fallback).
//
// Every file is verified against the official SHA-256 digests reported by the
// GitHub release API before it is accepted into the site.
//
// Outputs:
//   public/dist/v<version>/...      binaries + per-version SHA256SUMS
//   public/dist/manifest.json       JSON manifest (humans + /api/releases)
//   public/dist/versions.env        flat key=value manifest (install.sh parser)
//   netlify/functions/_data/releases-data.mjs  bundled fallback for the API
import { mkdirSync, writeFileSync, existsSync, readFileSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const DIST = join(ROOT, "public", "dist");
const GH = "https://github.com/crossberry-in/mozhi-doc/releases/download";

// Official digests as reported by the GitHub release API (release v3.7.0).
const V370 = {
  version: "v3.7.0",
  published_at: "2026-10-26T12:56:38Z",
  notes: "Runtime stability, networking & performance; safe calls (RUNTIME010), safe navigation ?., lazy ??, 64-bit ints, ~8.6x faster float loop. Zig-built binaries have no TLS.",
  files: {
    "mozhi-interpreter-linux-x86_64":  { flavor: "linux",  arch: "x86_64", sha256: "3d903735c716bebfdba950fe6f345a8729b8f3749276cd90c4d38d71eb4ee1fb" },
    "mozhi-interpreter-linux-arm64":   { flavor: "linux",  arch: "arm64",  sha256: "a15b858168d21a5b459e264cd904f490fd54cae6ca077d9522d95db1136d7885" },
    "mozhi-interpreter-alpine-x86_64": { flavor: "alpine", arch: "x86_64", sha256: "fd3f4558821648c3ebc6f71d4c0d354e4f3de99ca6417d8466aac6aceb18890f" },
    "mozhi-interpreter-alpine-arm64":  { flavor: "alpine", arch: "arm64",  sha256: "dbb0c6a28587c0574a230b2bea5d037b6c64152d02feba91d1fc125bf251e11c" },
    "mozhi-interpreter-macos-x86_64":  { flavor: "macos",  arch: "x86_64", sha256: "a4a31288b0dc624cd80904fa1748f2c73832055f647760e3cbeb9e5ea840b445" },
    "mozhi-interpreter-macos-arm64":   { flavor: "macos",  arch: "arm64",  sha256: "eb1f7fd7d32b71657ee7001cd42c84f82064734f4c3c7aec6cee836f190f5274" }
  }
};

// Legacy fallback still used for Windows (no windows asset in v3.7.0).
const V250 = {
  version: "v2.5.0",
  published_at: "2026-08-03T09:14:56Z",
  notes: "Legacy fallback — supplies the Windows build used when the latest release has no windows asset.",
  files: {
    "mozhi-interpreter-windows-x86_64.exe": { flavor: "windows", arch: "x86_64", sha256: "005858db501af1ce8476dac1f80a3dfeb391517c4532a94d23ae25f8d22f3a2e" }
  }
};

const RELEASES = [V370, V250];

function sha256(buf) {
  return createHash("sha256").update(buf).digest("hex");
}

async function download(url) {
  const res = await fetch(url, { redirect: "follow" });
  if (!res.ok) throw new Error(`download failed ${res.status} for ${url}`);
  return Buffer.from(await res.arrayBuffer());
}

// NxDB file storage — primary source. Returns a Buffer or null.
async function downloadFromDb(version, filename) {
  const databaseId = process.env.NXDB_ID;
  const password = process.env.NXDB_PASSWORD;
  if (!databaseId || !password) return null;
  let db;
  try {
    const NxDB = (await import("nxmirror-db")).default;
    db = await NxDB.connect({ databaseId, password });
    const row = await db.query(
      "SELECT file_id FROM mz_db_files WHERE version = ? AND filename = ?",
      [version, filename]
    );
    const fileId = row.rows?.[0]?.file_id;
    if (!fileId) return null;
    return await db.storage.download(fileId);
  } catch (e) {
    console.log(`  db source unavailable (${e.message}) — falling back to GitHub`);
    return null;
  }
}

let downloaded = 0;
let skipped = 0;
let fromDb = 0;

for (const rel of RELEASES) {
  const dir = join(DIST, rel.version);
  mkdirSync(dir, { recursive: true });
  for (const [name, meta] of Object.entries(rel.files)) {
    const path = join(dir, name);
    const want = meta.sha256;
    let ok = false;
    if (existsSync(path)) {
      const got = sha256(readFileSync(path));
      if (got === want) { ok = true; skipped++; }
      else console.log(`hash mismatch on existing ${rel.version}/${name} — re-downloading`);
    }
    if (!ok) {
      process.stdout.write(`fetching ${rel.version}/${name} ... `);
      let buf = await downloadFromDb(rel.version, name);
      if (buf && buf.length > 1000 && sha256(buf) === want) {
        fromDb++;
        process.stdout.write("[nxdb] ");
      } else {
        buf = await download(`${GH}/${rel.version}/${name}`);
      }
      if (sha256(buf) !== want) throw new Error(`SHA256 mismatch for ${rel.version}/${name}`);
      writeFileSync(path, buf);
      downloaded++;
      console.log("ok");
    }
    meta.bytes = statSync(path).size;
  }
  // Per-version SHA256SUMS (canonical format)
  const sums = Object.entries(rel.files)
    .map(([name]) => `${rel.files[name].sha256}  ${name}`)
    .join("\n") + "\n";
  writeFileSync(join(dir, "SHA256SUMS"), sums);
}

// JSON manifest (human-readable + consumed by /api/releases fallback)
const manifest = {
  registry: "mz-docs",
  updated: new Date().toISOString().slice(0, 10),
  latest: V370.version,
  allowed: RELEASES.map(r => r.version),
  source: "https://github.com/crossberry-in/mozhi-doc/releases",
  base: "/dist",
  versions: Object.fromEntries(RELEASES.map(r => [r.version, {
    published_at: r.published_at,
    latest: r.version === V370.version,
    allowed: true,
    notes: r.notes,
    files: Object.fromEntries(Object.entries(r.files).map(([name, m]) => [`${m.flavor}.${m.arch}`, {
      filename: name,
      flavor: m.flavor,
      arch: m.arch,
      bytes: m.bytes,
      sha256: m.sha256,
      url: `/dist/${r.version}/${name}`
    }]))
  }]))
};
writeFileSync(join(DIST, "manifest.json"), JSON.stringify(manifest, null, 2) + "\n");

// Flat key=value manifest for the POSIX installer (grep-parsed, never sourced)
const envLines = [
  "# mz-docs version manifest for install.sh (generated by scripts/fetch-dist.mjs)",
  `latest=${V370.version}`,
  `allowed=${RELEASES.map(r => r.version).join(" ")}`,
  `manifest_updated=${manifest.updated}`
];
for (const rel of RELEASES) {
  for (const [name, m] of Object.entries(rel.files)) {
    envLines.push(`${rel.version}.${m.flavor}.${m.arch}.file=${name}`);
    envLines.push(`${rel.version}.${m.flavor}.${m.arch}.sha256=${m.sha256}`);
    envLines.push(`${rel.version}.${m.flavor}.${m.arch}.bytes=${m.bytes}`);
  }
}
writeFileSync(join(DIST, "versions.env"), envLines.join("\n") + "\n");

// Bundled fallback data for the releases API function
const fnDataDir = join(ROOT, "netlify", "functions", "_data");
mkdirSync(fnDataDir, { recursive: true });
writeFileSync(join(fnDataDir, "releases-data.mjs"),
  "// Generated by scripts/fetch-dist.mjs — do not edit by hand.\n" +
  `export const RELEASES = ${JSON.stringify(manifest, null, 2)};\n`);

console.log(`fetch-dist: ${downloaded} downloaded (${fromDb} from NxDB), ${skipped} verified from cache, manifest + versions.env written`);
