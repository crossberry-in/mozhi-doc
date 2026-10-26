# Mozhi React Template

A React-like app with live reload, component-based architecture, and hash routing.

## Run

```bash
mozhi-interpreter app.mz
# Open http://127.0.0.1:3000
```

## Features

- **Live reload** — edit any `.mz` or `.css` file → browser auto-refreshes
- **CSS hot-swap** — CSS changes don't trigger full page reload
- **Components** — `.mz` files in `components/` rendered server-side
- **Hash routing** — `#/`, `#/counter`, `#/about`
- **Interactive** — counter with client-side JS

## Pages

| Route | Component |
|-------|-----------|
| `#/` | `components/index.mz` |
| `#/counter` | `components/counter.mz` |
| `#/about` | `components/about.mz` |

## Structure

```
myapp/
├── app.mz              # Dev server + live reload
├── public/
│   └── style.css       # Dark theme
└── components/
    ├── index.mz        # Home page
    ├── counter.mz      # Counter
    └── about.mz        # About
```

## Libraries Used

Libraries auto-download from GitHub on first run:
- `mozhi-http` — HTTP server
- `react.mz` — React core (elements, props)
- `react_devtools.mz` — File watcher, SSE, HMR
