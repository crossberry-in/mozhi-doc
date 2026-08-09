# Mozhi JS/NPM Interop (js-sdk)

Complete JavaScript and NPM interoperability for the Mozhi programming language.

## Overview

The js-sdk allows Mozhi programs to:
- Import and use any JavaScript/Node.js module
- Import NPM packages from `node_modules/`
- Call JavaScript functions from Mozhi code
- Pass values bidirectionally between Mozhi and JavaScript
- Handle async/Promise/Future seamlessly
- Create callbacks that JavaScript can invoke

## Installation

```bash
# Add to your project
mzpkg install js-sdk

# Or manually copy from
# https://github.com/crossberry-in/mozhi-doc/tree/main/mozhi-pkg/pkg/js-sdk
```

## Import Syntax

### Named Imports
```mozhi
import js { add, multiply } from "./math.js"

result = add(10, 20)
echo(result)  # 30
```

### Namespace Imports
```mozhi
import js * as math from "./math.js"

result = math.add(10, 20)
echo(result)  # 30
```

### Default Imports
```mozhi
import js express from "express"

app = express()
app.listen(3000)
```

### Node.js Built-ins
```mozhi
import js { readFile, writeFile } from "node:fs/promises"

data = await readFile("test.txt")
echo(data)
```

### Aliases
```mozhi
import js { add as sum, multiply as mul } from "./math.js"

result = sum(10, 20)
echo(result)  # 30
```

## NPM Package Support

Any Node.js-compatible NPM package can be imported:

```mozhi
# Install the package first
# npm install lodash

import js * as lodash from "lodash"

result = lodash.sum([1, 2, 3, 4])
echo(result)  # 10
```

### Resolution Order
1. Relative paths (`./module.js`)
2. Absolute paths (`/path/to/module.js`)
3. Node.js built-ins (`node:fs`)
4. Node modules (`node_modules/`)
5. Scoped packages (`@scope/package`)

## Supported Module Formats

- **ES Modules** (`.mjs`, `type: "module"`)
- **CommonJS** (`module.exports`)
- **Node.js built-ins** (`node:*`)
- **Default exports**
- **Named exports**
- **Namespace exports**

## Value Conversion

### Mozhi → JavaScript
| Mozhi Type | JavaScript Type |
|------------|-----------------|
| `number` | `Number` |
| `string` | `String` |
| `bool` | `Boolean` |
| `null` | `null` |
| `array` | `Array` |
| `map` | `Object` |
| `function` | `Function` |
| `buffer` | `Uint8Array` |

### JavaScript → Mozhi
Automatic conversion in the reverse direction.

## Async/Promise Support

```mozhi
import js { fetchData } from "./api.js"

# await automatically converts JS Promise to Mozhi Future
data = await fetchData("https://api.example.com/data")
echo(data)
```

## Callbacks

Mozhi functions can be passed to JavaScript as callbacks:

```mozhi
import js { calculate } from "./math.js"

calculate(10, 20, fn(result) {
    echo(result)
})
```

## Error Handling

JavaScript exceptions are converted to Mozhi errors:

```mozhi
try {
    result = jsFunction()
} catch error {
    echo(error.message)
}
```

## Object Access

```mozhi
import js { createUser } from "./user.js"

user = createUser("Alice")
echo(user.name)      # Property access
user.age = 30        # Property assignment
user.greet()         # Method call (preserves this)
```

## API Reference

### Runtime Functions

| Function | Description |
|----------|-------------|
| `mz_js_load(path)` | Load a JS module |
| `mz_js_export(module, name)` | Get an export from a module |
| `mz_js_call(fn, ...args)` | Call a JS function |
| `mz_js_method(obj, method, ...args)` | Call a JS method (preserves this) |
| `mz_js_get(obj, prop)` | Get a property |
| `mz_js_set(obj, prop, value)` | Set a property |
| `mz_js_await(promise)` | Await a JS Promise |
| `mz_js_callback(fn)` | Create a JS callback from Mozhi function |

### Example: Manual Module Loading

```mozhi
# Load module manually
mod = mz_js_load("./math.js")
add = mz_js_export(mod, "add")
result = mz_js_call(add, 10, 20)
echo(result)  # 30
```

## Testing

Run the test suite:

```bash
cd mozhi-pkg/pkg/js-sdk
node tests/run.js
```

All 44 tests pass, covering:
- Named/default/namespace/alias imports
- CommonJS and ESM modules
- Async/Promise/Future
- Method calls with this binding
- Callbacks (Mozhi → JS → Mozhi)
- Value conversion
- Error handling
- Module caching
- Handle lifecycle

## Examples

See `tests/jsinterop/fixtures/` for complete examples:
- `math.js` — ESM with named exports
- `cjs_module.js` — CommonJS module
- `async_module.js` — Async/Promise exports

## Architecture

```
Mozhi Code
    ↓
JS Import AST
    ↓
JS/NPM Resolver
    ↓
┌────────┼────────┐
↓        ↓        ↓
Local JS  NPM     node:
    ↓
JS Runtime
    ↓
JS Bridge
    ↓
Mozhi Values
```

## Security

- No arbitrary JavaScript execution from Mozhi
- All imports must be explicit `import js` statements
- Module resolution follows Node.js semantics
- No hardcoded package allowlists

## Performance

- Module caching for repeated imports
- Zero-copy buffer conversion where possible
- Handle-based object identity preservation
- Lazy function wrapping

## Future Enhancements

- WASM backend support
- `.mzi` type metadata files
- Automatic NPM installation integration
- Browser environment support
