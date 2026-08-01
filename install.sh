#!/usr/bin/env bash
#
# Mozhi Interpreter Installer
# Downloads pre-built binary from GitHub release (no compilation needed)
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

case "$os" in
    Linux*)  os="linux"  ;;
    Darwin*) os="macos"  ;;
    MINGW*|MSYS*|CYGWIN*) os="windows" ;;
    *) error "Unsupported OS: $os"; exit 1 ;;
esac

case "$arch" in
    x86_64|amd64)  arch="x86_64" ;;
    aarch64|arm64) arch="arm64"  ;;
    *) error "Unsupported architecture: $arch"; exit 1 ;;
esac

# --- Determine install location ---
install_dir="/usr/local/bin"
if [ ! -w "$install_dir" ]; then
    install_dir="$HOME/.local/bin"
    mkdir -p "$install_dir"
fi

# --- Get latest release version ---
info "Fetching latest release..."
version=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" 2>/dev/null | grep '"tag_name"' | sed -E 's/.*"tag_name":\s*"([^"]+)".*/\1/')
if [ -z "$version" ]; then
    error "Failed to determine latest release version"
    exit 1
fi
info "Latest version: $version"

# --- Try pre-built binary first ---
asset_name="mozhi-interpreter-${os}-${arch}"
download_url="https://github.com/${REPO}/releases/download/${version}/${asset_name}"

info "Downloading $asset_name..."
tmp_file="${TMPDIR:-/tmp}/${asset_name}"

if curl -fSL --progress-bar --max-time 30 -o "$tmp_file" "$download_url" 2>&1; then
    chmod +x "$tmp_file"
    info "Installing to $install_dir..."
    if [ -w "$install_dir" ]; then
        mv "$tmp_file" "$install_dir/$BINARY_NAME"
    else
        sudo mv "$tmp_file" "$install_dir/$BINARY_NAME"
    fi
else
    # Pre-built binary not available — build from source
    info "Pre-built binary not found. Building from source..."
    
    # Check for compiler
    CC=""
    for name in g++ gcc cc c++ clang++; do
        if command -v "$name" >/dev/null 2>&1; then
            CC="$name"
            break
        fi
    done
    
    if [ -z "$CC" ]; then
        error "No C/C++ compiler found. Install g++:"
        error "  sudo apt install g++ make"
        exit 1
    fi
    
    info "Using compiler: $CC"
    
    # Download source
    tmp_dir="${TMPDIR:-/tmp}/mozhi-build-$$"
    mkdir -p "$tmp_dir"
    cd "$tmp_dir"
    
    src_url="https://github.com/${REPO}/releases/download/${version}/mozhi-interpreter-src.tar.gz"
    if ! curl -fSL --max-time 30 -o src.tar.gz "$src_url"; then
        error "Download failed"
        exit 1
    fi
    
    tar xzf src.tar.gz
    cd mozhi-interpreter-src
    
    # Build directly without make (avoids Makefile tab issues)
    info "Compiling (this takes 5-10 seconds)..."
    mkdir -p build
    for f in src/*.c; do
        name=$(basename "$f" .c)
        $CC -Wall -Wextra -std=c++17 -O3 -I include -x c -c "$f" -o "build/${name}.o" 2>&1
    done
    $CC -O3 -s build/*.o -o mozhi-interpreter -lm 2>&1
    
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
    
    cd /
    rm -rf "$tmp_dir"
fi

# --- Verify ---
info "Verifying installation..."
if echo 'echo("Mozhi OK")' | "$install_dir/$BINARY_NAME" /dev/stdin 2>/dev/null; then
    success "Mozhi interpreter installed successfully!"
else
    success "Mozhi interpreter installed at: $install_dir/$BINARY_NAME"
fi

printf '\n' >&2
info "Install TUI CLI:" >&2
info "  curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install-tui.sh | bash" >&2
info "" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
