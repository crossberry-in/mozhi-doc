#!/usr/bin/env python3
"""helper.py — Example Python file for run_py() demo"""

import json
import sys
import os

print("Hello from Python!")
print(f"Python version: {sys.version}")
print(f"Platform: {sys.platform}")

# Data structure
data = {
    "name": "Mozhi",
    "version": "2.4.0",
    "features": ["file-io", "shell", "multi-language", "http-server"],
    "libraries": {
        "html": 38,
        "http": 15,
        "json": 14,
        "math_utils": 24,
        "strings": 21
    }
}

print("\nJSON output:")
print(json.dumps(data, indent=2))

# List comprehension
squares = [x**2 for x in range(1, 11)]
print(f"\nSquares 1..10: {squares}")

# Environment
print(f"\nCurrent user: {os.getenv('USER', 'unknown')}")
print(f"Home directory: {os.getenv('HOME', 'unknown')}")
