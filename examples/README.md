# Mozhi — Examples

This directory contains sample Mozhi programs (`.mz` files) to help you learn the language.

---

## Quick Start

```bash
# Install Mozhi
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/install.sh | bash

# Run any example
mozhi-interpreter hello.mz
mozhi-interpreter file_io.mz
mozhi-interpreter http_server.mz
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
mozhi-interpreter hello.mz

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
