# Mozhi Static Server Template

Serves static files (HTML, CSS, JS) from the `public/` directory.

## Run

```bash
mozhi-interpreter app.mz
# Open http://127.0.0.1:8080
```

## Structure

```
myapp/
├── app.mz              # Static file server
└── public/
    ├── index.html      # Home page
    ├── style.css       # Stylesheet
    └── script.js       # Frontend JS
```

## Customize

Edit files in `public/` — the server serves them automatically.
