---
title: DB file storage and API endpoints
description: How the NxDB database connects this site to its dist files, and every public API endpoint of mz.netlify.app.
---

# DB file storage and API endpoints

This site is built on two pillars: **db file storage** (the NxDB cloud
database mirrors everything in the site's file tree) and **public API
endpoints** (humans and LLMs read the same data, keyless).

## How the database connects the site to files

The build pipeline keeps the database and the file tree in lockstep:

```text
scripts/fetch-dist.mjs    downloads release binaries → public/dist/
                          writes manifest.json + versions.env + SHA256SUMS
scripts/build-content.mjs compiles content/*.md → indexes + /api/docs data
scripts/seed-db.mjs       syncs both into NxDB:
                            mz_releases  → one row per allowed release
                            mz_files     → one row per dist file (sha256, bytes, url)
                            mz_docs      → one row per docs page
```

So the database is the queryable mirror of the site files: for every
binary under `/dist/` there is an `mz_files` row with its SHA-256, size
and site URL; for every docs page there is an `mz_docs` row. The static
files are what gets downloaded; the database is what gets queried.

Credentials live only in the server environment. On Netlify set:

```text
NXDB_ID          the database id (nxdb-...)
NXDB_PASSWORD    the database password (Site configuration → Environment variables)
```

They are never committed to the repository and never appear in API
responses. When the variables are absent the API functions fall back to
the bundled build data, so the site keeps working without the database.

## Public API endpoints

All endpoints are GET, JSON, CORS-friendly and require **no
authentication**.

### `GET /api/docs` — the docs API (LLM-friendly)

| Call | Result |
| --- | --- |
| `/api/docs` | list every page (slug, guide, title, description) |
| `/api/docs?guide=users` | list one guide only |
| `/api/docs?q=install` | search titles + page text, scored results with excerpts |
| `/api/docs?path=developers/01-install-mz` | full markdown of one page |

The search+read pair is designed for LLM agents: search with `q=`, then
read the winner with `path=`. Every result carries its `read` URL
directly.

```sh
curl -fsSL "https://mz.netlify.app/api/docs?q=pkg"
curl -fsSL "https://mz.netlify.app/api/docs?path=users/01-users-guide"
```

### `GET /api/releases` — release and file index

| Call | Result |
| --- | --- |
| `/api/releases` | latest + allowed versions, every dist file with sha256/bytes/url |
| `/api/releases?version=v3.7.0` | one release |

The response includes the exact installer commands (default and pinned)
so agents can hand users a copy-paste line.

### `GET /api/dist/:version/:filename` — db-backed downloads

Streams any binary straight from NxDB file storage via a short-lived
signed URL (302 redirect, no credentials in the response). Falls back to
the public GitHub release asset when the database is unreachable. This
is the download path that keeps working when the repository is private.

```sh
curl -fL https://mz.netlify.app/api/dist/v3.7.0/mozhi-interpreter-linux-x86_64 -o mozhi
```

### Static files

| Path | Content |
| --- | --- |
| `/install.sh` | the manual installer (curl \| sh) |
| `/dist/manifest.json` | JSON manifest — versions, files, hashes |
| `/dist/versions.env` | flat manifest parsed by install.sh |
| `/dist/v3.7.0/SHA256SUMS` | canonical per-version checksums |
| `/dist/v3.7.0/mozhi-interpreter-*` | the interpreter binaries |
| `/docs-content.json` | client search index |

## Query the database yourself

With the SDK and server-side credentials you can inspect the same tables
from your own tooling:

```js
import NxDB from "nxmirror-db";

const db = await NxDB.connect({
  databaseId: process.env.NXDB_ID,
  password: process.env.NXDB_PASSWORD
});

const releases = await db.query("SELECT version, is_latest FROM mz_releases ORDER BY published_at DESC");
const files    = await db.query("SELECT filename, sha256, bytes, url FROM mz_files WHERE version = ?", ["v3.7.0"]);
const docs     = await db.query("SELECT slug, guide, title FROM mz_docs ORDER BY guide, sort");
```

## Table schemas

```sql
mz_releases(version TEXT PRIMARY KEY, published_at TEXT,
            is_latest INTEGER, is_allowed INTEGER, notes TEXT)

mz_files(version TEXT, filename TEXT, flavor TEXT, arch TEXT,
         bytes INTEGER, sha256 TEXT, url TEXT,
         PRIMARY KEY (version, filename))

mz_docs(slug TEXT PRIMARY KEY, guide TEXT, title TEXT, sort INTEGER,
        description TEXT, words INTEGER, updated_at TEXT)

mz_db_files(version TEXT, filename TEXT, file_id TEXT, public_url TEXT,
            sha256 TEXT, bytes INTEGER,
            PRIMARY KEY (version, filename))
```
