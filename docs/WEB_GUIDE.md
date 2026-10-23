# Mozhi Web Server Guide (v3.0)

Mozhi ships a native HTTP server, HTML template engine, JSON stack,
sandboxed filesystem, and SQLite database — all implemented inside the
interpreter's C runtime. No PHP, Python, Node.js, or external processes are
involved at any point.

> **Status:** Stable for development and internal tools. Marked experimental
> for heavy production use until keep-alive and TLS land (see
> "Known limitations" at the end).

## Quick start

```bash
mozhi new myapp --template web
cd myapp
mozhi dev            # auto-reload on change
```

Open http://127.0.0.1:8080. The scaffold already contains a rendered page,
a health endpoint, a calculation endpoint, tests, and a mozhi.toml.

## The web module

```mozhi
import web

let app = web.create({
    read_timeout: 15,        # seconds per request read
    body_limit: 1048576,     # max request body (bytes)
    log: true                # request logging to stdout
})

app.get("/", fn(req, res) {
    return res.html("<h1>Welcome to Mozhi</h1>")
})

app.get("/api/health", fn(req, res) {
    return res.json({ status: "ok", language: "Mozhi" })
})

app.listen("127.0.0.1", 8080)   # blocks until shutdown
```

### Server methods

| Method | Purpose |
|--------|---------|
| `app.get/post/put/patch/delete/options/head(path, handler)` | Register a route |
| `app.use(handler)` | Add middleware: `fn(req, res, next)` — call `next()` to continue |
| `app.static(root)` | Serve static files from a directory (mounted at `/`) |
| `app.views(root)` | Set the template root used by `res.render` |
| `app.config(map)` | Update `read_timeout`, `body_limit`, `log`, `host`, `port` |
| `app.listen(host, port[, opts])` | Bind and serve — blocks; returns after graceful stop |
| `app.shutdown()` | Stop the accept loop (from a handler or another goroutine) |
| `app.not_found(handler)` | Custom 404: `fn(req, res)` |
| `app.error(handler)` | Custom 500: `fn(req, res, errorMessage)` |

### The request object

| Call | Returns |
|------|---------|
| `req.method` / `req.path` / `req.query_string` / `req.ip` | Request properties |
| `req.json()` | Parsed JSON body (map/array/…) — errors on malformed input |
| `req.body()` | Raw body string |
| `req.form()` | urlencoded body as a map (requires form content type) |
| `req.header(name)` | One header value (or null) |
| `req.headers()` | All headers as a map |
| `req.param(name)` | Route parameter (`/users/:id` → `req.param("id")`) |
| `req.query(name)` | Query parameter; `req.query()` returns all as a map |
| `req.cookie(name)` | Request cookie value |

### The response object

All methods are chainable and record state on the response; the handler's
return value is not required to be the response object (returning it is
idiomatic).

| Call | Purpose |
|------|---------|
| `res.html(body)` | HTML response (Content-Type: text/html) |
| `res.text(body)` | Plain text |
| `res.json(value)` | Any Mozhi value serialized to JSON |
| `res.status(code)` | Set the status code (default 200) |
| `res.header(name, value)` | Set a response header |
| `res.cookie(name, value[, opts])` | Set-Cookie; opts: `max_age`, `path`, `domain`, `http_only`, `secure` |
| `res.render(template[, data])` | Render a template from the views root |
| `res.redirect(url[, code])` | 302 (or 3xx) redirect |
| `res.send(body)` | Raw body with octet-stream type |

### Routing

- Patterns are matched by path segment. `:name` captures one segment,
  `*name` captures the rest of the path.
- Precedence: exact segments > parameters > wildcards; ties broken by
  registration order.
- `HEAD` requests are served by `GET` handlers with the body omitted.
- `OPTIONS` on an unregistered path responds `204` with an `Allow` header
  listing the methods registered for that path.

```mozhi
app.get("/users/:id", fn(req, res) {
    return res.json({ id: req.param("id") })
})
app.get("/files/*path", fn(req, res) {
    return res.text("serving " + req.param("path"))
})
```

### Static files

```mozhi
app.static("public")     # /style.css -> public/style.css
```

- Directory requests try `index.html`.
- Path traversal (`..`) and symlinks escaping the root are rejected.
- Common MIME types are built in; unknown types use
  `application/octet-stream`. Files are capped at 64 MB.

### Middleware

```mozhi
app.use(fn(req, res, next) {
    let started = clock_ms()
    next()                        # run the rest of the chain
    echo(req.method + " " + req.path + " took " + (clock_ms() - started) + "ms")
})
```

Middleware runs in registration order. If a middleware errors, the 500
handler runs. Middleware only wraps *routed* requests — auto-OPTIONS and
static files bypass it.

### Error handling and safety defaults

- Handler/middleware errors are logged to the server's stderr **with full
  detail**, while clients receive a generic `500` page — internal messages,
  stack data, or secrets never reach the client.
- Oversized bodies get `413`; chunked request bodies get `501`; malformed
  request lines get `400`.
- Response header values are sanitized; cookie names/values reject
  control characters (header-injection guard).

### Graceful shutdown

`Ctrl-C` (SIGINT/SIGTERM) stops the accept loop, drains in-flight requests
(up to 10 s), and returns control to the script after `app.listen`.
`mozhi dev` uses the same mechanism to restart the app on file changes.

## Template engine

Templates live under the views root (`app.views("views")` or `MOZHI_VIEWS`).

```html
<!DOCTYPE html>
<html>
<head><title>{{ title }}</title></head>
<body>
    {% for note in notes %}
        <li>{{ note.title }} — {{ note.created_at }}</li>
    {% endfor %}
    {% if note_count == 0 %}<p>No notes.</p>{% else %}<p>{{ note_count }} notes</p>{% endif %}
    {% include "partials/footer.html" %}
</body>
</html>
```

Syntax:

- `{{ expr }}` — output, **HTML-escaped by default**
- `{{{ expr }}}` — output, unescaped (use only with trusted content)
- `{% if %} / {% elif %} / {% else %} / {% endif %}`
- `{% for name in expr %} … {% endfor %}` — arrays iterate elements, maps
  iterate keys; `loop.index` (1-based), `loop.first`, `loop.last` available
- `{% include "path.html" %}` — relative to the views root
- `{% extends "base.html" %}` + `{% block name %} … {% endblock %}` — layout
  inheritance (one level)
- `{% set name = expr %}` — template-local variable
- `{# comment #}` — stripped

Filters: `{{ name | upper }}`, `lower`, `trim`, `length`, `default(value)`,
`escape`, `json`, and `| safe` (disables escaping for that expression).

**Security model.** Template expressions are evaluated by a tiny internal
evaluator over the data map you pass: literals, dotted paths, indexing,
arithmetic/comparison/logic, and a fixed filter list. There are no function
calls and no host access — an untrusted template cannot execute arbitrary
code. Missing variables render as empty strings (enable
`template.strict(true)` to turn them into errors). Template paths that
contain `..` or absolute paths are rejected.

Parsed templates are cached in memory keyed by file + mtime; `mozhi dev`
reloads them automatically when files change.

## JSON

```mozhi
import json

let data = { name: "Mozhi", tags: ["web", "db"], nested: { ok: true } }
let text = json.stringify(data)
let back = json.parse(text)
back.tags.len()          # 2
```

- `json.parse(text)` — strict RFC 8259 parser: strings with escapes and
  `\uXXXX` (incl. surrogate pairs), numbers, arrays, objects. Duplicate
  keys: last wins. Depth-limited (128) against stack exhaustion. Malformed
  input raises an error with the byte position.
- `json.stringify(value)` / `json.stringify_pretty(value, indent)` — maps,
  arrays, strings, numbers, booleans, null. Functions/natives raise an error.
- `json.validate(text)` — `{ valid, error, position }` without raising.

## Math

```mozhi
import math

math.pi  math.e  math.tau
math.sqrt(16)                    # 4
math.pow(2, 10)                  # 1024
math.round(3.14159, 2)           # 3.14
math.min([3, 1, 2])              # 1    (array or varargs)
math.max(3, 1, 2)                # 3
math.sum([1, 2, 3])              # 6
math.average([2, 4, 6])          # 4
math.random()                    # [0,1) — xorshift64*, seedable
math.random_int(1, 6)            # inclusive, no modulo bias
math.safe_div(10, 0)             # null (documented safe division)
```

Error policy: domain errors (`sqrt(-1)`, `log(0)`) and overflow raise
runtime errors — math functions never return NaN/Infinity. `math.random()`
is **not** cryptographically secure.

## Filesystem (`fs`) and the sandbox

```mozhi
import fs

fs.read(path)  fs.write(path, content)  fs.append(path, content)
fs.exists(path)  fs.list(path)  fs.mkdir(path)      # creates parents
fs.remove(path)        # files and empty dirs only
fs.remove(path, true)  # recursive (explicit opt-in, symlink-safe)
fs.stat(path)          # { name, type, size, modified }
fs.set_root(path)  fs.get_root()
```

Every path is resolved against the sandbox root (the process working
directory at startup). `..` components are rejected; symlinks are verified
with `realpath()` so links cannot escape the sandbox. `fs.list` returns
maps: `{ name, type: "file"|"dir", size }`.

## Database (`db`)

```mozhi
import db

let conn = db.connect({ driver: "sqlite", path: "data/app.db" })

# parameterized queries — user input NEVER goes into the SQL string
let rows = conn.query("SELECT id, name FROM users WHERE active = ?", [true])

let info = conn.exec("INSERT INTO users (name) VALUES (?)", ["Ada"])
info.affected_rows      # 1
info.last_insert_id     # 1

conn.begin()
conn.exec("UPDATE accounts SET balance = balance - 10 WHERE id = ?", [1])
conn.exec("UPDATE accounts SET balance = balance + 10 WHERE id = ?", [2])
conn.commit()           # or conn.rollback()

# tracked migrations (runs each entry once, in a transaction each)
conn.migrate([
    { name: "001_users", sql: "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)" }
])

conn.close()
```

- Only the `sqlite` driver exists today; the `db.connect` config map keeps
  the door open for future drivers.
- Values bind through prepared statements: null, int, float, string, bool.
- Results: `query` returns an array of maps keyed by column name;
  `exec` returns `{ affected_rows, last_insert_id }`.
- `conn.migrate` records applied names in the `_mozhi_migrations` table.
- The SQLite file may live anywhere inside the fs sandbox; `:memory:` is
  supported for tests.

## Project configuration (mozhi.toml)

```toml
[project]
name = "mozhi-web"
version = "1.0.0"
entry = "main.mz"

[server]
host = "127.0.0.1"
port = 8080
read_timeout = 15
body_limit = 1048576

[paths]
public = "public"
views = "views"
data = "data"
```

`mozhi dev`, `mozhi serve`, and `mozhi build` read this file. The server
section provides defaults which `MOZHI_HOST`/`MOZHI_PORT` environment
variables and `--host`/`--port` CLI flags override.

## CLI commands

| Command | Purpose |
|---------|---------|
| `mozhi` | REPL |
| `mozhi run file.mz` / `mozhi file.mz` | Run a script |
| `mozhi new <name> --template web\|minimal` | Scaffold a project |
| `mozhi dev` | Run the project with auto-reload (entry, mozhi.toml, views) |
| `mozhi serve [--host H] [--port P]` | Run without auto-reload |
| `mozhi test [dir]` | Run `*.test.mz` files; exit code = failures |
| `mozhi fmt [path]` | Re-indent `.mz` files (string/comment aware) |
| `mozhi lint [path]` | Parse checks + `=`-in-`if` warning |
| `mozhi build [--release]` | Verify all imports resolve; emit `dist/<name>.mz` bundle |

## Known limitations

- HTTP/1.1 with `Connection: close` (no keep-alive pooling yet); TLS is not
  built in — put a reverse proxy in front for HTTPS.
- Chunked *request* bodies are rejected with 501 (chunked responses from
  upstreams are handled by the HTTP client).
- SQLite is the only database driver.
- Integers are 32-bit in the interpreter.
- The server processes one Mozhi handler at a time (global interpreter
  lock); socket I/O and slow clients are handled on worker threads.
