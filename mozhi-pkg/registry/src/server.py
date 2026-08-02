#!/usr/bin/env python3
"""
Mozhi Package Registry Server
Serves mz-registry.json and package files over HTTP for local testing.

Usage:
    python3 registry/src/server.py --port 8080
    # Then point pkg CLI at: http://localhost:8080/mz-registry.json
"""
import http.server
import socketserver
import json
import os
import sys
import argparse
from pathlib import Path

class RegistryHandler(http.server.SimpleHTTPRequestHandler):
    """Serves files from the registry/ directory with CORS headers."""
    
    def __init__(self, *args, **kwargs):
        # Serve from registry/ directory
        registry_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        super().__init__(*args, directory=registry_dir, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for local testing
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        # Content type for JSON
        if self.path.endswith('.json'):
            self.send_header('Content-Type', 'application/json')
        super().end_headers()
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom log format
        sys.stderr.write(f"  [{self.log_date_time_string()}] {format % args}\n")

def main():
    parser = argparse.ArgumentParser(description='Mozhi Package Registry Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on (default: 8080)')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    args = parser.parse_args()
    
    # Check if registry exists
    registry_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'mz-registry.json')
    if not os.path.exists(registry_file):
        print(f"⚠  Registry file not found: {registry_file}")
        print("   Run: bash scripts/build-registry.sh first")
        sys.exit(1)
    
    # Load and show stats
    with open(registry_file) as f:
        reg = json.load(f)
    
    print("=" * 60)
    print("  Mozhi Package Registry Server")
    print("=" * 60)
    print(f"  URL:     http://localhost:{args.port}")
    print(f"  Host:    {args.host}")
    print(f"  Packages: {len(reg.get('packages', []))}")
    print(f"  Updated:  {reg.get('updated', 'unknown')}")
    print("")
    print("  Endpoints:")
    print(f"    GET /mz-registry.json          — Full registry")
    print(f"    GET /api/v1/packages.json      — API: all packages")
    print(f"    GET /api/v1/categories.json    — API: by category")
    print(f"    GET /api/v1/stats.json         — API: statistics")
    print(f"    GET /index-<letter>.json       — Per-letter index")
    print("")
    print("  Press Ctrl+C to stop")
    print("=" * 60)
    print("")
    
    try:
        with socketserver.TCPServer((args.host, args.port), RegistryHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n  Server stopped.")
    except OSError as e:
        if 'Address already in use' in str(e):
            print(f"✗ Port {args.port} is already in use. Try a different port: --port {args.port + 1}")
        else:
            raise

if __name__ == '__main__':
    main()
