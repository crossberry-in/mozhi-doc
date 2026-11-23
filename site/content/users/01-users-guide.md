---
title: Users guide — run Mozhi every day
description: Running scripts, the project workflow, the web server, built-in modules, libraries and apps with mz.
---

# Users guide

Everything here assumes `mz` (or the full name `mozhi`) is installed —
see the install page in the developers guide if it is not. All commands
are verified against the latest allowed release (v3.7.0).

## Your first script

Save `hello.mz`:

```mozhi
print("Hello from Mozhi")
```

Run it three equivalent ways:

```sh
mz run hello.mz
mozhi run hello.mz
mz hello.mz
```

Top-level code runs directly — you do not need a `main` wrapper for
simple scripts. When you do want one, remember the rule: **function
declarations take no colon**:

```mozhi
func main() {
    print("hi")
}

main()
```

## The built-in modules

Mozhi ships a full server-side platform inside the interpreter:

```mozhi
import web
import json
import math
import db
import fs
```

| Module | What it gives you |
| --- | --- |
| `web` | HTTP server: routing with `:params`, middleware, static files, cookies |
| `json` | strict parser/serializer with validation |
| `math` | 30+ functions with a defined numeric error policy |
| `db` | SQLite with prepared statements, transactions, migrations |
| `fs` | sandboxed filesystem (traversal + symlink protected) |

## A tiny web app

```mozhi
import web

let app = web.create()

app.get("/", fn(req, res) {
    return res.render("index.html", { title: "Hello" })
})

app.get("/api/health", fn(req, res) {
    return res.json({ status: "ok", language: "Mozhi" })
})

app.listen("127.0.0.1", 8080)
```

The fast way to start a project is the scaffold:

```sh
mozhi new myapp --template web
cd myapp
mozhi dev          # auto-reload dev server from mozhi.toml
```

`mozhi dev` reads the `[server]` host/port from `mozhi.toml`; the
scaffold puts a working app template in place. The full guide is
`docs/WEB_GUIDE.md` in the mozhi repository, with a working example in
`examples/mozhi-web/`.

## Libraries

Two ways to get libraries:

**Auto-download imports** — just import; the interpreter fetches the
package on first run:

```mozhi
import strings from "strings"
print(strings.slugify("Hello Mozhi Docs"))    # → hello-mozhi-docs
```

Available libraries include `strings`, `datetime`, `crawler`,
`mozhi-html`, `mozhi-http`, `mozhi-json` and `mozhi-math-utils`.

**Registry packages** — install explicitly with nxc:

```sh
nxc pkg search crawler
nxc pkg install crossberry-in/crawler
```

## Everyday CLI commands

| Command | Purpose |
| --- | --- |
| `mozhi` | start the REPL |
| `mozhi <file.mz>` / `mozhi run <file.mz>` | run a script |
| `mozhi new <name> [--template web\|minimal]` | scaffold a new project |
| `mozhi dev` | run the project with auto-reload |
| `mozhi serve` | run the project without auto-reload |
| `mozhi test [dir]` | run `*.test.mz` files (default `tests/`) |
| `mozhi build [--release]` | verify imports, emit a `dist/` bundle |
| `mozhi fmt [path]` | re-indent `.mz` files |
| `mozhi lint [path]` | parse checks + basic warnings |
| `mozhi version` / `mozhi help` | version and help |

Global options worth knowing: `--json` (machine-readable diagnostics),
`--no-color`, `--no-ai` (disable AI Diagnosis), `--verbose`.

## Apps (packaging your code)

Mozhi apps follow an Android-like shape — write `.mz`, build a `.pkg`,
install, open from a launcher:

```sh
mz app new counter --id in.crossberry.counter --label Counter
mz app build counter                          # → dist/counter-0.1.0.pkg
mz app install counter/dist/counter-0.1.0.pkg # → ~/.mozhi/apps/<id>/
mz app open in.crossberry.counter
mz app home                                   # launcher home screen
```

This app toolchain is documented in the repository README
(`docs/APPS.md`, example in `examples/counter-app/`) and ships with
builds newer than the current allowed release — `mozhi dev`/`build`
above are what v3.7.0 gives you today.

## Known limits of the release binaries

The published binaries are built with Zig **without TLS**: `https://`
URLs from the HTTP client return a recoverable error instead of
crashing, and AI Diagnosis reports `NO_TLS` on those builds (it falls
back to local diagnosis). Building the interpreter from source with
OpenSSL gives native TLS. `http://` requests work everywhere.

## Updating

Re-run the installer (it always picks the latest allowed release) or use
npm:

```sh
curl -fsSL https://mz.netlify.app/install.sh | sh
npm update -g @crossberryweb/mozhi
```

See the FAQ page for the errors you are most likely to meet.
