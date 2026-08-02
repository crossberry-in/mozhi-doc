# Mozhi Templates

Create a new Mozhi project from a template — like `npm create react-app` or `cargo new`.

## Quick Start

```bash
# Create a React-like app with live reload
mozhi new myapp --template react-mozhi
cd myapp
mozhi-interpreter app.mz

# Create a basic HTTP server
mozhi new myapi --template api

# Create a static file server
mozhi new mysite --template static

# Create a hello world
mozhi new hello --template helloworld
```

## Available Templates

| Template | Description | Features |
|----------|-------------|----------|
| [`react-mozhi`](react-mozhi/) | React-like app with live reload | Components, SSE, CSS hot-swap, routing |
| [`basic`](basic/) | Basic Mozhi program | Hello world + examples |
| [`api`](api/) | JSON API server | REST endpoints, CRUD |
| [`static`](static/) | Static file server | Serves HTML/CSS/JS from `public/` |
| [`fullstack`](fullstack/) | Full-stack app | Static files + API + shell + multi-language |
| [`helloworld`](helloworld/) | Minimal hello world | Single file, simplest start |

## Template Details

### `react-mozhi` — React-like Framework

```
myapp/
├── app.mz              # Dev server with live reload
├── public/
│   └── style.css       # Dark theme
└── components/
    ├── index.mz        # Home page
    ├── counter.mz      # Interactive counter
    └── about.mz        # About page
```

**Features:**
- Live reload via SSE
- CSS hot-swap (no page reload)
- Component-based architecture
- Hash routing
- Interactive components

### `api` — JSON API Server

```
myapi/
├── app.mz              # API server
├── public/
│   └── index.html      # API docs page
└── scripts/
    └── data.sh         # Data script
```

**Endpoints:**
- `GET /` — API documentation
- `GET /api/items` — List items
- `GET /api/items/:id` — Get item
- `POST /api/items` — Create item
- `GET /api/health` — Health check

### `static` — Static File Server

```
mysite/
├── app.mz              # Static server
└── public/
    ├── index.html      # Home page
    ├── style.css       # Styles
    └── script.js       # Frontend JS
```

### `fullstack` — Full-Stack App

```
myapp/
├── app.mz              # Main server
├── public/             # Static files
├── components/         # Mozhi components
└── scripts/            # Shell/C/Python scripts
```

### `basic` — Basic Program

```
hello/
├── app.mz              # Main program
└── README.md           # Instructions
```

### `helloworld` — Minimal

```
hello/
└── app.mz              # Just a hello world
```

## Creating Custom Templates

1. Create a directory in `templates/`:
```bash
mkdir templates/my-template
```

2. Add an `app.mz` file (required):
```mozhi
echo("Hello from my template!")
```

3. Add a `template.json` manifest:
```json
{
  "name": "my-template",
  "description": "My custom template",
  "files": ["app.mz", "public/", "components/"]
}
```

4. Use it:
```bash
mozhi new myapp --template my-template
```

## Template Installation

Templates are fetched from the `mozhi-doc` repo on GitHub. The `mozhi new` command:

1. Downloads the template files from `https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/templates/<name>/`
2. Creates the project directory
3. Copies all files
4. Runs `mozhi-interpreter app.mz` if `--run` flag is passed

## Manual Installation

If `mozhi new` isn't available, you can install manually:

```bash
# Clone the template
git clone --depth 1 https://github.com/crossberry-in/mozhi-doc.git /tmp/mozhi-doc
cp -r /tmp/mozhi-doc/templates/react-mozhi myapp
cd myapp
mozhi-interpreter app.mz
```

Or download individual files:

```bash
mkdir myapp && cd myapp
curl -fsSL https://raw.githubusercontent.com/crossberry-in/mozhi-doc/main/templates/helloworld/app.mz -o app.mz
mozhi-interpreter app.mz
```
