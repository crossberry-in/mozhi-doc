# Mozhi Programming Language Specification v2.0

**Official Language Specification**

Version 2.0 — August 2026

Copyright © 2026 crossberry-in. All Rights Reserved.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Lexical Structure](#2-lexical-structure)
3. [Grammar (EBNF)](#3-grammar-ebnf)
4. [Type System](#4-type-system)
5. [Variables and Constants](#5-variables-and-constants)
6. [Functions](#6-functions)
7. [Control Flow](#7-control-flow)
8. [Composite Types](#8-composite-types)
9. [Pattern Matching](#9-pattern-matching)
10. [Error Handling](#10-error-handling)
11. [Module System](#11-module-system)
12. [Standard Library](#12-standard-library)
13. [Foreign Function Interface](#13-foreign-function-interface)
14. [Compiler and Interpreter](#14-compiler-and-interpreter)
15. [Package Manager](#15-package-manager)
16. [Diagnostics](#16-diagnostics)
17. [Runtime and Memory](#17-runtime-and-memory)
- [Appendix A: Error Code Reference](#appendix-a-error-code-reference)
- [Appendix B: Reserved Keywords](#appendix-b-reserved-keywords)
- [Appendix C: Operator Precedence](#appendix-c-operator-precedence)

---

## 1. Introduction

### 1.1 Purpose

This document constitutes the official language specification for the Mozhi programming language, version 2.0. It defines the syntax, semantics, type system, module system, standard library, and runtime behavior of the language. This specification serves as the authoritative reference for compiler implementers, tooling developers, and programmers who write Mozhi code. Any conforming implementation of Mozhi must adhere to the rules and behaviors described in this document. Where this document is silent or ambiguous, implementers should choose the interpretation most consistent with the stated design goals.

### 1.2 Design Goals

Mozhi is designed with the following principles as its foundation. Every language feature, syntax decision, and runtime behavior must align with these goals:

- **Simplicity** — The language must be easy to learn and read. Syntax should be minimal and consistent across all constructs.
- **Static Typing** — The type system provides compile-time type safety with automatic type inference to reduce annotation burden.
- **Performance** — Compiled code must achieve native execution speed. The compiler performs optimization passes including constant folding, dead code elimination, and inlining.
- **Memory Safety** — The runtime prevents buffer overflows, null pointer dereferences (where statically detectable), and use-after-free errors through ownership tracking and bounds checking.
- **Cross-Platform** — Mozhi programs compile to native code for Linux, macOS, Windows, and Android (via Termux) on x86_64 and ARM64 architectures.
- **Native Interoperability** — The Foreign Function Interface allows seamless calls to and from C, C++, Assembly, and Rust code through a stable ABI.
- **Production Readiness** — The toolchain provides deterministic builds, reproducible outputs, comprehensive diagnostics, and a complete package manager.

### 1.3 Scope

This specification covers the following components of the Mozhi ecosystem:

- Lexical structure and tokenization rules
- Context-free grammar in Extended Backus-Naur Form (EBNF)
- Static type system, type inference algorithm, and type checking rules
- Runtime semantics for all language constructs
- Module system, import/export mechanisms, and name resolution
- Standard library API surface and behavior contracts
- Foreign Function Interface (FFI) and ABI specifications
- Compiler pipeline: lexing, parsing, analysis, optimization, code generation
- Interpreter execution model for rapid development
- Package manager commands, manifest format, and dependency resolution
- Diagnostic error codes, message formats, and suggestion system
- Runtime memory model, garbage collection, and concurrency primitives

### 1.4 Terminology

| Term | Definition |
|------|-----------|
| **Shall** | Indicates a mandatory requirement. Conforming implementations must obey this rule. |
| **Should** | Indicates a recommendation. Conforming implementations are encouraged but not required to obey this rule. |
| **May** | Indicates optional behavior. Conforming implementations may or may not implement this feature. |
| **Implementation-defined** | Behavior that is not specified by this document. The implementer must document the chosen behavior. |
| **Undefined behavior** | Behavior that is not specified. Implementations are not required to handle this case predictably. |
| **Conforming implementation** | An implementation that satisfies all mandatory requirements (shall) of this specification. |
| **Conforming program** | A program that adheres to all syntactic and semantic rules of this specification. |

### 1.5 Conformance Levels

| Level | Requirements |
|-------|-------------|
| **Level 1: Core** | Lexical structure, grammar, type system, control flow, functions, arrays, strings, built-in functions, and the interpreter. |
| **Level 2: Standard** | Level 1 plus struct, enum, trait, impl, pattern matching, error handling (try/catch/throw), and the standard library core modules. |
| **Level 3: Full** | Level 2 plus the compiler (native code generation), module system, package manager, FFI, async/await, and the complete standard library. |
| **Level 4: Extended** | Level 3 plus generic types, trait default methods, advanced pattern matching, and the documentation generator. |

---

## 2. Lexical Structure

### 2.1 Source Encoding

Mozhi source files are encoded in UTF-8. All lexical analysis operates on UTF-8 code points. Identifiers may contain Unicode letters and digits as defined by the Unicode General Categories Lu, Ll, Lt, Lm, Lo, and Nd. String literals may contain any valid UTF-8 sequence. A byte order mark (BOM) at the start of a source file is permitted but ignored.

### 2.2 Whitespace

Whitespace characters are the space (U+0020), horizontal tab (U+0009), carriage return (U+000D), and line feed (U+000A). Whitespace separates tokens but has no semantic meaning otherwise. Consecutive whitespace characters are treated as a single separator. Line feed (LF) and carriage return followed by line feed (CRLF) both terminate lines. The lexer reports line numbers starting from 1 for diagnostic purposes.

### 2.3 Comments

Mozhi supports two comment styles. Comments are ignored by the compiler and do not affect program semantics.

#### 2.3.1 Single-Line Comments

A single-line comment begins with the hash character `#` or double slash `//` and extends to the end of the line.

```mozhi
# This is a comment
x = 10  // Also a comment
# Comments can appear anywhere whitespace is allowed
```

#### 2.3.2 Multi-Line Comments

A multi-line comment begins with `/*` and ends with `*/`. Multi-line comments support nesting — a `/*` inside a comment starts a nested comment that must be closed with a matching `*/`. This allows commenting out blocks of code that already contain comments.

```mozhi
/* This is a
   multi-line comment */

/* Outer comment
   /* nested comment */
   still outer comment
*/
```

### 2.4 Identifiers

An identifier is a sequence of letters, digits, and underscores. The first character must be a letter or underscore. Identifiers are case-sensitive. There is no length limit on identifiers, but implementations may truncate for display in diagnostics.

```ebnf
identifier = letter { letter | digit | "_" } ;
letter     = "A".."Z" | "a".."z" | "_" | <unicode letter> ;
digit      = "0".."9" ;
```

**Valid identifiers:**

```mozhi
name
user_name
_private
Parser2
JSON_RPC_METHOD
```

**Invalid identifiers:**

```mozhi
2nd_value    # starts with digit
my-var       # contains hyphen
class        # reserved keyword
```

### 2.5 Keywords

The following identifiers are reserved as keywords and cannot be used as variable, function, type, or module names. Keywords are case-sensitive and must appear exactly as listed.

| | | | |
|---|---|---|---|
| `const` | `fn` | `if` | `else` |
| `match` | `while` | `for` | `in` |
| `break` | `continue` | `return` | `import` |
| `public` | `private` | `struct` | `enum` |
| `trait` | `impl` | `async` | `await` |
| `try` | `catch` | `throw` | `defer` |
| `true` | `false` | `null` | |

### 2.6 Literals

#### 2.6.1 Integer Literals

Integer literals are sequences of digits. Decimal (base 10) is the default. Hexadecimal literals begin with `0x` or `0X`. Octal literals begin with `0o` or `0O`. Binary literals begin with `0b` or `0B`. Underscores may be used as digit separators for readability and are ignored.

```mozhi
42
1_000_000
0xFF
0o755
0b1010_1010
```

#### 2.6.2 Float Literals

Float literals consist of an integer part, a decimal point, and a fractional part. Either the integer part or the fractional part may be omitted but not both. An optional exponent may follow, introduced by `e` or `E`, with an optional sign. Float literals are always 64-bit (`float64`) unless explicitly cast.

```mozhi
3.14
0.5
10.
.5
1.5e10
2.5e-3
```

#### 2.6.3 String Literals

String literals are sequences of characters enclosed in double quotes. String literals support escape sequences for special characters. Strings are immutable and UTF-8 encoded.

| Escape | Meaning |
|--------|---------|
| `\n` | Line feed |
| `\r` | Carriage return |
| `\t` | Horizontal tab |
| `\"` | Double quote |
| `\\` | Backslash |
| `\0` | Null character |
| `\uXXXX` | Unicode code point (4 hex digits) |

```mozhi
"Hello, World!"
"Line 1\nLine 2"
"Tab\there"
"Quote: \"hi\""
```

#### 2.6.4 Boolean Literals

Boolean literals are the keywords `true` and `false`. They evaluate to the boolean values TRUE and FALSE respectively.

#### 2.6.5 Null Literal

The keyword `null` represents the absence of a value. Null is a valid value for any nullable type.

### 2.7 Operators

#### 2.7.1 Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `a + b` |
| `-` | Subtraction | `a - b` |
| `*` | Multiplication | `a * b` |
| `/` | Division | `a / b` |
| `%` | Modulo (remainder) | `a % b` |
| `**` | Exponentiation | `a ** b` |

#### 2.7.2 Compound Assignment Operators

| Operator | Description | Equivalent To |
|----------|-------------|---------------|
| `+=` | Add and assign | `a = a + b` |
| `-=` | Subtract and assign | `a = a - b` |
| `*=` | Multiply and assign | `a = a * b` |
| `/=` | Divide and assign | `a = a / b` |
| `%=` | Modulo and assign | `a = a % b` |

#### 2.7.3 Comparison Operators

| Operator | Description |
|----------|-------------|
| `==` | Equal |
| `!=` | Not equal |
| `<` | Less than |
| `>` | Greater than |
| `<=` | Less than or equal |
| `>=` | Greater than or equal |

#### 2.7.4 Logical Operators

| Operator | Description | Short-circuit |
|----------|-------------|---------------|
| `and` | Logical AND | Yes — evaluates right only if left is true |
| `or` | Logical OR | Yes — evaluates right only if left is false |
| `not` | Logical NOT (prefix) | N/A — single operand |
| `!` | Logical NOT (prefix, symbol) | N/A |

### 2.8 Delimiters

| Delimiter | Description |
|-----------|-------------|
| `(` | Opening parenthesis (grouping, function call) |
| `)` | Closing parenthesis |
| `{` | Opening brace (block, struct literal) |
| `}` | Closing brace |
| `[` | Opening bracket (array literal, index) |
| `]` | Closing bracket |
| `,` | Comma (separator) |
| `;` | Semicolon (statement terminator, optional) |
| `:` | Colon (type annotation, key-value) |
| `::` | Double colon (module path separator) |
| `.` | Dot (member access, method call) |
| `->` | Arrow (return type annotation) |
| `=>` | Fat arrow (match arm, key-value) |

---

## 3. Grammar (EBNF)

This chapter defines the context-free grammar of Mozhi using Extended Backus-Naur Form (EBNF). The grammar is the authoritative definition of syntactically valid Mozhi programs. All conforming parsers must accept exactly the language defined by these productions.

### 3.1 Notation

The EBNF notation used in this specification follows these conventions:

- Non-terminal symbols are written in lowercase (e.g., *program*).
- Terminal symbols are written in monospace font (e.g., `fn`).
- Square brackets `[ ... ]` denote optional elements.
- Braces `{ ... }` denote zero or more repetitions.
- Parentheses `( ... )` group alternatives.
- The pipe `|` separates alternatives.
- A trailing `*` denotes zero or more, `+` denotes one or more.
- Quoted strings are literal terminal symbols.

### 3.2 Program Structure

```ebnf
program        = { declaration } ;

declaration    = import_decl
                | fn_decl
                | const_decl
                | struct_decl
                | enum_decl
                | trait_decl
                | impl_decl
                | statement ;
```

### 3.3 Import Declarations

```ebnf
import_decl    = "import" module_path ;

module_path    = identifier { "." identifier } ;
```

**Examples:**

```mozhi
import std.io
import std.math
import mylib.utils.string
```

### 3.4 Function Declarations

```ebnf
fn_decl        = [ visibility ] "fn" identifier
                  "(" [ param_list ] ")"
                  [ "->" type ]
                  block ;

visibility     = "public" | "private" ;

param_list     = param { "," param } ;

param          = identifier [ ":" type ] [ "=" expression ] ;

block          = "{" { statement } "}" ;
```

**Examples:**

```mozhi
fn add(a, b) {
    return a + b
}

fn greet(name: string) -> string {
    return "Hello, " + name
}

public fn main() {
    echo("Hello, Mozhi!")
}

fn with_default(a, b = 10) {
    return a + b
}
```

### 3.5 Constant Declarations

```ebnf
const_decl     = "const" identifier [ ":" type ] "=" expression ;
```

```mozhi
const PI = 3.14159
const MAX_SIZE: int = 1024
const GREETING = "Hello"
```

### 3.6 Variable Declarations

```ebnf
var_decl       = identifier [ ":" type ] "=" expression ;
```

Variables are declared by assignment. The type is inferred from the right-hand side expression unless an explicit type annotation is provided. A variable declared without an initial value must have an explicit type annotation.

```mozhi
name = "Mozhi"
age = 20
price = 99.99
active = true

# Explicit type annotation
count: int = 0
label: string = "default"
```

### 3.7 Struct Declarations

```ebnf
struct_decl    = [ visibility ] "struct" identifier
                  "{" { field_decl } "}" ;

field_decl     = [ visibility ] identifier ":" type ;
```

```mozhi
struct User {
    name: string
    age: int
    email: string
}

struct Point {
    x: float
    y: float
}
```

### 3.8 Enum Declarations

```ebnf
enum_decl      = [ visibility ] "enum" identifier
                  "{" { identifier } "}" ;
```

```mozhi
enum Color {
    Red
    Green
    Blue
}

enum Status {
    Pending
    Active
    Closed
}
```

### 3.9 Trait Declarations

```ebnf
trait_decl     = [ visibility ] "trait" identifier
                  "{" { fn_signature } "}" ;

fn_signature   = "fn" identifier "(" [ param_list ] ")"
                  [ "->" type ] ;
```

```mozhi
trait Drawable {
    fn draw()
    fn area() -> float
}

trait Serializable {
    fn serialize() -> string
    fn deserialize(data: string)
}
```

### 3.10 Impl Declarations

```ebnf
impl_decl      = "impl" identifier "for" identifier
                  "{" { fn_decl } "}" ;
```

```mozhi
impl Drawable for Circle {
    fn draw() {
        echo("Drawing circle")
    }

    fn area() -> float {
        return 3.14159 * radius * radius
    }
}
```

### 3.11 Statements

```ebnf
statement      = var_decl
                | assignment
                | if_stmt
                | while_stmt
                | for_stmt
                | match_stmt
                | return_stmt
                | break_stmt
                | continue_stmt
                | try_stmt
                | defer_stmt
                | throw_stmt
                | expression_stmt ;

assignment     = identifier ( "=" | "+=" | "-=" | "*=" | "/=" | "%=" )
                  expression ;

expression_stmt = expression ;
```

### 3.12 Control Flow Statements

```ebnf
if_stmt        = "if" expression block
                  { "else" "if" expression block }
                  [ "else" block ] ;

while_stmt     = "while" expression block ;

for_stmt       = "for" identifier "in" expression block
                | "for" [ assignment ] ";"
                  [ expression ] ";"
                  [ assignment ] block ;

match_stmt     = "match" expression "{" { match_arm } "}" ;

match_arm      = ( pattern | "_" ) "=>" ( block | expression ) ;

return_stmt    = "return" [ expression ] ;

break_stmt     = "break" ;

continue_stmt  = "continue" ;

try_stmt       = "try" block
                  [ "catch" [ identifier ] block ] ;

defer_stmt     = "defer" block ;

throw_stmt     = "throw" expression ;
```

### 3.13 Expressions

```ebnf
expression     = logical_or ;

logical_or     = logical_and { "or" logical_and } ;

logical_and    = equality { "and" equality } ;

equality       = comparison { ( "==" | "!=" ) comparison } ;

comparison     = addition { ( "<" | ">" | "<=" | ">=" ) addition } ;

addition       = multiplication { ( "+" | "-" ) multiplication } ;

multiplication = power { ( "*" | "/" | "%" ) power } ;

power          = unary { "**" unary } ;

unary          = ( "!" | "-" | "not" ) unary
                | postfix ;

postfix        = primary { call_or_access } ;

call_or_access = "(" [ arg_list ] ")"
                | "[" expression "]"
                | "." identifier [ "(" [ arg_list ] ")" ] ;

primary        = integer_lit
                | float_lit
                | string_lit
                | "true"
                | "false"
                | "null"
                | identifier
                | "(" expression ")"
                | array_lit
                | fn_expr
                | struct_lit ;

arg_list       = expression { "," expression } ;

array_lit      = "[" [ arg_list ] "]" ;

fn_expr        = "fn" "(" [ param_list ] ")" [ "->" type ] block ;

struct_lit     = identifier "{" { field_init } "}" ;

field_init     = identifier ":" expression { "," identifier ":" expression } ;
```

### 3.14 Patterns

```ebnf
pattern        = literal_pattern
                | identifier_pattern
                | wildcard_pattern
                | struct_pattern
                | enum_pattern ;

literal_pattern = integer_lit | float_lit | string_lit
                  | "true" | "false" | "null" ;

identifier_pattern = identifier ;

wildcard_pattern = "_" ;

struct_pattern = identifier "{" { field_pattern } "}" ;

field_pattern  = identifier ":" pattern ;

enum_pattern   = identifier "::" identifier ;
```

### 3.15 Types

```ebnf
type           = primitive_type
                | identifier
                | array_type
                | map_type
                | tuple_type
                | fn_type ;

primitive_type = "int" | "int8" | "int16" | "int32" | "int64"
                | "uint" | "uint8" | "uint16" | "uint32" | "uint64"
                | "float" | "float32" | "float64"
                | "bool" | "char" | "string" | "byte" ;

array_type     = "[" type "]" ;

map_type       = "map" "[" type "," type "]" ;

tuple_type     = "(" type { "," type } ")" ;

fn_type        = "fn" "(" [ type_list ] ")" [ "->" type ] ;

type_list      = type { "," type } ;
```

---

## 4. Type System

Mozhi employs a static, strong type system with automatic type inference. Types are checked at compile time, preventing type errors before runtime. Type annotations are optional in most contexts — the compiler infers types from usage. This chapter defines all types in Mozhi, the inference algorithm, and the rules governing type compatibility.

### 4.1 Primitive Types

Mozhi provides the following primitive types. Each has a fixed size and representation.

| Type | Size | Range | Default |
|------|------|-------|---------|
| `int8` | 1 byte | -128 to 127 | 0 |
| `int16` | 2 bytes | -32768 to 32767 | 0 |
| `int32` | 4 bytes | -2147483648 to 2147483647 | 0 |
| `int64` | 8 bytes | -9223372036854775808 to 9223372036854775807 | 0 |
| `int` | 8 bytes (64-bit) / 4 bytes (32-bit) | Platform-dependent | 0 |
| `uint8` | 1 byte | 0 to 255 | 0 |
| `uint16` | 2 bytes | 0 to 65535 | 0 |
| `uint32` | 4 bytes | 0 to 4294967295 | 0 |
| `uint64` | 8 bytes | 0 to 18446744073709551615 | 0 |
| `uint` | 8 bytes (64-bit) / 4 bytes (32-bit) | Platform-dependent | 0 |
| `float32` | 4 bytes | IEEE 754 single precision | 0.0 |
| `float64` | 8 bytes | IEEE 754 double precision | 0.0 |
| `float` | 8 bytes | Alias for float64 | 0.0 |
| `bool` | 1 byte | true or false | false |
| `char` | 4 bytes | Unicode code point (U+0000 to U+10FFFF) | U+0000 |
| `byte` | 1 byte | 0 to 255 (unsigned) | 0 |
| `string` | variable | UTF-8 encoded byte sequence | "" |

### 4.2 Integer Type Inference

Integer literals are inferred as `int` by default. If the literal exceeds the range of `int`, the type is promoted to `int64`. If the literal is negative and exceeds `int64`, the compiler reports an error (MZ1008). When an integer literal is assigned to a variable with an explicit narrower type annotation, the literal is checked against that type's range.

```mozhi
x = 42           # inferred as int
y = 0xFF         # inferred as int
z: int8 = 100    # explicitly int8
big = 9999999999 # inferred as int64 (exceeds int range on 32-bit)
```

### 4.3 Float Type Inference

Float literals are inferred as `float64` (aliased as `float`). If a float literal is assigned to a variable with an explicit `float32` annotation, the literal is checked for precision loss.

### 4.4 Boolean Type

The `bool` type represents truth values. The only valid values are `true` and `false`. Boolean values are produced by comparison operators (`==`, `!=`, `<`, `>`, `<=`, `>=`) and logical operators (`and`, `or`, `not`). Boolean values cannot be implicitly converted to or from integers.

### 4.5 String Type

The `string` type represents immutable UTF-8 encoded text. Strings support concatenation with the `+` operator. Strings have a length property accessible via the built-in `len()` function. Individual characters cannot be accessed via indexing — use the `char_at()` method or iterate with a for-in loop. String comparison uses lexicographic ordering based on UTF-8 byte sequences.

```mozhi
name = "Mozhi"
greeting = "Hello, " + name
length = len(name)  # 4

for ch in name {
    echo(ch)
}
```

### 4.6 Collection Types

#### 4.6.1 Array

Arrays are ordered, mutable collections of elements of the same type. Arrays are dynamically sized — they can grow and shrink at runtime. Array elements are accessed via zero-based indexing with square brackets. Arrays support `push()`, `pop()`, `len()`, and iteration with for-in.

```mozhi
nums = [1, 2, 3, 4, 5]
first = nums[0]    # 1
nums.push(6)       # nums is now [1, 2, 3, 4, 5, 6]
last = nums.pop()  # last = 6, nums is [1, 2, 3, 4, 5]
count = len(nums)  # 5
```

#### 4.6.2 Vector

Vectors are contiguous growable arrays, similar to arrays but with guaranteed contiguous memory layout. Vectors are preferred for numeric computations and FFI. Vectors support the same operations as arrays plus capacity management.

#### 4.6.3 Map

Maps are unordered collections of key-value pairs. Keys and values can be of any type. Map keys must be hashable (implement the Hash trait). Maps support insertion, lookup, deletion, and iteration.

```mozhi
ages = map {
    "Alice": 30,
    "Bob": 25,
    "Carol": 35
}

alice_age = ages["Alice"]  # 30
ages["Dave"] = 40          # add new entry
delete(ages, "Bob")        # remove entry
```

#### 4.6.4 Set

Sets are unordered collections of unique values. Set elements must be hashable. Sets support membership testing, union, intersection, and difference.

#### 4.6.5 Tuple

Tuples are fixed-size, heterogeneous collections. Tuple elements can be of different types. Tuples are immutable. Tuple elements are accessed by position using dot notation.

```mozhi
point = (10, 20)
x = point.0  # 10
y = point.1  # 20

person = ("Alice", 30, true)
name = person.0  # "Alice"
```

### 4.7 Type Inference Algorithm

Mozhi uses a bidirectional type inference algorithm. The algorithm works in two phases: type synthesis (bottom-up) and type checking (top-down). In synthesis mode, the type of an expression is determined from its sub-expressions. In checking mode, an expected type is pushed down from the context and the expression is checked against it. This allows the compiler to infer types in most situations without requiring explicit annotations.

#### 4.7.1 Variable Declaration Inference

When a variable is declared with `name = expression` and no type annotation, the type is synthesized from the expression:

```mozhi
x = 42         # int (synthesized from integer literal)
y = 3.14       # float (synthesized from float literal)
z = "hello"    # string
flag = true    # bool
items = [1, 2] # [int] (element type inferred from first element)
pair = (1, "a") # (int, string)
```

#### 4.7.2 Function Return Type Inference

If a function declaration omits the return type annotation, the compiler infers the return type from the return statements in the function body. All return statements must return values of compatible types. If the function has no return statements, the return type is void (unit).

#### 4.7.3 Generic Type Inference

When calling a generic function, type parameters are inferred from the argument types. If inference is ambiguous, the programmer must provide explicit type arguments.

### 4.8 Type Compatibility

Types are compatible if they are identical, or if an implicit conversion exists between them. Mozhi allows implicit widening conversions between numeric types where no precision is lost. Narrowing conversions require explicit casts.

| From | To | Conversion |
|------|-----|-----------|
| `int8` | `int16 / int32 / int64` | Implicit (widening) |
| `int16` | `int32 / int64` | Implicit (widening) |
| `int32` | `int64` | Implicit (widening) |
| `uint8` | `uint16 / uint32 / uint64` | Implicit (widening) |
| `float32` | `float64` | Implicit (widening) |
| `int` | `float` | Implicit (widening) |
| `int64` | `int32` | Explicit cast required |
| `float64` | `float32` | Explicit cast required (may lose precision) |
| `float` | `int` | Explicit cast required (truncates) |
| `int` | `uint` | Explicit cast required (may change sign) |

### 4.9 Explicit Type Casts

Explicit type casts use the target type as a function call. Casts that would lose data emit a warning (MZ2003) unless suppressed.

```mozhi
x = 3.99
y = int(x)        # 3 (truncates)

n = 65
c = char(n)       # 'A'

s = "42"
num = int(s)      # 42 (parses string)

big = 1000
small = int8(big) # MZ2003 warning: narrowing cast may lose data
```

### 4.10 Nullable Types

By default, all types are non-nullable. A variable of type `T` cannot hold the value `null`. To allow null, use the optional type modifier: `T?` (read as "T or null"). Nullable types must be checked before access using pattern matching or the null-coalescing operator.

```mozhi
name: string? = null

if name != null {
    echo("Hello, " + name)
} else {
    echo("No name provided")
}

# Null-coalescing operator
display = name ?? "Anonymous"
```

---

## 5. Variables and Constants

### 5.1 Variable Declaration

Variables in Mozhi are declared by assignment. The syntax `name = expression` creates a new variable in the current scope, infers its type from the expression, and binds the value. A variable must be declared before it is used. Redeclaring a variable in the same scope shadows the previous declaration and emits a warning (MZ2002).

```mozhi
name = "Mozhi"
age = 20
price = 99.99
active = true
```

### 5.2 Explicit Type Annotations

An explicit type annotation can be provided using the colon syntax: `name: type = expression`. The expression's type must be compatible with the annotated type. If the types are incompatible, the compiler reports an error (MZ1003).

```mozhi
count: int = 0
label: string = "default"
ratio: float = 3.14
flag: bool = true
```

### 5.3 Variable Assignment

An existing variable can be reassigned using the `=` operator. The new value must be type-compatible with the variable's declared type. Compound assignment operators (`+=`, `-=`, `*=`, `/=`, `%=`) combine an arithmetic operation with assignment.

```mozhi
x = 10
x = 20          # reassignment
x += 5          # x is now 25
x -= 10         # x is now 15
x *= 2          # x is now 30
x /= 3          # x is now 10
x %= 3          # x is now 1
```

### 5.4 Constant Declaration

Constants are declared with the `const` keyword. Constants must be initialized at declaration with a value that is a compile-time constant. Constants cannot be reassigned after declaration. Attempted reassignment of a constant produces an error (MZ1004).

```mozhi
const PI = 3.14159
const MAX_SIZE = 1024
const GREETING = "Hello, Mozhi!"
const BUFFER_SIZE: int = 4096
```

### 5.5 Scope Rules

Mozhi uses lexical scoping. A variable's scope is the block in which it is declared, from the point of declaration to the end of the block. Variables declared in an inner block shadow variables with the same name in outer blocks. Variables declared in a block are not accessible outside that block.

```mozhi
x = 10  # outer x

if true {
    x = 20      # modifies outer x
    y = 30      # y is local to this block
    echo(x, y)  # 20 30
}

echo(x)  # 20
# echo(y)  # MZ1001: y is not defined here
```

### 5.6 Block Scopes

The following constructs introduce new scopes:

| Construct | Scope Behavior |
|-----------|---------------|
| Function body | Variables declared inside a function are local to that function. |
| If/else blocks | Each if and else block has its own scope. |
| While loops | Each iteration creates a new scope for the loop body. |
| For loops | The loop variable and variables in the body are scoped to the loop. |
| Match arms | Each match arm has its own scope. |
| Try/catch blocks | The try and catch blocks each have their own scope. |
| Defer blocks | Defer blocks have their own scope, capturing variables by value. |

### 5.7 Lifetime

A variable's lifetime is the duration for which it is valid and accessible. Variables declared on the stack are destroyed when their scope exits. Variables allocated on the heap (via dynamic allocation) are managed by the garbage collector. The compiler tracks lifetimes to prevent use-after-free and dangling reference errors.

### 5.8 Mutability

By default, all variables are mutable — their values can be changed after declaration. Constants declared with `const` are immutable. Struct fields are mutable by default but can be made immutable using the `const` modifier on the field declaration. Function parameters are mutable by default — the function can reassign them locally without affecting the caller's variables.

---

## 6. Functions

### 6.1 Function Declaration

Functions are declared with the `fn` keyword followed by a name, parameter list, optional return type, and body block. Functions are first-class values — they can be assigned to variables, passed as arguments, and returned from other functions. A function declaration introduces the function name into the enclosing scope.

```mozhi
fn add(a, b) {
    return a + b
}

fn greet(name: string) -> string {
    return "Hello, " + name
}

fn print_message(msg: string) {
    echo(msg)
}
```

### 6.2 Parameters

Parameters are declared as a comma-separated list of names with optional type annotations. Parameters with type annotations are checked at the call site. Parameters without annotations use type inference from the call site. Default parameter values can be specified with the `=` syntax.

```mozhi
fn compute(a: int, b: int, op: string = "add") {
    if op == "add" {
        return a + b
    }
    return a * b
}

result1 = compute(2, 3)              # 5 (uses default op)
result2 = compute(2, 3, "multiply")  # 6
```

### 6.3 Return Values

Functions return values using the `return` statement. If a function has a declared return type, the return expression must be type-compatible. If no return type is declared, the compiler infers it from the return statements. A function with no return statement returns `null` (the unit value). A return statement with no expression returns `null`.

### 6.4 Anonymous Functions

Anonymous functions (lambdas) are declared with `fn` followed by a parameter list and body, without a name. Anonymous functions can be assigned to variables, passed as arguments, or returned from functions. Anonymous functions capture variables from their enclosing scope by reference (closures).

```mozhi
add = fn(a, b) {
    return a + b
}

result = add(3, 4)  # 7

# Inline anonymous function as argument
nums = [1, 2, 3]
doubled = map(nums, fn(x) { return x * 2 })
```

### 6.5 Closures

A closure is a function that captures variables from its enclosing scope. Closures capture variables by reference — modifications to captured variables inside the closure affect the outer scope. Closures can outlive the scope in which they were created; captured variables remain valid as long as the closure exists.

```mozhi
fn make_counter() {
    count = 0
    return fn() {
        count += 1
        return count
    }
}

counter = make_counter()
echo(counter())  # 1
echo(counter())  # 2
echo(counter())  # 3
```

### 6.6 Higher-Order Functions

Higher-order functions are functions that take other functions as parameters or return functions. Mozhi supports higher-order functions natively. The standard library provides common higher-order functions like `map`, `filter`, and `reduce`.

```mozhi
fn apply(f, x) {
    return f(x)
}

double = fn(x) { return x * 2 }
result = apply(double, 5)  # 10
```

### 6.7 Recursion

Functions can call themselves recursively. Recursive functions must have a base case to terminate recursion. The compiler does not guarantee tail-call optimization; deep recursion may cause stack overflow. For guaranteed stack-safe recursion, use the trampoline pattern or iterative loops.

```mozhi
fn factorial(n) {
    if n <= 1 {
        return 1
    }
    return n * factorial(n - 1)
}

fn fibonacci(n) {
    if n <= 1 {
        return n
    }
    return fibonacci(n - 1) + fibonacci(n - 2)
}

echo(factorial(5))    # 120
echo(fibonacci(10))   # 55
```

### 6.8 Function Visibility

Functions can be declared with `public` or `private` visibility. Public functions are accessible from other modules that import the declaring module. Private functions are only accessible within the declaring module. If no visibility modifier is specified, the function is private by default.

```mozhi
public fn api_function() {
    echo("This is public")
    helper()
}

private fn helper() {
    echo("This is private")
}
```

---

## 7. Control Flow

### 7.1 If Statements

The `if` statement conditionally executes a block based on a boolean expression. An optional `else` block executes when the condition is false. Multiple conditions can be chained using `else if`. The condition expression must evaluate to a `bool`; implicit truthiness is not supported.

```mozhi
age = 20

if age >= 18 {
    echo("Adult")
} else if age >= 13 {
    echo("Teenager")
} else {
    echo("Child")
}
```

### 7.2 While Loops

The `while` loop repeatedly executes a block as long as a condition is true. The condition is evaluated before each iteration. If the condition is initially false, the block is never executed. The `break` statement exits the loop early; the `continue` statement skips to the next iteration.

```mozhi
i = 0
while i < 10 {
    if i == 5 {
        break
    }
    if i % 2 == 0 {
        i += 1
        continue
    }
    echo(i)
    i += 1
}
```

### 7.3 For Loops (C-Style)

The C-style `for` loop has three parts separated by semicolons: an initializer, a condition, and an increment. The initializer executes once before the loop. The condition is evaluated before each iteration. The increment executes after each iteration. All three parts are optional.

```mozhi
sum = 0
for i = 0; i < 10; i += 1 {
    sum += i
}
echo(sum)  # 45
```

### 7.4 For-In Loops

The `for-in` loop iterates over elements of a collection. It works with arrays, vectors, maps, sets, and any type implementing the Iterable trait. The loop variable is bound to each element in sequence. Modifying the collection during iteration produces undefined behavior.

```mozhi
fruits = ["apple", "banana", "cherry"]
for fruit in fruits {
    echo(fruit)
}

# Iterating a map
ages = map { "Alice": 30, "Bob": 25 }
for name in ages {
    echo(name, ages[name])
}
```

### 7.5 Match Statements

The `match` statement compares a value against a series of patterns and executes the first matching arm. Each arm consists of a pattern, the `=>` operator, and a body (either a block or a single expression). The `_` pattern (wildcard) matches any value and serves as a default case. Match expressions must be exhaustive — if no default arm is provided, the compiler warns about non-exhaustive matching (MZ2004).

```mozhi
x = 2

match x {
    1 => echo("One")
    2 => echo("Two")
    3 => echo("Three")
    _ => echo("Other")
}
```

### 7.6 Break and Continue

The `break` statement immediately exits the enclosing loop. The `continue` statement skips the rest of the current iteration and proceeds to the next. Both statements only affect the innermost loop. Using `break` or `continue` outside a loop is a compile error (MZ1005).

### 7.7 Return

The `return` statement exits the current function and optionally returns a value. A `return` without an expression returns `null`. Using `return` outside a function is a compile error (MZ1006).

### 7.8 Defer

The `defer` statement schedules a block to execute when the enclosing function returns, regardless of how the function exits (normal return, error, or panic). Deferred blocks execute in last-in-first-out (LIFO) order. Defer is commonly used for resource cleanup (closing files, releasing locks).

```mozhi
fn process_file(path) {
    file = open(path)
    defer {
        close(file)
    }

    # Process file contents
    data = read(file)
    return parse(data)
    # close(file) executes here, before function returns
}
```

---

## 8. Composite Types

### 8.1 Struct

A struct is a composite data type that groups named fields. Structs are declared with the `struct` keyword followed by a name and a block containing field declarations. Each field has a name and a type. Struct instances are created with struct literals that specify field values.

```mozhi
struct User {
    name: string
    age: int
    email: string
}

user = User {
    name: "Alice"
    age: 30
    email: "alice@example.com"
}

echo(user.name)  # Alice
echo(user.age)   # 30
```

### 8.2 Enum

An enum is a type that can hold one of several named variants. Enums are declared with the `enum` keyword followed by a name and a block listing the variants. Enum variants are accessed using the `::` operator. Enums are commonly used with match statements for exhaustive handling.

```mozhi
enum Color {
    Red
    Green
    Blue
}

enum Status {
    Pending
    Active
    Closed
}

c = Color::Red
match c {
    Color::Red => echo("Red")
    Color::Green => echo("Green")
    Color::Blue => echo("Blue")
}
```

### 8.3 Trait

A trait defines a set of method signatures that a type can implement. Traits are declared with the `trait` keyword followed by a name and a block of method signatures. Traits do not contain implementations — they define a contract that implementing types must fulfill. Types implement traits using the `impl` keyword.

```mozhi
trait Drawable {
    fn draw()
    fn area() -> float
}

trait Comparable {
    fn compare(other) -> int
}
```

### 8.4 Impl

The `impl` block provides method implementations for a type to satisfy a trait. The syntax is `impl TraitName for TypeName` followed by a block of method implementations. All methods declared in the trait must be implemented. A type can implement multiple traits via separate impl blocks.

```mozhi
struct Circle {
    radius: float
}

impl Drawable for Circle {
    fn draw() {
        echo("Drawing circle")
    }

    fn area() -> float {
        return 3.14159 * radius * radius
    }
}

c = Circle { radius: 5.0 }
c.draw()         # Drawing circle
echo(c.area())   # 78.54
```

### 8.5 Method Calls

Methods are functions associated with a type. Methods are called using dot notation: `object.method(args)`. Inside a method, the receiver object is accessible via the implicit `self` parameter. The first parameter of a method is implicitly the receiver type.

---

## 9. Pattern Matching

### 9.1 Match Expression

The `match` expression is Mozhi's primary pattern matching construct. It evaluates a scrutinee expression and compares it against a series of patterns, executing the body of the first matching arm. Match is an expression — it evaluates to the value of the matched arm's body. This makes match useful for conditional value assignment.

```mozhi
x = 2
description = match x {
    1 => "one"
    2 => "two"
    3 => "three"
    _ => "many"
}
echo(description)  # two
```

### 9.2 Literal Patterns

Literal patterns match exact values. Integer, float, string, boolean, and null literals can all be used as patterns. The match is by value equality.

```mozhi
status = "active"
match status {
    "active" => echo("User is active")
    "inactive" => echo("User is inactive")
    "banned" => echo("User is banned")
    _ => echo("Unknown status")
}
```

### 9.3 Variable Patterns

A variable pattern binds the matched value to a variable. Variable patterns match any value. Variable patterns are useful for capturing the scrutinee value in a catch-all arm.

```mozhi
x = 42
match x {
    0 => echo("zero")
    n => echo("non-zero: ", n)  # n captures x
}
```

### 9.4 Wildcard Pattern

The `_` (underscore) pattern matches any value without binding it. It is used as a default case at the end of a match. Only one wildcard arm is permitted per match, and it must be the last arm.

### 9.5 Struct Patterns

Struct patterns match struct values and can bind field values to variables. The pattern uses the struct name followed by field patterns in braces. Partial matching is supported — unnamed fields are ignored.

```mozhi
struct Point { x: float, y: float }

p = Point { x: 1.0, y: 2.0 }
match p {
    Point { x: 0, y: 0 } => echo("origin")
    Point { x, y } => echo("point at ", x, ", ", y)
}
```

### 9.6 Enum Patterns

Enum patterns match specific enum variants. The pattern uses the enum name, the `::` operator, and the variant name. Enum patterns with associated data can bind the data to variables.

```mozhi
enum Shape {
    Circle(float)
    Square(float)
    Rectangle(float, float)
}

shape = Shape::Circle(5.0)
match shape {
    Shape::Circle(r) => echo("circle, radius=", r)
    Shape::Square(s) => echo("square, side=", s)
    Shape::Rectangle(w, h) => echo("rect ", w, "x", h)
}
```

### 9.7 Pattern Guards

A pattern guard is an additional condition that must be true for the arm to match. Guards are introduced with the `if` keyword after the pattern. Guards allow more complex matching logic without splitting into multiple arms.

```mozhi
x = 15
match x {
    n if n < 10 => echo("small")
    n if n < 100 => echo("medium")
    _ => echo("large")
}
```

### 9.8 Exhaustiveness Checking

The compiler checks that match expressions are exhaustive — every possible value of the scrutinee type must be handled by some arm. For enums, all variants must be covered (unless a wildcard arm is present). For integers and strings, a wildcard arm is required for exhaustiveness. Non-exhaustive matches produce a warning (MZ2004) unless the scrutinee type is open-ended.

---

## 10. Error Handling

### 10.1 Try/Catch

The `try/catch` construct handles errors (exceptions) that occur during execution. The `try` block contains code that may produce an error. The `catch` block executes if an error is thrown within the try block. The caught error is bound to an optional variable for inspection.

```mozhi
try {
    file = open("config.json")
    data = read(file)
    close(file)
    config = parse_json(data)
} catch err {
    echo("Failed to load config: ", err.message)
    config = default_config()
}
```

### 10.2 Throw

The `throw` statement raises an error, immediately transferring control to the nearest enclosing catch block. If no catch block is found, the error propagates to the top level and the program terminates with an uncaught error panic. The thrown value can be of any type, but using the Error type is recommended.

```mozhi
fn divide(a, b) {
    if b == 0 {
        throw Error { message: "Division by zero" }
    }
    return a / b
}
```

### 10.3 Error Type

The `Error` type is the standard error type in Mozhi. It contains a `message` field (string) and an optional `code` field (int). Custom error types can be created by implementing the Error trait. Error types should provide a clear, human-readable message.

```mozhi
struct Error {
    message: string
    code: int
}

fn validate_age(age) {
    if age < 0 {
        throw Error {
            message: "Age cannot be negative"
            code: 1001
        }
    }
    if age > 150 {
        throw Error {
            message: "Age is unreasonably large"
            code: 1002
        }
    }
}
```

### 10.4 Error Propagation

Errors propagate up the call stack until a catch block handles them. If a function does not catch an error thrown within it, the error propagates to the caller. If no caller handles the error, the program terminates with a panic. Functions that may throw should document this in their type signature.

### 10.5 Panic

A panic is an unrecoverable error that terminates the program immediately. Panics occur when the runtime detects an invalid state (null pointer dereference, stack overflow, out of memory). Panics print a stack trace to stderr and exit with code 1. Panics cannot be caught by try/catch — use `throw` for recoverable errors.

### 10.6 Error Codes

Mozhi uses a standardized error code system. Error codes are formatted as `SNxNNN` where `x` is the category and `NNN` is the specific error. Error codes are used in diagnostics and can be looked up in the documentation.

| Code Range | Category | Description |
|-----------|----------|-------------|
| MZ1xxx | Parse errors | Syntax errors, invalid tokens, malformed expressions |
| MZ2xxx | Type errors | Type mismatches, undefined variables, scope errors |
| MZ3xxx | Runtime errors | Null dereference, index out of bounds, division by zero |
| MZ4xxx | I/O errors | File not found, permission denied, network errors |
| MZ5xxx | Link errors | Undefined symbols, duplicate symbols, missing libraries |
| MZ6xxx | Module errors | Module not found, circular imports, visibility errors |
| MZ7xxx | FFI errors | ABI mismatches, marshalling failures, dangling pointers |
| MZ8xxx | Concurrency errors | Deadlock, race condition, channel closed |
| MZ9xxx | Internal errors | Compiler bugs, unexpected state |

---

## 11. Module System

### 11.1 Modules

A module is a unit of code organization. Each source file is a module. A directory containing source files can form a package, with each file being a submodule. Modules encapsulate code and control visibility of declarations.

### 11.2 Import

The `import` statement brings declarations from another module into the current scope. The import path uses dots to separate module components. Imported names are accessible without qualification if they are public.

```mozhi
import std.io
import std.math
import mylib.utils.string

# Use imported functions
echo("Hello")  # from std.io
result = sqrt(16)  # from std.math
```

### 11.3 Visibility

Declarations can be marked `public` or `private`. Public declarations are accessible from any module that imports the declaring module. Private declarations are only accessible within the declaring module. The default visibility is private.

```mozhi
# public: accessible from other modules
public fn api_function() {
    helper()
}

# private: only accessible in this module
private fn helper() {
    echo("internal helper")
}

# no modifier: defaults to private
fn another_helper() {
    echo("also private")
}
```

### 11.4 Module Resolution

Module paths are resolved in the following order:

| Step | Description |
|------|-------------|
| 1. Standard library | Paths starting with `std.` are resolved from the Mozhi standard library installation. |
| 2. Local modules | Paths not starting with `std.` are resolved from the project's source directory. |
| 3. Package dependencies | If not found locally, the resolver checks installed package dependencies. |
| 4. Global cache | If not in a package, the resolver checks the global module cache at `~/.mozhi/cache/`. |

### 11.5 Namespaces

Modules create namespaces for their declarations. Two modules can declare functions with the same name without conflict. To access a declaration from a specific module, use the module path: `module.function()`. The import statement can optionally alias a module: `import std.math as m`.

---

## 12. Standard Library

The Mozhi standard library provides a comprehensive set of modules for common programming tasks. All standard library modules are accessible via the `std.` prefix. This chapter documents the available modules and their key functions.

### 12.1 std.core

Core language primitives and built-in functions.

| Function | Signature | Description |
|----------|-----------|-------------|
| `echo` | `echo(...args)` | Print values to stdout |
| `print` | `print(...args)` | Same as echo |
| `len` | `len(x) -> int` | Length of array, string, or map |
| `typeof` | `typeof(x) -> string` | Type name as string |
| `int` | `int(x) -> int` | Convert to integer |
| `float` | `float(x) -> float` | Convert to float |
| `string` | `string(x) -> string` | Convert to string |
| `bool` | `bool(x) -> bool` | Convert to boolean |
| `char` | `char(n) -> char` | Convert code point to char |
| `push` | `push(arr, val)` | Append element to array |
| `pop` | `pop(arr) -> value` | Remove and return last element |

### 12.2 std.io

Input/output operations.

| Function | Signature | Description |
|----------|-----------|-------------|
| `echo` | `echo(...args)` | Print to stdout |
| `input` | `input(prompt) -> string` | Read line from stdin |
| `open` | `open(path) -> File` | Open file for reading |
| `close` | `close(file)` | Close a file |
| `read` | `read(file) -> string` | Read entire file contents |
| `write` | `write(file, data)` | Write data to file |
| `readline` | `readline(file) -> string` | Read one line from file |
| `writeline` | `writeline(file, data)` | Write line with newline |

### 12.3 std.fs

Filesystem operations.

| Function | Signature | Description |
|----------|-----------|-------------|
| `exists` | `exists(path) -> bool` | Check if path exists |
| `is_file` | `is_file(path) -> bool` | Check if path is a file |
| `is_dir` | `is_dir(path) -> bool` | Check if path is a directory |
| `mkdir` | `mkdir(path)` | Create directory |
| `rmdir` | `rmdir(path)` | Remove empty directory |
| `remove` | `remove(path)` | Delete file |
| `rename` | `rename(old, new)` | Rename or move file |
| `copy` | `copy(src, dst)` | Copy file |
| `listdir` | `listdir(path) -> [string]` | List directory contents |

### 12.4 std.math

Mathematical functions.

| Function | Signature | Description |
|----------|-----------|-------------|
| `sqrt` | `sqrt(x) -> float` | Square root |
| `abs` | `abs(x) -> number` | Absolute value |
| `floor` | `floor(x) -> int` | Floor to integer |
| `ceil` | `ceil(x) -> int` | Ceiling to integer |
| `round` | `round(x) -> int` | Round to nearest integer |
| `pow` | `pow(base, exp) -> float` | Exponentiation |
| `sin` | `sin(x) -> float` | Sine (radians) |
| `cos` | `cos(x) -> float` | Cosine (radians) |
| `tan` | `tan(x) -> float` | Tangent (radians) |
| `log` | `log(x) -> float` | Natural logarithm |
| `log10` | `log10(x) -> float` | Base-10 logarithm |
| `min` | `min(a, b) -> number` | Minimum of two values |
| `max` | `max(a, b) -> number` | Maximum of two values |

### 12.5 std.string

String manipulation functions.

| Function | Signature | Description |
|----------|-----------|-------------|
| `len` | `len(s) -> int` | String length |
| `upper` | `upper(s) -> string` | Convert to uppercase |
| `lower` | `lower(s) -> string` | Convert to lowercase |
| `trim` | `trim(s) -> string` | Remove leading/trailing whitespace |
| `split` | `split(s, sep) -> [string]` | Split string by separator |
| `join` | `join(arr, sep) -> string` | Join array with separator |
| `contains` | `contains(s, sub) -> bool` | Check if string contains substring |
| `replace` | `replace(s, old, new) -> string` | Replace all occurrences |
| `substring` | `substring(s, start, end) -> string` | Extract substring |
| `reverse` | `reverse(s) -> string` | Reverse string |
| `starts_with` | `starts_with(s, prefix) -> bool` | Check prefix |
| `ends_with` | `ends_with(s, suffix) -> bool` | Check suffix |

### 12.6 std.time

Time and date functions.

| Function | Signature | Description |
|----------|-----------|-------------|
| `now` | `now() -> int` | Current Unix timestamp (seconds) |
| `now_ms` | `now_ms() -> int` | Current time in milliseconds |
| `sleep` | `sleep(seconds)` | Pause execution |
| `format_time` | `format_time(ts, fmt) -> string` | Format timestamp |
| `parse_time` | `parse_time(s, fmt) -> int` | Parse time string |

### 12.7 std.json

JSON encoding and decoding.

| Function | Signature | Description |
|----------|-----------|-------------|
| `parse` | `parse(s) -> value` | Parse JSON string |
| `stringify` | `stringify(v) -> string` | Convert value to JSON string |
| `stringify_pretty` | `stringify_pretty(v, indent) -> string` | Pretty-print JSON |

### 12.8 std.http

HTTP client.

| Function | Signature | Description |
|----------|-----------|-------------|
| `get` | `get(url) -> Response` | HTTP GET request |
| `post` | `post(url, body) -> Response` | HTTP POST request |
| `put` | `put(url, body) -> Response` | HTTP PUT request |
| `delete` | `delete(url) -> Response` | HTTP DELETE request |

### 12.9 std.crypto

Cryptographic functions.

| Function | Signature | Description |
|----------|-----------|-------------|
| `md5` | `md5(data) -> string` | MD5 hash (hex) |
| `sha256` | `sha256(data) -> string` | SHA-256 hash (hex) |
| `sha512` | `sha512(data) -> string` | SHA-512 hash (hex) |
| `hmac` | `hmac(key, data) -> string` | HMAC-SHA256 |
| `base64_encode` | `base64_encode(data) -> string` | Base64 encode |
| `base64_decode` | `base64_decode(s) -> bytes` | Base64 decode |

### 12.10 std.regex

Regular expressions.

| Function | Signature | Description |
|----------|-----------|-------------|
| `match` | `match(pattern, s) -> bool` | Check if pattern matches |
| `find` | `find(pattern, s) -> [string]` | Find all matches |
| `replace` | `replace(pattern, s, repl) -> string` | Replace matches |
| `split` | `split(pattern, s) -> [string]` | Split by pattern |

### 12.11 std.thread

Threading and concurrency.

| Function | Signature | Description |
|----------|-----------|-------------|
| `spawn` | `spawn(fn) -> Thread` | Start new thread |
| `join` | `join(thread)` | Wait for thread to finish |
| `sleep` | `sleep(seconds)` | Sleep current thread |
| `channel` | `channel() -> Channel` | Create communication channel |
| `send` | `send(ch, value)` | Send value to channel |
| `recv` | `recv(ch) -> value` | Receive value from channel |

### 12.12 std.process

Process and system operations.

| Function | Signature | Description |
|----------|-----------|-------------|
| `exec` | `exec(cmd) -> Result` | Execute system command |
| `exit` | `exit(code)` | Exit program with code |
| `getenv` | `getenv(name) -> string` | Get environment variable |
| `setenv` | `setenv(name, value)` | Set environment variable |
| `args` | `args() -> [string]` | Get command-line arguments |

---

## 13. Foreign Function Interface

### 13.1 extern Keyword

The `extern` keyword declares a function implemented in a foreign language. The function signature specifies the Mozhi types for parameters and return value; the actual implementation is in a linked native library. Foreign functions use the C calling convention by default.

```mozhi
extern fn c_add(a: int, b: int) -> int
extern fn c_sqrt(x: float) -> float
extern fn c_strlen(s: string) -> int
```

### 13.2 Type Marshalling

Mozhi types are marshalled to and from native types at the FFI boundary. The following table defines the type correspondences:

| Mozhi Type | Native Type | Notes |
|-----------|-------------|-------|
| `int` | `int64_t` | 64-bit signed integer |
| `int32` | `int32_t` | 32-bit signed integer |
| `uint` | `uint64_t` | 64-bit unsigned integer |
| `float` | `double` | 64-bit IEEE float |
| `float32` | `float` | 32-bit IEEE float |
| `bool` | `bool / int8_t` | 1-byte boolean |
| `char` | `uint32_t` | Unicode code point |
| `string` | `const char*` | Null-terminated UTF-8 |
| `byte` | `uint8_t` | Raw byte |
| `pointer` | `void*` | Raw pointer (unsafe) |

### 13.3 Supported Backend Languages

Mozhi's FFI supports the following backend languages. Each requires its respective compiler to be installed.

| Language | File Extension | Compiler | Notes |
|----------|---------------|----------|-------|
| C | `.c` | cc / gcc / clang | Direct linking, C ABI |
| C++ | `.cpp` | c++ / g++ / clang++ | Requires `extern "C"` wrapper |
| Assembly | `.S` | cc / gcc / clang | Platform-specific (x86_64/ARM64) |
| Rust | `.rs` | rustc | Requires `#[no_mangle]` and `extern "C"` |

### 13.4 Memory Ownership

When passing data across the FFI boundary, ownership rules apply. Primitive types (int, float, bool) are passed by value — no ownership concerns. Strings are passed as `const char*` (read-only) — the foreign code must not modify or free the string. Arrays and structs require explicit marshalling functions. Pointers returned from foreign code must be explicitly freed by the caller.

---

## 14. Compiler and Interpreter

### 14.1 Compilation Pipeline

The Mozhi compiler transforms source code into native executables through a multi-stage pipeline. Each stage transforms the program representation and may report errors. The pipeline is designed for fast compilation and comprehensive error reporting.

```
Source Code (.mz)
       |
       v
  [1. Lexer]      -- Tokenizes source text
       |
       v
  [2. Parser]     -- Builds AST from tokens
       |
       v
  [3. Analyzer]   -- Semantic analysis
       |
       v
  [4. Type Checker] -- Static type checking
       |
       v
  [5. Optimizer]  -- Optimization passes
       |
       v
  [6. Code Gen]   -- Generate native code
       |
       v
  [7. Linker]     -- Link into executable
```

### 14.2 Lexical Analysis

The lexer converts source text into a stream of tokens. It handles whitespace, comments, and produces tokens with line/column information for diagnostics. Lexical errors (illegal characters) are reported at this stage.

### 14.3 Parsing

The parser consumes the token stream and builds an Abstract Syntax Tree (AST) according to the grammar in Chapter 3. The parser is a recursive descent parser with Pratt-style expression parsing for operator precedence. Syntax errors (malformed constructs) are reported at this stage.

### 14.4 Semantic Analysis

The analyzer walks the AST and performs semantic checks: variable scope resolution, function signature validation, struct/enum/trait registration, and module import resolution. Semantic errors (undefined names, scope violations) are reported at this stage.

### 14.5 Type Checking

The type checker applies the type rules from Chapter 4 to every expression and statement. It performs type inference, checks compatibility, and verifies exhaustiveness of match expressions. Type errors (MZ2xxx) are reported at this stage.

### 14.6 Optimization

The optimizer applies transformation passes to improve performance without changing program semantics. Optimization passes include:

| Pass | Description |
|------|-------------|
| Constant folding | Evaluate constant expressions at compile time. |
| Dead code elimination | Remove unreachable code and unused variables. |
| Function inlining | Inline small functions at call sites. |
| Common subexpression elimination | Reuse results of identical computations. |
| Loop optimization | Hoist invariant code out of loops, unroll small loops. |
| Tail call optimization | Convert tail-recursive calls to loops where possible. |

### 14.7 Code Generation

The code generator translates the optimized AST into native machine code. On x86_64, it generates x86-64 assembly. On ARM64, it generates AArch64 assembly. The generated assembly is assembled into object files (.o) by the system assembler.

### 14.8 Linking

The linker combines object files and libraries into the final executable. It resolves symbols, performs relocation, and produces the output file. Link errors (MZ5xxx) are reported at this stage.

### 14.9 Interpreter Mode

For rapid development, Mozhi provides an interpreter that executes source code directly without compilation. The interpreter builds the AST and walks it, evaluating expressions and executing statements in real time. The interpreter is used by the REPL and for running scripts. Interpreter behavior matches compiled behavior for all defined semantics.

### 14.10 Bytecode Format

An intermediate representation between interpretation and native compilation is the Mozhi bytecode format. Bytecode is a compact, portable representation that can be executed by a virtual machine or further compiled to native code. Bytecode files use the `.sibc` extension. This format enables fast startup (no parsing overhead) and portability across architectures.

---

## 15. Package Manager (mzpkg)

The Mozhi Package Manager (`mzpkg`) is a CLI tool for installing, searching, publishing, and managing Mozhi packages and tools. It connects to the pkgs-mz cloud registry at https://pkgs-mz.vercel.app.

### 15.1 Installation

Install mzpkg with a single command:

```bash
curl -fsSL https://pkgs-mz.vercel.app/install.sh | bash
source ~/.bashrc
```

This installs the CLI to `~/.mzpkg/bin/` and adds it to your PATH.

### 15.2 Account System

Create an account and log in to publish packages:

```bash
# Create a new account
mzpkg register

# Log in (saved to ~/.mzpkg/config.json)
mzpkg login

# Check logged-in user
mzpkg status

# View profile details
mzpkg profile

# Log out
mzpkg logout
```

**Profile fields** (editable via web at https://pkgs-mz.vercel.app/profile):
- Username, Display Name, Email
- Bio, Location, Website
- Avatar (uploaded to GitHub release assets)

Account data is stored securely in a private GitHub repository as release tags. Passwords are hashed with SHA-256 + salt.

### 15.3 Package Commands

| Command | Description | Auth Required |
|---------|-------------|:---:|
| `mzpkg install <name>` | Install a package | ✗ |
| `mzpkg install <user/pkg>` | Install a user-published package | ✗ |
| `mzpkg install -g <name>` | Install globally (interpreter/tools) | ✗ |
| `mzpkg search <query>` | Search packages | ✗ |
| `mzpkg list` | List installed packages | ✗ |
| `mzpkg info <name>` | Show package details | ✗ |
| `mzpkg update [name]` | Update packages | ✗ |
| `mzpkg remove <name>` | Remove a package | ✗ |
| `mzpkg init [name]` | Create package template | ✗ |
| `mzpkg push` | Publish package to cloud | ✓ |

### 15.4 Installing Packages

Install official packages from the registry:

```bash
mzpkg install strings
mzpkg install http
mzpkg install math_utils
```

Install user-published packages (shown as `username/pkg-name`):

```bash
mzpkg install tree              # finds Cross/tree automatically
mzpkg install cross/tree        # or specify author explicitly
```

Packages are installed to `~/.mzpkg/libs/<name>/mod.mz` and can be imported:

```mozhi
import strings from "strings/mod.mz"
echo(strings.capitalize("hello"))
```

### 15.5 Global Install (Interpreters & Tools)

Install Mozhi interpreters and tools globally to `~/.mzpkg/bin/`:

```bash
mzpkg install -g interpreter-fast   # Mozhi fast interpreter (Rust VM)
mzpkg install -g interpreter        # Mozhi C interpreter
mzpkg install -g libs               # Standard libraries
```

The CLI auto-detects your platform (linux-arm64, linux-x64, macos-arm64, windows-x64) and downloads the correct binary from the mozhi-doc GitHub releases.

### 15.6 Publishing Packages

Create and publish your own packages:

```bash
# Step 1: Create package template
mzpkg init mylib

# Step 2: Edit your code
cd mylib
# Edit src/mod.mz with your functions

# Step 3: Log in (if not already)
mzpkg login

# Step 4: Push to cloud
mzpkg push
```

The push command:
1. Reads `package.json` for name, version, description
2. Collects all `.mz` files from `src/` and `tests/`
3. Uploads files as GitHub release assets under `pkgs/<name>/`
4. Updates the registry — your package appears in search as `username/pkg-name`

**Only the package owner can update their packages.** Pushing a package with the same name replaces the previous version.

### 15.7 Package Template (mzpkg init)

The `mzpkg init` command creates a package scaffold:

```
mylib/
├── package.json      # Name, version, description, category
├── README.md         # Documentation
├── src/
│   └── mod.mz        # Main module (your code)
└── tests/
    └── test.mz       # Tests
```

**package.json** format:

```json
{
  "name": "mylib",
  "version": "1.0.0",
  "description": "My Mozhi library",
  "category": "general",
  "license": "MIT",
  "author": "your-username",
  "main": "src/mod.mz"
}
```

### 15.8 Package Storage

| Item | Storage Location |
|------|-----------------|
| Official packages | crossberry-in/mozhi-doc registry |
| User packages | crosslink369/pkgs-mz → Releases → account-\<user\>/pkgs/\<name\>/ |
| User avatars | crosslink369/pkgs-mz → Releases → account-\<user\>/avatar.png |
| Account data | GitHub release tag body (hashed passwords) |
| CLI config | ~/.mzpkg/config.json |
| Installed libs | ~/.mzpkg/libs/\<name\>/ |
| Global binaries | ~/.mzpkg/bin/ |
| Registry cache | ~/.mzpkg/cache/registry.json |

### 15.9 Search

Search works across official and user packages:

```bash
mzpkg search http          # finds official 'http' package
mzpkg search tree          # finds user 'Cross/tree' package
mzpkg interpreter-fast     # finds Mozhi fast interpreter
```

Search results show:

```
PACKAGE                  VERSION    CATEGORY     AUTHOR       DESCRIPTION
────────────────────────────────────────────────────────────────────────
Cross/tree               v1.0.0     clis         Cross        tree in folder
http                     v1.0.0     web          official     HTTP server utilities
```

### 15.10 Dependency Resolution

The package manager resolves dependencies using semantic versioning:

| Operator | Example | Matches |
|----------|---------|---------|
| `^` | `^1.2.3` | >=1.2.3, <2.0.0 (compatible) |
| `~` | `~1.2.3` | >=1.2.3, <1.3.0 (patch only) |
| `>=` | `>=1.0.0` | >=1.0.0 |
| `=` | `=1.2.3` | exactly 1.2.3 |
| `*` | `*` | any version |

### 15.11 Other Commands

```bash
mzpkg doctor             # Check environment, login status, API connection
mzpkg version            # Show mzpkg version
mzpkg help               # Show all commands
```

### 15.12 API Endpoints

The pkgs-mz cloud provides these API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/registry-json` | GET | Full package registry (official + user) |
| `/api/file?path=...` | GET | Download official package file |
| `/api/file?user=X&pkg=Y` | GET | Download user package (proxy) |
| `/api/auth/register` | POST | Create account |
| `/api/auth/login` | POST | Log in |
| `/api/auth/profile` | GET/PUT | Get/update profile |
| `/api/auth/avatar` | POST | Upload avatar image |
| `/api/auth/push` | POST | Publish package |
| `/api/auth/pkgs` | GET | List user-published packages |
| `/api/global?q=...` | GET | Search mozhi-doc releases |
| `/api/download/binary` | GET | Download CLI binary |

---

## 16. Diagnostics

### 16.1 Error Format

Mozhi diagnostics follow a consistent format designed for readability and IDE integration. Each diagnostic includes a severity, error code, message, source location, and optional hints.

```
error[MZ1001]: Unknown variable

  --> src/main.mz:12:8
   |
12 | print(total)
   |        ^^^^^

Variable 'total' does not exist in this scope.

Hint: Did you mean 'totalPrice'?

Documentation: https://crossberry-in.github.io/mozhi-doc/errors/MZ1001
```

### 16.2 Severity Levels

| Level | Description | Exit Code |
|-------|-------------|-----------|
| error | Prevents compilation/execution | 1 |
| warning | Potential issue, does not prevent compilation | 0 |
| note | Additional context for a preceding diagnostic | 0 |
| help | Suggestion for fixing a preceding diagnostic | 0 |

### 16.3 Source Location

Diagnostics include source locations in the format `file:line:column`. The location points to the start of the relevant code. For multi-token constructs, a caret (`^`) highlights the specific tokens involved. Source context shows the line(s) surrounding the error with line numbers.

### 16.4 Hints and Suggestions

Diagnostics may include hints (additional context) and suggestions (fix proposals). Hints use the "Hint:" prefix. Suggestions use the "Suggestion:" prefix and may include code snippets. These help programmers quickly understand and fix errors.

### 16.5 Documentation Links

Each error code has a corresponding documentation page. The URL format is `https://crossberry-in.github.io/mozhi-doc/errors/SNxxxx`. The documentation explains the error cause, common scenarios, and fix approaches.

---

## 17. Runtime and Memory

### 17.1 Memory Model

Mozhi uses a managed memory model with automatic garbage collection. Memory is allocated on the stack for local variables with known lifetimes, and on the heap for dynamically allocated objects. The runtime tracks object references and reclaims memory that is no longer reachable. The garbage collector uses a mark-and-sweep algorithm with generational optimization.

### 17.2 Stack vs Heap

Primitive types (int, float, bool, char) and small structs are allocated on the stack. Strings, arrays, maps, and large structs are allocated on the heap. The compiler determines allocation strategy based on type and lifetime analysis. Stack allocation is preferred for performance; heap allocation is used when the lifetime extends beyond the stack frame.

### 17.3 Garbage Collection

The garbage collector (GC) automatically reclaims memory that is no longer referenced by the program. The GC runs periodically and during memory pressure. GC pauses are typically under 1 millisecond for small heaps. Programs can hint the GC to run at specific points using the `std.gc.collect()` function.

### 17.4 Ownership

Mozhi tracks ownership of heap-allocated objects. An object has a single owner at a time. When the owner goes out of scope, the object is scheduled for deallocation. Ownership can be transferred (moved) or shared (via reference counting). This prevents use-after-free and double-free errors.

### 17.5 Concurrency

Mozhi supports concurrent programming via threads and async/await. Threads are operating system threads managed by the runtime. Channels provide type-safe communication between threads. The async/await mechanism enables efficient asynchronous I/O without blocking threads.

```mozhi
import std.thread

fn worker(id) {
    for i = 0; i < 5; i += 1 {
        echo("Worker ", id, ": ", i)
        sleep(0.1)
    }
}

t1 = spawn(fn() { worker(1) })
t2 = spawn(fn() { worker(2) })
join(t1)
join(t2)
```

### 17.6 Async/Await

The `async` keyword marks a function as asynchronous. Asynchronous functions return a Future that can be awaited. The `await` keyword suspends execution until the Future completes. Async functions enable non-blocking I/O operations.

```mozhi
async fn fetch_data(url) {
    response = await http.get(url)
    return response.body
}

async fn main() {
    data = await fetch_data("https://api.example.com")
    echo(data)
}
```

---

## Appendix A: Error Code Reference

This appendix lists all error codes defined by the Mozhi specification. Error codes are prefixed with `SN` and categorized by the first digit.

### A.1 Parse Errors (MZ1xxx)

| Code | Error | Description |
|------|-------|-------------|
| MZ1001 | Unknown variable | A variable used before declaration |
| MZ1002 | Unexpected token | A token that doesn't fit the grammar |
| MZ1003 | Type mismatch | Incompatible types in assignment |
| MZ1004 | Cannot reassign constant | Attempt to modify a const value |
| MZ1005 | Break outside loop | break used outside a loop |
| MZ1006 | Return outside function | return used outside a function |
| MZ1007 | Missing semicolon | Expected ; between statements |
| MZ1008 | Integer overflow | Literal exceeds type range |
| MZ1009 | Invalid escape sequence | Unknown \\ escape in string |
| MZ1010 | Unterminated string | String literal not closed |
| MZ1011 | Unterminated comment | /* without matching */ |
| MZ1012 | Expected { | Block opening brace missing |
| MZ1013 | Expected } | Block closing brace missing |
| MZ1014 | Expected ( | Opening parenthesis missing |
| MZ1015 | Expected ) | Closing parenthesis missing |

### A.2 Type Errors (MZ2xxx)

| Code | Error | Description |
|------|-------|-------------|
| MZ2001 | Type inference failure | Cannot infer type from context |
| MZ2002 | Variable shadowing | Variable redeclared in same scope |
| MZ2003 | Narrowing cast | Cast may lose data |
| MZ2004 | Non-exhaustive match | Match missing cases |
| MZ2005 | Undefined function | Function not found |
| MZ2006 | Argument count mismatch | Wrong number of arguments |
| MZ2007 | Undefined type | Type not found |
| MZ2008 | Undefined trait | Trait not found |
| MZ2009 | Trait not implemented | Type doesn't implement trait |
| MZ2010 | Field not found | Struct field doesn't exist |

### A.3 Runtime Errors (MZ3xxx)

| Code | Error | Description |
|------|-------|-------------|
| MZ3001 | Null dereference | Accessing member of null |
| MZ3002 | Index out of bounds | Array index exceeds length |
| MZ3003 | Division by zero | Integer division by zero |
| MZ3004 | Stack overflow | Recursion too deep |
| MZ3005 | Out of memory | Heap allocation failed |
| MZ3006 | Invalid cast | Runtime type cast failed |
| MZ3007 | Uncaught error | Error not caught by try/catch |
| MZ3008 | Channel closed | Sending to closed channel |

### A.4 I/O Errors (MZ4xxx)

| Code | Error | Description |
|------|-------|-------------|
| MZ4001 | File not found | Specified file does not exist |
| MZ4002 | Permission denied | Insufficient permissions |
| MZ4003 | Network error | Network operation failed |
| MZ4004 | Connection refused | Cannot connect to host |
| MZ4005 | Timeout | Operation timed out |
| MZ4006 | Disk full | No space to write |

---

## Appendix B: Reserved Keywords

The following identifiers are reserved as keywords in Mozhi and cannot be used as variable, function, type, or module names.

| | | | |
|---|---|---|---|
| `const` | `fn` | `if` | `else` |
| `match` | `while` | `for` | `in` |
| `break` | `continue` | `return` | `import` |
| `public` | `private` | `struct` | `enum` |
| `trait` | `impl` | `async` | `await` |
| `try` | `catch` | `throw` | `defer` |
| `true` | `false` | `null` | |

### B.1 Contextual Keywords

The following identifiers are contextual keywords — they have special meaning in specific contexts but can be used as identifiers elsewhere:

| Keyword | Context |
|---------|---------|
| `as` | Module aliasing: `import std.math as m` |
| `for` | Impl blocks: `impl Trait for Type` |
| `not` | Logical NOT: `not x` |

---

## Appendix C: Operator Precedence

Operators are listed from lowest precedence (evaluated last) to highest precedence (evaluated first). Operators on the same line have equal precedence and are evaluated according to their associativity.

| Precedence | Operator | Associativity | Description |
|-----------|----------|---------------|-------------|
| 1 (lowest) | `or` | Left | Logical OR (short-circuit) |
| 2 | `and` | Left | Logical AND (short-circuit) |
| 3 | `== !=` | Left | Equality comparison |
| 4 | `< > <= >=` | Left | Relational comparison |
| 5 | `+ -` | Left | Addition and subtraction |
| 6 | `* / %` | Left | Multiplication, division, modulo |
| 7 | `**` | Right | Exponentiation |
| 8 | `not - !` | Prefix | Unary NOT, negation |
| 9 | `. () []` | Left | Member access, call, index |
| 10 (highest) | `(grouping)` | N/A | Parenthesized expression |

### C.1 Assignment Operators

Assignment operators (`=`, `+=`, `-=`, `*=`, `/=`, `%=`) have lower precedence than all other operators. They are right-associative: `a = b = c` assigns `c` to `b`, then `b` to `a`.

### C.2 Examples

```mozhi
# Precedence: * before +
result = 2 + 3 * 4    # 14, not 20

# Parentheses override
result = (2 + 3) * 4  # 20

# Exponentiation is right-associative
result = 2 ** 3 ** 2  # 512 = 2^(3^2) = 2^9

# Logical operators short-circuit
result = false and expensive()  # expensive() not called
result = true or expensive()    # expensive() not called
```

---

*End of Mozhi Programming Language Specification v2.0*

Copyright © 2026 crossberry-in. All Rights Reserved.

### 15.13 Bytecode Compilation (.mzb)

The Mozhi interpreter can compile `.mz` source files into bytecode binary format (`.mzb`). This enables faster startup and closed-source distribution.

**Compile to bytecode:**

```bash
mozhi-fast build app.mz              # → app.mzb
mozhi-fast build app.mz -o out.mzb   # custom output name
```

**Run bytecode:**

```bash
mozhi-fast run app.mzb              # run compiled bytecode
mozhi-fast app.mzb                  # also works (auto-detects .mzb)
```

**Encrypted bytecode (closed source):**

```bash
# Compile with encryption
mozhi-fast build app.mz --encrypt
mozhi-fast build app.mz --encrypt --password mysecret

# Run encrypted bytecode
mozhi-fast run app.mzb --password mysecret
mozhi-fast run app.mzb -p mysecret
```

**Binary format (.mzb):**

| Field | Size | Description |
|-------|------|-------------|
| Magic | 4 bytes | `MZBC` (unencrypted) or `MZBE` (encrypted) |
| Version | 2 bytes | Format version (u16) |
| Flags | 2 bytes | Bit flags (encrypted, compressed) |
| Chunks | variable | Serialized bytecode chunks |

Each chunk contains: opcodes, constants, variable names, parameters.

**Distribution:**

```bash
# Distribute compiled bytecode (source not included)
mozhi-fast build secret_app.mz --encrypt --password s3cret
# Ship only secret_app.mzb to users

# Users run with password
mozhi-fast run secret_app.mzb -p s3cret
```


### 15.14 Multi-Target Compilation

Mozhi supports compiling to multiple output targets. No password is required for JS, C, or native targets.

**Build targets:**

| Target | Command | Output | Run with |
|--------|---------|--------|----------|
| Bytecode | `mozhi-fast build app.mz` | `app.mzb` | `mozhi-fast run app.mzb` |
| JavaScript | `mozhi-fast build app.mz --target js` | `app.js` | `node app.js` |
| C source | `mozhi-fast build app.mz --target c` | `app.c` | `cc -O2 app.c -o app` |
| Native binary | `mozhi-fast build app.mz --target native` | `app` | `./app` |
| Encrypted | `mozhi-fast build app.mz --encrypt` | `app.mzb` | `mozhi-fast run app.mzb -p <pw>` |

**Examples:**

```bash
# JavaScript — runs anywhere with Node.js
mozhi-fast build hello.mz --target js
node hello.js

# Native binary — no interpreter needed
mozhi-fast build hello.mz --target native
./hello

# Custom output name
mozhi-fast build hello.mz --target native -o myapp
./myapp

# All targets from one source
mozhi-fast build app.mz                          # → app.mzb
mozhi-fast build app.mz --target js              # → app.js
mozhi-fast build app.mz --target c               # → app.c
mozhi-fast build app.mz --target native          # → app
mozhi-fast build app.mz --encrypt -p secret      # → app.mzb (encrypted)
```

**JavaScript target features:**
- All Mozhi builtins mapped to JS (`Math.*`, `console.log`, `JSON.*`, `require('fs')`)
- Control flow: `if/else`, `while`, `for-in`, `fn`
- Arrays, maps, strings, numbers
- Output runs with Node.js or in browsers

**Native target:**
- AST → C source → machine code via cc/gcc/clang
- `-O2` optimization applied automatically
- Produces standalone executable (no interpreter/runtime needed)
- Auto-detects available compiler: `cc` → `gcc` → `clang`

