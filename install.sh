#!/usr/bin/env bash
#
# Mozhi — Universal installer
#
# Supported platforms:
#   - Linux x86_64 (Ubuntu, Debian, Fedora, Arch, etc.)  → mozhi-linux-x86_64
#   - Linux ARM64 (Raspberry Pi 4/5, ARM servers)        → mozhi-linux-arm64
#   - Alpine Linux x86_64 (musl libc)                    → mozhi-alpine-x86_64
#   - Alpine Linux ARM64 (musl libc)                     → mozhi-alpine-arm64
#   - Termux on Android ARM64                            → mozhi-alpine-arm64 (static)
#   - Termux on Android x86_64                           → mozhi-alpine-x86_64 (static)
#   - macOS Intel                                         → mozhi-macos-x86_64
#   - macOS Apple Silicon (M1/M2/M3/M4)                  → mozhi-macos-arm64
#   - Windows x86_64 (via Git Bash / WSL)                → mozhi-windows-x86_64.exe
#
# Usage:
#   curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
#
set -e

# --- Configuration ------------------------------------------------------

REPO="crossberry-in/mozhi-doc"
# Install as 'mozhi-interpreter' to avoid conflict with the mozhi-pkg
# package manager, which installs as 'mozhi' (the unified dispatcher).
# The mozhi-pkg dispatcher will find this binary via find_mozhi_interpreter().
BINARY_NAME="mozhi-interpreter"

# --- Helpers (ALL output goes to stderr so it never pollutes $(...)) ----

info()    { printf "\033[1;34m[info]\033[0m  %s\n"  "$*" >&2; }
warn()    { printf "\033[1;33m[warn]\033[0m  %s\n"  "$*" >&2; }
error()   { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }
success() { printf "\033[1;32m[ok]\033[0m    %s\n"  "$*" >&2; }

# --- Detect platform ----------------------------------------------------

detect_platform() {
    local os arch libc

    # Detect OS
    case "$(uname -s 2>/dev/null || echo unknown)" in
        Linux*)  os="linux"  ;;
        Darwin*) os="macos"  ;;
        MINGW*|MSYS*|CYGWIN*) os="windows" ;;
        *) error "Unsupported OS: $(uname -s)"; exit 1 ;;
    esac

    # Detect Termux (Android) — overrides os="linux"
    # Termux sets $TERMUX_VERSION and $PREFIX=/data/data/com.termux/files/usr
    if [ -n "$TERMUX_VERSION" ]; then
        os="termux"
    elif [ -n "$PREFIX" ] && case "$PREFIX" in /data/data/com.termux*) true;; *) false;; esac; then
        os="termux"
    fi

    # Detect architecture
    case "$(uname -m 2>/dev/null || echo unknown)" in
        x86_64|amd64)   arch="x86_64" ;;
        aarch64|arm64)  arch="arm64"  ;;
        *) error "Unsupported architecture: $(uname -m)"; exit 1 ;;
    esac

    # Detect libc on Linux
    libc="gnu"
    if [ "$os" = "linux" ]; then
        if ldd --version 2>&1 | grep -qi musl; then
            libc="musl"
        fi
    fi

    echo "${os}-${arch}-${libc}"
}

# --- Map platform to asset name -----------------------------------------

asset_for_platform() {
    local platform="$1"
    local os arch libc

    os="${platform%%-*}"               # linux | termux | macos | windows
    local rest="${platform#*-}"        # arch-libc
    arch="${rest%%-*}"                 # x86_64 | arm64
    libc="${rest#*-}"                  # gnu | musl

    case "$os" in
        linux)
            if [ "$libc" = "musl" ]; then
                echo "mozhi-alpine-${arch}"
            else
                echo "mozhi-linux-${arch}"
            fi
            ;;
        termux)
            # Termux uses Android's bionic libc — only static musl binaries work
            echo "mozhi-alpine-${arch}"
            ;;
        macos)
            echo "mozhi-macos-${arch}"
            ;;
        windows)
            echo "mozhi-windows-${arch}.exe"
            ;;
        *)
            return 1
            ;;
    esac
}

# --- Determine install location -----------------------------------------

install_dir_for() {
    local os="$1"
    case "$os" in
        termux)
            # Termux: user-owned directory, no sudo needed
            echo "$PREFIX/bin"
            ;;
        macos)
            if [ "$2" = "arm64" ] && [ -d "/opt/homebrew/bin" ]; then
                echo "/opt/homebrew/bin"
            elif [ -w "/usr/local/bin" ] || sudo -n true 2>/dev/null; then
                echo "/usr/local/bin"
            else
                echo "$HOME/.local/bin"
            fi
            ;;
        linux|windows|*)
            if [ -w "/usr/local/bin" ] || sudo -n true 2>/dev/null; then
                echo "/usr/local/bin"
            else
                echo "$HOME/.local/bin"
            fi
            ;;
    esac
}

# --- Get the latest release version -------------------------------------

get_latest_version() {
    local version
    version="$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
        | grep '"tag_name"' \
        | sed -E 's/.*"tag_name":\s*"([^"]+)".*/\1/')"

    if [ -z "$version" ]; then
        error "Failed to determine the latest Mozhi release version."
        exit 1
    fi
    echo "$version"
}

# --- Download binary ----------------------------------------------------

download_binary() {
    local asset_name="$1"
    local version="$2"
    local tmp_file

    # Use TMPDIR if set (Termux sets this to $PREFIX/tmp), fallback to /tmp
    local tmp_dir="${TMPDIR:-/tmp}"
    tmp_file="${tmp_dir}/${asset_name}"
    local download_url="https://github.com/${REPO}/releases/download/${version}/${asset_name}"

    info "Downloading $asset_name ($version) to $tmp_file ..."
    if ! curl -fSL --progress-bar -o "$tmp_file" "$download_url"; then
        error "Download failed. URL: $download_url"
        exit 1
    fi
    chmod +x "$tmp_file"
    # Print tmp_file to STDOUT (this is the only thing captured by $())
    printf '%s' "$tmp_file"
}

# --- Install binary -----------------------------------------------------

install_binary() {
    local tmp_file="$1"
    local install_dir="$2"
    local final_path
    local need_sudo=0

    final_path="$install_dir/$BINARY_NAME"
    mkdir -p "$install_dir" 2>/dev/null || need_sudo=1

    if [ ! -w "$install_dir" ]; then
        need_sudo=1
    fi

    if [ "$need_sudo" = "1" ]; then
        info "Installing to $final_path (sudo required)..."
        sudo cp "$tmp_file" "$final_path"
        sudo chmod +x "$final_path"
    else
        info "Installing to $final_path..."
        cp "$tmp_file" "$final_path"
        chmod +x "$final_path"
    fi
    rm -f "$tmp_file"
}

# --- Verify installation ------------------------------------------------

verify_installation() {
    local mozhi_cmd
    mozhi_cmd="$(command -v mozhi-interpreter 2>/dev/null || true)"

    if [ -z "$mozhi_cmd" ]; then
        warn "Mozhi interpreter was installed but 'mozhi-interpreter' is not on your PATH."
        warn "Open a new terminal, or run: source ~/.bashrc  (or ~/.zshrc)"
        return 0
    fi

    info "Verifying installation..."
    # The interpreter doesn't have --version, so just run it with a tiny script
    if echo 'echo "Mozhi interpreter OK"' | "$mozhi_cmd" /dev/stdin 2>/dev/null; then
        success "Mozhi interpreter is installed and working!"
    else
        # Fallback: just check the binary exists and is executable
        if [ -x "$mozhi_cmd" ]; then
            success "Mozhi interpreter installed at: $mozhi_cmd"
        else
            warn "Mozhi interpreter was installed but verification failed."
        fi
    fi

    printf '\n' >&2
    info "The interpreter is installed as 'mozhi-interpreter'." >&2
    info "Install the mozhi-pkg dispatcher ('mozhi') from:" >&2
    info "  https://github.com/crossberry-in/mozhi-pkg" >&2
    printf '\n' >&2
    info "Then use the unified 'mozhi' command:" >&2
    info "  mozhi                    # start REPL" >&2
    info "  mozhi my_script.si       # run a script" >&2
    info "  mozhi build              # build a project" >&2
    info "  mozhi test               # run tests" >&2
}

# --- Main ---------------------------------------------------------------

main() {
    printf '\n' >&2
    printf '  \033[1;36m===================================\033[0m\n' >&2
    printf '  \033[1;36m   Mozhi Language Installer\033[0m\n'     >&2
    printf '  \033[1;36m===================================\033[0m\n' >&2
    printf '\n' >&2

    local platform version asset_name install_dir tmp_file
    local os arch

    platform="$(detect_platform)"
    version="$(get_latest_version)"
    asset_name="$(asset_for_platform "$platform")"

    os="${platform%%-*}"
    arch="$(echo "$platform" | cut -d- -f2)"

    info "Detected platform: $platform"
    info "Target asset:      $asset_name"
    info "Latest version:    $version"
    printf '\n' >&2

    # Download (output to STDOUT, captured in tmp_file)
    tmp_file="$(download_binary "$asset_name" "$version")"

    install_dir="$(install_dir_for "$os" "$arch")"
    install_binary "$tmp_file" "$install_dir"

    printf '\n' >&2
    verify_installation

    printf '\n' >&2
    success "Done! Docs: https://github.com/crossberry-in/mozhi-doc" >&2
    printf '\n' >&2
}

main "$@"
