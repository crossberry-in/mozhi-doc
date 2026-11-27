# Packages — import & `mz install`

Mozhi supports importing source libraries and installing packages with `mz install`.
Packages can come from the existing registry, NxMirror, GitHub release packages,
or local archives and source directories.

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

## `mz install` — package manager

Install a package by name. Mozhi checks the existing registry first and can fall back to NxMirror when the package is absent:

```bash
mz install <name>                  # Existing registry, then NxMirror if absent
mz install nx:<name>               # Explicitly select NxMirror
mz install nx:<name>@1.2.0 --local  # Pin an exact NxMirror version
mz install @owner/repo             # GitHub release package
mz install ./tool.mz.pkg.zip       # Local package archive
mz install ./package-directory    # Local source package
```

List installed packages and remove one:

```bash
mz list
mz uninstall <name>
```

The `--local` option selects the local installation scope for the explicit NxMirror version in the example above. Package source archives and package directories are installed as package content; installation does not automatically execute a package binary.

### Auto-install on import

If a package isn't found locally, `import` can automatically fetch it from the
configured registry flow and install it, then load it. Explicit `mz install`
remains available when you want to choose a source such as NxMirror, GitHub, or
a local package archive.

## Example

```bash
# install the charts library
mz install charts

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
`import` and `mz install` work from any folder.

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
`MZ_LIB` to the environment's `libs/` dir; `mz install` installs there and
`import` resolves from there (before project/global libs).

## Native package artifacts

A package can optionally ship a standalone executable produced by the native
build workflow. Build or publish with native output enabled:

```bash
mz pkg build . --native
mz pkg publish . --native
```

Declare the executable path in the package metadata:

```toml
binary = "dist/release/myapp"
```

The package can still include its Mozhi source modules. Consumers import
those modules from their `.mz` source files using the normal package import
mechanism. The generated executable is a standalone program artifact; it
cannot currently be imported as a Mozhi module. Binary-module imports require
a separate module format and loader.

For project-level native build configuration, compiler support, and
troubleshooting, see the [Native Build Guide](BUILD.md).

## Notes & limitations

- **Self-recursion** and **mutual recursion** between module functions both work
  (e.g. `fib`, and `is_even`/`is_odd` calling each other).
- The registry packages live in the `mozhi-doc` repo under
  `mozhi-pkg/pkg/<name>/` with `package.toml` metadata; `mz-registry.json`
  provides the install paths.
- To add a new package to the registry, see `mozhi-pkg` (mozhi-doc repo).
