# Sino — FAQ (Frequently Asked Questions)

---

## General

### What is Sino?

Sino is a simple, Python-like scripting language implemented in C with a tree-walking interpreter. It is designed for learning, rapid prototyping, and embedding in larger applications.

### Who created Sino?

Sino is developed by [crossberry-in](https://github.com/crossberry-in).

### Is Sino open source?

No. Sino is **closed-source and proprietary**. The binary is freely available for download and use, but the source code is private and not for redistribution.

### Is Sino free to use?

Yes, the Sino binary is free to download and use. See the [LICENSE](LICENSE) file for full terms.

### What does the name "Sino" mean?

"Sino" is a short, memorable name chosen for the language. It has no specific meaning beyond being the language's name.

---

## Technical

### What language is Sino written in?

Sino is implemented in **C99**. The interpreter is a tree-walking interpreter that parses source code into an AST and evaluates it directly.

### What platforms does Sino support?

Sino runs natively on 7 platform/architecture combinations:

| Platform | Architecture | Build type |
|----------|--------------|------------|
| Linux (Ubuntu, Debian, Fedora, Arch, etc.) | x86_64 | Dynamic (glibc) |
| Linux (Raspberry Pi 4/5, ARM servers) | ARM64 (aarch64) | Dynamic (glibc) |
| Alpine Linux | x86_64 | **Static** (musl) |
| Alpine Linux | ARM64 | **Static** (musl) |
| Termux on Android | ARM64 | **Static** (musl) |
| Termux on Android | x86_64 | **Static** (musl) |
| macOS (Intel) | x86_64 | Dynamic (Darwin) |
| macOS (Apple Silicon M1/M2/M3/M4) | ARM64 | Dynamic (Darwin) |
| Windows 10/11 | x86_64 | **Static** (MSVCRT) |

See [Supported Platforms](README.md#supported-platforms) for details.

### Does Sino run on Termux (Android)?

Yes! Sino uses statically-linked musl binaries for Termux, which run natively on Android's Linux kernel — no `proot` or `proot-distro` needed. Just run:

```bash
curl -fsSL https://github.com/crossberry-in/sino-doc/raw/main/install.sh | bash
```

The installer will detect Termux and download `sino-alpine-arm64` (for ARM phones) or `sino-alpine-x86_64` (for x86 emulators).

### Does Sino run on Alpine Linux?

Yes. The installer detects Alpine's `musl` libc and downloads `sino-alpine-x86_64` or `sino-alpine-arm64`, both statically linked. No additional dependencies are needed.

### Does Sino run on Windows?

Yes, two ways:

1. **Natively** — Download `sino-windows-x86_64.exe` and run it from PowerShell/CMD. Or use the PowerShell installer:
   ```powershell
   irm https://github.com/crossberry-in/sino-doc/raw/main/install.ps1 | iex
   ```
2. **Via WSL** — Install WSL (Ubuntu) and run the Linux installer inside your WSL terminal.

### Does Sino run on macOS?

Yes. Both Intel Macs and Apple Silicon (M1/M2/M3/M4) are supported. The installer auto-detects your architecture and downloads `sino-macos-x86_64` (Intel) or `sino-macos-arm64` (Apple Silicon).

> **macOS Gatekeeper note:** The first time you run `sino`, you may see a security prompt. Right-click the binary in Finder → **Open** → confirm, or run `xattr -d com.apple.quarantine /path/to/sino`.

### How fast is Sino?

Sino is a tree-walking interpreter, so it is **not designed for high-performance computing**. It is suitable for:

- Learning programming concepts
- Prototyping algorithms
- Writing simple scripts and automation
- Embedding in larger applications as a scripting engine

For CPU-intensive tasks, consider using a compiled language like C, Rust, or Go.

### Does Sino support multithreading?

No, Sino is single-threaded. The `async` and `await` keywords exist in the lexer but are not yet implemented in the interpreter.

### Does Sino have a standard library?

Sino has a small set of **built-in functions** (echo, input, len, typeof, int, float, string, push, pop, join, sqrt, abs, floor, ceil). There is no separate standard library yet.

### Does Sino support modules or imports?

The `use` keyword is reserved for future module support, but it is not yet implemented.

### Does Sino support file I/O?

Not in the current release. File reading and writing may be added in a future version.

### Does Sino support networking?

No, Sino has no built-in networking capabilities.

### Does Sino support string interpolation?

The lexer has limited support for interpolated strings. Use `string()` and `+` to concatenate values into strings:

```sino
var name = "Sino"
var age = 1
echo "Name: " + name + ", Age: " + string(age)
```

---

## Installation

### How do I install Sino?

See the [Installation Guide](INSTALL.md). The fastest method is to download the binary from the [Releases page](https://github.com/crossberry-in/sino-doc/releases) and place it on your `PATH`.

### How do I check my Sino version?

```bash
sino --version
```

### How do I upgrade Sino?

Download the latest binary from the [Releases page](https://github.com/crossberry-in/sino-doc/releases) and overwrite the old binary. See [Upgrading](INSTALL.md#upgrading) for details.

### How do I uninstall Sino?

Simply delete the binary:

```bash
sudo rm /usr/local/bin/sino
```

See [Uninstalling](INSTALL.md#uninstalling) for details.

### Can I build Sino from source?

The source code is **closed-source**, so public builds are not supported. If you need a build for a platform not listed under [Supported Platforms](README.md#supported-platforms), please [open an issue](https://github.com/crossberry-in/sino-doc/issues).

---

## Usage

### How do I run a Sino script?

```bash
sino my_script.si
```

See [Running a Sino File](USAGE.md#running-a-sino-file) for details.

### How do I start the REPL?

```bash
sino
```

See [Using the REPL](USAGE.md#using-the-repl) for details.

### What file extension do Sino files use?

Sino source files use the **`.si`** extension. For example: `hello.si`, `fibonacci.si`.

### Can I pass command-line arguments to a Sino script?

Not in the current release. Command-line argument passing may be added in a future version.

### Can I use Sino as an embedded scripting language in my C/C++ application?

The source code is closed, so embedding is not publicly supported. If you are interested in embedding Sino, please [open an issue](https://github.com/crossberry-in/sino-doc/issues) to discuss licensing.

---

## Language

### What's the difference between `var` and `fix`?

- `var` declares a **mutable** variable (can be reassigned).
- `fix` declares an **immutable constant** (cannot be reassigned after initialization).

```sino
var x = 10
x = 20           # OK

fix PI = 3.14
# PI = 3.0       # ERROR
```

### What's the difference between `func` and `fn`?

Both define functions. `func` is used for **named functions** at the statement level, while `fn` is used for **anonymous functions** as expressions.

```sino
# Named function
func add(a, b):
    return a + b
end

# Anonymous function assigned to a variable
var square = fn(x): return x * x end
```

### Does Sino support inheritance?

No, the current version of Sino does not support class inheritance. Classes can only have their own methods and instance variables via `self`.

### Does Sino support exceptions?

No, Sino uses runtime errors that halt execution. There is no `try/catch` mechanism.

### Does Sino support garbage collection?

Sino uses manual memory management internally. From the user's perspective, memory is managed automatically — you don't need to free objects manually.

---

## Troubleshooting

### I get `command not found: sino`

The binary is not on your `PATH`. See [Troubleshooting](INSTALL.md#troubleshooting) in the Installation Guide.

### I get `cannot execute binary file: Exec format error`

You downloaded a binary for the wrong architecture. Check your architecture with `uname -m` and download the correct binary.

### I get `Permission denied`

The binary is not marked executable. Run:

```bash
chmod +x /path/to/sino
```

### My Sino script produces a parse error

Check the line and column number in the error message. Common causes:

- Missing `:` after `if`, `while`, `for`, `func`, `class`, `match`, `case`
- Missing `end` at the end of a block
- Unbalanced parentheses, brackets, or quotes
- Invalid syntax

See [Common Errors](USAGE.md#common-errors) for more.

### Where can I report bugs?

Please [open an issue](https://github.com/crossberry-in/sino-doc/issues) with:

1. Your Sino version (`sino --version`)
2. Your OS and architecture
3. The smallest Sino script that reproduces the bug
4. The exact error message or unexpected behavior

---

## Still Have Questions?

- 💬 **Ask in [GitHub Discussions](https://github.com/crossberry-in/sino-doc/discussions)**
- 🐛 **Report bugs via [Issues](https://github.com/crossberry-in/sino-doc/issues)**
- 📖 **Read the [Language Reference](LANGUAGE_REFERENCE.md)**
