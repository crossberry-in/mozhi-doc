#!/usr/bin/env bash
set -e
REPO="crossberry-in/mozhi"
BINARY_NAME="mozhi-interpreter"

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
url="https://github.com/${REPO}/releases/download/v2.3.0/${asset_name}"
tmp_file="${TMPDIR:-/tmp}/${asset_name}"

info "Downloading ${asset_name}..."
if ! curl -fSL --progress-bar --max-time 30 -o "$tmp_file" "$url"; then
    info "Pre-built binary not found, building from source..."
    # Clone and build from source
    src_dir="${TMPDIR:-/tmp}/mozhi-src"
    rm -rf "$src_dir"
    git clone --depth 1 https://github.com/${REPO}.git "$src_dir" 2>&1 | tail -3
    if [ -d "$src_dir/interpreter" ]; then
        (cd "$src_dir/interpreter" && \
         gcc -O2 -I include src/*.c -o "$tmp_file" -lm 2>&1) || {
            error "Build failed. Install gcc and try again."
            exit 1
        }
    else
        error "Download failed and source not found. URL: $url"
        exit 1
    fi
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
    success "Mozhi interpreter installed!" || \
    success "Installed at: $install_dir/$BINARY_NAME"

printf '\n' >&2
info "Install TUI: curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install-tui.sh | bash" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
