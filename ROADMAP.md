# Sino Programming Language — Development Roadmap

**Version:** 2.0 | **Last Updated:** 2026-08-01

This document defines the complete development roadmap for the Sino programming language, organized into 12 phases plus long-term goals. Each phase is prioritized by dependency order — earlier phases provide foundations for later ones.

---

## Phase 1 — Language Core

**Status:** In Progress | **Priority:** Critical | **Target:** v2.1

The language core defines the fundamental building blocks that all other features depend on.

| Feature | Status | Description |
|---------|--------|-------------|
| Generic Functions | Planned | Functions parameterized by type: `fn identity<T>(x: T) -> T` |
| Generic Types | Planned | Structs/enums with type parameters: `struct Vec<T> { ... }` |
| Trait / Interface System | Planned | Full trait dispatch, default methods, trait objects |
| Struct Methods | Planned | `impl` blocks with `self` receiver for structs |
| Enum Methods | Planned | `impl` blocks for enums with match-based dispatch |
| Extension Methods | Planned | Add methods to existing types via `impl Type { ... }` |
| Named Arguments | Planned | `fn f(name: string, age: int = 0)` called as `f(name: "Alice")` |
| Default Arguments | Planned | Parameters with default values: `fn f(x, y = 10)` |
| Function Overloading | Planned | Multiple functions with same name, different signatures |
| Operator Overloading | Planned | `impl Add for Vec { fn add(self, other) { ... } }` |
| Lambda Functions | ✅ Done | Anonymous functions: `fn(x) { return x * 2 }` |
| Closures | ✅ Done | Functions capturing enclosing scope variables |
| Iterator System | Planned | `Iterator` trait, `map()`, `filter()`, `collect()`, lazy evaluation |
| Range Type | Planned | `1..10`, `1..=10`, `0..` for infinite ranges |
| Pattern Matching Enhancement | Planned | Guards, destructuring, or-patterns, bindings |
| Destructuring | Planned | `let (x, y) = point` and `let Point { x, y } = p` |
| Tuple Type | Planned | `(int, string, bool)` heterogeneous fixed-size collections |

---

## Phase 2 — Collections

**Status:** Not Started | **Priority:** High | **Target:** v2.2

A complete collections library is essential for productive programming.

| Feature | Status | Description |
|---------|--------|-------------|
| Vector | Planned | Contiguous growable array with capacity management |
| Hash Map | Planned | Key-value store with O(1) average lookup |
| Hash Set | Planned | Unique element collection with O(1) membership |
| Linked List | Planned | Doubly-linked list for O(1) insert/remove |
| Queue | Planned | FIFO queue |
| Stack | Planned | LIFO stack |
| Deque | Planned | Double-ended queue |
| Priority Queue | Planned | Heap-based priority queue |
| Ordered Map | Planned | Map preserving insertion order |
| Ordered Set | Planned | Set preserving insertion order |
| Ring Buffer | Planned | Fixed-size circular buffer |
| Bit Set | Planned | Compact bit-level storage |

---

## Phase 3 — Standard Library

**Status:** Partial | **Priority:** High | **Target:** v2.3

| Module | Status | Description |
|--------|--------|-------------|
| std.fs | Planned | File system operations (exists, mkdir, rmdir, list, copy, rename) |
| std.path | Planned | Cross-platform path manipulation |
| std.process | Planned | Process spawning, pipe, exit, environment variables |
| std.env | Planned | Environment variable access |
| std.time | Planned | Timestamps, durations, sleep, timers |
| std.date | Planned | Date parsing, formatting, arithmetic, timezones |
| std.random | Planned | Random number generation (thread-safe, seedable) |
| std.uuid | Planned | UUID v4/v5 generation and parsing |
| std.base64 | Planned | Base64 encode/decode |
| std.hex | Planned | Hex encode/decode |
| std.json | Planned | JSON parse, stringify, streaming |
| std.xml | Planned | XML parse, serialize, XPath |
| std.csv | Planned | CSV read/write with configurable delimiters |
| std.toml | Planned | TOML parse/serialize |
| std.yaml | Planned | YAML parse/serialize |
| std.compress | Planned | gzip, zlib, deflate, bzip2 |
| std.archive | Planned | tar, zip, extraction |
| std.crypto | Planned | AES, RSA, HMAC, SHA family, random bytes |
| std.hash | Planned | MD5, SHA-1, SHA-256, SHA-512, BLAKE3 |

---

## Phase 4 — Networking

**Status:** Not Started | **Priority:** Medium | **Target:** v2.4

| Feature | Status | Description |
|---------|--------|-------------|
| HTTP Client | Planned | GET, POST, PUT, DELETE, streaming, TLS |
| HTTP Server | Planned | Request routing, middleware, static files |
| TCP | Planned | TCP socket client and server |
| UDP | Planned | UDP socket support |
| WebSocket | Planned | Client and server, ping/pong, frames |
| DNS | Planned | DNS resolution, custom resolvers |
| TLS | Planned | TLS/SSL for secure connections |
| URL Parser | Planned | URL parsing, building, encoding |
| MIME Parser | Planned | MIME type detection, multipart parsing |

---

## Phase 5 — Concurrency

**Status:** Not Started | **Priority:** Medium | **Target:** v2.5

| Feature | Status | Description |
|---------|--------|-------------|
| Threads | Planned | OS-level threads with join/detach |
| Async | Planned | `async fn` returning `Future<T>` |
| Await | Planned | `await` expression for async functions |
| Task Scheduler | Planned | Cooperative async runtime, work stealing |
| Channels | Planned | MPSC, SPSC, broadcast channels |
| Mutex | Planned | Mutual exclusion lock |
| RWLock | Planned | Read-write lock for concurrent read access |
| Atomic Types | Planned | AtomicInt, AtomicBool, AtomicPtr |
| Thread Pool | Planned | Fixed-size worker pool with task queue |

---

## Phase 6 — Package Manager

**Status:** Partial | **Priority:** High | **Target:** v2.2

| Feature | Status | Description |
|---------|--------|-------------|
| `sino install` | ✅ Done | Install dependencies from sino.toml |
| `sino update` | ✅ Done | Update dependencies |
| `sino remove` | ✅ Done | Remove dependencies |
| `sino search` | ✅ Done | Search packages |
| `sino publish` | Partial | Stub — needs public registry |
| Dependency Lock File | ✅ Done | sino.lock with resolved versions |
| Version Resolution | ✅ Done | Semantic versioning with ^, ~, >=, <, * |
| Offline Cache | ✅ Done | ~/.sino/cache/ for offline builds |
| Mirrors | Planned | Mirror servers for faster downloads |
| Private Registry | Planned | Self-hosted registry for private packages |

---

## Phase 7 — Compiler

**Status:** Partial | **Priority:** Critical | **Target:** v3.0

| Feature | Status | Description |
|---------|--------|-------------|
| Lexer | ✅ Done | Full tokenizer with all token types |
| Parser | ✅ Done | Recursive descent + Pratt expression parser |
| AST Generation | ✅ Done | Complete AST for all language constructs |
| Semantic Analysis | ✅ Done | Scope resolution, function validation |
| Type Checking | ✅ Done | Static type checking with inference |
| Incremental Compilation | Planned | Only recompile changed modules |
| Bytecode Generation | Planned | Compile AST to .sibc bytecode format |
| Dead Code Elimination | Planned | Remove unreachable code |
| Constant Folding | Planned | Evaluate constants at compile time |
| Inline Expansion | Planned | Inline small functions automatically |
| Escape Analysis | Planned | Determine stack vs heap allocation |
| Register Allocation | Planned | Efficient register usage in codegen |
| Link Time Optimization | Planned | Cross-module optimization at link time |

---

## Phase 8 — Runtime

**Status:** Partial | **Priority:** Critical | **Target:** v3.0

| Feature | Status | Description |
|---------|--------|-------------|
| Tree-walking Interpreter | ✅ Done | Current execution model (v2.0) |
| Bytecode VM | Planned | Stack-based VM executing .sibc bytecode |
| Garbage Collector | Planned | Mark-sweep GC with generational optimization |
| JIT Compiler | Planned | Just-in-time compilation for hot paths |
| Native Code Generator | Planned | LLVM backend for native executables |
| Dynamic Loader | Planned | Load .silib packages at runtime |
| Plugin System | Planned | Dynamically loadable modules with stable ABI |

---

## Phase 9 — Developer Experience

**Status:** Not Started | **Priority:** Medium | **Target:** v3.0

| Feature | Status | Description |
|---------|--------|-------------|
| LSP Server | Planned | Language Server Protocol implementation |
| Auto Completion | Planned | Context-aware code completion |
| Hover Help | Planned | Show type and documentation on hover |
| Go to Definition | Planned | Jump to symbol definition |
| Rename Symbol | Planned | Project-wide symbol renaming |
| Formatter (`sino fmt`) | ✅ Done | Basic code formatting (indentation, whitespace) |
| Linter (`sino lint`) | ✅ Done | Basic linting (unused variables) |
| Debugger | Planned | Source-level debugger with breakpoints |
| Profiler | Planned | CPU and memory profiler with flame graphs |
| Coverage Tool | Planned | Code coverage reporting |
| Documentation Generator | ✅ Done | `sino doc` generates API documentation |

---

## Phase 10 — Testing

**Status:** Partial | **Priority:** High | **Target:** v2.3

| Feature | Status | Description |
|---------|--------|-------------|
| Unit Testing | ✅ Done | `sino test` runs test files in tests/ |
| Integration Testing | Planned | Multi-module integration tests |
| Benchmark Framework | ✅ Done | Full benchmark framework with 26 tests, statistics, history |
| Mock Library | Planned | Mock functions and types for testing |
| Snapshot Testing | Planned | Golden file comparison |
| Property Testing | Planned | Random input generation for property verification |
| Fuzz Testing | Planned | Automated fuzzing for crash discovery |

---

## Phase 11 — Cross Platform

**Status:** Partial | **Priority:** High | **Target:** v2.2

| Platform | Architecture | Status | Notes |
|----------|-------------|--------|-------|
| Linux | x86_64 | ✅ Done | Primary development platform |
| Linux | ARM64 (aarch64) | ✅ Done | Raspberry Pi, ARM servers |
| Alpine Linux | x86_64 | ✅ Done | Static musl build |
| Alpine Linux | ARM64 | ✅ Done | Static musl build |
| Termux (Android) | ARM64 | ✅ Done | Via static musl build |
| macOS | Intel (x86_64) | ✅ Done | Mach-O binary |
| macOS | Apple Silicon (ARM64) | ✅ Done | Mach-O binary |
| Windows | x86_64 | ✅ Done | PE32+ executable |
| WebAssembly | wasm32 | Planned | Compile to WASM for browser execution |

---

## Phase 12 — Security

**Status:** Not Started | **Priority:** Low | **Target:** v3.0+

| Feature | Status | Description |
|---------|--------|-------------|
| Sandboxed Execution | Planned | Restrict file/network/process access |
| Capability Permissions | Planned | Explicit permission grants for operations |
| Memory Leak Detection | Planned | Runtime leak detection with allocation tracking |
| Race Detection | Planned | Thread sanitizer for data race detection |
| Static Analyzer | Planned | Compile-time security analysis (taint, overflow) |
| Secure Package Verification | Planned | Package signing and verification |
| Package Signature Validation | Planned | GPG/minisign signature checking |

---

## Long-Term Goals

These are ambitious goals that extend beyond the 12-phase roadmap.

| Goal | Description |
|------|-------------|
| **Self-hosting Compiler** | Rewrite the Sino compiler in Sino itself |
| **Native IDE** | Full-featured IDE built specifically for Sino development |
| **Official GUI Toolkit** | Cross-platform GUI library (desktop + mobile) |
| **Database Driver Framework** | Unified interface for SQL/NoSQL databases |
| **Embedded Runtime** | Lightweight runtime for embedded systems (RTOS, microcontrollers) |
| **Plugin Ecosystem** | VS Code extension, IntelliJ plugin, Vim plugin |
| **Official Package Registry** | Hosted package registry at registry.sino-lang.org |
| **Continuous Benchmark Dashboard** | Automated benchmark CI with web dashboard |
| **Language Server Ecosystem** | LSP for all major editors |
| **Stable ABI** | Binary compatibility for compiled libraries across versions |

---

## Version Timeline

| Version | Target Date | Focus |
|---------|------------|-------|
| **v2.0** | ✅ Released | New syntax (braces, fn, const, match), C++/ASM/Rust backend |
| **v2.1** | Q3 2026 | Language core: generics, traits, iterators, tuples, destructuring |
| **v2.2** | Q4 2026 | Collections library + package manager improvements |
| **v2.3** | Q1 2027 | Standard library + testing framework |
| **v2.4** | Q2 2027 | Networking library |
| **v2.5** | Q3 2027 | Concurrency (threads, async/await, channels) |
| **v3.0** | Q4 2027 | Compiler: bytecode VM + JIT + native codegen |
| **v3.1** | Q1 2028 | Developer experience: LSP, debugger, profiler |
| **v4.0** | Q4 2028 | Self-hosting compiler |

---

## Current Progress Summary

| Phase | Features Total | Done | In Progress | Planned | Completion |
|-------|---------------|------|-------------|---------|------------|
| 1. Language Core | 17 | 2 | 0 | 15 | 12% |
| 2. Collections | 12 | 1 | 0 | 11 | 8% |
| 3. Standard Library | 19 | 0 | 0 | 19 | 0% |
| 4. Networking | 9 | 0 | 0 | 9 | 0% |
| 5. Concurrency | 9 | 0 | 0 | 9 | 0% |
| 6. Package Manager | 10 | 7 | 1 | 2 | 70% |
| 7. Compiler | 13 | 5 | 0 | 8 | 38% |
| 8. Runtime | 7 | 1 | 0 | 6 | 14% |
| 9. Developer Experience | 11 | 3 | 0 | 8 | 27% |
| 10. Testing | 7 | 2 | 0 | 5 | 29% |
| 11. Cross Platform | 9 | 8 | 0 | 1 | 89% |
| 12. Security | 7 | 0 | 0 | 7 | 0% |
| **Total** | **130** | **29** | **1** | **100** | **22%** |

---

*This roadmap is a living document. Features may be reprioritized based on community feedback and implementation discoveries.*
