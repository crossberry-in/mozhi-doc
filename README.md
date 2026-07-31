# Sino Programming Language

<div align="center">

**A simple, Python-like scripting language implemented in C with a tree-walking interpreter.**

[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)
[![Platform: Linux x86_64](https://img.shields.io/badge/Platform-Linux%20x86__64-blue.svg)](#installation)
[![Version: v1.0.0](https://img.shields.io/badge/Version-v1.0.0-green.svg)](https://github.com/crossberry-in/sino-lang-docs/releases)

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

### 1. Download

Download the latest binary release from the [Releases page](https://github.com/crossberry-in/sino-lang-docs/releases).

### 2. Install

```bash
# Make the binary executable
chmod +x sino-linux-x86_64

# Move it to a directory in your PATH (e.g., /usr/local/bin)
sudo mv sino-linux-x86_64 /usr/local/bin/sino
```

### 3. Verify

```bash
sino --version
# or simply:
sino
```

You should see the Sino REPL prompt.

### 4. Hello, World!

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
- **Lightweight** — Single static binary, no runtime dependencies beyond `libc` and `libm`

---

## Supported Platforms

| Platform | Architecture | Status | Download |
|----------|--------------|--------|----------|
| Linux | x86_64 (64-bit) | ✅ Supported | `sino-linux-x86_64` |
| Linux | ARM64 (aarch64) | ⚠️ Community | Build from source |
| macOS | Intel / Apple Silicon | ⚠️ Community | Build from source |
| Windows | x86_64 | ⚠️ Use WSL | Run via Windows Subsystem for Linux |

> **Building from source:** Source code is private. If you need a build for an unsupported platform, please [open an issue](https://github.com/crossberry-in/sino-lang-docs/issues) to request a binary.

---

## License

Sino is **proprietary software**. The binary is freely available for download and use, but the source code is closed and may not be redistributed.

See [LICENSE](LICENSE) for full terms.

---

## Community

- **Report bugs:** [Open an issue](https://github.com/crossberry-in/sino-lang-docs/issues)
- **Request features:** [Open an issue](https://github.com/crossberry-in/sino-lang-docs/issues)
- **Discussions:** [GitHub Discussions](https://github.com/crossberry-in/sino-lang-docs/discussions)

---

## Links

- **Releases:** https://github.com/crossberry-in/sino-lang-docs/releases
- **Documentation:** This repository
- **Author:** [crossberry-in](https://github.com/crossberry-in)

---

<div align="center">

**Sino** — Crafted with care for learners and tinkerers.

</div>
