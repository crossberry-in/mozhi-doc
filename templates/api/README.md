# Mozhi API Server Template

A JSON REST API server with CRUD endpoints.

## Run

```bash
mozhi-interpreter app.mz
# Open http://127.0.0.1:8080
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API documentation |
| GET | `/api/items` | List all items |
| GET | `/api/items/:id` | Get single item |
| POST | `/api/items` | Create new item |
| GET | `/api/health` | Health check |

## Test

```bash
curl http://127.0.0.1:8080/api/items
curl http://127.0.0.1:8080/api/items/1
curl http://127.0.0.1:8080/api/health
```
