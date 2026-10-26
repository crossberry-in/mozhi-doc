# Mozhi React Framework

A React-like framework for the Mozhi programming language with:
- **Component-based architecture** (`.mz` files)
- **Server-side rendering** (SSR)
- **Live reload** via Server-Sent Events (SSE)
- **CSS hot-swap** (no page reload for CSS changes)
- **Hash-based routing**
- **Hooks** (useState, useEffect, useMemo, useRef)
- **Dev tools** (error overlay, dev status indicator)

## Installation

Libraries auto-download on first use. No installation needed!

## Quick Start

### 1. Create a new app

```bash
mkdir my-app && cd my-app
```

### 2. Create `app.mz`

```mozhi
import http from "mozhi-http"
import react from "react.mz"

fn handler(method, path) {
    # Serve index.html with live reload
    return http.http_serve_static(path, "public")
}

server = http.http_start(3000)
http.http_serve_loop(server, handler)
```

### 3. Run

```bash
mozhi-interpreter app.mz
# Open http://127.0.0.1:3000
```

## Framework Modules

### `mozhi-react` (core)

Virtual DOM helpers and component system:

```mozhi
import react from "react.mz"

# Create elements (like React.createElement)
react.div("class=\"card\"", "Hello!")
react.h1("", "Title")
react.button("onclick=\"inc()\"", "Click Me")

# Props helpers
react.className("card")
react.props([["id", "main"], ["class", "container"]])

# Full HTML document
react.html_document("Title", "<body>...</body>", "<link...>")
```

### `react_hooks.mz`

State management hooks:

```mozhi
import hooks from "react_hooks.mz"

# useState — generate client-side state
hooks.useState("count", 0, "inc")

# useEffect — run code on load
hooks.useEffectOnLoad("console.log('loaded!');")

# Serialize state for hydration
hooks.serialize_state([["count", "0"], ["theme", "dark"]])
```

### `react_router.mz`

Hash-based routing:

```mozhi
import router from "react_router.mz"

# Create links
router.link("/about", "About Page")

# Navigation bar
router.navbar([
    ["/", "Home"],
    ["/about", "About"],
    ["/contact", "Contact"]
], "/")
```

### `react_devtools.mz`

Development tools:

```mozhi
import devtools from "react_devtools.mz"

# File watcher
devtools.init_watcher()
devtools.check_dir_changed("public", "/tmp/.mozhi_dev_marker")

# SSE responses
devtools.sse_reload()
devtools.sse_heartbeat()

# Inject live reload script
devtools.inject_reload_script(html_content)

# Dev overlay
devtools.dev_overlay("running")
devtools.error_overlay("Syntax error in components/card.mz")
```

## Creating Components

A component is a `.mz` file that outputs HTML:

```mozhi
# components/my_button.mz
import react from "react.mz"

echo(react.button(
    "class=\"btn\" onclick=\"handleClick()\"",
    "Click Me"
))
```

### Using Components

Components are loaded via `fetch()` in the browser:

```javascript
// public/app.js
async function loadComponent(name) {
    const res = await fetch('/components/' + name + '.mz');
    return res.ok ? await res.text() : '';
}

async function render() {
    const app = document.getElementById('app');
    app.innerHTML = await loadComponent('my_button');
}
render();
```

## Interactive Components

```mozhi
# components/counter.mz
import react from "react.mz"

echo(react.div(className("card"),
    react.h2("", "Counter") +
    react.p("", "Click to change the count") +
    "<button class='btn' onclick='dec()'>-</button>" +
    "<span id='count'>0</span>" +
    "<button class='btn' onclick='inc()'>+</button>" +
    "<script>
function inc() {
    var el = document.getElementById('count');
    el.textContent = parseInt(el.textContent) + 1;
}
function dec() {
    var el = document.getElementById('count');
    el.textContent = parseInt(el.textContent) - 1;
}
</script>"
))
```

## Live Reload

The dev server watches `public/`, `components/`, and `pages/` directories. When you save a file:

1. **CSS changed** → stylesheet is hot-swapped (no page reload)
2. **JS/MZ changed** → full page reload via SSE

```mozhi
# In your server handler:
if route == "/__dev_reload" {
    change_type = devtools.hmr_check()
    if change_type == "full_reload" {
        return devtools.sse_reload()
    }
    if change_type == "css_reload" {
        # Send CSS reload event
        ...
    }
    return devtools.sse_heartbeat()
}
```

## Comparison with React

| Feature | React | Mozhi React |
|---------|-------|-------------|
| Language | JSX (JS) | Mozhi (.mz) |
| Components | `.jsx` files | `.mz` files |
| Rendering | Client (VDOM) | Server (SSR) |
| Live reload | Vite HMR | SSE + smart reload |
| State | useState/hooks | Client-side JS |
| Routing | react-router | Hash-based router |
| Build step | Required | None |
| Dependencies | npm | Auto-download |

## Examples

See `examples/react-app/` for a complete working example with:
- Counter page (interactive)
- Todo list (CRUD)
- About page (static)
- Hash-based routing
- Live reload
- CSS hot-swap

## API Reference

### Core (`mozhi-react`)

| Function | Description |
|----------|-------------|
| `react.h(tag, props, children)` | Create element |
| `react.div(props, children)` | `<div>` |
| `react.h1(props, children)` | `<h1>` |
| `react.p(props, children)` | `<p>` |
| `react.button(props, children)` | `<button>` |
| `react.a(props, children)` | `<a>` |
| `react.input(props)` | `<input>` |
| `react.script(code)` | `<script>` |
| `react.style(css)` | `<style>` |
| `react.className(name)` | `class="..."` |
| `react.props(pairs)` | Build props string |
| `react.html_document(title, body, head)` | Full HTML doc |
| `react.if_else(cond, a, b)` | Conditional render |

### Hooks (`react_hooks.mz`)

| Function | Description |
|----------|-------------|
| `hooks.useState(name, val, setter)` | Client-side state |
| `hooks.useEffect(code)` | Run on load |
| `hooks.useEffectOnLoad(code)` | Run on DOMContentLoaded |
| `hooks.serialize_state(pairs)` | JSON state |
| `hooks.useRef()` | Unique ID |

### Router (`react_router.mz`)

| Function | Description |
|----------|-------------|
| `router.link(to, text)` | Navigation link |
| `router.navbar(links, active)` | Nav bar |
| `router.redirect(to)` | Redirect |

### DevTools (`react_devtools.mz`)

| Function | Description |
|----------|-------------|
| `devtools.init_watcher()` | Start file watcher |
| `devtools.hmr_check()` | Check for changes |
| `devtools.sse_reload()` | SSE reload response |
| `devtools.inject_reload_script(html)` | Add reload script |
| `devtools.dev_overlay(status)` | Status indicator |
| `devtools.error_overlay(msg)` | Error display |
