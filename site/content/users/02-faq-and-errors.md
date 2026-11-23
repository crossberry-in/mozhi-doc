---
title: FAQ and common errors
description: The errors real terminal sessions hit most — PARSE001 func colon, missing mozhi.toml entry, no test files, TLS limits — with fixes.
---

# FAQ and common errors

All outputs below are real terminal captures from the latest allowed
release (v3.7.0).

## PARSE001 — unexpected token at the function colon

You put a colon after a function declaration:

```mozhi
# WRONG
func main():
    print("hi")
```

Real terminal output (note the `3:13` pointer):

```text
error[PARSE001]: unexpected token
  --> bad.mz:3:13
3 | func main():
  |             ^
```

Mozhi function declarations use braces and **no colon**:

```mozhi
# RIGHT
func main() {
    print("hi")
}
```

This is the most common error from converting Python-style habits —
braces, not colons. Related colon diagnostics are documented as
`PARSE004`, and every error page lives under
`https://crossberry-in.github.io/mozhi-doc/errors/`.

## `mozhi dev` / `mozhi build` — entry not found

Outside a project (or with a missing `mozhi.toml`) these fail with:

```text
mozhi build: entry 'main.mz' not found (set [project] entry in mozhi.toml)
```

Fix: run the command inside the project folder, and make sure
`mozhi.toml` defines the entry:

```toml
[project]
name = "mylib"
version = "0.1.0"
entry = "main.mz"
```

Note the split: `mozhi.toml` belongs to the language tools (`mozhi dev`,
`build`, `test`, `serve`), while `nx-pkg.json` belongs to the registry
tools (`nxc pkg`). Different files, different commands.

## `mozhi test` finds no tests

```text
No *.test.mz files in /path/to/project
```

The test runner looks for `*.test.mz` files (in `tests/` by default).
Add at least one:

```text
mylib/
├── mozhi.toml
└── tests/
    └── mylib.test.mz
```

## HTTPS client calls return an error

The release binaries are built with Zig without TLS, so `https://`
requests from the HTTP client return a recoverable error (a value you
can handle, not a crash). Use `http://`, or build the interpreter from
source with OpenSSL for native TLS. The AI Diagnosis service reports
`NO_TLS` for the same reason and falls back to local diagnosis — disable
it entirely with `--no-ai` if you prefer.

## The installer warns about an existing `mz`

If a different program already owns the name `mz`, the installer leaves
it alone and skips the alias (it never overwrites a foreign command).
Use the full `mozhi` command, or rename your other `mz` and re-run the
installer.

## `~/.local/bin is not on your PATH`

```sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

## Which install method should I use?

Both produce identical installs:

- `curl -fsSL https://mz.netlify.app/install.sh | sh` — no Node.js
  needed; works on glibc, musl/Alpine, Termux, macOS; verifies SHA-256.
- `npm install -g @crossberryweb/mozhi` — the Node.js route with the
  static Linux binaries bundled.

Pin versions with `sh -s -- v3.7.0` (any allowed version), and list
versions with `sh -s -- list`.

## How do agents and LLMs read these docs?

Without any login:

```sh
curl -fsSL "https://mz.netlify.app/api/docs?q=func colon"
curl -fsSL "https://mz.netlify.app/api/docs?path=users/02-faq-and-errors"
curl -fsSL "https://mz.netlify.app/api/releases"
```

Search with `q=`, read the winning page with `path=` — the docs API page
in the developers guide documents every parameter.

## Where do the error pages live?

The full error reference (one page per diagnostic code) is published at
`https://crossberry-in.github.io/mozhi-doc/errors/` — for example the
`PARSE001` and `PARSE004` pages. The developers guide explains how to
add a new error page when a diagnostic code is introduced.
