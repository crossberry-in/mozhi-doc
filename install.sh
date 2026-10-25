#!/usr/bin/env bash
set -e
# ============================================================
# Mozhi Interpreter Installer
# Downloads pre-built binaries from the PUBLIC mozhi-doc repo.
# The source repo (mozhi) is private/closed-source — no source
# code is released, only pre-built binaries.
#
# Installs the interpreter as `mozhi` (canonical command used by
# all docs: mozhi run app.mz, mozhi new myapp, mozhi --version).
# Also installs the short alias `mz` (identical behavior, same binary):
#   mz run app.mz == mozhi run app.mz
# If an unrelated `mz` executable already exists it is left untouched
# and a warning is printed (never overwrite a foreign command).
# Also installs the short alias `mz` (same binary, identical behavior):
#   mz run app.mz == mozhi run app.mz
# If an unrelated executable named `mz` already exists it is left
# untouched (never overwrite a foreign command).
# A `mozhi-interpreter` symlink is kept for backwards
# compatibility with older installs.
#
# v3.1.1+ Linux binaries are fully static (musl, SQLite vendored)
# so one binary serves glibc distros, Alpine, and Termux alike.
# For platforms without a v3.1.1 build (macOS, Windows) the
# installer automatically falls back to the v2.5.0 assets.
# ============================================================

REPO="crossberry-in/mozhi-doc"
BINARY_NAME="mozhi"
COMPAT_NAME="mozhi-interpreter"
SHORT_NAME="mz"
VERSION="v3.2.0"
FALLBACK_VERSION="v2.5.0"

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }
warn()    { printf "\033[1;33m[warn]\033[0m  %s\n" "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }

# ---------- platform detection ----------
os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"
case "$os" in Linux*)  os="linux";;  Darwin*) os="darwin";; MINGW*|MSYS*) os="windows";; esac
case "$arch" in x86_64|amd64) arch="x86_64";; aarch64|arm64) arch="arm64";; esac

is_termux=0
if [ -n "${TERMUX_VERSION:-}" ] || case "${PREFIX:-}" in *com.termux*) true;; *) false;; esac; then
    is_termux=1
fi

is_musl=0
if [ "$is_termux" -eq 0 ] && ldd --version 2>&1 | grep -qi musl; then
    is_musl=1
fi

[ "$os" = "windows" ] && BINARY_NAME="mozhi.exe" && COMPAT_NAME="mozhi-interpreter.exe" && SHORT_NAME="mz.exe"

# ---------- asset candidates (tried in order) ----------
# Flavor names: linux = glibc build, alpine = musl static build.
# Since v3.1.1 the linux builds are themselves fully static, so they
# are tried first even on musl/Termux systems.
candidates=""
if [ "$os" = "linux" ]; then
    if [ "$is_termux" -eq 1 ] || [ "$is_musl" -eq 1 ]; then
        candidates="$VERSION linux
$FALLBACK_VERSION alpine
$FALLBACK_VERSION linux"
    else
        candidates="$VERSION linux
$FALLBACK_VERSION linux"
    fi
elif [ "$os" = "darwin" ]; then
    candidates="$FALLBACK_VERSION macos"
else
    candidates="$FALLBACK_VERSION windows"
fi

# ---------- install directory ----------
install_dir=""
if [ -n "${MOZHI_INSTALL_DIR:-}" ]; then
    install_dir="$MOZHI_INSTALL_DIR"
    mkdir -p "$install_dir"
elif [ "$is_termux" -eq 1 ] && [ -n "${PREFIX:-}" ]; then
    install_dir="$PREFIX/bin"
elif [ "$os" = "darwin" ] && [ "$arch" = "arm64" ] && [ -d "/opt/homebrew/bin" ] && [ -w "/opt/homebrew/bin" ]; then
    install_dir="/opt/homebrew/bin"
elif [ -d "/usr/local/bin" ] && [ -w "/usr/local/bin" ]; then
    install_dir="/usr/local/bin"
else
    install_dir="$HOME/.local/bin"
    mkdir -p "$install_dir"
fi

# ---------- download (with version/flavor fallback) ----------
tmp_file=""
downloaded=""
flavor_used=""
while read -r ver flav; do
    [ -z "$ver" ] && continue
    asset_name="mozhi-interpreter-${flav}-${arch}"
    [ "$os" = "windows" ] && asset_name="${asset_name}.exe"
    url="https://github.com/${REPO}/releases/download/${ver}/${asset_name}"
    info "Downloading ${asset_name} ${ver} from public release..."
    if curl -fSL --progress-bar --max-time 180 -o "${TMPDIR:-/tmp}/${asset_name}" "$url"; then
        tmp_file="${TMPDIR:-/tmp}/${asset_name}"
        downloaded="$ver"
        flavor_used="$flav"
        break
    fi
    info "Not available, trying next candidate..."
done <<EOF
$candidates
EOF

if [ -z "$tmp_file" ]; then
    error "Download failed — no matching binary found."
    error "Available binaries at:"
    error "  https://github.com/${REPO}/releases"
    exit 1
fi

chmod +x "$tmp_file"

# ---------- install ----------
info "Installing to $install_dir ..."
mv "$tmp_file" "$install_dir/$BINARY_NAME"
# keep the legacy command name working (older docs/scripts used it)
ln -sf "$BINARY_NAME" "$install_dir/$COMPAT_NAME" 2>/dev/null || true

# ---------- short alias `mz` (identical behavior to `mozhi`) ----------
short_status="installed"
if [ -e "$install_dir/$SHORT_NAME" ] && [ "$(readlink "$install_dir/$SHORT_NAME" 2>/dev/null || true)" != "$BINARY_NAME" ]; then
    if [ -L "$install_dir/$SHORT_NAME" ]; then
        # an existing symlink pointing elsewhere: repoint it to our binary
        ln -sf "$BINARY_NAME" "$install_dir/$SHORT_NAME" 2>/dev/null || short_status="failed"
    else
        # a real foreign executable named `mz`: never overwrite it
        short_status="conflict"
        warn "found an existing '$install_dir/$SHORT_NAME' executable -- leaving it untouched"
        warn "the short 'mz' alias was NOT installed; remove/rename that file and re-run to enable it"
    fi
else
    ln -sf "$BINARY_NAME" "$install_dir/$SHORT_NAME" 2>/dev/null || short_status="failed"
fi
[ "$short_status" = "failed" ] && warn "could not create the 'mz' alias symlink (non-fatal)"

# ---------- verify ----------
info "Verifying..."
installed_version=""
if installed_version="$("$install_dir/$BINARY_NAME" --version 2>/dev/null | head -1)" && [ -n "$installed_version" ]; then
    success "$installed_version installed!"
else
    # older releases had no --version flag; run a real script instead
    check_mz="$(mktemp "${TMPDIR:-/tmp}/mozhi-check-XXXXXX.mz")"
    printf 'echo("Mozhi OK")' > "$check_mz"
    if "$install_dir/$BINARY_NAME" "$check_mz" >/dev/null 2>&1; then
        success "Mozhi interpreter ${downloaded} installed!"
    else
        warn "Installed at: $install_dir/$BINARY_NAME (verification could not run)"
    fi
    rm -f "$check_mz"
fi

# ---------- PATH check ----------
case ":$PATH:" in
    *":$install_dir:"*) ;;
    *)
        warn "$install_dir is not on your PATH."
        info "Add it now:"
        info "  echo 'export PATH=\"$install_dir:\$PATH\"' >> ~/.bashrc && source ~/.bashrc"
        ;;
esac

printf '\n' >&2
info "Get started:"
info "  mozhi --version          show the interpreter version"
info "  mozhi run app.mz         run a script (plain: mozhi app.mz)"
info "  mz run app.mz            same thing — 'mz' is the short alias for 'mozhi'"
info "  mozhi new myapp          scaffold a new project"
success "Docs: https://crossberry-in.github.io/mozhi-doc/" >&2
info "Libraries: just use 'import http from \"mozhi-http\"' — auto-downloads on first run" >&2
