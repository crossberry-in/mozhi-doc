# Sino — Installation Guide

This guide walks you through installing the Sino interpreter on Linux, macOS, and Windows.

---

## System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Linux x86_64 (kernel 3.2+) | Ubuntu 20.04+ / Debian 11+ |
| Architecture | x86_64 (64-bit) | x86_64 |
| RAM | 16 MB free | 64 MB free |
| Disk | 1 MB free | 10 MB free |
| Dependencies | `libc` (glibc 2.17+), `libm` | Same |

Sino is shipped as a single statically-linked-friendly ELF binary. No additional runtime libraries are required beyond the standard C library already present on most Linux systems.

---

## Method 1: Direct Download (Recommended)

### Step 1 — Download the binary

Go to the [Releases page](https://github.com/crossberry-in/sino-lang-docs/releases) and download the latest `sino-linux-x86_64` binary.

Or use `curl` from the terminal:

```bash
# Replace v1.0.0 with the latest version from the Releases page
curl -L -o sino https://github.com/crossberry-in/sino-lang-docs/releases/download/v1.0.0/sino-linux-x86_64
```

### Step 2 — Make it executable

```bash
chmod +x sino
```

### Step 3 — Move it to a directory on your PATH

For a system-wide installation (requires `sudo`):

```bash
sudo mv sino /usr/local/bin/sino
```

For a user-local installation (no `sudo` needed):

```bash
mkdir -p ~/.local/bin
mv sino ~/.local/bin/sino

# Make sure ~/.local/bin is on your PATH (add to ~/.bashrc or ~/.zshrc)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Step 4 — Verify the installation

```bash
sino --version
```

You should see output similar to:

```
Sino Interpreter v1.0.0
```

If you see `command not found`, your `PATH` does not include the install location. Re-open your terminal or run `source ~/.bashrc` / `source ~/.zshrc`.

---

## Method 2: One-Line Install Script

For convenience, you can install Sino with a single command:

```bash
curl -fsSL https://github.com/crossberry-in/sino-lang-docs/raw/main/install.sh | bash
```

This script will:

1. Detect your OS and architecture
2. Download the correct binary from the latest release
3. Place it in `/usr/local/bin/sino` (may prompt for `sudo`)
4. Verify the installation

---

## Method 3: Manual Build from Source (Not Publicly Available)

> ⚠️ **Note:** The Sino source code is **closed-source**. Public builds are not supported. If you need a build for a platform not listed under [Supported Platforms](README.md#supported-platforms), please [open an issue](https://github.com/crossberry-in/sino-lang-docs/issues).

If you are a maintainer with access to the private source repository, you can build Sino as follows:

```bash
git clone https://github.com/crossberry-in/sino-lang.git
cd sino-lang
make
# Binary will be at bin/sino
```

Requirements for building from source:

- `gcc` 4.8+ (or any C99-compliant compiler)
- `make`
- `libc` development headers
- `libm` (math library)

---

## Platform-Specific Notes

### Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y curl ca-certificates
# Then follow Method 1 or Method 2 above
```

### Fedora / RHEL / CentOS

```bash
sudo dnf install -y curl
# Then follow Method 1 or Method 2 above
```

### Arch Linux

```bash
sudo pacman -S --needed curl
# Then follow Method 1 or Method 2 above
```

### macOS (Community)

Sino is built for Linux. On macOS, you can:

1. Run the Linux binary via **Docker**:

   ```bash
   docker run --rm -it -v "$PWD":/work -w /work ubuntu:22.04 \
     bash -c "apt update && apt install -y curl && \
     curl -fsSL https://github.com/crossberry-in/sino-lang-docs/raw/main/install.sh | bash && sino"
   ```

2. Or use a **Linux VM** (UTM, Parallels, VirtualBox).

### Windows (via WSL)

Sino runs natively on Linux. On Windows 10/11, you can use the Windows Subsystem for Linux:

```powershell
# In PowerShell as Administrator
wsl --install -d Ubuntu
```

Once WSL is set up, open the Ubuntu terminal and follow Method 1 or Method 2 above.

---

## Upgrading

To upgrade Sino to a newer version, simply repeat the installation steps. The new binary will overwrite the old one.

To check your current version:

```bash
sino --version
```

---

## Uninstalling

To remove Sino from your system:

```bash
# If installed system-wide
sudo rm /usr/local/bin/sino

# If installed user-locally
rm ~/.local/bin/sino
```

That's it — Sino stores no configuration files or caches outside the binary itself.

---

## Troubleshooting

### `bash: sino: command not found`

The binary is not on your `PATH`. Verify with:

```bash
which sino
echo $PATH
```

If `which sino` returns nothing, the binary is not in any directory listed in `$PATH`. Move it (see [Step 3](#step-3--move-it-to-a-directory-on-your-path)) or add its directory to `PATH`.

### `cannot execute binary file: Exec format error`

You downloaded a binary for the wrong architecture. Check your architecture:

```bash
uname -m
```

- `x86_64` → use `sino-linux-x86_64`
- `aarch64` or `arm64` → ARM64 build (community-supported; please open an issue)

### `Permission denied`

The binary is not marked executable. Run:

```bash
chmod +x /path/to/sino
```

### `error while loading shared libraries: libm.so.6`

Your `libm` library is missing. On Debian/Ubuntu, install it with:

```bash
sudo apt install -y libc6
```

---

## Verify the Installation

After installation, run the following smoke test to make sure Sino works:

```bash
echo 'echo "Sino is working!"' > /tmp/test.si
sino /tmp/test.si
```

Expected output:

```
Sino is working!
```

If you see this output, you're ready to start coding in Sino! Head over to the [Usage Guide](USAGE.md) to learn more.

---

## Need Help?

- 🐛 **Bug reports:** [Open an issue](https://github.com/crossberry-in/sino-lang-docs/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/crossberry-in/sino-lang-docs/discussions)
- 📖 **Documentation:** [Usage Guide](USAGE.md) | [Language Reference](LANGUAGE_REFERENCE.md)
