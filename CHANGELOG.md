# Changelog

All notable changes to the Sino programming language will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

_No unreleased changes yet._

---

## [v1.0.0] — 2026-08-01

### Added

- **Initial public release** of the Sino programming language.
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
- **File Execution**: Run Sino scripts from `.si` files.
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
- **Linux x86_64 is the only officially supported platform**. macOS, Windows, and other Linux architectures are community-supported.
- **Reserved but unimplemented keywords**: `async`, `await`, `this`, `new`, `use`.

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
[Releases page](https://github.com/crossberry-in/sino-lang-docs/releases).
