# js-sdk

JavaScript/NPM interoperability for Mozhi.

## Install

```bash
mzpkg install js-sdk
```

## Usage

```mozhi
import js { add } from "./math.js"

result = add(10, 20)
echo(result)  # 30
```

## Features

- Import any JS/Node.js module
- Import NPM packages
- ESM + CommonJS support
- Bidirectional value conversion
- Async/Promise support
- Callback support
- Error handling
- Object access with `this` binding

## Documentation

See [js-sdk.md](../../js-sdk.md) for full documentation.

## Tests

```bash
node tests/run.js
```

44 tests, all passing.

## License

MIT
