# mozhi-pkg — Mozhi Package Registry

A community package registry for the Mozhi programming language. Add packages from your laptop, push to GitHub, and they automatically appear in the public registry on GitHub Pages.

## Quick Start

### One-time Setup

```bash
# 1) Clone the repo
git clone https://github.com/crossberry-in/mozhi-doc.git
cd mozhi-doc/mozhi-pkg

# 2) Make scripts executable
chmod +x scripts/*.sh registry/src/server.py

# 3) In GitHub repo settings:
#    Settings → Pages → Source = "GitHub Actions"
#    Settings → Actions → General → Workflow permissions:
#      ☑ Read and write permissions
#      ☑ Allow GitHub Actions to create and approve pull requests
```

### Add a Package

```bash
cd mozhi-pkg
git pull --rebase

# A) Scaffold
bash scripts/new-pkg.sh mypackage --category math --desc "My math package"

# B) Implement
#    Edit pkg/mypackage/src/mod.mz with your functions
#    Update pkg/mypackage/package.toml [exports] section

# C) Build registry locally
bash scripts/build-registry.sh

# D) Test locally
python3 registry/src/server.py --port 8080 &
# In another terminal:
#   pkg install --registry http://localhost:8080/mz-registry.json mypackage

# E) Commit and push
git add pkg/mypackage registry
git commit -m "feat(mypackage): add mypackage package"
git push origin main
```

After ~60 seconds, your package is live at:

```
https://crossberry-in.github.io/mozhi-pkg/mz-registry.json
```

Install it:

```bash
pkg registry add mozhi https://crossberry-in.github.io/mozhi-pkg/mz-registry.json --default
pkg install mypackage
```

## Available Packages

| Package | Version | Category | Description |
|---------|---------|----------|-------------|
| `physics` | v1.0.0 | general | Physics library: mechanics, motion, energy, gravity, etc. |
| `math_utils` | v1.0.0 | math | Extended math helpers: arithmetic, geometry, statistics |

## Structure

```
mozhi-pkg/
├── .github/workflows/
│   └── registry.yml           # CI: validate → build → publish to Pages
├── docs/
│   └── PKG_PROMPT.md          # Template for designing new packages
├── pkg/                       # All packages live here
│   ├── math_utils/
│   │   ├── package.toml       # Package metadata
│   │   ├── README.md          # Documentation
│   │   ├── src/
│   │   │   └── mod.mz         # Main module
│   │   ├── tests/
│   │   │   └── test_basic.mz  # Tests
│   │   └── examples/
│   │       └── demo.mz        # Examples
│   └── physics/
│       ├── package.toml
│       ├── README.md
│       ├── src/
│       │   └── mod.mz
│       └── ...
├── registry/                  # Auto-generated (don't edit manually)
│   ├── mz-registry.json       # Main registry index
│   ├── index-a.json           # Per-letter indexes
│   ├── index-m.json
│   ├── index-p.json
│   ├── api/
│   │   └── v1/
│   │       ├── packages.json  # API: all packages
│   │       ├── categories.json # API: by category
│   │       └── stats.json     # API: statistics
│   └── src/
│       └── server.py          # Local registry server
├── scripts/
│   ├── new-pkg.sh             # Scaffold new packages
│   └── build-registry.sh      # Rebuild registry JSON
└── README.md                  # This file
```

## CI/CD Pipeline

When you push to `main`, the `registry.yml` workflow runs:

| Step | What it does |
|------|--------------|
| **validate** | Checks every `pkg/*/package.toml` has `name`, `version`, `description` |
| **build-index** | Runs `build-registry.sh`, rebuilds `mz-registry.json`, commits back to `main` as `mozhi-bot` |
| **publish** | Uploads `registry/` to GitHub Pages |
| **pr-comment** | On PRs: posts a summary table of all packages |

After ~60 seconds, the registry is live at:

```
https://crossberry-in.github.io/mozhi-pkg/mz-registry.json
```

## Local Development

```bash
# Rebuild registry (no push)
bash scripts/build-registry.sh

# Serve registry locally
python3 registry/src/server.py --port 8080

# Inspect registry
python3 -c "import json; d=json.load(open('registry/mz-registry.json')); print(len(d['packages']),'pkgs')"

# Show diff after rebuild
git status registry
git diff --stat registry
```

## Creating a Package

### Option A: Use the scaffold script

```bash
bash scripts/new-pkg.sh mypackage --category math --desc "My math package"
```

This creates:
```
pkg/mypackage/
├── package.toml     # Metadata (edit this)
├── README.md        # Documentation (edit this)
├── src/
│   └── mod.mz       # Main module (implement here)
├── tests/
│   └── test_basic.mz
└── examples/
    └── demo.mz
```

### Option B: Use the design prompt

```bash
cp docs/PKG_PROMPT.md docs/pkg-mypackage-design.md
# Edit the <REPLACE> placeholders
# Feed to an AI assistant
# Save generated code to pkg/mypackage/src/mod.mz
```

## package.toml Format

```toml
[package]
name = "mypackage"
version = "0.1.0"
category = "math"          # general, math, science, web, crypto, os, data, text, net, media
description = "My package"
license = "MIT"
edition = "2024"

[modules]
mod = "Main module"

[exports]
# Map exported names to module.function
my_func = "mod.my_func"
my_const = "mod.my_const"
```

## Categories

| Category | Description |
|----------|-------------|
| `general` | General-purpose utilities |
| `math` | Math, arithmetic, geometry |
| `science` | Physics, chemistry, biology |
| `web` | HTTP, HTML, web frameworks |
| `crypto` | Cryptography, hashing |
| `os` | OS interaction, file system |
| `data` | Data structures, JSON, CSV |
| `text` | String manipulation, parsing |
| `net` | Networking, sockets |
| `media` | Image, audio, video |

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Pages 404 after push | Ensure Pages source is set to **GitHub Actions**, not a branch |
| Workflow can't push back | Check Workflow permissions: "Read and write" |
| Package not in registry | `package.toml` must have `name`, `version`, `description` |
| `pkg install` fails | Wait ~60s for Pages deploy, check the URL in browser |
| Need native libs | Set `native = true` in `package.toml`, document deps in README |

## Links

- [Mozhi Documentation](https://crossberry-in.github.io/mozhi-doc/)
- [Mozhi Libraries](https://crossberry-in.github.io/mozhi-doc/libs.html)
- [Registry JSON](https://crossberry-in.github.io/mozhi-pkg/mz-registry.json)

## License

MIT
