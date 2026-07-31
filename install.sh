#!/usr/bin/env bash
#
# Sino — One-line installer
#
# Usage:
#   curl -fsSL https://github.com/crossberry-in/sino-lang-docs/raw/main/install.sh | bash
#
# This script:
#   1. Detects the OS and architecture
#   2. Downloads the correct Sino binary from the latest release
#   3. Installs it to /usr/local/bin/sino (or ~/.local/bin/sino as fallback)
#   4. Verifies the installation
#
set -e

# --- Configuration ------------------------------------------------------

REPO="crossberry-in/sino-lang-docs"
INSTALL_DIR="/usr/local/bin"
FALLBACK_DIR="$HOME/.local/bin"
BINARY_NAME="sino"

# --- Helpers ------------------------------------------------------------

info()  { printf "\033[1;34m[info]\033[0m  %s\n"  "$*"; }
warn()  { printf "\033[1;33m[warn]\033[0m  %s\n"  "$*" >&2; }
error() { printf "\033[1;31m[error]\033[0m %s\n" "$*" >&2; }
success(){ printf "\033[1;32m[ok]\033[0m    %s\n"  "$*"; }

# --- Detect OS and architecture -----------------------------------------

detect_platform() {
    local os arch

    os="$(uname -s 2>/dev/null || echo unknown)"
    arch="$(uname -m 2>/dev/null || echo unknown)"

    case "$os" in
        Linux*)  os="linux"  ;;
        Darwin*) os="macos"  ;;
        *)       error "Unsupported OS: $os"; exit 1 ;;
    esac

    case "$arch" in
        x86_64|amd64)  arch="x86_64"  ;;
        aarch64|arm64) arch="arm64"   ;;
        *)             error "Unsupported architecture: $arch"; exit 1 ;;
    esac

    if [ "$os" = "macos" ]; then
        warn "Sino is built for Linux. On macOS, you must run the binary via Docker or a Linux VM."
        warn "Continuing with the Linux x86_64 binary — it will NOT run natively on macOS."
        arch="x86_64"
    fi

    echo "${os}-${arch}"
}

# --- Get the latest release version -------------------------------------

get_latest_version() {
    local version
    version="$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
        | grep '"tag_name"' \
        | sed -E 's/.*"tag_name":\s*"([^"]+)".*/\1/')"

    if [ -z "$version" ]; then
        error "Failed to determine the latest Sino release version."
        exit 1
    fi

    echo "$version"
}

# --- Download binary ----------------------------------------------------

download_binary() {
    local platform="$1"
    local version="$2"
    local asset_name

    case "$platform" in
        linux-x86_64) asset_name="sino-linux-x86_64" ;;
        linux-arm64)  asset_name="sino-linux-arm64"  ;;
        *)            error "No binary asset available for platform: $platform"; exit 1 ;;
    esac

    local download_url="https://github.com/${REPO}/releases/download/${version}/${asset_name}"
    local tmp_file="/tmp/${asset_name}"

    info "Downloading Sino $version for $platform..."
    if ! curl -fSL -o "$tmp_file" "$download_url"; then
        error "Download failed. Check your internet connection and try again."
        exit 1
    fi

    chmod +x "$tmp_file"
    echo "$tmp_file"
}

# --- Install binary -----------------------------------------------------

install_binary() {
    local tmp_file="$1"
    local target_path

    if [ -w "$INSTALL_DIR" ] || sudo -n true 2>/dev/null; then
        target_path="$INSTALL_DIR/$BINARY_NAME"
        if [ -w "$INSTALL_DIR" ]; then
            mv "$tmp_file" "$target_path"
        else
            sudo mv "$tmp_file" "$target_path"
        fi
        success "Installed to $target_path"
    else
        warn "Cannot write to $INSTALL_DIR (need sudo). Installing to $FALLBACK_DIR instead."
        mkdir -p "$FALLBACK_DIR"
        target_path="$FALLBACK_DIR/$BINARY_NAME"
        mv "$tmp_file" "$target_path"
        success "Installed to $target_path"

        case ":$PATH:" in
            *":$FALLBACK_DIR:"*) ;;
            *)
                warn "$FALLBACK_DIR is not on your PATH."
                warn "Add the following line to your ~/.bashrc or ~/.zshrc:"
                printf '\n    export PATH="%s:$PATH"\n\n' "$FALLBACK_DIR"
                ;;
        esac
    fi
}

# --- Verify installation ------------------------------------------------

verify_installation() {
    local sino_cmd
    sino_cmd="$(command -v sino || true)"

    if [ -z "$sino_cmd" ]; then
        warn "Sino installed but 'sino' is not on your PATH."
        warn "Open a new terminal or run: source ~/.bashrc"
        return 0
    fi

    info "Verifying installation..."
    if "$sino_cmd" --version 2>/dev/null; then
        success "Sino is installed and working!"
        printf '\n'
        info "Run the REPL with:    sino"
        info "Run a script with:    sino my_script.si"
    else
        warn "Sino was installed but 'sino --version' failed."
        warn "Try opening a new terminal, then run 'sino --version'."
    fi
}

# --- Main ---------------------------------------------------------------

main() {
    printf '\n'
    printf '  \033[1;36m===================================\033[0m\n'
    printf '  \033[1;36m   Sino Language Installer\033[0m\n'
    printf '  \033[1;36m===================================\033[0m\n'
    printf '\n'

    local platform version tmp_file
    platform="$(detect_platform)"
    version="$(get_latest_version)"

    info "Detected platform: $platform"
    info "Latest version:    $version"

    tmp_file="$(download_binary "$platform" "$version")"
    install_binary "$tmp_file"
    verify_installation

    printf '\n'
    success "Done! For docs, visit: https://github.com/crossberry-in/sino-lang-docs\n"
    printf '\n'
}

main "$@"
