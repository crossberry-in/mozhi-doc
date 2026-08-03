# mozhi-fast — Rust bytecode VM

`mozhi-fast` is a **faster implementation** of the Mozhi interpreter, written in
**Rust**. It compiles Mozhi source to **bytecode** and executes it on a
stack-based virtual machine, instead of walking the AST like the reference
`mozhi-mini` interpreter.

## Why mozhi-fast?

| | mozhi-mini | mozhi-fast |
|---|---|---|
| Execution model | tree-walking (AST) | **bytecode VM** |
| Safety | manual memory | **memory-safe Rust** |
| Integers | 32-bit (can overflow) | **64-bit (correct)** |
| Speed | fast | **~1.3–1.6× faster** |
| File | `interpreter/` | `mozhi-fast/` (Rust) |

## Build

Requires [Rust](https://rustup.rs) (1.75+):

```bash
git clone https://github.com/crossberry-in/mozhi
cd mozhi/mozhi-fast
cargo build --release
# binary: target/release/mozhi-fast
```

## Run

```bash
./target/release/mozhi-fast path/to/file.mz        # bytecode VM
./target/release/mozhi-fast --native file.mz       # native codegen (JIT)
```

## Native code generation (JIT)

`mozhi-fast --native` compiles Mozhi to C and runs it with gcc `-O2`, giving
near-native speed for compute-heavy programs:

| Benchmark | bytecode VM | native (`--native`) | speedup |
|-----------|-------------|---------------------|---------|
| `fib(30)` | 1562 ms | ~80 ms (incl. gcc) | **~20×** |
| loop 10M  | 4269 ms | ~80 ms (incl. gcc) | **~50×** |

> Execution is microseconds; the ~80 ms is gcc compilation overhead. Native
> codegen supports scalar programs, functions, recursion, arithmetic, loops,
> `if`, string `echo`, and basic arrays. Complex features (functions returning
> arrays, `push`, string params) are not yet supported — use the bytecode VM.

## Supported language features

- Variables & assignment, including `a[i] = v`, `m[i][j] = v`, compound `a[i] += v`
- Functions, recursion, closures
- Arrays (reference semantics), maps, `for-in` loops
- Control flow: `if`/`else`, `while`, c-style `for`, `match`
- String/array methods: `len`, `upper`, `split`, `join`, `push`, ...
- Math builtins: `exp`, `log`, `pow`, `sqrt`, `min`, `max`, `round`, `clamp`, ...
- Multi-line and trailing-comma array literals

## Architecture

```
src/token.rs      token types
src/lexer.rs      source → tokens
src/ast.rs        abstract syntax tree
src/parser.rs     Pratt parser (tokens → AST)
src/opcode.rs     bytecode opcodes + constant pool
src/compiler.rs   AST → bytecode chunks (one per function)
src/value.rs      runtime values
src/vm.rs         stack-based bytecode VM
src/builtins.rs   built-in functions
src/main.rs       entry point
```

## Benchmark

Measured on x86_64 Linux with the release builds (median of 3 runs):

| Benchmark | mozhi-mini | mozhi-fast VM | mozhi-fast native (`--native`) |
|-----------|------------|---------------|-------------------------------|
| `fib(30)` | 2252 ms | 1654 ms | **85.6 ms** |
| 1M `while` loop | 685 ms | 381 ms | **50.8 ms** |

Relative speedup vs mozhi-mini:

| Benchmark | mozhi-fast VM | mozhi-fast native |
|-----------|---------------|-------------------|
| `fib(30)` | ~1.4× | **~26×** |
| 1M loop | ~1.8× | **~13×** |

mozhi-fast is faster than the mozhi-mini tree-walking interpreter on both
recursion and tight loops. The **bytecode VM** gives ~1.4–1.8× speedup (with
correct 64-bit results where mozhi-mini's 32-bit integers overflow), and the
**native codegen (`--native`)** gives ~13–26× speedup — approaching native
speed. (VM optimizations: `Rc`-shared environments so calls are cheap, and
`#[inline]` hot-path helpers.)

Reproduce:

```bash
# fib(30)
printf 'fn fib(n) { if n <= 1 { return n } return fib(n-1)+fib(n-2) }\necho(fib(30))\n' > fib.mz
time ./mozhi-fast fib.mz          # 832040 (bytecode VM)
time ./mozhi-fast --native fib.mz # 832040 (native, ~26x faster)

# 1M loop
printf 'i=0\ns=0\nwhile i<1000000 { s=s+i; i=i+1 }\necho(s)\n' > loop.mz
time ./mozhi-fast loop.mz          # 499999500000 (correct, bytecode VM)
time ./mozhi-fast --native loop.mz # 499999500000 (native)
```

## Examples

```mozhi
# recursion
fn fib(n) {
    if n <= 1 { return n }
    return fib(n - 1) + fib(n - 2)
}
echo("fib(10) = " + string(fib(10)))   # 55

# arrays + matrix
M = [[1.0, 2.0], [3.0, 4.0]]
M[0][1] = 9.0
echo(M[0][1])                          # 9
```

## Notes / limitations

- `match` arms using `=> return X` (as in the `enums` example) are not yet
  supported; value arms (`0 => "a"`) work.
- `enum`/`struct` declarations are skipped (parsed as no-ops), matching the
  current mozhi-mini behavior.
