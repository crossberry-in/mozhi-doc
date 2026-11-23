#!/bin/sh
# ============================================================
#  Mozhi (mz) installer — manual install from the mz-docs site
#
#  Usage:
#    curl -fsSL https://mz.netlify.app/install.sh | sh
#    curl -fsSL https://mz.netlify.app/install.sh | sh -s -- v3.7.0
#    curl -fsSL https://mz.netlify.app/install.sh | sh -s -- list
#    MOZHI_VERSION=v3.7.0 curl -fsSL https://mz.netlify.app/install.sh | sh
#
#  What it does:
#    - resolves the requested version against dist/versions.env
#      (default: the latest allowed release; any allowed version can be pinned)
#    - detects OS (linux glibc / musl / Termux, macOS, Windows fallback),
#      architecture (x86_64 / arm64)
#    - downloads the interpreter binary from this site's /dist files
#      (db-backed /api/dist fallback included)
#    - verifies the SHA-256 digest before anything is installed
#    - installs `mozhi` and the short `mz` alias (never overwrites a foreign `mz`)
#
#  Environment overrides:
#    MOZHI_INSTALL_DIR   install target (default: auto-detected)
#    MOZHI_VERSION       version to install (same as first argument)
#    MZ_DOCS_BASE        override the site base URL (testing/staging mirrors)
#    MZ_SKIP_CHECKSUM=1  skip SHA-256 verification (not recommended)
# ============================================================
set -eu

BASE="${MZ_DOCS_BASE:-https://mz.netlify.app}"
BINARY_NAME="mozhi"
SHORT_NAME="mz"

info()    { printf "\033[info]\033  %s\n" "$*" >&2; }
success() { printf "\033[ok]\033    %s\n" "$*" >&2; }
warn()    { printf "\033[warn]\033  %s\n" "$*" >&2; }
error()   { printf "\033[error]\033 %s\n" "$*" >&2; }

# ---------- download helper ----------
fetch() {
    # fetch <url> <outfile>
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL --retry 3 --max-time 300 -o "$2" "$1"
    elif command -v wget >/dev/null 2>&1; then
        wget -q --tries=3 -O "$2" "$1"
    else
        error "need curl or wget to download files"
        exit 1
    fi
}

# ---------- platform detection ----------
os="$(uname -s 2>/dev/null || echo unknown)"
arch="$(uname -m 2>/dev/null || echo unknown)"
case "$os" in Linux*)  os="linux";;  Darwin*) os="darwin";; MINGW*|MSYS*|CYGWIN*) os="windows";; esac
case "$arch" in x86_64|amd64) arch="x86_64";; aarch64|arm64) arch="arm64";; esac

is_termux=0
if [ -n "${TERMUX_VERSION:-}" ] || case "${PREFIX:-}" in *com.termux*) true;; *) false;; esac; then
    is_termux=1
fi

is_musl=0
if [ "$is_termux" -eq 0 ] && command -v ldd >/dev/null 2>&1 && ldd --version 2>&1 | grep -qi musl; then
    is_musl=1
fi

[ "$os" = "windows" ] && BINARY_NAME="mozhi.exe" && SHORT_NAME="mz.exe"

# ---------- version manifest ----------
tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/mz-install.XXXXXX")"
trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
envfile="$tmpdir/versions.env"

info "Reading version manifest from $BASE/dist/versions.env"
fetch "$BASE/dist/versions.env" "$envfile" || { error "could not download the version manifest"; exit 1; }
grep -q '^latest=' "$envfile" || { error "invalid version manifest at $BASE/dist/versions.env"; exit 1; }

latest="$(grep -E '^latest=' "$envfile" | head -n1 | cut -d= -f2-)"
allowed="$(grep -E '^allowed=' "$envfile" | head -n1 | cut -d= -f2-)"

# list mode: show latest + allowed versions and exit
if [ "${1:-}" = "list" ] || [ "${MOZHI_LIST:-}" = "1" ]; then
    echo "latest:  $latest"
    echo "allowed: $allowed"
    echo "manifest: $BASE/dist/manifest.json"
    exit 0
fi

# resolve requested version
requested="${1:-${MOZHI_VERSION:-}}"
if [ -z "$requested" ] || [ "$requested" = "latest" ]; then
    requested="$latest"
fi
case "$requested" in
    *[!A-Za-z0-9._-]*) error "invalid version string: $requested"; exit 1;;
esac

version_ok=0
for v in $allowed; do
    [ "$v" = "$requested" ] && version_ok=1
done
if [ "$version_ok" -ne 1 ]; then
    error "version '$requested' is not an allowed release."
    error "latest:  $latest"
    error "allowed: $allowed"
    exit 1
fi

# ---------- flavor candidates (tried in order) ----------
# flavor names: linux = glibc build, alpine = musl static build, macos, windows
if [ "$os" = "linux" ]; then
    if [ "$is_termux" -eq 1 ] || [ "$is_musl" -eq 1 ]; then
        flavors="alpine linux"
    else
        flavors="linux alpine"
    fi
elif [ "$os" = "darwin" ]; then
    flavors="macos"
else
    flavors="windows"
fi

# ---------- resolve (version, flavor, arch) across allowed releases ----------
# The latest release may lack a platform (e.g. no windows build in v3.7.0);
# fall back through the allowed releases in order.
target_version=""
target_file=""
target_sha=""
for v in $requested $allowed; do
    for flav in $flavors; do
        f="$(grep -E "^${v}\.${flav}\.${arch}\.file=" "$envfile" | head -n1 | cut -d= -f2-)"
        if [ -n "$f" ]; then
            target_version="$v"
            target_file="$f"
            target_sha="$(grep -E "^${v}\.${flav}\.${arch}\.sha256=" "$envfile" | head -n1 | cut -d= -f2-)"
            break 2
        fi
    done
done

if [ -z "$target_file" ]; then
    error "no binary for os=$os arch=$arch in any allowed release ($allowed)."
    error "Check $BASE/api/releases for the full file list."
    exit 1
fi

[ "$target_version" != "$requested" ] && \
    warn "$requested has no $os/$arch build — using $target_version instead"

# ---------- download ----------
# Primary: static site files (/dist, CDN-cached). Fallback: the db-backed
# API (/api/dist — streams from NxDB file storage, works even when the
# source repository is private).
url="$BASE/dist/$target_version/$target_file"
api_url="$BASE/api/dist/$target_version/$target_file"
tmp_file="$tmpdir/$target_file"
info "Downloading $target_file ($target_version)"
if ! fetch "$url" "$tmp_file"; then
    rm -f "$tmp_file"
    warn "static download failed — trying the db-backed endpoint"
    fetch "$api_url" "$tmp_file" || {
        rm -f "$tmp_file"
        error "download failed: $url and $api_url"
        error "Alternative install methods:"
        error "  npm install -g @crossberryweb/mozhi"
        error "  or browse $BASE/api/releases"
        exit 1
    }
fi

# ---------- SHA-256 verification ----------
if [ "${MZ_SKIP_CHECKSUM:-0}" = "1" ]; then
    warn "MZ_SKIP_CHECKSUM=1 — skipping SHA-256 verification (not recommended)"
else
    got="$(sha256sum "$tmp_file" 2>/dev/null | cut -d' ' -f1 || true)"
    if [ -z "$got" ] && command -v shasum >/dev/null 2>&1; then
        got="$(shasum -a 256 "$tmp_file" | cut -d' ' -f1)"
    fi
    if [ -z "$got" ]; then
        error "no sha256sum / shasum available to verify the download"
        error "re-run with MZ_SKIP_CHECKSUM=1 to bypass (at your own risk)"
        exit 1
    fi
    if [ "$got" != "$target_sha" ]; then
        error "SHA-256 MISMATCH for $target_file"
        error "  expected: $target_sha"
        error "  got:      $got"
        error "the file was NOT installed"
        exit 1
    fi
    success "SHA-256 verified: $got"
fi

chmod +x "$tmp_file"

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

info "Installing to $install_dir/$BINARY_NAME"
mv "$tmp_file" "$install_dir/$BINARY_NAME"

# ---------- short alias `mz` (identical behavior; never clobber foreign `mz`) ----------
short_status="installed"
if [ -e "$install_dir/$SHORT_NAME" ] && [ "$(readlink "$install_dir/$SHORT_NAME" 2>/dev/null || true)" != "$BINARY_NAME" ]; then
    if [ -L "$install_dir/$SHORT_NAME" ]; then
        ln -sf "$BINARY_NAME" "$install_dir/$SHORT_NAME" 2>/dev/null || short_status="failed"
    else
        short_status="conflict"
        warn "found an existing '$install_dir/$SHORT_NAME' executable — leaving it untouched"
        warn "the short 'mz' alias was NOT installed; remove/rename that file and re-run to enable it"
    fi
else
    ln -sf "$BINARY_NAME" "$install_dir/$SHORT_NAME" 2>/dev/null || short_status="failed"
fi
[ "$short_status" = "failed" ] && warn "could not create the '$SHORT_NAME' alias (non-fatal)"

# ---------- verify ----------
installed_version=""
if installed_version="$("$install_dir/$BINARY_NAME" --version 2>/dev/null | head -1)" && [ -n "$installed_version" ]; then
    success "$installed_version installed!"
else
    check_mz="$tmpdir/check.mz"
    printf 'echo("Mozhi OK")' > "$check_mz"
    if "$install_dir/$BINARY_NAME" "$check_mz" >/dev/null 2>&1; then
        success "Mozhi interpreter $target_version installed!"
    else
        warn "Installed at $install_dir/$BINARY_NAME (verification could not run)"
    fi
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
info "  mozhi run app.mz         run a script (plain: mz app.mz)"
info "  mz run app.mz            same thing — 'mz' is the short alias for 'mozhi'"
info "  mozhi new myapp          scaffold a new project"
info "Docs:   $BASE"
info "APIs:   $BASE/api/docs  ·  $BASE/api/releases"
info "Packages: nxc pkg search · nxc pkg install owner/name · nxc pkg push"
success "Installed from $BASE/dist/$target_version/$target_file"
