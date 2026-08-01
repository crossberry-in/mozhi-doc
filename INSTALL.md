# Mozhi — Installation Guide

Mozhi runs on **Linux**, **macOS**, **Windows**, and **Termux** (Android). The installer auto-detects your platform and architecture, so in most cases you can install with a single command.

---

## Table of Contents

- [Quick Install](#quick-install)
- [System Requirements](#system-requirements)
- [Supported Platforms](#supported-platforms)
- [Platform-Specific Guides](#platform-specific-guides)
  - [Linux (Ubuntu / Debian / Fedora / Arch)](#linux-ubuntu--debian--fedora--arch)
  - [Alpine Linux](#alpine-linux)
  - [Termux (Android)](#termux-android)
  - [macOS (Intel and Apple Silicon)](#macos-intel-and-apple-silicon)
  - [Windows 10/11](#windows-1011)
  - [Windows Subsystem for Linux (WSL)](#windows-subsystem-for-linux-wsl)
- [Manual Installation](#manual-installation)
- [Upgrading](#upgrading)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)

---

## Quick Install

### Linux / macOS / WSL / Termux

```bash
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

The installer:

1. Detects your OS (Linux, macOS, Termux), architecture (x86_64 or ARM64), and libc (glibc or musl)
2. Downloads the correct binary from the latest release
3. Installs it to a directory on your `PATH` (`/usr/local/bin`, `$PREFIX/bin` for Termux, `/opt/homebrew/bin` for Apple Silicon, or `~/.local/bin` as fallback)
4. Verifies the installation

### Windows (PowerShell)

```powershell
irm https://github.com/crossberry-in/mozhi-doc/raw/main/install.ps1 | iex
```

The PowerShell installer:

1. Downloads `mozhi-windows-x86_64.exe` from the latest release
2. Installs it to `%USERPROFILE%\.mozhi\bin\mozhi.exe`
3. Adds `%USERPROFILE%\.mozhi\bin` to your user `PATH`
4. Verifies the installation

> Open a **new** PowerShell window after installation for `mozhi` to be on your `PATH`.

---

## System Requirements

| Platform | Minimum OS | Architecture | Disk | RAM |
|----------|-----------|--------------|------|-----|
| Linux (glibc) | Kernel 2.0+ (any distro from ~2014+) | x86_64 or ARM64 | 1 MB | 16 MB |
| Linux (musl/Alpine) | Alpine 3.x | x86_64 or ARM64 | 1 MB | 16 MB |
| Termux | Android 7.0+ | ARM64 or x86_64 | 1 MB | 16 MB |
| macOS | 10.14 Mojave or later | x86_64 or ARM64 | 1 MB | 16 MB |
| Windows | Windows 10 (1809+) or Windows 11 | x86_64 | 1 MB | 16 MB |

The glibc Linux builds dynamically link against `libc` and `libm` (already present on every Linux distro). The Alpine, Termux, and Windows builds are statically linked — they have **no runtime dependencies**.

---

## Supported Platforms

| Platform | Architecture | Libc | Asset name | Build type |
|----------|--------------|------|------------|-----------|
| Linux (Ubuntu, Debian, Fedora, Arch) | x86_64 | glibc | `mozhi-linux-x86_64` | Dynamic |
| Linux (Raspberry Pi 4/5, ARM servers) | ARM64 (aarch64) | glibc | `mozhi-linux-arm64` | Dynamic |
| Alpine Linux | x86_64 | musl | `mozhi-alpine-x86_64` | **Static** |
| Alpine Linux | ARM64 | musl | `mozhi-alpine-arm64` | **Static** |
| Termux on Android | ARM64 | bionic | `mozhi-alpine-arm64` | **Static** |
| Termux on Android | x86_64 | bionic | `mozhi-alpine-x86_64` | **Static** |
| macOS (Intel) | x86_64 | Darwin | `mozhi-macos-x86_64` | Dynamic |
| macOS (Apple Silicon M1/M2/M3/M4) | ARM64 | Darwin | `mozhi-macos-arm64` | Dynamic |
| Windows 10/11 | x86_64 | MSVCRT | `mozhi-windows-x86_64.exe` | Static |

> Termux uses the static musl build because Android's bionic libc is not API-compatible with glibc or musl. Static musl binaries run natively on the Linux kernel that Android uses — no `proot` needed.

---

## Platform-Specific Guides

### Linux (Ubuntu / Debian / Fedora / Arch)

```bash
# One-line install
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

If `curl` is not installed:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install -y curl

# Fedora / RHEL / CentOS
sudo dnf install -y curl

# Arch Linux
sudo pacman -S --needed curl
```

After install, verify:

```bash
mozhi --version
```

### Alpine Linux

Alpine uses `musl` libc by default. The installer detects this and downloads the static musl binary (`mozhi-alpine-*`).

```bash
# Install curl if not present
apk add --no-cache curl

# Install Mozhi
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

Verify:

```bash
mozhi --version
```

### Termux (Android)

Termux runs on Android, which uses Bionic libc. The installer detects Termux and downloads the static musl binary, which runs natively on the Android kernel — **no `proot` or `proot-distro` needed**.

```bash
# Make sure curl is installed
pkg install -y curl

# Install Mozhi
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

Mozhi will be installed to `$PREFIX/bin/mozhi` (typically `/data/data/com.termux/files/usr/bin/mozhi`), which is already on your Termux `PATH`. No `sudo` is needed — you own that directory.

Verify:

```bash
mozhi --version
```

### macOS (Intel and Apple Silicon)

```bash
# Install via Homebrew (if you have brew)
brew install curl

# Or use the system curl (preinstalled on macOS)
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

The installer:

- On **Apple Silicon** (M1/M2/M3/M4), installs to `/opt/homebrew/bin` if it exists, otherwise `/usr/local/bin`, otherwise `~/.local/bin`
- On **Intel** Macs, installs to `/usr/local/bin`, otherwise `~/.local/bin`
- Downloads `mozhi-macos-arm64` for Apple Silicon or `mozhi-macos-x86_64` for Intel

Verify:

```bash
mozhi --version
```

> **Note on macOS Gatekeeper:** The first time you run `mozhi`, macOS may show a security prompt saying "Mozhi cannot be opened because the developer cannot be verified." Right-click the binary in Finder and select **Open** to whitelist it, or run:
>
> ```bash
> xattr -d com.apple.quarantine /path/to/mozhi
> ```

### Windows 10/11

#### Option A: Native Windows (recommended for casual use)

Open **PowerShell** (Windows 10 1809+ or Windows 11) and run:

```powershell
irm https://github.com/crossberry-in/mozhi-doc/raw/main/install.ps1 | iex
```

The installer:

1. Downloads `mozhi-windows-x86_64.exe`
2. Installs it to `%USERPROFILE%\.mozhi\bin\mozhi.exe`
3. Adds `%USERPROFILE%\.mozhi\bin` to your user `PATH`

Open a **new** PowerShell window after install, then verify:

```powershell
mozhi --version
```

#### Option B: Windows Subsystem for Linux (WSL)

If you prefer the Linux workflow, install [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and follow the [Linux install instructions](#linux-ubuntu--debian--fedora--arch) inside your WSL terminal.

```powershell
# In PowerShell as Administrator
wsl --install -d Ubuntu
```

Then in the Ubuntu terminal:

```bash
curl -fsSL https://github.com/crossberry-in/mozhi-doc/raw/main/install.sh | bash
```

### Windows Subsystem for Linux (WSL)

Follow the [Linux (Ubuntu / Debian / Fedora / Arch)](#linux-ubuntu--debian--fedora--arch) guide inside your WSL terminal. The installer will detect `linux-x86_64-gnu` (or `linux-arm64-gnu` on ARM Windows) and install the appropriate Linux binary.

---

## Manual Installation

If the installer doesn't work for you, you can install Mozhi manually.

### Step 1 — Download the binary

Go to the [Releases page](https://github.com/crossberry-in/mozhi-doc/releases) and download the correct binary for your platform:

| Your platform | Download this asset |
|---------------|---------------------|
| Ubuntu / Debian / Fedora / Arch (x86_64) | `mozhi-linux-x86_64` |
| Raspberry Pi 4/5, ARM servers | `mozhi-linux-arm64` |
| Alpine Linux (x86_64) | `mozhi-alpine-x86_64` |
| Alpine Linux (ARM64) | `mozhi-alpine-arm64` |
| Termux on Android (arm64) | `mozhi-alpine-arm64` |
| Termux on Android (x86_64) | `mozhi-alpine-x86_64` |
| macOS Intel | `mozhi-macos-x86_64` |
| macOS Apple Silicon | `mozhi-macos-arm64` |
| Windows 10/11 x86_64 | `mozhi-windows-x86_64.exe` |

Or download from the command line:

```bash
# Example: Linux x86_64
curl -L -o mozhi https://github.com/crossberry-in/mozhi-doc/releases/download/v1.0.0/mozhi-linux-x86_64
```

### Step 2 — Make it executable (Linux / macOS / Termux only)

```bash
chmod +x mozhi
```

(On Windows, skip this step.)

### Step 3 — Move it to a directory on your PATH

```bash
# System-wide (Linux/macOS, requires sudo)
sudo mv mozhi /usr/local/bin/mozhi

# User-local (no sudo)
mkdir -p ~/.local/bin
mv mozhi ~/.local/bin/mozhi
# Make sure ~/.local/bin is on your PATH (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For Termux, no `sudo` is needed:

```bash
mv mozhi $PREFIX/bin/mozhi
```

For Windows, move `mozhi-windows-x86_64.exe` to `%USERPROFILE%\.mozhi\bin\mozhi.exe` and add that directory to your `PATH`:

```powershell
mkdir "$env:USERPROFILE\.mozhi\bin"
move mozhi-windows-x86_64.exe "$env:USERPROFILE\.mozhi\bin\mozhi.exe"
$env:Path += ";$env:USERPROFILE\.mozhi\bin"
# Make permanent:
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";$env:USERPROFILE\.mozhi\bin", "User")
```

### Step 4 — Verify

```bash
mozhi --version
```

---

## Upgrading

To upgrade Mozhi to a newer version, simply re-run the install command. The new binary will overwrite the old one.

To check your current version:

```bash
mozhi --version
```

---

## Uninstalling

To remove Mozhi from your system:

```bash
# Linux / macOS (system-wide)
sudo rm /usr/local/bin/mozhi

# Linux / macOS (user-local)
rm ~/.local/bin/mozhi

# Termux
rm $PREFIX/bin/mozhi
```

On Windows:

```powershell
Remove-Item "$env:USERPROFILE\.mozhi\bin\mozhi.exe" -Force
# Optionally remove the directory:
Remove-Item "$env:USERPROFILE\.mozhi" -Recurse -Force
```

That's it — Mozhi stores no configuration files or caches outside the binary itself.

---

## Troubleshooting

### `bash: mozhi: command not found`

The binary is not on your `PATH`. Verify with:

```bash
which mozhi
echo $PATH
```

If `which mozhi` returns nothing, the binary is not in any directory listed in `$PATH`. Move it (see [Step 3](#step-3--move-it-to-a-directory-on-your-path)) or add its directory to `PATH`.

### `cannot execute binary file: Exec format error`

You downloaded a binary for the wrong architecture. Check your architecture:

```bash
uname -m
```

- `x86_64` → use `mozhi-linux-x86_64`, `mozhi-alpine-x86_64`, `mozhi-macos-x86_64`, or `mozhi-windows-x86_64.exe`
- `aarch64` or `arm64` → use `mozhi-linux-arm64`, `mozhi-alpine-arm64`, or `mozhi-macos-arm64`

### `Permission denied`

The binary is not marked executable. Run:

```bash
chmod +x /path/to/mozhi
```

### `error while loading shared libraries: libm.so.6` (Linux glibc only)

Your `libm` library is missing. On Debian/Ubuntu:

```bash
sudo apt install -y libc6
```

On Fedora/RHEL:

```bash
sudo dnf install -y glibc
```

If you're on Alpine Linux or Termux, you should be using the static musl build (`mozhi-alpine-*`) instead of the glibc build.

### `mv: cannot stat '...': No such file or directory` during install

This was a bug in early versions of `install.sh` where `info` messages polluted the `tmp_file` variable. The bug is fixed in the current version — please re-download and re-run the install command.

### `mozhi --version` returns nothing or fails on macOS

macOS Gatekeeper may be blocking the binary. Run:

```bash
xattr -d com.apple.quarantine /usr/local/bin/mozhi
# or wherever you installed it
```

Or right-click the binary in Finder, select **Open**, and confirm the security prompt.

### `mozhi` works but the install script printed errors

The install script is defensive — even if some checks print warnings, the binary may have installed successfully. Run `mozhi --version` to verify. If it works, you're good.

### Termux: `No such file or directory` when running `mozhi`

This usually means you accidentally downloaded the glibc binary (which won't run on Android's bionic). Re-run the installer — it should download `mozhi-alpine-arm64` (static musl), which works on Termux natively.

---

## Verify the Installation

After installation, run the following smoke test to make sure Mozhi works:

```bash
echo 'echo "Mozhi is working!"' > /tmp/test.si
mozhi /tmp/test.si
```

Expected output:

```
Mozhi is working!
```

If you see this output, you're ready to start coding in Mozhi! Head over to the [Usage Guide](USAGE.md) to learn more.

---

## Need Help?

- 🐛 **Bug reports:** [Open an issue](https://github.com/crossberry-in/mozhi-doc/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/crossberry-in/mozhi-doc/discussions)
- 📖 **Documentation:** [Usage Guide](USAGE.md) | [Language Reference](LANGUAGE_REFERENCE.md)
