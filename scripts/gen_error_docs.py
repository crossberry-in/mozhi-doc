#!/usr/bin/env python3
"""
gen_error_docs.py — Generate the Mozhi error reference site pages from the
single source of truth: the MZ_CODE_REGISTRY table in
mozhi/interpreter/src/mz_diag.c.

Outputs (into mozhi-doc/errors/):
  index.html                  — all v3.4.0 codes by category (+ legacy MZxxxx index link)
  <CODE>.html                 — one page per code with the 12 required elements
  <category>.html             — per-category pages (lexer/parser/types/names/...)
  ai-diagnosis.html           — the free AI Diagnosis documentation

Also run with --check to validate registry/page consistency (CI + tests):
every registered code has a page, every page has all 12 sections, and the
index lists every code.

The prose below documents ACTUAL, verified interpreter behavior (checked
against the v3.5.1 binary) — nothing speculative.
"""
import re
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DOC_REPO = os.path.dirname(HERE)
DEFAULT_REGISTRY = os.environ.get("MZ_INTERPRETER_SRC", os.path.join(DOC_REPO, "..", "mozhi", "interpreter", "src", "mz_diag.c"))
OUT_DIR = os.path.join(DOC_REPO, "errors")

DOCS_BASE = "https://crossberry-in.github.io/mozhi-doc/errors"
CLI_DOCS = "https://github.com/crossberry-in/mozhi/blob/main/docs/CLI.md"
VERSION = "3.5.1"

# ---------------------------------------------------------------- registry
def parse_registry(path):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"MZ_CODE_REGISTRY\[\]\s*=\s*\{(.*?)\n\};", src, re.S)
    if not m:
        raise SystemExit("registry table not found in " + path)
    entries = []
    for line in m.group(1).splitlines():
        mm = re.match(r'\s*\{\s*"([A-Z0-9]+)"\s*,\s*MZ_SEV_(\w+)\s*,\s*MZ_CAT_(\w+)\s*,\s*"([^"]+)"\s*\}', line)
        if mm:
            entries.append({"code": mm.group(1), "severity": mm.group(2).lower(),
                            "category": mm.group(3).lower(), "title": mm.group(4)})
    return entries

CAT_SLUGS = {
    "lexer": "lexer", "parser": "parser", "type": "types", "name": "names",
    "runtime": "runtime", "import": "imports", "compiler": "compiler",
    "stdlib": "standard-library", "cli": "cli",
}
CAT_TITLES = {
    "lexer": "Lexer diagnostics", "parser": "Parser diagnostics",
    "type": "Type diagnostics", "name": "Name-resolution diagnostics",
    "runtime": "Runtime diagnostics", "import": "Import diagnostics",
    "compiler": "Compiler diagnostics", "stdlib": "Standard-library diagnostics",
    "cli": "CLI diagnostics",
}

# ---------------------------------------------------------------- per-code prose
P = {}

P["LEX001"] = dict(
    trigger="A byte appears where no Mozhi token can start — most often an operator "
            "borrowed from another language, or a non-ASCII character inside an identifier.",
    cause="The lexer's scanner has a fixed token set. Characters such as `^`, `|`, `&`, `~` "
          "have no meaning in Mozhi (there are no bitwise operators and no caret operator), "
          "so they cannot begin any token and are reported as illegal. Identifiers are ASCII "
          "(letters, digits, `_`).",
    bad='echo(string(5 ^ 3))',
    fix='echo(string(5 ** 3))',
    fix_note="`**` is the exponentiation operator (verified: `5 ** 3` prints `125`). "
             "For logical operations use the keywords `and` / `or` / `!`.",
    suggest="Replace the character with the Mozhi equivalent: `^` → `**` for exponentiation, "
            "`||` → `or`, `&&` → `and`, `~x` → `!x`. For single quotes around strings, use "
            "double quotes. For non-ASCII names, rename using ASCII letters.",
    related_syntax="Operators, string literals",
    related=["PARSE004"],
    limits="One diagnostic is emitted per illegal byte; all of them on the same line are "
           "grouped under the first one. Bitwise operations do not exist in Mozhi — this is "
           "a language property, not a parse failure.",
)

P["LEX002"] = dict(
    trigger="A string literal reaches the end of the input without a closing double quote.",
    cause="The lexer scans from the opening `\"` to the next `\"`. When the input ends first, "
          "the string is unterminated — usually a missing quote or an accidentally swapped "
          "quote character.",
    bad='let msg = "hello',
    fix='let msg = "hello"',
    fix_note="The diagnostic names the line and column where the string started, so you can "
             "find the opening quote even in long files.",
    suggest="Add the closing quote. If the string legitimately contains a quote character, "
            "escape it as `\\\"`.",
    related_syntax="String literals",
    related=["LEX003"],
    limits="For backward compatibility the token is still produced (running to end of input) "
           "in addition to the diagnostic, so downstream errors may also appear.",
)

P["LEX003"] = dict(
    trigger="A string contains an escape sequence the language does not define, e.g. `\\q` or `\\x`.",
    cause="Mozhi supports exactly six escapes: `\\n`, `\\t`, `\\r`, `\\\"`, `\\\\` and `\\0`. "
          "Anything else after a backslash is kept literally and reported as a warning — the "
          "program still runs.",
    bad='echo("col1\\qcol2")',
    fix='echo("col1\\\\qcol2")',
    fix_note="Use `\\\\` when a literal backslash is intended, or pick one of the six supported escapes.",
    suggest="Replace the unknown escape with the intended character or escape the backslash.",
    related_syntax="String literals, escape sequences",
    related=["LEX002"],
    limits="This is a warning (severity `warning`), not an error: the exit code is not affected. "
           "The diagnostic was added in v3.2.0; older versions silently accepted unknown escapes.",
)

P["LEX004"] = dict(
    trigger="A `/*` block comment is never closed with `*/` before the end of the input.",
    cause="Block comments nest in Mozhi (`/* /* */ */` is one comment). When the scanner runs "
          "out of input while the nesting depth is still positive, the whole remainder of the "
          "file is comment — usually a missing `*/` or an accidentally nested opener.",
    bad='/* TODO: fix this\nfn main() {\n  echo("unreachable")\n}',
    fix='/* TODO: fix this */\nfn main() {\n  echo("reachable")\n}',
    fix_note="The diagnostic points at the line/column where the comment opened.",
    suggest="Close the comment with `*/`. Prefer `//` line comments for short notes.",
    related_syntax="Comments",
    related=[],
    limits="The diagnostic reports the opening position; finding the intended close point is up to you.",
)

P["PARSE001"] = dict(
    trigger="The parser encounters a token that cannot continue the current construct — "
            "with the found token named in the message.",
    cause="Mozhi is parsed with a recursive-descent/Pratt parser. Each construct states which "
          "tokens may follow; anything else is unexpected. The message always contains "
          "`found <token>` so you can see exactly what the parser saw.",
    bad='let x = (1 + 2\nlet y = 3',
    fix='let x = (1 + 2)\nlet y = 3',
    fix_note="Unbalanced delimiters also get a dedicated code (PARSE002) that names where the "
             "construct was opened.",
    suggest="Read the `found` part of the message; it names the offending token and position. "
            "Check the construct that starts on that line for a missing delimiter, comma or operator.",
    related_syntax="Statements and declarations",
    related=["PARSE002", "PARSE004", "PARSE005"],
    limits="Identical duplicates are collapsed, and consequences of one root cause are grouped "
           "(shown with `--verbose`).",
)

P["PARSE002"] = dict(
    trigger="A closing delimiter (`)`, `]`, `}`) is missing — for example a function call or "
            "grouped expression is left open.",
    cause="The parser tracks every open `(`, `[`, `{` with its exact position. When the "
          "expected closer does not appear, the message names the position of the matching "
          "opening delimiter so multi-line mistakes are easy to find.",
    bad='let total = add(1, 2\nlet next = 4',
    fix='let total = add(1, 2)\nlet next = 4',
    fix_note="Message shape: `Expected ')' to match '(' opened at line L, column C`.",
    suggest="Add the missing closer. For long expressions, format one argument per line so "
            "unbalanced delimiters are visible.",
    related_syntax="Function calls, arrays, maps",
    related=["PARSE001", "PARSE005"],
    limits="Mismatched pairs (e.g. `(]`) are tolerated by the tracker: it pops the innermost "
           "matching opener, so the reported opener is the best local match.",
)

P["PARSE003"] = dict(
    trigger="An assignment targets something that cannot hold a value — a literal, "
            "an expression result, or a non-container property access.",
    cause="Only variables (`x = ...`), array slots (`a[i] = ...`) and map keys (`m[\"k\"] = ...`) "
          "are assignable. Assignments are checked at evaluation time; literals and computed "
          "values have no storage to write to.",
    bad='5 = x',
    fix='let x = 5',
    fix_note="Assign to a declared variable or to a container slot that exists.",
    suggest="Declare the target first with `let`/`const`, or restructure so the left side is "
            "a variable, array index, or map key.",
    related_syntax="Assignment, let/const, maps and arrays",
    related=["NAME001"],
    limits="The check runs at evaluation; a code path that never executes the bad assignment "
           "will not report it (the interpreter has no static type checker).",
)

P["PARSE004"] = dict(
    trigger="An expression is required but the next token cannot start one — for example a "
            "closing parenthesis or operator in operand position.",
    cause="Every expression must begin with a prefix-able token (literal, identifier, `(`, `[`, "
          "`{`, unary operator, `fn`, ...). Tokens that only occur *between* operands (like `)` "
          "or `,`) cannot start an expression.",
    bad='let x = ( + 1)',
    fix='let x = (1 + 1)',
    fix_note="When the real problem is an illegal character, the parser groups this diagnostic "
             "under the LEX001 root cause.",
    suggest="Look at what precedes the position: usually an operand is missing between two operators, "
            "or a stray closing delimiter appeared early.",
    related_syntax="Expressions, operators",
    related=["LEX001", "PARSE001"],
    limits="Position points at the token that could not start the expression; the actual "
           "omission is usually slightly earlier in the line.",
)

P["PARSE005"] = dict(
    trigger="The input ends while the parser still needs a token to finish a construct — "
            "e.g. after `fn name(` or an unclosed `{`.",
    cause="When the current token is EOF and a specific token was required, the end-of-input "
          "diagnostic is emitted instead of a generic unexpected-token error, because the fix "
          "is almost always 'continue the construct that was left open'.",
    bad='fn greet(name {\n  echo(name)\n}',
    fix='fn greet(name) {\n  echo(name)\n}',
    fix_note="Combine with the PARSE002 message to find the construct that was left open.",
    suggest="Check the last open construct — functions, blocks, calls, arrays — and complete it.",
    related_syntax="Function declarations, blocks",
    related=["PARSE002", "LEX004"],
    limits="Only the first EOF problem is reported per parse; fix it and re-run to see any others.",
)

P["NAME001"] = dict(
    trigger="A variable is read that was never declared in any visible scope.",
    cause="Identifier reads walk the local scope chain, then fall back to the built-in table. "
          "If neither knows the name, the lookup fails. The diagnostic suggests the closest "
          "known name (edit distance ≤ 2) from visible variables and built-ins.",
    bad='let count = 1\necho(conut)',
    fix='let count = 1\necho(count)',
    fix_note="The message includes a `did you mean 'count'?` hint when a close match exists.",
    suggest="Fix the typo (see the suggestion), or declare the variable with `let`. "
            "Remember that user variables may shadow built-ins since v3.1.1.",
    related_syntax="Variables and scopes, built-ins",
    related=["NAME002", "PARSE003"],
    limits="Suggestions are heuristic (edit distance ≤ 2). Scope-chain walk is bounded by the "
           "frames live at the failure point.",
)

P["NAME002"] = dict(
    trigger="A call names a function that does not exist — neither a user function, a built-in, "
            "nor a member of the targeted module.",
    cause="Calls resolve in order: local/global variables holding functions, built-in table, "
          "module members (`module.func`). An unresolvable name produces this diagnostic with "
          "the offending name in the message.",
    bad='upcase("hello")',
    fix='echo("hello")',
    fix_note="Mozhi has no global `upcase`; use the built-ins that exist (echo, len, string, ...) "
             "or functions from an imported module.",
    suggest="Check the spelling against the built-in list and your imports. For module functions "
            "the import must come first: `import math` then `math.pow(2, 10)`.",
    related_syntax="Function calls, imports",
    related=["NAME001", "IMPORT001"],
    limits="Argument-count mismatches are NOT errors in Mozhi (missing parameters read as null, "
           "extras are ignored) — that leniency is a language property, not a bug.",
)

P["RUNTIME001"] = dict(
    trigger="An operator is applied to a value type it cannot work with — e.g. subtraction on "
            "strings, `!` on a non-boolean, ordering `null` values, indexing an array with a string.",
    cause="Mozhi is dynamically typed with per-operator type rules. Arithmetic requires numbers "
          "(string concatenation with `+` is the exception), comparisons need comparable types, "
          "and index types are fixed per container.",
    bad='echo("total: " - 5)',
    fix='echo("total: " + string(5))',
    fix_note="Use `+` for string concatenation and `string(...)` conversions to move "
             "between types.",
    suggest="Print the operands with `string(...)` first to see their types, then convert "
            "operands explicitly before the operation.",
    related_syntax="Operators, type conversions",
    related=["RUNTIME003", "RUNTIME004"],
    limits="The diagnostic names the operation in the message (as before v3.2.0) and adds the "
           "code/span; it does not yet print the operand types.",
)

P["RUNTIME002"] = dict(
    trigger="A `/` or `%` operation has a zero right-hand side.",
    cause="Integer and float division by zero is undefined in Mozhi and reported instead of "
          "producing infinity or crashing.",
    bad='let n = 0\necho(10 / n)',
    fix='let n = 0\nif n != 0 { echo(10 / n) } else { echo("n is zero") }',
    fix_note="Guard the divisor, or use a fallback value.",
    suggest="Check the divisor before dividing; for user input, validate with a condition first.",
    related_syntax="Arithmetic operators",
    related=["RUNTIME001"],
    limits="Float division also rejects zero (Mozhi does not produce IEEE infinities).",
)

P["RUNTIME003"] = dict(
    trigger="An array or string index is outside `0..length-1`, or a negative index is used.",
    cause="Arrays and strings are zero-based. Indexing beyond the end (or with a negative number) "
          "has no defined element, so it is an error — unlike map indexing, which returns null "
          "for missing keys by design.",
    bad='let a = [1, 2, 3]\necho(a[5])',
    fix='let a = [1, 2, 3]\nif 5 < len(a) { echo(a[5]) }',
    fix_note="Bounds-check with `len(a)` before indexing; iterate with `for x in a` to avoid "
             "manual indexes.",
    suggest="Validate the index, clamp it, or iterate the collection instead of indexing.",
    related_syntax="Arrays, strings, for-in loops",
    related=["RUNTIME001"],
    limits="Mozhi has no negative indexing (`a[-1]` is an error, not 'last element').",
)

P["RUNTIME004"] = dict(
    trigger="A method is called on a value that has no such method — commonly a bitwise method "
            "like `bxor` on a number.",
    cause="Method tables exist per type (arrays: push/pop/..., maps: has/delete/..., strings: "
          "replace/split/..., modules: their exports). Numbers have no methods. Mozhi has no "
          "bitwise operations at all — `bxor`, `band`, `bor`, `shl`, `shr` do not exist anywhere.",
    bad='echo(string(5.bxor(3)))',
    fix='echo(string(5 ** 3))',
    fix_note="Exponentiation is `**` (verified: `5 ** 3` → `125`). There is no XOR/bxor in Mozhi; "
             "if you need bitwise math, compute it in arithmetic terms or wait for a future "
             "language release.",
    suggest="Check the method table for the value's type. For power use `**`; for logical "
            "conditions use `and`/`or`/`!`.",
    related_syntax="Method calls, operators",
    related=["LEX001", "NAME002"],
    limits="The error message names the value's type and the method; per-type method lists are in "
           "the standard-library docs.",
)

P["RUNTIME006"] = dict(
    trigger="A recursion (or mutual recursion) exceeds the call-depth limit — previously this "
            "crashed the interpreter with a stack overflow SIGSEGV.",
    cause="Each Mozhi call consumes C stack. Since v3.2.0 the interpreter counts nested calls "
          "and stops at the limit with this diagnostic instead of crashing. The stack rlimit is "
          "also raised at startup so legitimate deep recursion has headroom.",
    bad='fn f(n) { return 1 + f(n) }\necho(string(f(1)))',
    fix='fn f(n) { if n <= 0 { return 0 } return 1 + f(n-1) }\necho(string(f(500)))',
    fix_note="Every recursion needs a terminating condition that eventually holds.",
    suggest="Add/strengthen the base case, or convert to a loop (`while`). Verified: depth 5000 "
            "completes; the default guard fires at 8000 nested calls.",
    related_syntax="Functions, recursion, while loops",
    related=[],
    limits="The depth limit is fixed (8000) in v3.2.0 and not yet configurable. Extremely deep "
           "legitimate recursion must be restructured into loops.",
)

P["RUNTIME007"] = dict(
    trigger="A value that is not a function is called: `x()` where `x` holds a number, string, "
            "array, etc.",
    cause="Only functions (user `fn`), built-ins, and native-module functions are callable. "
          "Calling anything else is an error — often the result of shadowing a function name "
          "with a variable, or calling a module constant like a function.",
    bad='let x = 5\nx()',
    fix='let x = 5\necho(string(x))',
    fix_note="Call functions, not values. For module constants, access them without parentheses: "
             "`math.pi`, not `math.pi()`.",
    suggest="Check what the name holds at the call site; rename one of the conflicting bindings.",
    related_syntax="Function calls, modules",
    related=["NAME002", "RUNTIME004"],
    limits="Native objects report a separate message ('Native object is not callable') under the "
           "same code.",
)

P["RUNTIME009"] = dict(
    trigger="Any runtime error whose message has no dedicated code yet (raised deep inside a "
            "built-in or native module without an AST position).",
    cause="The central engine classifies every top-level error message to a code. Messages that "
          "match no pattern receive this generic code so machine readers always see a valid "
          "`code` field.",
    bad='(any runtime failure whose message is not yet mapped)',
    fix='(diagnose from the message text; the local diagnosis and docs index still apply)',
    fix_note="The full original message is always preserved in the `reason` field.",
    suggest="Treat as a normal runtime error: read the message, check the docs index, and if it "
            "resembles a known pattern report an issue so it can get a dedicated code.",
    related_syntax="Any",
    related=[],
    limits="This is the classifier's fallback. Over time messages migrate to dedicated codes; "
           "the generic code remains reserved for unmapped cases.",
)

P["RUNTIME010"] = dict(
    trigger="A function is called with a number of arguments it does not accept: too few "
            "required arguments, or too many arguments for a function without a `...rest` "
            "parameter. Applies to declared functions, anonymous `fn` expressions, nested "
            "and recursive calls, constructors, and module-member functions.",
    cause="Before v3.5 the interpreter bound parameters without checking the argument count "
          "and could read past the end of the argument array (measured with AddressSanitizer "
          "as an 8-byte heap-buffer-overflow). Since v3.5 every call path shares one arity "
          "model: required parameters must be present, defaulted parameters fill in when "
          "omitted, and a trailing `...rest` collects surplus arguments.",
    bad='fn add(a, b, c) {\n    return a + b + c\n}\nprint(add(1, 2))',
    fix='fn add(a, b, c) {\n    return a + b + c\n}\nprint(add(1, 2, 3))',
    fix_note="The error message always names the function and both counts, for example: "
             "`function 'add' expects 3 arguments, got 2`. Functions with default values "
             "report `expects at least N arguments`; functions with a rest parameter never "
             "reject extra arguments.",
    suggest="Count the arguments at the call site against the function's parameter list. If "
            "the extra or missing arguments are intentional, declare a default value "
            "(`b = 10`) or a rest parameter (`...rest`).",
    related_syntax="Function declarations, default parameters, rest parameters",
    related=["PARSE001", "RUNTIME007"],
    limits="The diagnostic is emitted at the call site when one is available; calls made "
           "through the native-module callback API report the error without a source span. "
           "The arity check is exact (no implicit argument coercion).",
)

P["IMPORT001"] = dict(
    trigger="An import names a module that cannot be found: not a built-in module, not in "
            "`./.mozhi/libs/`, `~/.mozhi/libs/`, or the project tree.",
    cause="Import resolution tries, in order: built-in native modules (math, json, web, http, "
          "fs, db, template), local library paths, and the public registry (auto-download on "
          "first use). Exhausting all paths yields this diagnostic.",
    bad='import physics',
    fix='import math',
    fix_note="Built-in modules always resolve: math, json, web, http, fs, db, template.",
    suggest="Use a built-in module name, or put the library file in `./.mozhi/libs/<name>.mz`, "
            "or run `mozhi add <package>` for registry packages.",
    related_syntax="import statement",
    related=["IMPORT002", "IMPORT003"],
    limits="Auto-download needs network access; offline environments only see local+built-in "
           "modules (the plain message lists the paths that were tried).",
)

P["IMPORT002"] = dict(
    trigger="Import syntax that Mozhi does not support — most commonly `import(\"math\")`, "
            "treating import as a function call.",
    cause="`import` is a bare keyword statement in Mozhi, not a function: the module name follows "
          "directly without parentheses or quotes. The aliased form is "
          "`import alias from \"package\"`.",
    bad='import("math")',
    fix='import math',
    fix_note="Verified behavior: bare keyword form loads the built-in module; the call form is a "
             "parse error.",
    suggest="Write `import math` (no parentheses, no quotes). For aliases: "
            "`import http from \"mozhi-http\"`.",
    related_syntax="import statement",
    related=["IMPORT001"],
    limits="The diagnostic fires specifically when `(` follows `import`; other malformed imports "
           "surface as PARSE001.",
)

P["IMPORT003"] = dict(
    trigger="An imported module was found but failed to load — unreadable file or a parse error "
            "inside the module source.",
    cause="Module sources are parsed with the same parser as main programs. Errors inside the "
          "module are reported with this code and name the module file, so the problem is "
          "attributed to the dependency rather than your code.",
    bad='./.mozhi/libs/mylib.mz contains `let = 5` (a parse error)',
    fix='fix mylib.mz: `let x = 5`',
    fix_note="Fix the syntax error in the named module file and re-run.",
    suggest="Open the file named in the message at the reported position; run "
            "`mozhi lint <module file>` to see its diagnostics with codes.",
    related_syntax="Modules, libraries",
    related=["PARSE001", "IMPORT001"],
    limits="Diagnostics from the module body are reported as a summary here; run the linter on "
           "the module file for the full per-line detail.",
)

P["STDLIB001"] = dict(
    trigger="A built-in or native-module function received an invalid argument — wrong type, "
            "out-of-domain value, malformed input.",
    cause="Native functions validate their inputs and report failures with a module-prefixed "
          "message (`math:`, `json:`, `fs:`, `db:`, `http:`, `web:`, `template:`). The classifier "
          "maps those prefixes to this code.",
    bad='import math\necho(string(math.factorial(-1)))',
    fix='(validate the argument before calling the function)',
    fix_note="Check the function's documented domain before calling; validate inputs.",
    suggest="Read the `reason` text — it names the module and the specific problem. Guard inputs "
            "with conditions before the call.",
    related_syntax="Standard library",
    related=["RUNTIME001"],
    limits="These errors carry no source span (the AST node is not available inside built-ins); "
           "the message and docs link are still complete.",
)

P["CLI001"] = dict(
    trigger="A script path was passed that does not exist or cannot be opened for reading.",
    cause="The CLI reads the file before parsing; failure to open produces this diagnostic with "
          "the path in the message.",
    bad='$ mozhi run missing.mz',
    fix='$ mozhi run existing.mz',
    fix_note="Pass a path that exists; relative paths resolve against the current directory.",
    suggest="Check the path and your current directory. Note: `mozhi run` needs the file argument; "
            "see CLI003 for the missing-argument case.",
    related_syntax="CLI: run",
    related=["CLI003"],
    limits="Permission errors are reported with the same code (the OS error text is included).",
)

P["CLI002"] = dict(
    trigger="The first argument is a word that is neither a known command nor an existing file — "
            "e.g. a typo like `mozhi ruun app.mz`.",
    cause="Unknown single words used to fall through to 'treat as script', producing a confusing "
          "'cannot open file'. Since v3.2.0, a word that (a) is not an existing path, (b) contains "
          "no `/`, and (c) does not end in `.mz` is reported as an unknown command.",
    bad='$ mozhi ruun app.mz',
    fix='$ mozhi run app.mz',
    fix_note="Known commands: run, new, dev, serve, test, fmt, lint, build, repl, version, help.",
    suggest="Run `mozhi help` for the command list. To run a script, pass a path ending in `.mz`.",
    related_syntax="CLI commands",
    related=["CLI001"],
    limits="The heuristic keeps legacy behavior for anything that names an existing file or ends "
           "in `.mz` — those still run through the script path (CLI001 if unreadable).",
)

P["CLI003"] = dict(
    trigger="A required argument is missing — currently `mozhi run` without a file.",
    cause="Some commands need an operand; `run` requires the script path.",
    bad='$ mozhi run',
    fix='$ mozhi run app.mz',
    fix_note="The usage line is printed together with the diagnostic.",
    suggest="Provide the missing argument as shown in the usage line.",
    related_syntax="CLI: run",
    related=["CLI001", "CLI002"],
    limits="Only `mozhi run` validates this way in v3.2.0; other commands keep their previous "
           "argument handling.",
)

P["CLI004"] = dict(
    trigger="More than 200 diagnostics were produced in one run.",
    cause="To keep output readable and memory bounded, the engine stores at most 200 diagnostics. "
          "When the limit is hit, this informational note is appended.",
    bad='(a file with hundreds of independent syntax errors)',
    fix='fix the reported errors and re-run',
    fix_note="The note appears with severity `info` and never affects the exit code.",
    suggest="Fix errors iteratively — after each round the remaining ones are reported.",
    related_syntax="CLI: diagnostics output",
    related=[],
    limits="Counts in the JSON summary reflect what was kept, not what was dropped; the note is "
           "the only signal that truncation happened.",
)

REQUIRED_SECTIONS = ["Trigger", "Minimal failing example", "Verified fix",
                     "Suggested fix", "Related syntax", "Related diagnostics", "Reference links",
                     "Limitations"]

# ---------------------------------------------------------------- MD3 page scaffold
def drawer(active_suffix=""):
    marks = {"index": "", "ai": "", "lexer": "", "parser": "", "names": "",
             "runtime": "", "imports": "", "standard-library": "", "cli": ""}
    if active_suffix in marks:
        marks[active_suffix] = ' class="active"'
    return f"""
    <aside class="md-drawer" id="drawer">
        <div class="md-drawer-section">
            <div class="md-drawer-heading">Getting started</div>
            <a href="../index.html"><span class="msym">home</span>Overview</a>
            <a href="../install.html"><span class="msym">download</span>Installation</a>
            <a href="../quickstart.html"><span class="msym">rocket_launch</span>Quick start</a>
            <a href="../examples.html"><span class="msym">code_blocks</span>Examples</a>
            <a href="../packages.html"><span class="msym">packages</span>Packages</a>
        </div>
        <div class="md-drawer-section">
            <div class="md-drawer-heading">Errors</div>
            <a href="../v35.html"><span class="msym">auto_awesome</span>What's new in v3.5</a>
            <a href="index.html"{marks['index']}><span class="msym">error</span>Error reference</a>
            <a href="ai-diagnosis.html"{marks['ai']}><span class="msym">psychology</span>AI Diagnosis</a>
        </div>
        <div class="md-drawer-section">
            <div class="md-drawer-heading">Categories</div>
            <a href="lexer.html"{marks['lexer']}><span class="msym">text_fields</span>Lexer</a>
            <a href="parser.html"{marks['parser']}><span class="msym">schema</span>Parser</a>
            <a href="names.html"{marks['names']}><span class="msym">badge</span>Names</a>
            <a href="runtime.html"{marks['runtime']}><span class="msym">play_circle</span>Runtime</a>
            <a href="imports.html"{marks['imports']}><span class="msym">package_2</span>Imports</a>
            <a href="standard-library.html"{marks['standard-library']}><span class="msym">inventory_2</span>Standard library</a>
            <a href="cli.html"{marks['cli']}><span class="msym">terminal</span>CLI</a>
        </div>
        <div class="md-drawer-section">
            <div class="md-drawer-heading">Project</div>
            <a href="https://github.com/crossberry-in/mozhi" target="_blank" rel="noopener"><span class="msym">deployed_code</span>Source code</a>
            <a href="https://github.com/crossberry-in/mozhi/blob/main/CHANGELOG.md" target="_blank" rel="noopener"><span class="msym">history</span>Changelog</a>
        </div>
    </aside>"""


HEAD = """<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} — Mozhi Error Reference</title>
    <meta name="description" content="{DESC}">
    <meta name="color-scheme" content="light dark">
    <script>
    (function(){{try{{var t=localStorage.getItem('md3-theme');document.documentElement.setAttribute('data-theme',t||'light');}}catch(e){{document.documentElement.setAttribute('data-theme','light');}}}})();
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&family=Roboto+Mono:wght@400;500&display=swap">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block">
    <link rel="stylesheet" href="../md3.css">
    <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><defs><linearGradient id='g' x1='0' y1='0' x2='1' y2='1'><stop offset='0' stop-color='%23415F91'/><stop offset='1' stop-color='%23705575'/></linearGradient></defs><rect width='100' height='100' rx='24' fill='url(%23g)'/><text x='50' y='71' font-size='58' font-weight='bold' fill='white' text-anchor='middle' font-family='sans-serif'>M</text></svg>">
    <style>
        .err-head {{ border-left: 4px solid var(--md-error, #B3261E); padding: 4px 0 4px 16px; margin: 18px 0; }}
        .err-code {{ font-family: 'Roboto Mono', monospace; font-size: 14px; opacity: .75; }}
        .err-title {{ font-size: 30px; font-weight: 700; margin: 2px 0; }}
        .sev {{ display:inline-block; padding: 2px 10px; border-radius: 999px; font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: .4px; }}
        .sev-error {{ background: #FDE7E5; color: #B3261E; }} .sev-warning {{ background: #FFF0D2; color: #8A5A00; }}
        .sev-info {{ background: #DFF3FA; color: #00639B; }} .sev-hint {{ background: #E8DEF8; color: #4A2F8F; }}
        h2 {{ font-size: 19px; margin: 30px 0 8px; }}
        .md-code {{ margin: 10px 0 18px; }}
        pre {{ margin: 0; padding: 14px 16px; overflow-x: auto; }}
        code {{ font-family: 'Roboto Mono', monospace; font-size: 13px; }}
        p code, li code, td code {{ background: rgba(127,127,127,.14); padding: 1px 5px; border-radius: 4px; }}
        .pill {{ display:inline-block; margin: 2px 4px 2px 0; padding: 3px 10px; border-radius: 999px;
                 background: rgba(127,127,127,.12); font-family:'Roboto Mono',monospace; font-size:12px; }}
        .pill:hover {{ text-decoration: none; background: rgba(127,127,127,.22); }}
        .meta-chip {{ display:inline-flex; align-items:center; gap:6px; padding:4px 12px; border-radius:999px;
                      background: rgba(127,127,127,.1); margin-right:8px; font-size:13px; }}
        .callout {{ border-left: 3px solid rgba(127,127,127,.4); padding: 8px 14px; margin: 14px 0; opacity: .9; }}
        .crumb {{ font-size: 13px; margin-bottom: 6px; }}
        .crumb a {{ opacity: .7; }}
        table td, table th {{ padding: 8px 12px; border-bottom: 1px solid rgba(127,127,127,.18); }}
    </style>
</head>
<body>
    <header class="md-appbar" id="appbar">
        <button class="md-iconbtn md-menu-btn" id="menuToggle" aria-label="Open navigation menu">
            <span class="msym">menu</span>
        </button>
        <a href="../index.html" class="md-brand">
            <span class="md-brand-badge">M</span>
            Mozhi
        </a>
        <span class="md-version-chip">v{VERSION}</span>
        <span class="md-appbar-spacer"></span>
        <a class="md-iconbtn" href="https://github.com/crossberry-in/mozhi" target="_blank" rel="noopener" aria-label="GitHub repository">
            <span class="msym">code</span>
        </a>
        <button class="md-iconbtn" id="themeToggle" aria-label="Toggle dark theme">
            <span class="msym">dark_mode</span>
        </button>
    </header>
{DRAWER}
    <div class="md-scrim" id="scrim"></div>

    <div class="md-content">
        <main class="md-main-col">
"""

FOOT = """
        </main>
    </div>
    <script src="../md3.js"></script>
</body>
</html>
"""


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def codeblock(src):
    return f'<div class="md-code"><pre><code>{esc(src)}</code></pre></div>'


def term_block(lines):
    inner = "\n".join(lines)
    return f'<div class="md-code"><pre><code>{esc(inner)}</code></pre></div>'


def code_page(entry):
    c, title, info = entry["code"], entry["title"], P[entry["code"]]
    sev = entry["severity"]
    related = info.get("related", [])
    rel_pills = "".join(
        f'<a class="pill" href="{r}.html">{r}</a>' for r in related)
    cat_slug = CAT_SLUGS[entry["category"]]
    example_term = [
        "error[%s]: %s" % (c, title),
        "  --> app.mz:1:16",
        " 1 | %s" % info["bad"].splitlines()[0],
        "   |                 ^",
        "   |",
        "reason: (the exact problem, with positions)",
        "help:   (a suggested fix appears here)",
        "docs:   %s/%s" % (DOCS_BASE, c),
    ]
    body = f"""
            <p class="crumb"><a href="index.html">Error reference</a> › <a href="{cat_slug}.html">{CAT_TITLES[entry['category']]}</a></p>
            <div class="err-head">
                <span class="err-code">{c}</span>
                <h1 class="err-title">{esc(title)}</h1>
                <span class="sev sev-{sev}">{sev}</span>
            </div>

            <span class="meta-chip"><span class="msym" style="font-size:16px">verified</span>verified on v{VERSION}</span>
            <span class="meta-chip"><span class="msym" style="font-size:16px">category</span>{entry['category']}</span>
            <span class="meta-chip"><span class="msym" style="font-size:16px">terminal</span>stable code</span>

            <h2>What it means</h2>
            <p>{esc(info['cause'])}</p>

            <h2>Trigger condition</h2>
            <p>{esc(info['trigger'])}</p>

            <h2>Minimal failing example</h2>
            {codeblock(info['bad'])}

            <h2>Verified fix</h2>
            {codeblock(info['fix'])}
            <p>{esc(info.get('fix_note',''))}</p>

            <h2>What the interpreter prints</h2>
            {term_block(example_term)}
            <div class="callout">Run <code>mozhi --json run app.mz</code> to get the same information as
            machine-readable JSON (schema <code>mozhi.diagnostics.v1</code>), or <code>--verbose</code> to
            also show grouped related diagnostics. See the <a href="{CLI_DOCS}">CLI reference</a>.</div>

            <h2>Suggested fix</h2>
            <p>{esc(info['suggest'])}</p>

            <h2>Related syntax</h2>
            <p>{esc(info['related_syntax'])}</p>

            <h2>Related diagnostics</h2>
            <p>{rel_pills if rel_pills else '<em>None</em>'}</p>

            <h2>Reference links</h2>
            <ul>
                <li><a href="index.html">All error codes</a></li>
                <li><a href="{CLI_DOCS}">CLI reference — output flags and JSON schema</a></li>
                <li><a href="ai-diagnosis.html">Free AI Diagnosis for this error</a></li>
            </ul>

            <h2>Limitations</h2>
            <p>{esc(info['limits'])}</p>
"""
    return (HEAD.format(TITLE=c + " " + title, VERSION=VERSION,
                        DESC=f"Mozhi error {c}: {title} — trigger, cause, verified fix.",
                        DRAWER=drawer(cat_slug))
            + body + FOOT)


def category_page(cat, entries):
    if cat in ("type", "compiler"):
        body = f"""
            <p class="crumb"><a href="index.html">Error reference</a></p>
            <div class="err-head" style="border-color:rgba(127,127,127,.4)">
                <h1 class="err-title">{CAT_TITLES[cat]}</h1>
            </div>
            <div class="callout">The current interpreter performs no static type checking and
            has no separate compiler stage — type problems are reported at runtime
            (<a href="RUNTIME001.html"><code>RUNTIME001</code></a>). Codes will appear here when those
            subsystems gain dedicated diagnostics.</div>
"""
    else:
        rows = ""
        for e in entries:
            rows += (f'<tr><td><a href="{e["code"]}.html"><code>{e["code"]}</code></a></td>'
                     f'<td>{esc(e["title"])}</td>'
                     f'<td><span class="sev sev-{e["severity"]}">{e["severity"]}</span></td></tr>\n')
        body = f"""
            <p class="crumb"><a href="index.html">Error reference</a></p>
            <div class="err-head" style="border-color:rgba(127,127,127,.4)">
                <h1 class="err-title">{CAT_TITLES[cat]}</h1>
            </div>
            <table style="width:100%;border-collapse:collapse">
                <thead><tr><th style="text-align:left">Code</th><th style="text-align:left">Title</th>
                <th style="text-align:left">Severity</th></tr></thead>
                <tbody>{rows}</tbody>
            </table>
"""
    return (HEAD.format(TITLE=CAT_TITLES[cat], VERSION=VERSION,
                        DESC=f"Mozhi {CAT_TITLES[cat].lower()} — error codes and documentation.",
                        DRAWER=drawer(cat))
            + body + FOOT)


def index_page(entries):
    sections = ""
    by_cat = {}
    for e in entries:
        by_cat.setdefault(e["category"], []).append(e)
    for cat in ["lexer", "parser", "name", "runtime", "import", "stdlib", "cli"]:
        if cat not in by_cat:
            continue
        rows = ""
        for e in by_cat[cat]:
            rows += (f'<tr><td><a href="{e["code"]}.html"><code>{e["code"]}</code></a></td>'
                     f'<td>{esc(e["title"])}</td>'
                     f'<td><span class="sev sev-{e["severity"]}">{e["severity"]}</span></td></tr>\n')
        sections += (f'<h2 id="{CAT_SLUGS[cat]}">{CAT_TITLES[cat]}</h2>'
                     f'<table style="width:100%;border-collapse:collapse">'
                     f'<thead><tr><th style="text-align:left">Code</th><th style="text-align:left">Title</th>'
                     f'<th style="text-align:left">Severity</th></tr></thead><tbody>{rows}</tbody></table>')
    sample = term_block([
        "error[LEX001]: illegal character in source",
        "  --> app.mz:1:16",
        " 1 | echo(string(5 ^ 3))",
        "   |                ^",
        "   |",
        "reason: the character '^' is not part of the Mozhi language",
        "help:   exponentiation is written with '**' in Mozhi, e.g. 5 ** 3",
        "docs:   %s/LEX001" % DOCS_BASE,
        "",
        "── AI Diagnosis ────────────────────────────",
        " Replace `^` with `**`. For example, change `5 ^ 3` to `5 ** 3`.",
        " Note: AI-generated suggestion — may be wrong; the local diagnosis above is authoritative.",
    ])
    body = f"""
            <div class="err-head" style="border-color:rgba(127,127,127,.4)">
                <h1 class="err-title">Mozhi error reference</h1>
            </div>
            <p>Every diagnostic produced by the Mozhi interpreter carries a stable code, a source span,
            a suggested fix and a link to its page. These pages document the <strong>v{VERSION} central
            diagnostics registry</strong> — the same table the interpreter's CLI is built from, and this
            site is generated from that registry, so codes and docs cannot drift apart. For the legacy
            v2.x <code>MZ1xxx–MZ4xxx</code> specification pages, see
            <a href="MZ1001.html">the archived MZ1001 page</a> (also kept under <code>errors/</code>).</p>

            <h2>Anatomy of a diagnostic</h2>
            {sample}

            <h2>Machine-readable output</h2>
            <p>Run <code>mozhi --json run app.mz</code> — diagnostics are printed to stderr as JSON
            (schema <code>mozhi.diagnostics.v1</code>) with fields
            <code>code, severity, category, message, reason, help, file, line, column, endLine, endColumn,
            documentation</code>. Coordinates are 1-based; a column counts Unicode code points and a tab
            counts as one column. See the <a href="{CLI_DOCS}">CLI reference</a>.</p>

            <h2>Free AI Diagnosis</h2>
            <p>Interactive runs attach a free, anonymous explanation below the local diagnostics — no API
            key, no account. Details and privacy notes: <a href="ai-diagnosis.html">AI Diagnosis</a>.</p>

            {sections}
"""
    return (HEAD.format(TITLE="Error reference", VERSION=VERSION,
                        DESC="All Mozhi error codes: lexer, parser, names, runtime, imports, standard library, CLI.",
                        DRAWER=drawer("index"))
            + body + FOOT)


def ai_page():
    config_rows = [
        "$ mozhi run app.mz                # interactive: AI Diagnosis attaches automatically",
        "$ mozhi --no-ai run app.mz        # skip it entirely",
        "$ MOZHI_NO_AI=1 mozhi run app.mz  # same via environment",
        "$ mozhi --ai --json run app.mz    # force in scripts; emits {\"ai\": ...} on stderr",
    ]
    body = f"""
            <p class="crumb"><a href="index.html">Error reference</a></p>
            <div class="err-head" style="border-color:rgba(127,127,127,.4)">
                <h1 class="err-title">AI Diagnosis</h1>
            </div>
            <p>Mozhi can attach a <strong>free AI explanation</strong> under the local error diagnostics —
            the feature is named exactly <strong>AI Diagnosis</strong>. It requires no API key, no
            account, no registration and no payment: the default service is an anonymous, keyless
            HTTPS endpoint that was verified reachable before this release.</p>

            <h2>How it works</h2>
            <ol>
                <li>The interpreter first prints its <strong>local</strong> diagnosis (codes, spans,
                    suggested fixes) — that part is deterministic and authoritative.</li>
                <li>When errors occurred and output is interactive, it collects a <strong>minimal
                    context</strong>: up to 4 error entries (code, message, reason, position) plus at
                    most ~1.2&nbsp;KB of the offending source lines. The whole project is never uploaded;
                    no other files are read.</li>
                <li>The context is sent over <strong>HTTPS</strong> with a bounded timeout (20&nbsp;s by
                    default) and the reply is size-capped and validated before display.</li>
                <li>The suggestion is shown in an <code>AI Diagnosis</code> block with a disclaimer:
                    <em>AI-generated suggestion — may be wrong; the local diagnosis above is
                    authoritative.</em> Suggestions are never executed and never modify files.</li>
            </ol>

            <h2>When it is off</h2>
            <p>AI Diagnosis is <strong>off</strong> for non-interactive runs (piped output, CI) unless
            you pass <code>--ai</code> or set <code>MOZHI_AI=1</code>, and <strong>always off</strong>
            with <code>--no-ai</code> or <code>MOZHI_NO_AI=1</code>. If the service is unreachable,
            rate-limited, slow, or returns garbage, you see one line
            (<code>AI Diagnosis unavailable: …</code>) with a link to the error index — the exit code
            and the local diagnosis are completely unaffected.</p>

            <h2>Privacy</h2>
            <ul>
                <li>Only the minimal context above leaves the machine — never the project tree.</li>
                <li>Anything that looks like a credential (<code>sk-…</code>, <code>ghp_…</code>,
                    <code>npm_…</code>, AWS keys, <code>Bearer …</code>) is scrubbed to
                    <code>[REDACTED]</code> before sending.</li>
                <li>Transport is HTTPS; plain HTTP is only accepted for loopback endpoints (tests).</li>
                <li>No API key exists, so nothing can leak a key.</li>
                <li>The response is advisory text; it is never executed or written to disk.</li>
            </ul>

            <h2>Configuration</h2>
            {term_block(config_rows)}
            <table style="width:100%;border-collapse:collapse">
                <thead><tr><th style="text-align:left">Variable</th><th style="text-align:left">Meaning</th><th style="text-align:left">Default</th></tr></thead>
                <tbody>
                    <tr><td><code>MOZHI_NO_AI=1</code></td><td>disable AI Diagnosis</td><td>unset (enabled)</td></tr>
                    <tr><td><code>MOZHI_AI=1</code></td><td>force-enable, also in scripts/JSON mode</td><td>unset</td></tr>
                    <tr><td><code>MOZHI_AI_TIMEOUT_MS</code></td><td>request timeout (500–60000)</td><td>20000</td></tr>
                    <tr><td><code>MOZHI_AI_ENDPOINT</code></td><td>replace the service (maintenance/testing)</td><td>built-in default</td></tr>
                    <tr><td><code>MOZHI_AI_MODEL</code></td><td>override the model id sent to the service</td><td>built-in default</td></tr>
                    <tr><td><code>MOZHI_AI_MAX_CONTEXT</code></td><td>max source-context bytes (200–8000)</td><td>1200</td></tr>
                </tbody>
            </table>

            <h2>Honest limits</h2>
            <ul>
                <li>The default free service was verified keyless and anonymous on
                    2026-10-26 (repeated back-to-back requests, no throttling observed),
                    but it is still a courtesy service: if it is unreachable,
                    rate-limited, slow, or returns garbage, you get the one-line
                    notice instead of a suggestion.</li>
                <li>Suggestions can be wrong — the block always says so. Verified local facts (codes,
                    spans, fixes) always come first.</li>
                <li>Binaries built without TLS support (some release targets) report
                    <code>AI Diagnosis unavailable</code> and fall back to local diagnosis.</li>
            </ul>
"""
    return (HEAD.format(TITLE="AI Diagnosis", VERSION=VERSION,
                        DESC="Mozhi free AI Diagnosis: anonymous, keyless error explanations with strict privacy.",
                        DRAWER=drawer("ai"))
            + body + FOOT)


def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate(registry_path=DEFAULT_REGISTRY, out_dir=OUT_DIR):
    entries = parse_registry(registry_path)
    write(os.path.join(out_dir, "index.html"), index_page(entries))
    for e in entries:
        write(os.path.join(out_dir, e["code"] + ".html"), code_page(e))
    for cat, slug in CAT_SLUGS.items():
        write(os.path.join(out_dir, slug + ".html"),
              category_page(cat, [e for e in entries if e["category"] == cat]))
    write(os.path.join(out_dir, "ai-diagnosis.html"), ai_page())
    return entries


def check(registry_path=DEFAULT_REGISTRY, out_dir=OUT_DIR):
    entries = parse_registry(registry_path)
    errors = []
    for e in entries:
        p = os.path.join(out_dir, e["code"] + ".html")
        if not os.path.exists(p):
            errors.append(f"missing page for {e['code']}")
            continue
        html = open(p, encoding="utf-8").read()
        for sec in REQUIRED_SECTIONS:
            if sec not in html:
                errors.append(f"{e['code']}.html missing section '{sec}'")
        if e["code"] not in html:
            errors.append(f"{e['code']}.html does not mention its own code")
    idx = open(os.path.join(out_dir, "index.html"), encoding="utf-8").read()
    for e in entries:
        if e["code"] not in idx:
            errors.append(f"index.html does not list {e['code']}")
    for slug in CAT_SLUGS.values():
        if not os.path.exists(os.path.join(out_dir, slug + ".html")):
            errors.append(f"missing category page {slug}.html")
    return errors


if __name__ == "__main__":
    if "--check" in sys.argv:
        errs = check()
        if errs:
            print("\n".join(errs))
            sys.exit(1)
        print("error docs consistent with registry")
        sys.exit(0)
    entries = generate()
    print(f"generated {len(entries)} code pages + categories + index + ai-diagnosis")
