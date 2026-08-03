# Mozhi v2.5.0 — Array, Matrix & Math Upgrades

This document describes the syntax and library upgrades shipped with the
rebuilt Mozhi C interpreter (v2.5.0). These changes make Mozhi practical for
data and neural-network programming.

All examples run with the bundled interpreter:

```bash
./mozhi-linux-x86_64 examples/arrays-and-matrices/app.mz
```

---

## 1. Array element assignment

You can now mutate arrays (and nested matrices) in place:

```mozhi
a = [1.0, 2.0, 3.0]
a[1] = 9.0            # a is now [1.0, 9.0, 3.0]

M = [
    [0.0, 0.0,],
    [0.0, 0.0,],
]
M[1][1] = 7.0         # nested element assignment
```

Previously this raised `Invalid assignment target`.

## 2. Compound element assignment

```mozhi
w = [1.0, 2.0, 3.0]
w[1] += 10.0          # w is now [1.0, 12.0, 3.0]
w[0] *= 2.0
```

## 3. Trailing commas & multi-line literals

Array and matrix literals may span multiple lines and end with a trailing comma:

```mozhi
data = [
    1.0,
    2.0,
    3.0,
]

weights = [
    [0.5, -0.2,],
    [0.1,  0.9,],
]
```

## 4. Functions can return arrays & matrices

A function may build an array with `push` and return it safely (a
use-after-free that crashed earlier versions is fixed):

```mozhi
fn ones(n) {
    out = []
    i = 0
    while i < n {
        push(out, 1.0)
        i = i + 1
    }
    return out
}

v = ones(3)      # v = [1.0, 1.0, 1.0]
```

## 5. Correct function-local scoping

A variable assigned inside a function is local to that function; it no longer
overwrites a same-named variable in the caller:

```mozhi
i = 100
fn set() { i = 5 }
set()
echo(i)            # 100  (the function did NOT change the caller's i)
```

`if`/`while`/`for` blocks still update the enclosing scope, as documented.

## 6. New math builtins

| Function | Signature | Description |
|----------|-----------|-------------|
| `min` | `min(a, b) -> number` | Smaller of two numbers |
| `max` | `max(a, b) -> number` | Larger of two numbers |
| `round` | `round(x) -> int` | Round to nearest integer |
| `clamp` | `clamp(x, lo, hi) -> number` | Bound x to `[lo, hi]` |

These join the existing `exp`, `log`/`ln`, `log10`, `pow`, `sqrt`, `abs`,
`floor`, `ceil`, `sin`, `cos`, `tan` builtins.

## 7. Standard library (`std/math`)

`std/math` now provides neural-network helpers built on the native builtins:

```mozhi
import math from "mozhi-math"

math.sigmoid(0.0)     # 0.5
math.tanh(1.0)        # 0.761594
math.relu(-3.0)       # 0.0
math.lerp(0.0, 10.0, 0.5)   # 5.0
math.clamp_value(5.0, 1.0, 3.0)  # 3.0
```

---

## Example

`examples/arrays-and-matrices/app.mz` exercises every feature above, including a
matrix multiply and a tiny neural-network forward pass, all in pure Mozhi.
