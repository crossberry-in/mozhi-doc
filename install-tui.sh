#!/usr/bin/env bash
#
# Mozhi TUI CLI Installer
#
# Installs the Go-based Mozhi TUI CLI (mozhi command)
#
# Usage:
#   curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install-tui.sh | bash
#
set -e

REPO="crossberry-in/mozhi-doc"
BINARY_NAME="mozhi"

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
    Darwin*) os="darwin" ;;
    *) error "Unsupported OS: $os"; exit 1 ;;
esac

case "$arch" in
    x86_64|amd64)  arch="amd64" ;;
    aarch64|arm64) arch="arm64"  ;;
    *) error "Unsupported architecture: $arch"; exit 1 ;;
esac

# --- Determine install location ---

install_dir="/usr/local/bin"
if [ ! -w "$install_dir" ]; then
    install_dir="$HOME/.local/bin"
    mkdir -p "$install_dir"
fi

# --- Download ---

asset_name="mozhi-tui-${os}-${arch}"
download_url="https://github.com/${REPO}/releases/download/v2.0.0/${asset_name}"

tmp_file="${TMPDIR:-/tmp}/${asset_name}"

info "Detected platform: ${os}-${arch}"
info "Installing Mozhi TUI CLI to: $install_dir"
info "Downloading $asset_name..."

if ! curl -fSL --progress-bar -o "$tmp_file" "$download_url"; then
    error "Download failed. URL: $download_url"
    error "The TUI binary may not be available for your platform yet."
    exit 1
fi

chmod +x "$tmp_file"

# --- Install ---

if [ -w "$install_dir" ]; then
    mv "$tmp_file" "$install_dir/$BINARY_NAME"
else
    sudo mv "$tmp_file" "$install_dir/$BINARY_NAME"
fi

# --- Verify ---

info "Verifying installation..."
if "$install_dir/$BINARY_NAME" version 2>/dev/null; then
    success "Mozhi TUI CLI is installed and working!"
else
    warn "Mozhi TUI installed but verification failed."
fi

# --- Check for interpreter ---

if ! command -v mozhi-interpreter >/dev/null 2>&1; then
    printf '\n' >&2
    warn "Mozhi interpreter not found. Install it for 'mozhi run' to work:" >&2
    info "  curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash" >&2
fi

printf '\n' >&2
info "Quick start:" >&2
info "  mozhi new myapp       # create a project" >&2
info "  mozhi run src/main.mz # run a file" >&2
info "  mozhi build           # build a project" >&2
info "  mozhi test            # run tests" >&2
info "" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
