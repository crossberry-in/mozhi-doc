---
title: Install mz — manual, npm and pinned versions
description: Install the Mozhi interpreter (mozhi / mz) with curl | sh, npm, or a pinned allowed version.
---

# Install mz

Mozhi installs two identical commands: `mozhi` (full name) and `mz`
(short alias). Everything in these docs works with either one.

There are two supported ways to install:

| Method | Command | Best for |
| --- | --- | --- |
| Manual (this site) | `curl -fsSL https://mz.netlify.app/install.sh \| sh` | servers, CI, Termux, no Node.js needed |
| npm | `npm install -g @crossberryweb/mozhi` | machines already using Node.js |

## Manual install (curl \| sh)

```sh
curl -fsSL https://mz.netlify.app/install.sh | sh
```

The installer:

1. reads the version manifest served by this site (`/dist/versions.env`)
2. detects your platform — Linux (glibc), Alpine (musl static), Termux,
   macOS (x86_64 / arm64) and Windows (legacy fallback release)
3. downloads the matching `mozhi-interpreter-*` binary from this site's
   `/dist` files
4. verifies the **SHA-256 digest** before installing anything
5. installs `mozhi` and the `mz` alias, then checks your `PATH`

Install locations, in priority order: `$MOZHI_INSTALL_DIR` → Termux
`$PREFIX/bin` → `/opt/homebrew/bin` (macOS arm64) → `/usr/local/bin`
(if writable) → `~/.local/bin`.

If a **foreign** executable named `mz` already exists the installer leaves
it untouched and tells you — it never overwrites a command it did not
install.

## npm install

```sh
npm install -g @crossberryweb/mozhi
mz --version
```

The npm distribution (`@crossberryweb/mozhi`) bundles the official static
Linux x86_64 / arm64 binaries and installs the same `mozhi` command.
Both methods produce identical installs; pick whichever suits the machine.

## Latest and allowed versions

Every release listed in the manifest is an **allowed** version — verified
binaries the installer will accept. The newest one is **latest**.

```sh
# see what is available
curl -fsSL https://mz.netlify.app/install.sh | sh -s -- list

# pin an exact allowed version
curl -fsSL https://mz.netlify.app/install.sh | sh -s -- v3.7.0

# same thing through the environment (handy for CI)
MOZHI_VERSION=v3.7.0 curl -fsSL https://mz.netlify.app/install.sh | sh
```

Pinning a version that is not in the allowed list is refused, and the
error prints the current latest + allowed list. The JSON view of the same
data, including every file hash, is public:

```sh
curl -fsSL https://mz.netlify.app/api/releases
```

A version can be *allowed but not latest* — for example an older release
may be kept allowed because it carries a platform build (such as the
Windows binary) that newer releases do not have yet. The installer
resolves this automatically: it tries your requested version first, then
falls back through the allowed releases until it finds a build for your
platform, and tells you when it substituted one.

## Verify the install

```sh
mz --version
mz run hello.mz
```

`hello.mz`:

```mozhi
print("Hello from Mozhi")
```

## Update

Re-run the same command — the installer always installs the latest
allowed release unless you pin one:

```sh
curl -fsSL https://mz.netlify.app/install.sh | sh
```

For npm installs: `npm update -g @crossberryweb/mozhi`.

## Installer environment variables

| Variable | Meaning |
| --- | --- |
| `MOZHI_INSTALL_DIR` | install target directory |
| `MOZHI_VERSION` | pin the version (same as first argument) |
| `MZ_DOCS_BASE` | override the site base URL (staging mirrors) |
| `MZ_SKIP_CHECKSUM` | set to `1` to skip SHA-256 verification (not recommended) |

Checksum skipping exists only for exotic environments without a
`sha256sum`/`shasum` binary. The default is always verify.
