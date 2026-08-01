# Sino Programming Language

<div align="center">

**A simple, Python-like scripting language implemented in C with a tree-walking interpreter.**

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Platform: Linux](https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows%20%7C%20Termux-blue.svg)](#supported-platforms)
[![Version: v1.0.0](https://img.shields.io/badge/Version-v1.0.0-green.svg)](https://github.com/crossberry-in/sino-doc/releases)

</div>

---

## Overview

**Sino** is a lightweight, beginner-friendly scripting language with its own unique syntax. It is implemented in C as a tree-walking interpreter, designed for learning, rapid prototyping, and embedding in larger applications. Sino supports variables, constants, functions, closures, classes, arrays, and a rich set of built-in functions.

> **Note:** The Sino source code is **closed-source and proprietary**. This repository contains only the **public documentation, installation guide, usage guide, and binary releases**. Source code is maintained privately by the project maintainers.

---

## Documentation

- **[Installation Guide](INSTALL.md)** — How to install Sino on your system
- **[Usage Guide](USAGE.md)** — How to use the Sino interpreter (REPL, files, examples)
- **[Language Reference](LANGUAGE_REFERENCE.md)** — Complete language syntax and features
- **[Examples](examples/)** — Sample Sino programs to learn from
- **[Changelog](CHANGELOG.md)** — Version history and changes
- **[FAQ](FAQ.md)** — Frequently asked questions

---

## Quick Start

### 1. Install

**Linux / macOS / WSL / Termux** (auto-detects platform and architecture):

```bash
curl -fsSL https://github.com/crossberry-in/sino-doc/raw/main/install.sh | bash
```

**Windows** (PowerShell):

```powershell
irm https://github.com/crossberry-in/sino-doc/raw/main/install.ps1 | iex
```

### 2. Verify

```bash
sino --version
# or simply:
sino
```

You should see the Sino REPL prompt.

### 3. Hello, World!

Create a file `hello.si`:

```sino
echo "Hello, World!"
```

Run it:

```bash
sino hello.si
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
| Linux (Ubuntu, Debian, Fedora, Arch) | x86_64 | glibc | `sino-linux-x86_64` | ✅ Supported |
| Linux (Raspberry Pi 4/5, ARM servers) | ARM64 (aarch64) | glibc | `sino-linux-arm64` | ✅ Supported |
| Alpine Linux | x86_64 | musl (static) | `sino-alpine-x86_64` | ✅ Supported |
| Alpine Linux | ARM64 (aarch64) | musl (static) | `sino-alpine-arm64` | ✅ Supported |
| Termux on Android | ARM64 (aarch64) | bionic (static musl) | `sino-alpine-arm64` | ✅ Supported |
| Termux on Android | x86_64 | bionic (static musl) | `sino-alpine-x86_64` | ✅ Supported |
| macOS (Intel) | x86_64 | Darwin | `sino-macos-x86_64` | ✅ Supported |
| macOS (Apple Silicon M1/M2/M3/M4) | ARM64 | Darwin | `sino-macos-arm64` | ✅ Supported |
| Windows 10/11 | x86_64 | MSVCRT | `sino-windows-x86_64.exe` | ✅ Supported |

> **Note for Termux users:** Sino uses static musl binaries which run natively in Termux — no `proot` needed. Just run the install command above.
>
> **Note for Windows users:** You can run Sino natively (via `sino.exe` in PowerShell/CMD) or via WSL (using the Linux x86_64 build). Both work.
>
> **Building from source:** Source code is private. If you need a build for an unsupported platform (e.g., FreeBSD, OpenBSD, Linux 32-bit), please [open an issue](https://github.com/crossberry-in/sino-doc/issues) to request a binary.

---

## License

Sino is **proprietary software**. The binary is freely available for download and use, but the source code is closed and may not be redistributed.

See [LICENSE](LICENSE) for full terms.

---

## Community

- **Report bugs:** [Open an issue](https://github.com/crossberry-in/sino-doc/issues)
- **Request features:** [Open an issue](https://github.com/crossberry-in/sino-doc/issues)
- **Discussions:** [GitHub Discussions](https://github.com/crossberry-in/sino-doc/discussions)

---

## Links

- **Releases:** https://github.com/crossberry-in/sino-doc/releases
- **Documentation:** This repository
- **Author:** [crossberry-in](https://github.com/crossberry-in)

---

<div align="center">

**Sino** — Crafted with care for learners and tinkerers.

</div>
