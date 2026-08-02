#!/usr/bin/env bash
# ============================================================
# mozhi-template.sh — Install a Mozhi project from a template
# Usage:
#   mozhi-template.sh <project-name> <template-name>
#   mozhi-template.sh myapp react-mozhi
#
# Available templates:
#   helloworld   - Minimal hello world
#   basic        - Basic program with examples
#   api          - JSON API server
#   static       - Static file server
#   react-mozhi  - React-like app with live reload
#   fullstack    - Static + API + shell + multi-language
# ============================================================
set -euo pipefail

REPO="crossberry-in/mozhi-doc"
BASE_URL="https://raw.githubusercontent.com/${REPO}/main/templates"

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

# Available templates
TEMPLATES="helloworld basic api static react-mozhi fullstack"

# Parse arguments
PROJECT_NAME="${1:-}"
TEMPLATE_NAME="${2:-basic}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Mozhi Template Installer"
    echo ""
    echo "Usage: mozhi-template.sh <project-name> [template-name]"
    echo ""
    echo "Available templates:"
    echo "  helloworld   - Minimal hello world"
    echo "  basic        - Basic program with examples"
    echo "  api          - JSON API server"
    echo "  static       - Static file server"
    echo "  react-mozhi  - React-like app with live reload"
    echo "  fullstack    - Static + API + shell + multi-language"
    echo ""
    echo "Examples:"
    echo "  mozhi-template.sh myapp react-mozhi"
    echo "  mozhi-template.sh myapi api"
    echo "  mozhi-template.sh hello helloworld"
    exit 0
fi

# Validate template name
if ! echo "$TEMPLATES" | grep -qw "$TEMPLATE_NAME"; then
    err "Unknown template: $TEMPLATE_NAME"
    echo ""
    echo "Available templates: $TEMPLATES"
    exit 1
fi

# Check if project directory already exists
if [ -d "$PROJECT_NAME" ]; then
    err "Directory already exists: $PROJECT_NAME"
    exit 1
fi

info "Creating project '$PROJECT_NAME' from template '$TEMPLATE_NAME'..."

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Download template files
TEMPLATE_URL="${BASE_URL}/${TEMPLATE_NAME}"

# List of files to download for each template
case "$TEMPLATE_NAME" in
    helloworld)
        FILES="app.mz"
        ;;
    basic)
        FILES="app.mz README.md"
        ;;
    api)
        FILES="app.mz README.md public/index.html"
        ;;
    static)
        FILES="app.mz README.md public/index.html public/style.css public/script.js"
        ;;
    react-mozhi)
        FILES="app.mz README.md"
        ;;
    fullstack)
        FILES="app.mz README.md"
        ;;
    *)
        FILES="app.mz"
        ;;
esac

# Download each file
DOWNLOADED=0
FAILED=0

for file in $FILES; do
    # Create subdirectory if needed
    dir=$(dirname "$file")
    if [ "$dir" != "." ]; then
        mkdir -p "$dir"
    fi

    url="${TEMPLATE_URL}/${file}"
    info "  Downloading ${file}..."

    if curl -fsSL --max-time 30 "$url" -o "$file" 2>/dev/null; then
        ok "  ✓ ${file}"
        DOWNLOADED=$((DOWNLOADED + 1))
    else
        warn "  ✗ ${file} (skipped)"
        FAILED=$((FAILED + 1))
    fi
done

# For react-mozhi, the app.mz creates components/ and public/ on first run
# For fullstack, same

echo ""
info "Project created!"
echo ""
echo "  Template: $TEMPLATE_NAME"
echo "  Files:    $DOWNLOADED downloaded, $FAILED failed"
echo "  Path:     $(pwd)"
echo ""

# Show next steps
case "$TEMPLATE_NAME" in
    helloworld)
        echo "Next steps:"
        echo "  cd $PROJECT_NAME"
        echo "  mozhi-interpreter app.mz"
        ;;
    basic)
        echo "Next steps:"
        echo "  cd $PROJECT_NAME"
        echo "  mozhi-interpreter app.mz"
        ;;
    api)
        echo "Next steps:"
        echo "  cd $PROJECT_NAME"
        echo "  mozhi-interpreter app.mz"
        echo "  # Open http://127.0.0.1:8080"
        echo "  # Test: curl http://127.0.0.1:8080/api/items"
        ;;
    static)
        echo "Next steps:"
        echo "  cd $PROJECT_NAME"
        echo "  mozhi-interpreter app.mz"
        echo "  # Open http://127.0.0.1:8080"
        ;;
    react-mozhi)
        echo "Next steps:"
        echo "  cd $PROJECT_NAME"
        echo "  mozhi-interpreter app.mz"
        echo "  # Open http://127.0.0.1:3000"
        echo "  # Edit components/*.mz - browser auto-reloads!"
        ;;
    fullstack)
        echo "Next steps:"
        echo "  cd $PROJECT_NAME"
        echo "  mozhi-interpreter app.mz"
        echo "  # Open http://127.0.0.1:8080"
        ;;
esac

echo ""
ok "Done!"
