# Mozhi Mini-App — React-like Live Reload

A React-style development experience using Mozhi v2.4.0+ with:
- **Live reload** — edit any file and the browser auto-refreshes
- **Component-based architecture** — `.mz` files as reusable components
- **Server-side rendering** — components rendered by Mozhi on the server
- **Static file serving** — HTML, CSS, JS from `public/`

## Quick Start

### 1. Install Mozhi v2.4.0+

```bash
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/install.sh | bash
```

### 2. Run the Dev Server

```bash
cd mini-app
mozhi-interpreter dev_server.mz
```

### 3. Open in Browser

Go to **http://127.0.0.1:3000**

### 4. Start Editing

Edit any file in `public/` or `components/` — the browser will auto-reload!

## Project Structure

```
mini-app/
├── dev_server.mz          # Dev server with live reload (SSE)
├── README.md              # This file
├── components/            # Server-rendered .mz components
│   ├── header.mz          # Navigation header
│   ├── card.mz            # Reusable card component
│   ├── counter.mz         # Interactive counter (client-side JS)
│   └── footer.mz          # Footer
└── public/                # Static files
    ├── index.html         # HTML entry point
    ├── style.css          # Stylesheet
    └── app.js             # Frontend JS (loads components)
```

## How Live Reload Works

```
┌─────────────────┐     SSE      ┌──────────────────┐
│  dev_server.mz  │◄────────────►│   Browser        │
│                 │              │                  │
│ 1. Watches      │  2. Detects  │ 3. Receives      │
│    files        │    change    │    reload event  │
│                 │              │                  │
│ 4. Sends SSE    │─────────────►│ 5. Auto-refreshes│
│    reload event │              │    page          │
└─────────────────┘              └──────────────────┘
```

1. **File watcher** polls `public/` and `components/` every second
2. When a file changes, the server sends a `reload` event via SSE
3. The browser's `EventSource` receives the event and calls `location.reload()`
4. The page reloads, fetching updated components from the server

## Creating Components

A component is a `.mz` file in `components/` that outputs HTML:

```mozhi
# components/my_component.mz
import html from "mozhi-html"

echo(html.html_div("my-component",
    html.html_h2("My Component") +
    html.html_p("This is rendered by Mozhi!")
))
```

### Using a Component

In `public/app.js`, add the component to the render function:

```javascript
async function render() {
    const app = document.getElementById('app');
    const [header, myComponent, footer] = await Promise.all([
        loadComponent('header'),
        loadComponent('my_component'),  // ← add here
        loadComponent('footer')
    ]);
    app.innerHTML = header + myComponent + footer;
}
```

## Interactive Components

Components can include client-side JavaScript for interactivity:

```mozhi
# components/counter.mz
echo("
<div class=\"card counter\">
    <h2>Counter</h2>
    <button class=\"btn\" onclick=\"inc()\">+</button>
    <span id=\"count\">0</span>
    <button class=\"btn\" onclick=\"dec()\">-</button>
</div>
<script>
function inc() { /* ... */ }
function dec() { /* ... */ }
</script>
")
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | HTML page (with live-reload script injected) |
| `GET /style.css` | CSS stylesheet |
| `GET /app.js` | Frontend JavaScript |
| `GET /components/<name>.mz` | Render a component (returns HTML) |
| `GET /__dev_reload` | SSE stream for live reload events |
| `GET /__dev_status` | Dev server status (JSON) |

## Customization

### Change the Port

Edit `dev_server.mz`:
```mozhi
server = http.http_start(4000)  # use port 4000
```

### Add More Watched Directories

Edit the `check_changes()` function in `dev_server.mz`:
```mozhi
result = run("find public components lib src -type f ...")
```

### Disable Live Reload

Remove or comment out the reload script injection in `dev_server.mz` (the `reload_script` variable).

## Production Build

For production, use a regular static server (no live reload):

```bash
# Build components to static HTML
mozhi-interpreter build.mz  # (you'd need to create this)

# Serve with Python
python3 -m http.server 8080 --directory public
```

## Requirements

- **Mozhi v2.4.0+** (for `import`, `run()`, `http_serve_static()`, file I/O)
- **bash** (for file watching via `find`)
- **Internet access** (first run, to auto-download `mozhi-http` and `mozhi-html` libraries)

## Comparison with React

| Feature | React | Mozhi Mini-App |
|---------|-------|----------------|
| Components | `.jsx` files | `.mz` files |
| Rendering | Client-side (VDOM) | Server-side (string concat) |
| Live reload | Vite/webpack HMR | SSE + `location.reload()` |
| State | useState/hooks | Client-side JS |
| Styling | CSS-in-JS / CSS modules | Plain CSS |
| Build step | Required (Babel) | None (interpreted) |
| Dependencies | npm install | Auto-download on import |

## Links

- [Mozhi Documentation](https://crossberry-in.github.io/mozhi-doc/)
- [Mozhi Libraries](https://crossberry-in.github.io/mozhi-doc/libs.html)
- [More Examples](https://github.com/crossberry-in/mozhi-doc/tree/main/examples)
