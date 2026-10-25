#!/usr/bin/env bash
set -e
# ============================================================
# Mozhi TUI CLI Installer
# Downloads pre-built binaries from the PUBLIC mozhi-doc repo.
# ============================================================

REPO="crossberry-in/mozhi-doc"
BINARY_NAME="mozhi-tui"
VERSION="v2.5.0"

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }

os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"
case "$os" in Linux*) os="linux";; Darwin*) os="darwin";; MINGW*|MSYS*) os="windows";; esac
case "$arch" in x86_64|amd64) arch="amd64";; aarch64|arm64) arch="arm64";; esac

install_dir=""
if [ -n "${MOZHI_INSTALL_DIR:-}" ]; then
    install_dir="$MOZHI_INSTALL_DIR"
    mkdir -p "$install_dir"
elif [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    install_dir="/usr/local/bin"
else
    install_dir="$HOME/.local/bin"
    mkdir -p "$install_dir"
fi

asset_name="mozhi-tui-${os}-${arch}"
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
mv "$tmp_file" "$install_dir/$BINARY_NAME"
case ":$PATH:" in
    *":$install_dir:"*) ;;
    *)
        printf "\033[1;33m[warn]\033[0m  %s\n" "$install_dir is not on your PATH." >&2
        printf "\033[1;34m[info]\033[0m  %s\n" "  echo 'export PATH=\"$install_dir:\$PATH\"' >> ~/.bashrc && source ~/.bashrc" >&2
        ;;
esac

info "Verifying..."
"$install_dir/$BINARY_NAME" version 2>/dev/null && \
    success "Mozhi TUI CLI ${VERSION} installed!" || \
    success "Installed at: $install_dir/$BINARY_NAME"

printf '\n' >&2
info "The interactive TUI is installed as 'mozhi-tui' (the main interpreter owns 'mozhi')." >&2
info "Interpreter quick start: mozhi new myapp && cd myapp && mozhi run src/main.mz" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
