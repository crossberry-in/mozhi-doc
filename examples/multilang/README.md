# Multi-Language Helper Files

These files are used by the `run_c()`, `run_cpp()`, `run_py()`, `run_sh()`, and `run_mz()` builtins in Mozhi v2.4.0+.

## Files

| File | Language | Run Builtin | Description |
|------|----------|-------------|-------------|
| `helper.c` | C | `run_c("helper.c")` | C demo with math and time |
| `helper.cpp` | C++ | `run_cpp("helper.cpp")` | C++ demo with vectors and lambdas |
| `helper.py` | Python | `run_py("helper.py")` | Python demo with JSON |
| `helper.sh` | Shell | `run_sh("helper.sh")` | Shell demo with system info |
| `helper.mz` | Mozhi | `run_mz("helper.mz")` | Mozhi demo with math and strings |

## Usage

```mozhi
# Run each language file
echo(run_c("multilang/helper.c"))
echo(run_cpp("multilang/helper.cpp"))
echo(run_py("multilang/helper.py"))
echo(run_sh("multilang/helper.sh"))
echo(run_mz("multilang/helper.mz"))
```

## Requirements

- **C**: `gcc` must be installed
- **C++**: `g++` must be installed
- **Python**: `python3` or `python` must be installed
- **Shell**: `bash` must be installed
- **Mozhi**: `mozhi-interpreter` must be in PATH

## See Also

- [`../multilang.mz`](../multilang.mz) — Example that runs all these files
- [`../web_app.mz`](../web_app.mz) — Web server that exposes these via HTTP
