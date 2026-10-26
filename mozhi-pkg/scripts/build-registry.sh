#!/usr/bin/env bash
# ============================================================
# build-registry.sh — Rebuild mz-registry.json from pkg/*/package.toml
# Usage:
#   bash scripts/build-registry.sh
# Output:
#   registry/mz-registry.json          (main index)
#   registry/index-a.json              (per-letter indexes)
#   registry/api/v1/packages.json      (API endpoint)
# ============================================================
set -euo pipefail

REGISTRY_DIR="registry"
INDEX_FILE="$REGISTRY_DIR/mz-registry.json"
API_DIR="$REGISTRY_DIR/api/v1"
mkdir -p "$REGISTRY_DIR" "$API_DIR"

# Colors
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()  { echo -e "${BLUE}ℹ${NC}  $*"; }
ok()    { echo -e "${GREEN}✓${NC}  $*"; }
err()   { echo -e "${RED}✗${NC}  $*" >&2; }

info "Building registry from pkg/*/package.toml..."

# Find all package directories
PKG_DIRS=$(find pkg -maxdepth 2 -name "package.toml" -exec dirname {} \; 2>/dev/null | sort)

if [ -z "$PKG_DIRS" ]; then
    err "No packages found in pkg/"
    err "Create one with: bash scripts/new-pkg.sh <name> --category <cat> --desc \"<desc>\""
    exit 1
fi

# Count packages
PKG_COUNT=$(echo "$PKG_DIRS" | wc -l | tr -d ' ')
info "Found $PKG_COUNT package(s)"

# Build registry JSON using Python
python3 << 'PYEOF'
import os, json, re, sys, hashlib

registry = {
    "name": "mozhi",
    "version": "1.0.0",
    "updated": os.popen("date -u +%Y-%m-%dT%H:%M:%SZ").read().strip(),
    "packages": []
}

pkg_dirs = []
for root, dirs, files in os.walk("pkg"):
    if "package.toml" in files:
        pkg_dirs.append(root)
pkg_dirs.sort()

errors = []

for pkg_dir in pkg_dirs:
    toml_path = os.path.join(pkg_dir, "package.toml")
    
    # Simple TOML parser (handles [package] section with key = "value")
    config = {}
    current_section = None
    with open(toml_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
            if '=' in line:
                key, _, val = line.partition('=')
                key = key.strip()
                val = val.strip()
                # Remove quotes
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                config[f"{current_section}.{key}" if current_section else key] = val

    name = config.get("package.name", "")
    version = config.get("package.version", "")
    description = config.get("package.description", "")
    category = config.get("package.category", "general")
    license_val = config.get("package.license", "MIT")
    edition = config.get("package.edition", "2024")

    if not name:
        errors.append(f"{toml_path}: missing 'name'")
        continue
    if not version:
        errors.append(f"{toml_path}: missing 'version'")
        continue
    if not description:
        errors.append(f"{toml_path}: missing 'description'")
        continue

    # Check for src/mod.mz
    mod_path = os.path.join(pkg_dir, "src", "mod.mz")
    has_mod = os.path.exists(mod_path)

    # Collect module files
    modules = []
    src_dir = os.path.join(pkg_dir, "src")
    if os.path.isdir(src_dir):
        for f in sorted(os.listdir(src_dir)):
            if f.endswith(".mz"):
                modules.append(f)

    # Collect exported symbols from [exports] section
    exports = {}
    for key, val in config.items():
        if key.startswith("exports."):
            exports[key[8:]] = val

    # Compute checksum of src/mod.mz
    checksum = ""
    if has_mod:
        with open(mod_path, 'rb') as f:
            checksum = hashlib.sha256(f.read()).hexdigest()

    # List example files
    examples = []
    ex_dir = os.path.join(pkg_dir, "examples")
    if os.path.isdir(ex_dir):
        for f in sorted(os.listdir(ex_dir)):
            if f.endswith(".mz"):
                examples.append(f)

    # List test files
    tests = []
    test_dir = os.path.join(pkg_dir, "tests")
    if os.path.isdir(test_dir):
        for f in sorted(os.listdir(test_dir)):
            if f.endswith(".mz"):
                tests.append(f)

    pkg_entry = {
        "name": name,
        "version": version,
        "description": description,
        "category": category,
        "license": license_val,
        "edition": edition,
        "path": pkg_dir,
        "modules": modules,
        "exports": exports,
        "examples": examples,
        "tests": tests,
        "checksum_sha256": checksum,
        "has_mod": has_mod,
        "source": f"{pkg_dir}/src/mod.mz",
        "install": f"{pkg_dir}/src/"
    }

    registry["packages"].append(pkg_entry)

if errors:
    for e in errors:
        print(f"  ✗ {e}", file=sys.stderr)
    sys.exit(1)

# Write main registry
with open("registry/mz-registry.json", "w") as f:
    json.dump(registry, f, indent=2, sort_keys=True)

# Write per-letter indexes
letters = {}
for pkg in registry["packages"]:
    first = pkg["name"][0].lower()
    if first not in letters:
        letters[first] = []
    letters[first].append(pkg)

os.makedirs("registry", exist_ok=True)
for letter, pkgs in letters.items():
    with open(f"registry/index-{letter}.json", "w") as f:
        json.dump({"letter": letter, "count": len(pkgs), "packages": pkgs}, f, indent=2)

# Write API endpoints
os.makedirs("registry/api/v1", exist_ok=True)
with open("registry/api/v1/packages.json", "w") as f:
    json.dump(registry, f, indent=2)

# Write categories index
categories = {}
for pkg in registry["packages"]:
    cat = pkg["category"]
    if cat not in categories:
        categories[cat] = []
    categories[cat].append(pkg["name"])

with open("registry/api/v1/categories.json", "w") as f:
    json.dump({"categories": categories}, f, indent=2)

# Write stats
stats = {
    "total_packages": len(registry["packages"]),
    "total_modules": sum(len(p["modules"]) for p in registry["packages"]),
    "total_exports": sum(len(p["exports"]) for p in registry["packages"]),
    "categories": {k: len(v) for k, v in categories.items()},
    "updated": registry["updated"]
}
with open("registry/api/v1/stats.json", "w") as f:
    json.dump(stats, f, indent=2)

print(f"  ✓ Registry built: {len(registry['packages'])} packages")
print(f"  ✓ Main index: registry/mz-registry.json")
print(f"  ✓ Per-letter indexes: {len(letters)} files")
print(f"  ✓ API: registry/api/v1/")
PYEOF

if [ $? -ne 0 ]; then
    err "Failed to build registry"
    exit 1
fi

ok "Registry build complete!"
echo ""
info "Files generated:"
find registry -type f | sort | while read f; do
    size=$(wc -c < "$f" | tr -d ' ')
    echo "  $f  ($size bytes)"
done
