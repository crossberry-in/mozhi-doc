#!/usr/bin/env bash
set -e
# Download from the PUBLIC doc repo (mozhi-doc) — works even if the
# source repo (mozhi) is private.
DOC_REPO="crossberry-in/mozhi-doc"
SRC_REPO="crossberry-in/mozhi"
BINARY_NAME="mozhi"
VERSION="v2.3.0"

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }

os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"
case "$os" in Linux*) os="linux";; Darwin*) os="darwin";; MINGW*|MSYS*) os="windows";; esac
case "$arch" in x86_64|amd64) arch="amd64";; aarch64|arm64) arch="arm64";; esac

install_dir="/usr/local/bin"
[ ! -w "$install_dir" ] && install_dir="$HOME/.local/bin" && mkdir -p "$install_dir"

asset_name="mozhi-tui-${os}-${arch}"
[ "$os" = "windows" ] && asset_name="${asset_name}.exe"
tmp_file="${TMPDIR:-/tmp}/${asset_name}"

# URL 1: Public doc repo release
url_doc="https://github.com/${DOC_REPO}/releases/download/${VERSION}/${asset_name}"
# URL 2: Source repo release
url_src="https://github.com/${SRC_REPO}/releases/download/${VERSION}/${asset_name}"

info "Downloading ${asset_name} ${VERSION}..."

if curl -fSL --progress-bar --max-time 60 -o "$tmp_file" "$url_doc" 2>&1; then
    success "Downloaded from public doc repo"
elif curl -fSL --progress-bar --max-time 60 -o "$tmp_file" "$url_src" 2>&1; then
    success "Downloaded from source repo"
else
    error "Download failed. Try manually:"
    error "  $url_doc"
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
"$install_dir/$BINARY_NAME" version 2>/dev/null && \
    success "Mozhi TUI CLI ${VERSION} installed!" || \
    success "Installed at: $install_dir/$BINARY_NAME"

printf '\n' >&2
info "Quick start: mozhi new myapp && cd myapp && mozhi run src/main.mz" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
