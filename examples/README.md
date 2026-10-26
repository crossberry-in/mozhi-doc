# Mozhi — Examples

This directory contains sample Mozhi programs (`.mz` files) to help you learn the language.

---

## Verified examples (v3.1)

These ten programs are **executed against the v3.1 interpreter before every
publish** — servers are curled, databases are queried, assertions must pass.
They are showcased on the [Examples page](https://crossberry-in.github.io/mozhi-doc/examples.html).

Run them with the current CLI:

```bash
mozhi run examples/basics_hello.mz
```

| File | What it shows | Needs |
|------|---------------|-------|
| [`basics_hello.mz`](basics_hello.mz) | Language tour: variables, functions, control flow, maps, string methods | — |
| [`math_showcase.mz`](math_showcase.mz) | Native math module: constants, trig, logs, reductions, seeded randomness | — |
| [`json_showcase.mz`](json_showcase.mz) | Strict JSON: parse, stringify, pretty, validate with position-tagged errors | — |
| [`fs_notebook.mz`](fs_notebook.mz) | Sandboxed filesystem: write/read/append/list/remove with path validation | — |
| [`templates_hello.mz`](templates_hello.mz) | HTML templates: auto-escaping (live XSS blocked), filters, if/for | — |
| [`db_notes.mz`](db_notes.mz) | SQLite: migrations, parameterized queries, transactions, injection attempt fails | writes `data/` |
| [`web_hello.mz`](web_hello.mz) | Minimal web server: routes, JSON health, path params, custom 404 | listens on :8080 |
| [`web_api.mz`](web_api.mz) | JSON API: middleware, validation, cookies, query strings, 404/500 handlers | listens on :8081 |
| [`http_client.mz`](http_client.mz) | HTTP client: GET/POST with JSON against the local example servers | run the servers first |
| [`app_tests.mz`](app_tests.mz) | Test pattern: assert family, grouping, timing | — |

Notes:
- Server examples listen until interrupted (Ctrl-C).
- The native HTTP client speaks plain `http://` — TLS is on the roadmap.
- `try`/`catch` is parsed but not yet evaluated; examples avoid it by design.

---

---

## Quick Start

```bash
# Install Mozhi
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/install.sh | bash

# Run any example
mozhi run hello.mz
mozhi run file_io.mz
mozhi run http_server.mz
```

---

## Examples by Category

### Basics

| File | Description |
|------|-------------|
| [`hello.mz`](hello.mz) | Hello World and basic syntax demo |
| [`basics.mz`](basics.mz) | Variables, constants, control flow, and functions |
| [`factorial.mz`](factorial.mz) | Recursive factorial function |
| [`fibonacci.mz`](fibonacci.mz) | Recursive Fibonacci sequence |
| [`match.mz`](match.mz) | Pattern matching with `match`/`case` |
| [`math.mz`](math.mz) | Math operations using built-in functions |
| [`sorting.mz`](sorting.mz) | Sorting algorithms (bubble sort) |
| [`classes.mz`](classes.mz) | Object-oriented programming with classes |

### File I/O (v2.4.0+)

| File | Description |
|------|-------------|
| [`file_io.mz`](file_io.mz) | `read_file`, `write_file`, `file_exists`, `list_dir` |
| [`file_processor.mz`](file_processor.mz) | Read, transform, and write files |

### Shell & System (v2.4.0+)

| File | Description |
|------|-------------|
| [`shell.mz`](shell.mz) | Run shell commands with `run()` |
| [`multilang.mz`](multilang.mz) | Run C, C++, Python, Shell, and Mozhi files |

### Imports & Libraries (v2.3.0+)

| File | Description |
|------|-------------|
| [`imports.mz`](imports.mz) | Three import styles: wildcard, namespace, file path |
| [`strings_demo.mz`](strings_demo.mz) | String library showcase |
| [`math_demo.mz`](math_demo.mz) | Math library showcase |
| [`json_demo.mz`](json_demo.mz) | JSON library showcase |

### HTTP Server (v2.4.0+)

| File | Description |
|------|-------------|
| [`http_server.mz`](http_server.mz) | Basic HTTP server with multiple routes |
| [`static_server.mz`](static_server.mz) | Serve static files from `public/` directory |
| [`api_server.mz`](api_server.mz) | JSON API server with CRUD endpoints |

### Complete Applications

| File | Description |
|------|-------------|
| [`web_app.mz`](web_app.mz) | Full web app: static files + API + multi-language |
| [`benchmark.mz`](benchmark.mz) | Benchmark Mozhi performance |

---

## Multi-Language Examples

Mozhi can run files in other languages via `run_c()`, `run_cpp()`, `run_py()`, `run_sh()`, and `run_mz()`. See the [`multilang/`](multilang/) directory for example files in each language.

---

## Running the Examples

After installing Mozhi (see the [Installation Guide](../INSTALL.md)), run any example with:

```bash
# Using the interpreter directly
mozhi run hello.mz

# Using the TUI
mozhi run hello.mz
```

---

## Importing Libraries

Libraries auto-download from GitHub on first use. No `mozhi add` needed!

```mozhi
import http from "mozhi-http"
import html from "mozhi-html"
import strings from "mozhi-strings"

# Functions are now available
echo(strings.reverse("hello"))
echo(html.html_h1("Title"))
```

See the [Libraries page](https://crossberry-in.github.io/mozhi-doc/libs.html) for the full catalog.
