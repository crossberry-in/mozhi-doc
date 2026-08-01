#!/usr/bin/env bash
#
# Mozhi Interpreter Installer (builds from source — works on ALL architectures)
#
# Usage:
#   curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
#
set -e

REPO="crossberry-in/mozhi-doc"
BINARY_NAME="mozhi-interpreter"

# --- Helpers ---

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
warn()    { printf "\033[1;33m[warn]\033[0m  %s\n"  "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }

# --- Detect platform ---

os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"

info "Detected platform: ${os}-${arch}"

# --- Check for compiler ---

CC=""
for name in g++ gcc cc c++ clang++; do
    if command -v "$name" >/dev/null 2>&1; then
        CC="$name"
        break
    fi
done

if [ -z "$CC" ]; then
    error "No C/C++ compiler found. Install g++ or gcc:"
    error "  Ubuntu/Debian: sudo apt install g++ make"
    error "  Fedora/RHEL:   sudo dnf install gcc-c++ make"
    error "  Alpine:         apk add build-base"
    error "  macOS:          xcode-select --install"
    exit 1
fi

info "Using compiler: $CC"

# Check for make
if ! command -v make >/dev/null 2>&1; then
    error "make not found. Install it:"
    error "  Ubuntu/Debian: sudo apt install make"
    error "  Alpine:         apk add make"
    exit 1
fi

# --- Determine install location ---

install_dir="/usr/local/bin"
if [ ! -w "$install_dir" ]; then
    install_dir="$HOME/.local/bin"
    mkdir -p "$install_dir"
fi

# --- Download and build from source ---

tmp_dir="${TMPDIR:-/tmp}/mozhi-build-$$"
mkdir -p "$tmp_dir"
cd "$tmp_dir"

info "Downloading interpreter source..."
src_url="https://github.com/${REPO}/releases/download/v2.0.0/mozhi-interpreter-src.tar.gz"
if ! curl -fSL --progress-bar -o src.tar.gz "$src_url"; then
    error "Download failed: $src_url"
    exit 1
fi

info "Extracting..."
tar xzf src.tar.gz
cd mozhi-interpreter-src

info "Building mozhi-interpreter (this may take a few seconds)..."
make clean 2>/dev/null || true
make 2>&1 | tail -5

if [ ! -f mozhi-interpreter ]; then
    error "Build failed!"
    exit 1
fi

info "Installing to $install_dir..."
if [ -w "$install_dir" ]; then
    mv mozhi-interpreter "$install_dir/$BINARY_NAME"
else
    sudo mv mozhi-interpreter "$install_dir/$BINARY_NAME"
fi
chmod +x "$install_dir/$BINARY_NAME"

# --- Verify ---

info "Verifying installation..."
if echo 'echo("Mozhi OK")' | "$install_dir/$BINARY_NAME" /dev/stdin 2>/dev/null; then
    success "Mozhi interpreter is installed and working!"
else
    if "$install_dir/$BINARY_NAME" --version 2>/dev/null; then
        success "Mozhi interpreter installed at: $install_dir/$BINARY_NAME"
    else
        warn "Mozhi interpreter installed but verification failed."
    fi
fi

# --- Cleanup ---

cd /
rm -rf "$tmp_dir"

# --- Info ---

printf '\n' >&2
info "The interpreter is installed as 'mozhi-interpreter'." >&2
info "" >&2
info "Use the unified 'mozhi' command:" >&2
info "  mozhi run src/main.mz     # run a .mz file" >&2
info "  mozhi new myapp           # create a project" >&2
info "  mozhi build               # build a project" >&2
info "  mozhi test                # run tests" >&2
info "" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
