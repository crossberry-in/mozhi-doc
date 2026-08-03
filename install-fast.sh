#!/usr/bin/env bash
set -e
# ============================================================
# Mozhi Fast Interpreter Installer (mozhi-fast, Rust bytecode VM)
# Downloads the pre-built mozhi-fast binary from the PUBLIC
# mozhi-doc repo release.
# ============================================================

REPO="crossberry-in/mozhi-doc"
BINARY_NAME="mozhi-fast"
VERSION="v2.6.0"

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }

os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"
case "$os" in Linux*) os="linux";; Darwin*) os="macos";; MINGW*|MSYS*) os="windows";; esac
case "$arch" in x86_64|amd64) arch="x86_64";; aarch64|arm64) arch="arm64";; esac

install_dir="/usr/local/bin"
[ ! -w "$install_dir" ] && install_dir="$HOME/.local/bin" && mkdir -p "$install_dir"

asset_name="mozhi-fast-${os}-${arch}"
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
echo 'echo("mozhi-fast OK")' > /tmp/_mzfast_check.mz
"$install_dir/$BINARY_NAME" /tmp/_mzfast_check.mz >/dev/null 2>&1 && \
    success "mozhi-fast ${VERSION} installed!" || \
    success "Installed at: $install_dir/$BINARY_NAME"
rm -f /tmp/_mzfast_check.mz

printf '\n' >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/docs/mozhi-fast" >&2
