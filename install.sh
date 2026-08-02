#!/usr/bin/env bash
set -e
# Download from the PUBLIC doc repo (mozhi-doc) — works even if the
# source repo (mozhi) is private.
DOC_REPO="crossberry-in/mozhi-doc"
SRC_REPO="crossberry-in/mozhi"
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

# Try the public doc repo first, then the source repo, then build from source.
tmp_file="${TMPDIR:-/tmp}/${asset_name}"

# URL 1: Public doc repo release (always works)
url_doc="https://github.com/${DOC_REPO}/releases/download/${VERSION}/${asset_name}"
# URL 2: Source repo release (works if repo is public)
url_src="https://github.com/${SRC_REPO}/releases/download/${VERSION}/${asset_name}"

info "Downloading ${asset_name} ${VERSION}..."

# Try doc repo first (public)
if curl -fSL --progress-bar --max-time 60 -o "$tmp_file" "$url_doc" 2>&1; then
    success "Downloaded from public doc repo"
# Try source repo
elif curl -fSL --progress-bar --max-time 60 -o "$tmp_file" "$url_src" 2>&1; then
    success "Downloaded from source repo"
# Build from source as fallback
else
    info "Pre-built binary not found, building from source..."
    src_dir="${TMPDIR:-/tmp}/mozhi-src"
    rm -rf "$src_dir"
    git clone --depth 1 "https://github.com/${SRC_REPO}.git" "$src_dir" 2>&1 | tail -3 || \
    git clone --depth 1 "https://github.com/${DOC_REPO}.git" "$src_dir" 2>&1 | tail -3 || true
    if [ -d "$src_dir/interpreter" ]; then
        (cd "$src_dir/interpreter" && \
         gcc -O2 -I include src/*.c -o "$tmp_file" -lm 2>&1) || {
            error "Build failed. Install gcc and try again."
            exit 1
        }
    elif [ -f "$src_dir/install-lib.sh" ]; then
        # Doc repo has install-lib.sh but no interpreter source — try downloading
        error "Cannot build from doc repo. Download manually from:"
        error "  $url_doc"
        exit 1
    else
        error "Download failed and source not found."
        error "  URL 1: $url_doc"
        error "  URL 2: $url_src"
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
    success "Mozhi interpreter ${VERSION} installed!" || \
    success "Installed at: $install_dir/$BINARY_NAME"

printf '\n' >&2
info "Install TUI: curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install-tui.sh | bash" >&2
info "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
info "Libraries: mozhi add mozhi-http  (or just use 'import http from \"mozhi-http\"')" >&2
