---
title: Mozhi docs — how to add and update pages
description: Where the Mozhi documentation lives and how to add or update pages in the mz-docs site and the mozhi-doc repository.
---

# Mozhi docs — add and update

Documentation lives in two repositories. This page explains what goes
where and the exact steps to change each.

## The two documentation homes

| Repo | Site | Content |
| --- | --- | --- |
| `crossberry-in/mz-docs` (this repo, private) | `https://mz.netlify.app` | install guide, package deploy, SDK, API docs |
| `crossberry-in/mozhi-doc` (public) | `https://crossberry-in.github.io/mozhi-doc/` | language spec, reference, error pages, benchmarks |

The release binaries that the installer downloads are attached to
releases in `crossberry-in/mozhi-doc` — that repository must stay
public, because it is the download host for every `install.sh`.

## Add or update a page on this site

1. Add a markdown file under `content/developers/` or `content/users/`.
   The filename pattern is `NN-slug.md` where `NN` sets the sidebar order:

   ```text
   content/developers/06-my-new-page.md
   ```

2. Optional frontmatter at the top — `title` and `description` fall back
   to the first `#` heading and first paragraph when omitted:

   ```markdown
   ---
   title: My new page
   description: One line shown in search results.
   ---
   ```

3. That is the whole job. The build regenerates everything automatically:
   the sidebar, the client search index, the static pages and the
   `/api/docs` data. Open a pull request and Netlify builds a deploy
   preview for it.

Page URLs follow the directory + filename:
`https://mz.netlify.app/docs/developers/my-new-page/`.

## Add or update error pages in mozhi-doc

The error reference uses one page per diagnostic code
(`PARSE001`, `PARSE004`, `RUNTIME010`, ...). To add one:

1. Create `errors/PARSEXXX.md` in `crossberry-in/mozhi-doc` with the
   standard shape: the error message, the smallest code that triggers it,
   the fix, and a link from the errors index.
2. The interpreter's diagnostics link directly to
   `https://crossberry-in.github.io/mozhi-doc/errors/PARSEXXX` — keep the
   filename exactly the code.
3. Example pages worth copying as templates: `errors/PARSE001.md`
   (function declaration colon) and `errors/PARSE004.md`.

## Add or update a library in the Mozhi registry

Library imports that auto-download are indexed by `mozhi-registry.json`
at the root of `crossberry-in/mozhi-doc`. To add or update a library:

```json
{
  "name": "mylib",
  "version": "1.0.0",
  "description": "What it does",
  "author": "...",
  "license": "MIT",
  "category": "general",
  "keywords": ["..."],
  "repo": "crossberry-in/mozhi-mylib",
  "dist": "releases",
  "asset": "mylib.mz.pkg.zip",
  "import_as": "mylib",
  "official": false
}
```

`import_as` is what users write after `import`; `repo` + `dist` + `asset`
tell the interpreter where to fetch the package archive. Keep
`LIBRARIES.md` in sync with the same change.

## Update the language spec / guides in mozhi-doc

The big documents (`spec.md`, `LANGUAGE_REFERENCE.md`, `USAGE.md`,
`INSTALL.md`, `FAQ.md`) are plain markdown at the repository root — edit,
open a PR, and GitHub Pages republishes. `install.sh` in that repository
is the legacy installer; the site installer on `mz.netlify.app` is the
canonical one documented here.

## Rules that apply everywhere

- Public docs never contain credentials, tokens or account secrets of
  any kind — placeholders like `process.env.NXDB_PASSWORD` only.
- Every code sample must be runnable with the latest allowed release.
- Every new command must appear in the users guide FAQ if it can fail in
  an obvious way (missing manifest, missing tests, colon after `func`).
