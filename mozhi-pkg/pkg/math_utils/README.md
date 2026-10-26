# math_utils

Extended math helpers for Mozhi: arithmetic, geometry, statistics, number theory.

## Install

```bash
pkg install math_utils
```

## Usage

```mozhi
import mod from "math_utils"

echo(mod.factorial(10))    # 3628800
echo(mod.fibonacci(20))    # 6765
echo(mod.is_prime(97))     # true
echo(mod.sqrt(144))        # 12
echo(mod.gcd(48, 36))      # 12
```

## API

| Function | Description |
|----------|-------------|
| `PI`, `E` | Mathematical constants |
| `abs(n)` | Absolute value |
| `sqrt(n)` | Square root (Newton-Raphson) |
| `factorial(n)` | n! |
| `gcd(a, b)` | Greatest Common Divisor |
| `lcm(a, b)` | Least Common Multiple |
| `is_prime(n)` | Primality test |
| `fibonacci(n)` | Nth Fibonacci number |
| `square(n)`, `cube(n)` | Powers |
| `pow_int(base, exp)` | Integer power |
| `clamp(n, lo, hi)` | Clamp to range |
| `lerp(a, b, t)` | Linear interpolation |
| `radians(deg)`, `degrees(rad)` | Angle conversion |
| `max_val(a, b)`, `min_val(a, b)` | Comparison |
| `sum_list(arr)`, `mean_list(arr)` | Statistics |

## License

MIT
