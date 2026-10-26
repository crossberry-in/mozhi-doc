#!/usr/bin/env bash
# ============================================================
# mozhi-add.sh — Install a Mozhi library package
# Usage:
#   mozhi add mozhi-html
#   mozhi add mozhi-http
#   mozhi add mozhi-json
#   mozhi add mozhi-math-utils
#   mozhi add mozhi-strings
#   mozhi add --all
# ============================================================
set -euo pipefail

# Configuration
REGISTRY_URL="https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/mozhi-registry.json"
LIBS_BASE_URL="https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/libs"
LOCAL_LIB_DIR="${MOZHI_LIB_DIR:-$HOME/.mozhi/libs}"
CACHE_DIR="${MOZHI_CACHE_DIR:-$HOME/.mozhi/cache}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${BLUE}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✓${NC}  $*"; }
warn()  { echo -e "${YELLOW}⚠${NC}  $*"; }
err()   { echo -e "${RED}✗${NC}  $*" >&2; }

# Ensure directories exist
mkdir -p "$LOCAL_LIB_DIR" "$CACHE_DIR"

# Fetch the registry
fetch_registry() {
    local cache_file="$CACHE_DIR/registry.json"
    if [ -f "$cache_file" ] && [ "$(( $(date +%s) - $(stat -c %Y "$cache_file" 2>/dev/null || echo 0) ))" -lt 3600 ]; then
        info "Using cached registry (use 'mozhi update' to refresh)"
        cat "$cache_file"
        return 0
    fi
    info "Fetching package registry..."
    if curl -fsSL "$REGISTRY_URL" -o "$cache_file"; then
        ok "Registry fetched"
        cat "$cache_file"
        return 0
    fi
    err "Failed to fetch registry from $REGISTRY_URL"
    return 1
}

# Find a package in the registry by name
find_package() {
    local name="$1"
    local registry_file="$1"
    python3 -c "
import json, sys
reg = json.load(open('$CACHE_DIR/registry.json'))
for p in reg['packages']:
    if p['name'] == '$name' or p['import_as'] == '$name':
        print(json.dumps(p))
        sys.exit(0)
sys.exit(1)
"
}

# Install a single package
install_package() {
    local pkg_name="$1"
    local pkg_json
    pkg_json=$(find_package "$pkg_name") || {
        err "Package '$pkg_name' not found in registry"
        echo "Available packages:"
        python3 -c "
import json
reg = json.load(open('$CACHE_DIR/registry.json'))
for p in reg['packages']:
    print(f'  - {p[\"name\"]} (import as: {p[\"import_as\"]})')
"
        return 1
    }

    local name version src install_path import_as target_dir target_file
    name=$(echo "$pkg_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['name'])")
    version=$(echo "$pkg_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['version'])")
    src=$(echo "$pkg_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['source'])")
    install_path=$(echo "$pkg_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['install'])")
    import_as=$(echo "$pkg_json" | python3 -c "import json,sys; print(json.load(sys.stdin)['import_as'])")

    target_dir="$LOCAL_LIB_DIR/$(dirname "$install_path")"
    target_file="$LOCAL_LIB_DIR/$install_path"
    mkdir -p "$target_dir"

    info "Installing $name v$version..."
    info "  → $target_file"

    if curl -fsSL "$LIBS_BASE_URL/$install_path" -o "$target_file"; then
        ok "Installed $name v$version"
        ok "  Import with: import $import_as from \"$name\""
        ok "  File: $target_file"
        return 0
    else
        err "Failed to download $src"
        return 1
    fi
}

# Install all packages
install_all() {
    info "Installing all packages from registry..."
    python3 -c "import json; [print(p['name']) for p in json.load(open('$CACHE_DIR/registry.json'))['packages']]" | while read -r pkg; do
        install_package "$pkg" || warn "Failed to install $pkg"
    done
    ok "All packages installed to $LOCAL_LIB_DIR"
}

# List installed packages
list_installed() {
    info "Installed packages in $LOCAL_LIB_DIR:"
    if [ ! -d "$LOCAL_LIB_DIR" ] || [ -z "$(find "$LOCAL_LIB_DIR" -name '*.mz' 2>/dev/null)" ]; then
        echo "  (none)"
        return
    fi
    find "$LOCAL_LIB_DIR" -name '*.mz' | sort | while read -r f; do
        rel="${f#$LOCAL_LIB_DIR/}"
        size=$(wc -c < "$f" | tr -d ' ')
        echo "  $rel  ($size bytes)"
    done
}

# Main
main() {
    if [ $# -eq 0 ]; then
        cat <<'USAGE'
Mozhi Library Installer

Usage:
  mozhi add <package>     Install a package (e.g. mozhi-html)
  mozhi add --all         Install all packages from the registry
  mozhi add --list        List installed packages
  mozhi update            Refresh the registry cache

Examples:
  mozhi add mozhi-html
  mozhi add mozhi-http
  mozhi add mozhi-json
  mozhi add mozhi-math-utils
  mozhi add mozhi-strings

Environment:
  MOZHI_LIB_DIR    Override install location (default: ~/.mozhi/libs)
  MOZHI_CACHE_DIR  Override cache location (default: ~/.mozhi/cache)
USAGE
        exit 0
    fi

    # Always ensure registry is present
    fetch_registry >/dev/null || exit 1

    case "$1" in
        --all|-a)
            install_all
            ;;
        --list|-l|list)
            list_installed
            ;;
        -h|--help|help)
            main
            ;;
        *)
            install_package "$1"
            ;;
    esac
}

main "$@"
