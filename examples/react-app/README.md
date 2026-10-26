# Mozhi React App — Example

A complete React-like app built with the Mozhi React framework.

## Quick Start

```bash
# Install Mozhi v2.4.0+
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/install.sh | bash

# Run the app
cd examples/react-app
mozhi-interpreter app.mz

# Open http://127.0.0.1:3000
```

## Features

- **Live reload** — edit any `.mz`, `.css`, or `.js` file and the browser auto-refreshes
- **CSS hot-swap** — CSS changes don't trigger full page reload
- **Component-based** — each page is a `.mz` component in `components/`
- **Hash routing** — `#/`, `#/counter`, `#/todos`, `#/about`
- **Interactive** — counter and todo list with client-side JS

## Pages

| Route | Component | Description |
|-------|-----------|-------------|
| `#/` | `components/index.mz` | Home page |
| `#/counter` | `components/counter.mz` | Interactive counter |
| `#/todos` | `components/todos.mz` | Todo list (add/remove) |
| `#/about` | `components/about.mz` | About page |

## File Structure

```
react-app/
├── app.mz              # Main server (HTTP + SSE + routing)
├── public/
│   └── style.css       # Dark theme CSS
└── components/
    ├── index.mz        # Home page
    ├── counter.mz      # Counter component
    ├── todos.mz        # Todo list component
    └── about.mz        # About page
```

## Creating a New Page

1. Create `components/mypage.mz`:
```mozhi
import react from "react.mz"
echo(react.div("class=\"card\"",
    react.h2("", "My Page") +
    react.p("", "Hello!")
))
```

2. Add a navigation link in `app.mz`:
```mozhi
"<a href=\"#/mypage\">My Page</a>"
```

3. Save — the browser auto-reloads!

## Libraries Used

- `mozhi-http` — HTTP server with static file serving
- `react.mz` — Core React framework (h, div, h1, p, button, etc.)
- `react_hooks.mz` — State management hooks
- `react_router.mz` — Hash-based routing
- `react_devtools.mz` — Live reload (SSE), file watcher, HMR
