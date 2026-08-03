# mznn — Mozhi Neural Network

Multi-language neural network: Python, C++, Julia, JavaScript. Auto-downloads from GitHub release.

## Install

```bash
pkg install mznn
```

## Usage

```mozhi
import mod from "mznn"
mod.demo()       # Python XOR demo
mod.demo_cpp()   # C++ XOR demo
mod.demo_js()    # JavaScript XOR demo
mod.demo_all()   # All available languages
mod.train("data.csv", "2 4 1", 1000, "model.json")
mod.predict("model.json", "0.5,0.3")
```

## Languages

- **Python** (numpy) — Full implementation with save/load
- **C++** (no deps) — Compiled and run via `run_cpp()`
- **JavaScript** (Node.js) — ES6 class implementation
- **Julia** — Full implementation

## Source

https://github.com/crossberry-in/mznn
