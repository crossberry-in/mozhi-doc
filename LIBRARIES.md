# Mozhi Libraries

A library package system for the Mozhi programming language. Install, import, and use community libraries in your `.mz` programs.

## Quick Start

```bash
# Install the mozhi CLI (interpreter + TUI)
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash

# Install a library
mozhi add mozhi-http
mozhi add mozhi-html

# Write a program that imports them
cat > server.mz << 'EOF'
import http from "mozhi-http"
import html from "mozhi-html"

fn handler(method, path) {
    body = html.html_page("Hello from Mozhi", html.html_h1("It works!"))
    return http.http_ok_html(body)
}

server = http.http_start(8080)
echo("Server running on http://localhost:8080")
http.http_serve_loop(server, handler)
EOF

# Run it
mozhi run server.mz
```

## Import Syntax

The **first non-comment, non-blank line** of a `.mz` file may declare imports:

```mozhi
import http from "mozhi-http"
import html from "mozhi-html"
import json from "mozhi-json"
import math_utils from "mozhi-math-utils"
import strings from "mozhi-strings"
```

After the import lines, all functions from the imported library are available as `library_name.function_name(...)`:

```mozhi
import strings from "mozhi-strings"

echo(strings.reverse("hello"))        # olleh
echo(strings.capitalize("mozhi"))     # Mozhi
echo(strings.snake_case("camelCase")) # camel_case
```

## Available Libraries

| Package | Import as | Description | Functions |
|---------|-----------|-------------|-----------|
| `mozhi-html` | `html` | HTML element generation | 38 |
| `mozhi-http` | `http` | HTTP server utilities | 15 |
| `mozhi-json` | `json` | JSON encoder/decoder | 14 |
| `mozhi-math-utils` | `math_utils` | Extended math helpers | 24 + 2 constants |
| `mozhi-strings` | `strings` | String manipulation | 21 |

**Total**: 5 packages, 112 functions, 2 constants.

## CLI Commands

### `mozhi add <package>`

Install a library from the registry.

```bash
mozhi add mozhi-html
mozhi add mozhi-http
mozhi add mozhi-json
mozhi add mozhi-math-utils
mozhi add mozhi-strings
```

### `mozhi add --all`

Install every package in the registry.

### `mozhi add --list`

List all currently installed packages.

```bash
$ mozhi add --list
Installed packages in /home/user/.mozhi/libs:
  html/html.mz                  (5,234 bytes)
  http_server/http_server.mz    (2,891 bytes)
  json/json.mz                  (3,012 bytes)
  math_utils/math_utils.mz      (4,156 bytes)
  strings/strings.mz            (3,978 bytes)
```

### `mozhi update`

Refresh the registry cache and reinstall all currently installed packages with their latest versions.

```bash
mozhi update              # refresh + reinstall installed
mozhi update --registry   # only refresh the cache
mozhi update --all        # refresh + install everything
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MOZHI_LIB_DIR` | `~/.mozhi/libs` | Where library `.mz` files are stored |
| `MOZHI_CACHE_DIR` | `~/.mozhi/cache` | Where the registry cache is stored |

## Registry Format

The registry is a single JSON file published at:

```
https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/mozhi-registry.json
```

```json
{
  "registry": "mozhi",
  "version": "1.0.0",
  "packages": [
    {
      "name": "mozhi-html",
      "version": "1.0.0",
      "description": "HTML element generation utilities for Mozhi",
      "category": "web",
      "source": "libs/html/html.mz",
      "install": "html/html.mz",
      "import_as": "html",
      "functions": ["html_doctype", "html_tag", ...]
    }
  ]
}
```

## Direct Download (without the CLI)

You can also download a library file directly with `curl`:

```bash
# Single library
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/libs/html/html.mz \
  -o ~/.mozhi/libs/html/html.mz

# All libraries as a tarball
curl -fsSL https://github.com/crossberry-in/mozhi-doc/releases/download/v-libs-latest/mozhi-libs-all-1.0.0.tar.gz \
  -o mozhi-libs.tar.gz
tar -xzf mozhi-libs.tar.gz -C ~/.mozhi/libs
```

## Verification

Every release ships a `checksums-sha256.txt` file. Verify any download:

```bash
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/libs/checksums-sha256.txt -o /tmp/checksums.txt
sha256sum ~/.mozhi/libs/html/html.mz
grep html.mz /tmp/checksums.txt
```

## Creating Your Own Library

1. Create a directory and a `.mz` file:

```bash
mkdir -p mylib
cat > mylib/mylib.mz << 'EOF'
# My Library v1.0.0
fn greet(name) {
    return "Hello, " + name + "!"
}
EOF
```

2. Add an entry to `mozhi-registry.json`:

```json
{
  "name": "mozhi-mylib",
  "version": "1.0.0",
  "description": "My custom library",
  "source": "libs/mylib/mylib.mz",
  "install": "mylib/mylib.mz",
  "import_as": "mylib",
  "functions": ["greet"]
}
```

3. Commit and push — the `libs-release.yml` workflow will automatically build a tarball, publish it to the docs site, and create a GitHub release tagged `v-libs-X.Y.Z`.

4. Install it:

```bash
mozhi add mozhi-mylib
```

## Release Workflow

The `.github/workflows/libs-release.yml` action:

1. **Triggers** on push to `main` when files under `libs/` change, or manually via `workflow_dispatch`.
2. **Validates** every `.mz` file (non-empty, balanced braces).
3. **Validates** the registry JSON manifest.
4. **Builds** per-package `.tar.gz` and raw `.mz` files.
5. **Bundles** everything into `mozhi-libs-all-<version>.tar.gz`.
6. **Generates** SHA-256 checksums.
7. **Copies** all artifacts into the `public/libs/` directory of the docs site.
8. **Generates** a human-readable HTML index page at `public/libs/index.html`.
9. **Commits** the docs update back to `main`.
10. **Tags** the commit as `v-libs-<version>` and `v-libs-latest`.
11. **Publishes** a GitHub release with all artifacts attached.

## License

MIT
