#!/usr/bin/env bash
# ============================================================
# mozhi-update.sh — Refresh the Mozhi library registry cache
#                  and reinstall all installed packages.
# Usage:
#   mozhi update              Refresh cache + reinstall installed libs
#   mozhi update --registry   Only refresh the registry cache
#   mozhi update --all        Refresh + install ALL packages from registry
# ============================================================
set -euo pipefail

REGISTRY_URL="https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/mozhi-registry.json"
LOCAL_LIB_DIR="${MOZHI_LIB_DIR:-$HOME/.mozhi/libs}"
CACHE_DIR="${MOZHI_CACHE_DIR:-$HOME/.mozhi/cache}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info() { echo -e "${BLUE}ℹ${NC}  $*"; }
ok()   { echo -e "${GREEN}✓${NC}  $*"; }
warn() { echo -e "${YELLOW}⚠${NC}  $*"; }
err()  { echo -e "${RED}✗${NC}  $*" >&2; }

mkdir -p "$LOCAL_LIB_DIR" "$CACHE_DIR"
cache_file="$CACHE_DIR/registry.json"

refresh_registry() {
    info "Refreshing package registry from $REGISTRY_URL ..."
    if curl -fsSL "$REGISTRY_URL" -o "$cache_file.tmp"; then
        mv "$cache_file.tmp" "$cache_file"
        local n
        n=$(python3 -c "import json; print(len(json.load(open('$cache_file'))['packages']))")
        ok "Registry updated: $n packages available"
    else
        err "Failed to fetch registry"
        return 1
    fi
}

reinstall_installed() {
    if [ ! -d "$LOCAL_LIB_DIR" ] || [ -z "$(find "$LOCAL_LIB_DIR" -name '*.mz' 2>/dev/null)" ]; then
        warn "No installed packages found. Use 'mozhi add <package>' first."
        return 0
    fi
    info "Reinstalling all currently installed packages..."
    # Map installed .mz files back to package import_as by directory name
    find "$LOCAL_LIB_DIR" -name '*.mz' | while read -r f; do
        rel="${f#$LOCAL_LIB_DIR/}"
        import_as=$(dirname "$rel")
        # Find matching package name in registry
        pkg_name=$(python3 -c "
import json
reg = json.load(open('$cache_file'))
for p in reg['packages']:
    if p['import_as'] == '$import_as':
        print(p['name'])
        break
" 2>/dev/null || true)
        if [ -n "$pkg_name" ]; then
            info "  → reinstalling $pkg_name"
            bash "$(dirname "$0")/install-lib.sh" "$pkg_name" || warn "  failed to reinstall $pkg_name"
        else
            warn "  unknown package: $import_as (skipping)"
        fi
    done
    ok "Update complete"
}

case "${1:-}" in
    --registry|-r)
        refresh_registry
        ;;
    --all|-a)
        refresh_registry
        info "Installing all packages from registry..."
        bash "$(dirname "$0")/install-lib.sh" --all
        ;;
    -h|--help|help)
        cat <<'USAGE'
Mozhi Library Updater

Usage:
  mozhi update              Refresh cache + reinstall installed libs
  mozhi update --registry   Only refresh the registry cache
  mozhi update --all        Refresh + install ALL packages
USAGE
        ;;
    *)
        refresh_registry
        reinstall_installed
        ;;
esac
