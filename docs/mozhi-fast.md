# mozhi-fast — Rust bytecode VM

`mozhi-fast` is a **faster implementation** of the Mozhi interpreter, written in
**Rust**. It compiles Mozhi source to **bytecode** and executes it on a
stack-based virtual machine, instead of walking the AST like the reference C
interpreter.

## Why mozhi-fast?

| | C interpreter (reference) | mozhi-fast (Rust VM) |
|---|---|---|
| Execution model | tree-walking (AST) | **bytecode VM** |
| Safety | manual memory | **memory-safe Rust** |
| Integers | 32-bit (can overflow) | **64-bit (correct)** |
| Speed | fast | **~1.3–1.6× faster** |
| File | `interpreter/` (C) | `mozhi-fast/` (Rust) |

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
./target/release/mozhi-fast path/to/file.mz
```

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

On `fib(30)` and tight `while` loops, mozhi-fast is faster than the C
interpreter and produces correct 64-bit results where the C interpreter's
32-bit integers overflow.

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
  current C interpreter behavior.
