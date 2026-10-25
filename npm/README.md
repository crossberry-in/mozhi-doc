# Mozhi (official npm distribution)

**Mozhi** (மொழி — "language" in Tamil) is a fast, beginner-friendly scripting language with a **native full-stack platform**: HTTP server, template engine, JSON stack, sandboxed filesystem and SQLite — all built into the interpreter, zero external runtimes.

This package installs the official `mozhi` command with a **prebuilt, fully static Linux binary** bundled inside — no compilation, no postinstall downloads, works offline behind any proxy.

## Install

```bash
npm install -g @crossberryweb/mozhi

# then:
mozhi --version
```

Bundled platforms (v3.1.1, static musl binaries with SQLite vendored):

| Platform | Binary |
|----------|--------|
| Linux x86_64 | bundled |
| Linux arm64 (aarch64, incl. Android/Termux chroots) | bundled |
| macOS / Windows | use the [installer script](https://github.com/crossberry-in/mozhi-doc#installation) instead |

The binaries are fully static, so one build serves glibc distros (Ubuntu/Debian/Fedora/Arch), Alpine/musl, and Termux alike.

## Quick start

`hello.mz`
```mozhi
let name = "Mozhi"
echo("Hello from " + name + "!")

fn fib(n) {
    if n < 2 {
        return n
    }
    return fib(n - 1) + fib(n - 2)
}
echo("fib(10) = " + string(fib(10)))
```

```bash
mozhi run hello.mz      # or simply: mozhi hello.mz
```

**Full-stack web app** — `app.mz`:
```mozhi
import web

let app = web.create({
    log: true
})

app.get("/", fn(req, res) {
    return res.html("<h1>Hello from Mozhi</h1>")
})

app.get("/api/health", fn(req, res) {
    return res.json({
        status: "ok",
        language: "Mozhi",
        version: web.version()
    })
})

app.listen("127.0.0.1", 8080)
```

```bash
mozhi run app.mz
# then: curl http://127.0.0.1:8080/api/health
```

## What's inside

- `bin/mozhi-linux-x86_64`, `bin/mozhi-linux-arm64` — official v3.1.1 interpreter binaries, sha256-verified against the [v3.1.1 release](https://github.com/crossberry-in/mozhi-doc/releases/tag/v3.1.1)
- `bin/mozhi.js` — tiny launcher that picks the right binary and forwards arguments, stdio, exit codes and signals

Versioning: the npm package version always matches the bundled interpreter release (package 3.1.1 = Mozhi v3.1.1).

## Docs

- [Documentation site](https://crossberry-in.github.io/mozhi-doc/)
- [Web Server Guide](https://github.com/crossberry-in/mozhi-doc/blob/main/docs/WEB_GUIDE.md)
- [Language Reference](https://github.com/crossberry-in/mozhi-doc/blob/main/LANGUAGE_REFERENCE.md)
- [Examples](https://github.com/crossberry-in/mozhi-doc/tree/main/examples)

## License

Mozhi is proprietary (closed-source interpreter, publicly released binaries). This package redistributes **unmodified official release binaries** as permitted by the bundled [LICENSE](./LICENSE) (§3c "verbatim copies"). By installing you accept its terms.
