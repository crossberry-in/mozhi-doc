// GET /api/dist/:version/:filename — download a dist binary from NxDB file
// storage. The db is the durable file host: this works regardless of whether
// the repository is public or private. Resolves the file_id from mz_db_files,
// then redirects to a short-lived signed URL (no credentials ever appear in
// the response — the signature is scoped and expires in 5 minutes).
//
// Fallback: if the database is unreachable or the file is unknown, redirect to
// the public GitHub release asset (works while the repo is public).
const GH = "https://github.com/crossberry-in/mozhi-doc/releases/download";
const SAFE = /^[A-Za-z0-9._-]+$/;

async function resolve(version, filename) {
  const databaseId = process.env.NXDB_ID;
  const password = process.env.NXDB_PASSWORD;
  if (!databaseId || !password) return { dbOff: true };
  try {
    const NxDB = (await import("nxmirror-db")).default;
    const db = await NxDB.connect({ databaseId, password });
    const row = await db.query(
      "SELECT file_id FROM mz_db_files WHERE version = ? AND filename = ?",
      [version, filename]
    );
    const fileId = row.rows?.[0]?.file_id;
    if (!fileId) return { notFound: true };
    const url = await db.storage.signedUrl(fileId, 300);
    return { url };
  } catch {
    return { error: true };
  }
}

export default async (req) => {
  // Path: /api/dist/<version>/<filename> (Netlify rewrite keeps the full path)
  const parts = (new URL(req.url).pathname).split("/").filter(Boolean);
  // parts = ["api", "dist", version, filename?...]
  const version = parts[2] || "";
  const filename = parts.slice(3).join("/") || "";

  if (!SAFE.test(version) || !SAFE.test(filename)) {
    return new Response(JSON.stringify({
      ok: false,
      error: "invalid version or filename",
      usage: "GET /api/dist/v3.7.0/mozhi-interpreter-linux-x86_64"
    }), { status: 400, headers: { "content-type": "application/json" } });
  }

  const r = await resolve(version, filename);
  if (r.url) {
    return new Response(null, { status: 302, headers: { location: r.url, "cache-control": "no-store" } });
  }

  // Fallbacks
  const ghFallback = `${GH}/${version}/${filename}`;
  const head = await fetch(ghFallback, { method: "HEAD" }).catch(() => null);
  if (head && head.ok) {
    return new Response(null, { status: 302, headers: { location: ghFallback, "cache-control": "no-store" } });
  }

  const listUrl = `https://mz.netlify.app/api/releases${version ? `?version=${version}` : ""}`;
  return new Response(JSON.stringify({
    ok: false,
    error: r.notFound ? `no file ${version}/${filename} in the distribution storage` : "distribution storage unavailable",
    hint: `browse available files at ${listUrl}`
  }), { status: 404, headers: { "content-type": "application/json" } });
};

export const config = { path: "/api/dist/*" };
