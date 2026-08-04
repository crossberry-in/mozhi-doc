# Packages — import & `mz add`

mozhi-fast supports importing libraries and installing them with a small
package manager. Packages are fetched from the **mozhi-doc package registry**
(or from git / local files).

## Import

```mozhi
import json from "json"            # package by name (auto-installs if missing)
import charts from "charts"        # same
import mylib from "/path/mylib.mz" # explicit file path
import "utils"                     # no alias (basename becomes the alias)
```

The module's functions are accessed via the alias namespace:

```mozhi
import math_utils from "math_utils"
echo(math_utils.factorial(10))     # 3628800
```

### Resolution order

1. Explicit file path (`/path/to/file.mz`)
2. Project-local installs: `./.mozhi/libs/<pkg>/...`
3. Global installs: `$HOME/.mozhi/libs/<pkg>/...`
4. Package layout: `<pkg>/src/mod.mz`
5. `$MZ_LIB` override
6. **Auto-install** from the mozhi-doc registry, then re-resolve

## `mz add` — package manager

Install libraries manually:

```bash
# from git
mz add @user/repo
mz add @user/repo:subpath

# from a local file
mz add /path/to/library.mz

# from the mozhi-doc registry (e.g. charts, json, math_utils, mznn, ...)
mz add charts
mz add json
```

`mozhi-fast add <spec>` is the same command.

### Auto-install on import

If a package isn't found locally, `import` will automatically fetch it from the
mozhi-doc registry and install it, then load it. No manual step needed.

## Example

```bash
# install the charts library
mozhi-fast add charts

# use it
cat > plot.mz <<'EOF'
import charts from "charts"
svg = charts.bar(["mini", "fast"], [7066.8, 4269.4])
write_file("/tmp/plot.svg", svg)
echo(svg)
EOF
mozhi-fast plot.mz
```

## Environment spaces (ens)

Like a Python virtualenv, you can create an isolated environment where
`import` and `mz add` work from any folder.

```bash
# create an environment (activates it in this shell)
source mz-ens.sh create myenv
# or programmatically:
mozhi-fast ens-create myenv

# from any folder, activate then install/import
source mz-ens.sh activate myenv
mozhi-fast add charts        # installs into the env's libs
mozhi-fast file.mz           # import charts resolves from the env

# manage
source mz-ens.sh deactivate
mozhi-fast ens-list
```

Environments live in `$HOME/.mozhi/ens/<name>/`. Activating sets `MZ_ENV` and
`MZ_LIB` to the environment's `libs/` dir; `mz add` installs there and
`import` resolves from there (before project/global libs).

## Notes & limitations

- **Self-recursion** and **mutual recursion** between module functions both work
  (e.g. `fib`, and `is_even`/`is_odd` calling each other).
- The registry packages live in the `mozhi-doc` repo under
  `mozhi-pkg/pkg/<name>/` with `package.toml` metadata; `mz-registry.json`
  provides the install paths.
- To add a new package to the registry, see `mozhi-pkg` (mozhi-doc repo).
