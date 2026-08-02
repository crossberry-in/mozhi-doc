#!/usr/bin/env bash
set -e
# ============================================================
# Mozhi Interpreter Installer
# Downloads pre-built binaries from the PUBLIC mozhi-doc repo.
# The source repo (mozhi) is private/closed-source — no source
# code is released, only pre-built binaries.
# ============================================================

REPO="crossberry-in/mozhi-doc"
BINARY_NAME="mozhi-interpreter"
VERSION="v2.3.0"

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }

os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"
case "$os" in Linux*) os="linux";; Darwin*) os="macos";; MINGW*|MSYS*) os="windows";; esac
case "$arch" in x86_64|amd64) arch="x86_64";; aarch64|arm64) arch="arm64";; esac

install_dir="/usr/local/bin"
[ ! -w "$install_dir" ] && install_dir="$HOME/.local/bin" && mkdir -p "$install_dir"

asset_name="mozhi-interpreter-${os}-${arch}"
[ "$os" = "windows" ] && asset_name="${asset_name}.exe"

url="https://github.com/${REPO}/releases/download/${VERSION}/${asset_name}"
tmp_file="${TMPDIR:-/tmp}/${asset_name}"

info "Downloading ${asset_name} ${VERSION} from public release..."

if ! curl -fSL --progress-bar --max-time 120 -o "$tmp_file" "$url"; then
    error "Download failed."
    error "  URL: $url"
    error ""
    error "Available binaries at:"
    error "  https://github.com/${REPO}/releases/tag/${VERSION}"
    exit 1
fi
chmod +x "$tmp_file"

info "Installing to $install_dir..."
if [ -w "$install_dir" ]; then
    mv "$tmp_file" "$install_dir/$BINARY_NAME"
else
    sudo mv "$tmp_file" "$install_dir/$BINARY_NAME"
fi

info "Verifying..."
echo 'echo("Mozhi OK")' | "$install_dir/$BINARY_NAME" /dev/stdin 2>/dev/null && \
    success "Mozhi interpreter ${VERSION} installed!" || \
    success "Installed at: $install_dir/$BINARY_NAME"

printf '\n' >&2
info "Install TUI: curl -fsSL https://github.com/${REPO}/raw/main/install-tui.sh | bash" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
info "Libraries: just use 'import http from \"mozhi-http\"' — auto-downloads on first run" >&2
