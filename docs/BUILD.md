# Native Build Guide

Mozhi can produce a standalone native executable from a supported `.mz` program. The native build uses the Rust compiler's C-generation path, then invokes a C compiler to produce a machine-code executable.

This is a separate output mode from the normal interpreter and the `mozhi-fast` bytecode VM.

## Requirements

- A working Mozhi installation that includes the native build command.
- The Mozhi native compiler included with the build-capable distribution.
- A C compiler available on `PATH` for the final compilation step.

The exact compiler/toolchain requirements can vary by platform and release.

## Configure a project

Add a `[build]` section to your project's `mozhi.toml`:

```toml
[build]
mode = "native"                 # "native" or "interpreter"
output = "dist/release/myapp"
release = true                  # false selects a debug build
```

| Setting | Meaning |
|---|---|
| `mode` | Selects native executable generation or interpreter mode. |
| `output` | Destination path for the generated executable. |
| `release` | Enables release build settings when `true`; `false` selects a debug build. |

## Build an executable

From the project directory:

```bash
mz build
```

Run the generated program directly:

```bash
./dist/release/myapp
```

The resulting executable is machine code and does not need the original `.mz` source file at runtime for the compiled program itself.

## Run a project

Use the project run command for the configured execution mode:

```bash
mz run
```

When `mode = "native"` is selected, the project uses its native build/run workflow. Use `mz build` when you specifically want to create the executable as a build artifact.

## Native package builds

Build or publish a package with native output explicitly enabled:

```bash
mz pkg build . --native
mz pkg publish . --native
```

A package can declare its generated executable in package metadata:

```toml
binary = "dist/release/myapp"
```

The package may still include and expose its Mozhi source modules. Source modules remain imported as `.mz` modules. A generated executable is a standalone program artifact; it is **not** automatically an importable Mozhi module. Importing compiled binaries as modules would require a separate binary module format and loader.

## Current native compiler support

The current native code-generation path supports a deliberately limited subset of the language, including:

- Numeric functions and arithmetic.
- Recursion.
- Loops.
- Literal printing.

Unsupported constructs, including imports and dynamic language features, are rejected rather than silently omitted. If a program uses unsupported features, use the interpreter or bytecode VM instead, or simplify the program to the supported native subset.

This feature is evolving. Do not assume that every valid Mozhi program can be compiled natively.

## Build, install, and security behavior

Native compilation is an explicit author/developer build step. Installing a downloaded package does not automatically compile or execute its build tools or source code. Review package contents and provenance as you would for any executable distribution.

## Performance

Native output can reduce runtime overhead for supported compute-heavy programs, but total performance depends on the program, compiler settings, platform, and C compiler. No fixed execution-time guarantee (including a 0.002 ms target) is implied.

## Troubleshooting

### C compiler not found

Install a supported C compiler for your platform and ensure its executable is available on `PATH`, then retry `mz build`.

### Program uses unsupported features

The native compiler reports unsupported imports or dynamic constructs. Run the program with the interpreter/bytecode VM, or refactor it to use the currently supported native subset.

### Executable path does not exist

Check the `output` value in `mozhi.toml` and confirm that the build completed successfully. Run the executable from the configured output path.

## Related documentation

- [Installation Guide](../INSTALL.md)
- [Usage Guide](../USAGE.md)
- [Package Guide](packages.md)
- [mozhi-fast bytecode VM](mozhi-fast.md)
