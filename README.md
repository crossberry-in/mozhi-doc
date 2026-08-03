# Mozhi Programming Language

<div align="center">

**A simple, Python-like scripting language implemented in C with a tree-walking interpreter.**

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Termux-blue.svg)](#supported-platforms)
[![Version: v2.4.0](https://img.shields.io/badge/Version-v2.4.0-green.svg)](https://github.com/crossberry-in/mozhi-doc/releases)

</div>

---

## Overview

**Mozhi** is a lightweight, beginner-friendly scripting language with its own unique syntax. It is implemented in C as a tree-walking interpreter, designed for learning, rapid prototyping, and embedding in larger applications. Mozhi supports variables, constants, functions, closures, classes, arrays, and a rich set of built-in functions.

> **Note:** The Mozhi source code is **closed-source and proprietary**. This repository contains only the **public documentation, installation guide, usage guide, and binary releases**. Source code is maintained privately by the project maintainers.

---

## Documentation

- **[Installation Guide](INSTALL.md)** — How to install Mozhi on your system
- **[Usage Guide](USAGE.md)** — How to use the Mozhi interpreter (REPL, files, examples)
- **[Language Reference](LANGUAGE_REFERENCE.md)** — Complete language syntax and features
- **[mozhi-fast (Rust VM)](docs/mozhi-fast.md)** — The faster Rust bytecode-VM interpreter
- **[Chart Gallery](docs/chart-gallery.html)** — 33 chart types of mozhi-mini vs mozhi-fast benchmarks
- **[Examples](examples/)** — Sample Mozhi programs to learn from
- **[Changelog](CHANGELOG.md)** — Version history and changes
- **[FAQ](FAQ.md)** — Frequently asked questions

---

## What's New in v2.6.0

### mozhi-fast — Rust bytecode VM
A **faster Rust implementation** of the Mozhi interpreter. Compiles Mozhi
source to bytecode and runs it on a stack-based VM — faster and memory-safe,
with correct 64-bit arithmetic.

```bash
# build from source (see docs/mozhi-fast.md)
cd mozhi-fast && cargo build --release
./target/release/mozhi-fast file.mz
```

Full details: **[docs/mozhi-fast.md](docs/mozhi-fast.md)**

## What's New in v2.4.0

### File I/O Builtins
```mozhi
content = read_file("data.txt")
write_file("output.txt", "Hello!")
if file_exists("config.json") {
    echo("Config found")
}
files = list_dir(".")
```

### Shell & Multi-Language Run
```mozhi
# Run shell commands
result = run("ls -la")

# Run other language files
output = run_c("program.c")      # compile & run C
output = run_cpp("program.cpp")  # compile & run C++
output = run_py("script.py")     # run Python
output = run_sh("script.sh")     # run shell script
output = run_mz("other.mz")      # run Mozhi file
```

### Smart Imports (v2.3.0+)
```mozhi
import html                        # wildcard (func() directly)
import http from "mozhi-http"      # namespace (http.func())
import my from "mylib.mz"          # file path (my.func())
```
Libraries auto-download from GitHub on first use — no `mozhi add` needed!

### HTTP Static File Serving
```mozhi
import http from "mozhi-http"

fn handler(method, path) {
    # Serve index.html for /, style.css for /style.css, etc.
    return http.http_serve_static(path, "public")
}

server = http.http_start(8080)
http.http_serve_loop(server, handler)
```

### Library Package System
5 official libraries (112 functions total):
- `mozhi-html` — 38 HTML generators
- `mozhi-http` — 15+ HTTP server utilities
- `mozhi-json` — 14 JSON encode/decode helpers
- `mozhi-math-utils` — 24 math functions + PI, E
- `mozhi-strings` — 21 string manipulation functions

Install with: `mozhi add mozhi-http` (or just use `import http from "mozhi-http"`)

---

## Quick Start

### 1. Install

**Linux / macOS / WSL / Termux** (auto-detects platform and architecture):

```bash
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

**Windows** (PowerShell):

```powershell
irm https://github.com/crossberry-in/mozhi-doc/raw/main/install.ps1 | iex
```

### 2. Verify

```bash
mozhi --version
# or simply:
mozhi
```

You should see the Mozhi REPL prompt.

### 3. Hello, World!

Create a file `hello.mz`:

```mozhi
echo "Hello, World!"
```

Run it:

```bash
mozhi hello.mz
```

Output:
```
Hello, World!
```

---

## Features

- **Simple Syntax** — Clean, Python-like syntax with `end` keyword instead of indentation
- **Variables** — Mutable `var` and immutable `fix` declarations
- **Functions** — Named functions (`func`) and anonymous functions (`fn`)
- **Closures** — Functions capture their enclosing scope
- **Classes** — Object-oriented programming with `class`, `self`, and methods
- **Arrays** — Ordered, mutable collections with `push`, `pop`, `len`
- **Control Flow** — `if/elseif/else`, `while`, `for`, `for-in`, `match`
- **Built-ins** — `echo`, `input`, `len`, `typeof`, `int`, `float`, `string`, `sqrt`, `abs`, `floor`, `ceil`, and more
- **String Interpolation** — Embed expressions inside strings
- **Lightweight** — Single static binary, no runtime dependencies (musl/static builds) or just `libc`+`libm` (glibc builds)
- **Cross-Platform** — Runs on Linux (glibc and musl/Alpine), macOS (Intel and Apple Silicon), Windows (10/11 x86_64), and Termux on Android

---

## Supported Platforms

The installer auto-detects your OS, architecture, and libc, then downloads the correct binary.

| Platform | Architecture | Libc | Asset name | Status |
|----------|--------------|------|------------|--------|
| Linux (Ubuntu, Debian, Fedora, Arch) | x86_64 | glibc | `mozhi-interpreter-linux-x86_64` | ✅ Supported |
| Linux (Raspberry Pi 4/5, ARM servers) | ARM64 (aarch64) | glibc | `mozhi-interpreter-linux-arm64` | ✅ Supported |
| Alpine Linux | x86_64 | musl (static) | `mozhi-interpreter-alpine-x86_64` | ✅ Supported |
| Alpine Linux | ARM64 (aarch64) | musl (static) | `mozhi-interpreter-alpine-arm64` | ✅ Supported |
| Termux on Android | ARM64 (aarch64) | bionic (static musl) | `mozhi-interpreter-alpine-arm64` | ✅ Supported |
| Termux on Android | x86_64 | bionic (static musl) | `mozhi-interpreter-alpine-x86_64` | ✅ Supported |
| macOS (Intel) | x86_64 | Darwin | `mozhi-interpreter-macos-x86_64` | ✅ Supported |
| macOS (Apple Silicon M1/M2/M3/M4) | ARM64 | Darwin | `mozhi-interpreter-macos-arm64` | ✅ Supported |
| Windows 10/11 | x86_64 | MSVCRT | `mozhi-windows-x86_64.exe` | ✅ Supported |

> **Note for Termux users:** Mozhi uses static musl binaries which run natively in Termux — no `proot` needed. Just run the install command above.
>
> **Note for Windows users:** You can run Mozhi natively (via `mozhi.exe` in PowerShell/CMD) or via WSL (using the Linux x86_64 build). Both work.
>
> **Building from source:** Source code is private. If you need a build for an unsupported platform (e.g., FreeBSD, OpenBSD, Linux 32-bit), please [open an issue](https://github.com/crossberry-in/mozhi-doc/issues) to request a binary.

---

## License

Mozhi is **proprietary software**. The binary is freely available for download and use, but the source code is closed and may not be redistributed.

See [LICENSE](LICENSE) for full terms.

---

## Community

- **Report bugs:** [Open an issue](https://github.com/crossberry-in/mozhi-doc/issues)
- **Request features:** [Open an issue](https://github.com/crossberry-in/mozhi-doc/issues)
- **Discussions:** [GitHub Discussions](https://github.com/crossberry-in/mozhi-doc/discussions)

---

## Links

- **Releases:** https://github.com/crossberry-in/mozhi-doc/releases
- **Documentation:** This repository
- **Author:** [crossberry-in](https://github.com/crossberry-in)

---

<div align="center">

**Mozhi** — Crafted with care for learners and tinkerers.

</div>
