# Package Design Prompt Template

Copy this file, fill in the two `<REPLACE>` lines, and feed to an AI assistant
to generate a complete design document for your new Mozhi package.

---

# Build the <REPLACE: Package Name> Standard Library for Mozhi (.mz)

Create a production-ready <REPLACE: Package Name> package for the Mozhi programming language.

## Requirements

- Package name: "<REPLACE: package-name>"
- Language: Mozhi (.mz)
- Follow Mozhi coding style.
- Write clean, well-documented code.
- No placeholder implementations.
- Include examples for every API.
- Organize code into modules.
- Export only public APIs.
- Use appropriate units/conventions throughout.
- Optimize for performance and readability.

## Directory Structure

```
pkg/
└── <package-name>/
    ├── package.toml
    ├── README.md
    ├── src/
    │   └── mod.mz
    ├── tests/
    │   └── test_basic.mz
    └── examples/
        └── demo.mz
```

## Implement

<REPLACE: List the functions/modules to implement>

## Examples

Every function must include:

```mozhi
import mod from "<package-name>"

# Show example usage of every public function
echo(my_function(arg1, arg2))
```

## Documentation

Generate:

- README with API reference
- Examples for every function
- Unit tests
- Error handling
- Package metadata (package.toml)

## Output

Produce complete production-ready Mozhi source code for every file with no TODOs or placeholders.

---

## How to Use This Template

1. Copy this file:
   ```bash
   cp docs/PKG_PROMPT.md docs/pkg-mypackage-design.md
   ```

2. Replace the `<REPLACE: ...>` placeholders with your package details.

3. Feed the filled prompt to an AI assistant (or write the code yourself).

4. Save the generated design to `docs/pkg-mypackage-design.md`.

5. Create the package:
   ```bash
   bash scripts/new-pkg.sh mypackage --category <cat> --desc "My package"
   ```

6. Fill in `pkg/mypackage/src/mod.mz` following the design.

7. Build and test:
   ```bash
   bash scripts/build-registry.sh
   cd pkg/mypackage && mozhi-interpreter tests/test_basic.mz
   ```

8. Commit and push:
   ```bash
   git add pkg/mypackage registry docs
   git commit -m "feat(mypackage): add mypackage package"
   git push
   ```
