# mz-docs (site/) — the Mozhi docs platform

This directory is the **Next.js** docs site for the Mozhi (mz) language,
deployed on Netlify (site name `mz` → https://mz.netlify.app). The legacy
gitHub Pages site at the repository root is untouched.

- No navigation bar — a clean sidebar + content layout
- Developer guide + users guide (`content/` markdown)
- Client-side search + a public docs API for humans, agents and LLMs
- Hosts the **manual mz installer**: `curl -fsSL https://mz.netlify.app/install.sh | sh`
- Release binaries materialize into `public/dist/` at build time — pulled
  from **NxDB file storage first** (mz_db_files → storage download), with
  the public GitHub releases as fallback. SHA-256 verified either way.
- NxDB mirrors releases, files and the docs index (`mz_releases`,
  `mz_files`, `mz_docs`, `mz_db_files`)
- `/api/dist/:version/:filename` streams any binary straight from NxDB
  file storage via a short-lived signed URL — works regardless of whether
  this repository is public or private.

## Deploy to Netlify

1. Netlify → **Add new site → Import an existing project** → connect this
   repository (private works fine).
2. Site configuration → **Site details → Change site name** → `mz`
   (gives https://mz.netlify.app).
3. Site configuration → **Environment variables** → add:
   - `NXDB_ID` — the NxDB database id (`nxdb-...`)
   - `NXDB_PASSWORD` — the database password (server-side only; the
     browser never sees it)
4. Deploy. `netlify.toml` at the repository root already points the build
   at `site/` (`npm run sync && npx next build`).

The database sync is non-fatal: without the env variables the site still
builds and the APIs serve their bundled build data + GitHub release
fallbacks.

## Local development

```sh
cd site
npm install
npm run sync          # fetch dist + build content + (optional) db sync
npm run dev           # http://localhost:3000/docs/
```

## API endpoints (public, no auth)

| Endpoint | Purpose |
| --- | --- |
| `GET /api/docs` | list docs pages |
| `GET /api/docs?q=term` | search (titles + text, scored) |
| `GET /api/docs?path=developers/01-install-mz` | read one page (markdown) |
| `GET /api/releases` | latest + allowed versions and every dist file |
| `GET /api/dist/:version/:filename` | download a binary from NxDB storage |

## Install commands served by this site

```sh
curl -fsSL https://mz.netlify.app/install.sh | sh        # latest allowed release
curl -fsSL https://mz.netlify.app/install.sh | sh -s -- list
curl -fsSL https://mz.netlify.app/install.sh | sh -s -- v3.7.0
npm install -g @crossberryweb/mozhi                       # npm route
```

## Layout

```text
content/developers/    developer guide pages (markdown)
content/users/         users guide pages (markdown)
app/                   Next.js app router (standalone layout, no nav bar)
components/Sidebar.jsx sidebar + live search
lib/md.js              safe markdown renderer (escaped first, no deps)
netlify/functions/     docs-api.mjs, releases-api.mjs, dist-proxy.mjs
public/install.sh      the manual installer
scripts/               fetch-dist.mjs, build-content.mjs, seed-db.mjs
```
