# Changelog

All notable changes to the Mozhi programming language will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

_No unreleased changes yet._
---

## [v2.4.0] — 2026-08-02

### Added

- **File I/O builtins**: `read_file(path)`, `write_file(path, content)`, `file_exists(path)`, `list_dir(path)`
- **Shell/System builtins**: `run(cmd)`, `shell(cmd)`, `run_mz(file)`, `run_c(file)`, `run_cpp(file)`, `run_py(file)`, `run_sh(file)`
- **HTTP static file serving**: `http_serve_file(path)`, `http_serve_static(path, dir)`, `http_content_type(path)`
- **HTTP multi-language**: `http_run_mz(path)`, `http_run_c(path)`, `http_run_py(path)`, `http_run_sh(path)`
- **Multi-language server example** (`multilang_server.mz`) — serves `index.html` + runs `.sh`/`.mz`/`.c`/`.py` via HTTP

## [v2.3.0] — 2026-08-02

### Added

- **Import system**: `import http from "mozhi-http"` (namespace), `import html` (wildcard), `import my from "mylib.mz"` (file path)
- **Auto-download**: libraries auto-download from GitHub to `./.mozhi/libs/` on first use
- **Smart search**: checks project-local `.mozhi/libs/` then global `~/.mozhi/libs/`
- **Module constants**: `math_utils.PI`, `math_utils.E`
- **New builtins**: `slice(start, end)`, `index(substring)`

## [v2.2.0] — 2026-08-02

### Added

- **Library package system**: `mozhi-registry.json` manifest with 5 official libraries
- **`mozhi add` / `mozhi update` commands** in TUI
- **Library CI workflow** that auto-builds and publishes libraries

## [v2.1.0] — 2026-08-01

### Added

- **Go TUI CLI** with glassmorphism UI (Bubble Tea, Lip Gloss)
- **Cross-compilation** with Zig for 7 interpreter targets + 5 TUI targets
- **GitHub Actions CI/CD** workflow


---

## [v1.0.0] — 2026-08-01

### Added

- **Initial public release** of the Mozhi programming language.
- **Cross-platform binaries** for 7 target platforms (built with `zig cc` as a cross-compiler):
  - `mozhi-interpreter-linux-x86_64` — Linux x86_64 (glibc, dynamically linked)
  - `mozhi-interpreter-linux-arm64` — Linux ARM64/aarch64 (glibc, dynamically linked)
  - `mozhi-interpreter-alpine-x86_64` — Alpine Linux x86_64 (musl, statically linked)
  - `mozhi-interpreter-alpine-arm64` — Alpine Linux ARM64 (musl, statically linked)
  - `mozhi-windows-x86_64.exe` — Windows 10/11 x86_64 (statically linked)
  - `mozhi-interpreter-macos-x86_64` — macOS Intel (Darwin)
  - `mozhi-interpreter-macos-arm64` — macOS Apple Silicon M1/M2/M3/M4 (Darwin)
- **Termux (Android) support** — works natively via the static musl build (`mozhi-interpreter-alpine-arm64` for Android phones, `mozhi-interpreter-alpine-x86_64` for x86 emulators). No `proot` or `proot-distro` needed.
- **Universal `install.sh` installer** for Linux / macOS / WSL / Termux — auto-detects OS, architecture, and libc, then downloads the correct binary.
- **`install.ps1` PowerShell installer** for native Windows 10/11 — installs to `%USERPROFILE%\.mozhi\bin\` and adds it to the user `PATH`.
- **Lexer** supporting identifiers, integers, floats, strings, booleans, `null`, keywords, operators, and comments.
- **Parser** producing an Abstract Syntax Tree (AST) for the entire language.
- **Tree-walking interpreter** evaluating the AST directly.
- **Variables**:
  - `var` — mutable variable declaration
  - `fix` — immutable constant declaration
  - `let` — alternative mutable declaration (alias for `var`)
  - `const` — alternative constant declaration (alias for `fix`)
- **Functions**:
  - `func` — named function declaration
  - `fn` — anonymous function expression
  - Closures (functions capture their enclosing scope)
  - Higher-order functions (functions as arguments and return values)
  - Recursion
- **Classes**:
  - `class` keyword for class declaration
  - `init` constructor
  - `self` reference within methods
  - Instance variables via `self.var = value`
  - Method calls on instances
- **Arrays**:
  - Literal syntax `[1, 2, 3]`
  - Index access `arr[i]`
  - Mixed-type arrays
  - `push(arr, val)` — add element
  - `pop(arr)` — remove and return last element
  - `len(arr)` — get array length
  - `join(arr, sep)` — join elements with separator
- **Control Flow**:
  - `if` / `elseif` / `else` / `end`
  - `while` / `end`
  - `for var i = 0; i < n; i = i + 1:` / `end`
  - `for var item in arr:` / `end`
  - `match` / `case` / `default` / `end`
  - `break` — exit loop
  - `continue` — skip to next iteration
- **Operators**:
  - Arithmetic: `+`, `-`, `*`, `/`, `%`, `**` (power), unary `-`
  - Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
  - Logical: `and`, `or`, `not`
  - String concatenation via `+`
- **Built-in Functions**:
  - `echo(...)` and `print(...)` — print values to stdout
  - `input(prompt)` — read input from stdin
  - `len(x)` — length of array or string
  - `typeof(x)` — type name as string
  - Type conversions: `int(x)`, `float(x)`, `string(x)`
  - Array operations: `push(arr, val)`, `pop(arr)`, `join(arr, sep)`
  - Math: `sqrt(x)`, `abs(x)`, `floor(x)`, `ceil(x)`
- **Comments**: Single-line comments with `#`.
- **REPL**: Interactive Read-Eval-Print Loop.
- **File Execution**: Run Mozhi scripts from `.mz` files.
- **Makefile**: Standard build system with `make`, `make clean`, `make run`, `make repl`, `make file` targets.

### Documentation

- **README.md** — Project overview and quick start.
- **INSTALL.md** — Installation guide for Linux, macOS, and Windows.
- **USAGE.md** — Usage guide covering REPL, file execution, and language basics.
- **LANGUAGE_REFERENCE.md** — Complete language reference.
- **FAQ.md** — Frequently asked questions.
- **CHANGELOG.md** — This file.

### Known Limitations

- **Single-threaded** execution only.
- **No file I/O** (file reading/writing not yet supported).
- **No networking** capabilities.
- **No module system** (the `use` keyword is reserved but not implemented).
- **No exception handling** (runtime errors halt execution).
- **No class inheritance**.
- **No string interpolation** in the current form (use `string()` and `+`).
- **Reserved but unimplemented keywords**: `async`, `await`, `this`, `new`, `use`.
- **Supported platforms**: Linux x86_64 (glibc), Linux ARM64 (glibc), Alpine Linux x86_64 (musl, static), Alpine Linux ARM64 (musl, static), Termux on Android ARM64/x86_64 (via static musl build), macOS Intel (x86_64), macOS Apple Silicon (ARM64), Windows 10/11 x86_64. macOS/Windows native builds work without WSL/Docker. Other platforms (FreeBSD, OpenBSD, Linux 32-bit, Windows ARM64) are not yet supported.

---

## Version History

| Version | Release Date | Notes |
|---------|--------------|-------|
| v1.0.0  | 2026-08-01   | Initial public release |

---

## How to Read This Changelog

- **Added** — New features
- **Changed** — Changes to existing functionality
- **Deprecated** — Soon-to-be removed features
- **Removed** — Removed features
- **Fixed** — Bug fixes
- **Security** — Security-related fixes

---

For the full release history and binary downloads, visit the
[Releases page](https://github.com/crossberry-in/mozhi-doc/releases).
