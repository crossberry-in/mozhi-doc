#!/usr/bin/env bash
# ============================================================
# new-pkg.sh — Scaffold a new Mozhi package
# Usage:
#   bash scripts/new-pkg.sh <name> --category <cat> --desc "<short description>"
# Example:
#   bash scripts/new-pkg.sh physics --category science --desc "Physics library"
# ============================================================
set -euo pipefail

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()  { echo -e "${BLUE}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✓${NC}  $*"; }
err()   { echo -e "${RED}✗${NC}  $*" >&2; }

# Defaults
CATEGORY="general"
DESC="A Mozhi package"

# Parse args
NAME=""
while [ $# -gt 0 ]; do
    case "$1" in
        --category) CATEGORY="$2"; shift 2 ;;
        --desc)     DESC="$2"; shift 2 ;;
        -h|--help)
            echo "Usage: bash scripts/new-pkg.sh <name> --category <cat> --desc \"<short description>\""
            echo ""
            echo "Categories: general, science, math, web, crypto, os, data, text, net, media"
            exit 0 ;;
        *) NAME="$1"; shift ;;
    esac
done

if [ -z "$NAME" ]; then
    err "Usage: bash scripts/new-pkg.sh <name> --category <cat> --desc \"<desc>\""
    exit 1
fi

# Validate name
if ! echo "$NAME" | grep -qE '^[a-z][a-z0-9_-]*$'; then
    err "Package name must be lowercase letters, digits, hyphens, underscores (got: $NAME)"
    exit 1
fi

PKG_DIR="pkg/$NAME"

if [ -d "$PKG_DIR" ]; then
    err "Package directory already exists: $PKG_DIR"
    exit 1
fi

info "Scaffolding package '$NAME' (category: $CATEGORY)..."

# Create directory structure
mkdir -p "$PKG_DIR/src" "$PKG_DIR/tests" "$PKG_DIR/examples"

# ---- package.toml ----
cat > "$PKG_DIR/package.toml" << TOML
[package]
name = "$NAME"
version = "0.1.0"
category = "$CATEGORY"
description = "$DESC"
license = "MIT"
edition = "2024"

[modules]
mod = "Main module"

[exports]
# Add exported symbols here
# my_func = "mod.my_func"
TOML

# ---- README.md ----
cat > "$PKG_DIR/README.md" << README
# $NAME

$DESC

## Install

\`\`\`bash
pkg install $NAME
\`\`\`

## Usage

\`\`\`mozhi
import mod from "$NAME"

# TODO: add usage examples
echo("Hello from $NAME!")
\`\`\`

## Modules

- \`mod.mz\` — Main module

## API

| Function | Description |
|----------|-------------|
| TODO | Add your functions here |

## License

MIT
README

# ---- src/mod.mz ----
cat > "$PKG_DIR/src/mod.mz" << MZ
# ============================================================
# $NAME — Main Module
# ============================================================

# TODO: Implement your package functions here

fn hello() {
    return "Hello from $NAME!"
}
MZ

# ---- tests/test_basic.mz ----
cat > "$PKG_DIR/tests/test_basic.mz" << TEST
# Basic tests for $NAME
import mod from "../src/mod.mz"

echo("Running tests for $NAME...")

result = mod.hello()
if result == "Hello from $NAME!" {
    echo("  ✓ hello() works")
} else {
    echo("  ✗ hello() failed: got '" + result + "'")
}

echo("Tests complete.")
TEST

# ---- examples/demo.mz ----
cat > "$PKG_DIR/examples/demo.mz" << DEMO
# $NAME — Example
import mod from "../src/mod.mz"

echo(mod.hello())
DEMO

# ---- .gitkeep for empty dirs ----
touch "$PKG_DIR/tests/.gitkeep" "$PKG_DIR/examples/.gitkeep"

ok "Package scaffolded at $PKG_DIR/"
echo ""
echo "  $PKG_DIR/"
echo "  ├── package.toml"
echo "  ├── README.md"
echo "  ├── src/"
echo "  │   └── mod.mz"
echo "  ├── tests/"
echo "  │   └── test_basic.mz"
echo "  └── examples/"
echo "      └── demo.mz"
echo ""
echo "Next steps:"
echo "  1. Edit src/mod.mz to implement your functions"
echo "  2. Update package.toml [exports] section"
echo "  3. Write tests in tests/"
echo "  4. Add examples in examples/"
echo "  5. Run: bash scripts/build-registry.sh"
echo "  6. git add pkg/$NAME && git commit -m 'feat($NAME): add $NAME package'"
