# Environment Variables Examples

This directory contains example `.env` files for different deployment scenarios.

## Files

| File | Purpose |
|------|---------|
| `minimal.env.example` | Minimum required variables |
| `api-server.env.example` | Full API server configuration |
| `frontend.env.example` | Frontend application variables |
| `js-sdk.env.example` | JS/NPM interop configuration |
| `development.env.example` | Local development settings |
| `production.env.example` | Production deployment settings |
| `.env.local.example` | Local overrides (gitignored) |

## Usage

1. Copy the appropriate example file:
   ```bash
   cp examples/env-examples/api-server.env.example .env
   ```

2. Edit `.env` with your actual values:
   ```bash
   nano .env
   ```

3. For local development, create `.env.local`:
   ```bash
   cp examples/env-examples/.env.local.example .env.local
   ```

## Quick Start

### Minimal Setup
```bash
cp examples/env-examples/minimal.env.example .env
# Edit .env with your GitHub token and settings
```

### Full API Server
```bash
cp examples/env-examples/api-server.env.example .env
# Edit with your production settings
```

### Local Development
```bash
cp examples/env-examples/development.env.example .env
cp examples/env-examples/.env.local.example .env.local
# Both files work together (.env.local overrides .env)
```

## Required Variables

### For API Server
- `GITHUB_TOKEN` — GitHub Personal Access Token
- `GITHUB_OWNER` — GitHub username or organization
- `GITHUB_REPO` — Repository name for package storage
- `API_SECRET_KEY` — Secret key for API authentication

### For Frontend
- `NEXT_PUBLIC_API_URL` — URL of the API server

## Security Notes

⚠️ **Never commit `.env` files with real secrets!**

- `.env` files are gitignored by default
- Use `.env.example` files as templates
- Use `.env.local` for local overrides
- In production, set environment variables directly in your hosting platform

## GitHub Token Scopes

For the GitHub Personal Access Token, you need:

| Scope | Purpose |
|-------|---------|
| `repo` | Full control of private repositories |
| `read:user` | Read user profile data |

### Creating a Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`
4. Generate and copy the token
5. Add to your `.env` file

## Environment-Specific Values

| Variable | Development | Production |
|----------|-------------|------------|
| `NODE_ENV` | `development` | `production` |
| `LOG_LEVEL` | `debug` | `warn` |
| `PORT` | `3000` | `8080` |
| `CACHE_TTL` | `0` | `300` |
| `CORS_ORIGIN` | `*` | `https://your-domain.com` |

## Platform-Specific Setup

### Vercel
Add variables in: Project Settings → Environment Variables

### Docker
```dockerfile
ENV GITHUB_TOKEN=your-token
ENV GITHUB_OWNER=your-username
```

### Docker Compose
```yaml
services:
  api:
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - GITHUB_OWNER=${GITHUB_OWNER}
```

### systemd
```ini
[Service]
Environment="GITHUB_TOKEN=your-token"
Environment="GITHUB_OWNER=your-username"
```

## Testing

To verify your `.env` file is loaded correctly:

```bash
# Node.js
node -e "require('dotenv').config(); console.log(process.env.GITHUB_TOKEN)"

# Or use the test script
node examples/test-env.js
```

## Troubleshooting

### Variables not loading
- Check file is named `.env` (not `.env.example`)
- Ensure no quotes around values (unless needed)
- Check file encoding (should be UTF-8)

### Token not working
- Verify token has correct scopes
- Check token hasn't expired
- Ensure token is for the correct GitHub account

### CORS errors
- Check `CORS_ORIGIN` matches your frontend domain
- In development, use `CORS_ORIGIN=*`
