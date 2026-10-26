# Mozhi Full-Stack Template

Static files + JSON API + Shell + Multi-language run in one app.

## Run

```bash
mozhi-interpreter app.mz
# Open http://127.0.0.1:8080
```

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Home page (HTML) |
| `GET /api/info` | JSON API |
| `GET /run/shell` | Run `scripts/status.sh` |
| `GET /run/c` | Compile & run `scripts/demo.c` |
| `GET /run/py` | Run `scripts/demo.py` |

## Structure

```
myapp/
├── app.mz              # Main server
├── public/             # Static files
│   ├── index.html
│   └── style.css
└── scripts/            # Multi-language scripts
    ├── status.sh
    ├── demo.c
    └── demo.py
```
