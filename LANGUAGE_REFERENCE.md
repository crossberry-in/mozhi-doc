# Sino — Language Reference

This is the complete reference for the Sino programming language.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Data Types](#data-types)
- [Variables](#variables)
- [Operators](#operators)
- [Control Flow](#control-flow)
- [Functions](#functions)
- [Classes](#classes)
- [Arrays](#arrays)
- [Built-in Functions](#built-in-functions)
- [Comments](#comments)
- [Error Handling](#error-handling)
- [Example Programs](#example-programs)
- [Quick Reference Card](#quick-reference-card)

---

## Getting Started

### REPL

```bash
./sino
>> var x = 10
>> echo x
10
>> exit
```

### Run a File

```bash
./sino examples/hello.si
```

### Build from Source (Maintainers Only)

> The Sino source code is closed-source. If you have access to the private repo:

```bash
make
```

---

## Data Types

| Type | Example | Description |
|------|---------|-------------|
| Integer | `42`, `-7`, `0` | Whole numbers |
| Float | `3.14`, `-0.5`, `2.0` | Decimal numbers |
| String | `"hello"` | Text strings |
| Boolean | `true`, `false` | Truth values |
| Null | `null` | Absence of value |
| Array | `[1, 2, 3]` | Ordered collection |
| Function | `func(x): return x end` | Callable block |
| Class | `class Foo: end` | Object blueprint |

### Type Checking

```sino
typeof(42)              # "int"
typeof(3.14)            # "float"
typeof("hello")         # "string"
typeof(true)            # "boolean"
typeof(null)            # "null"
typeof([1,2])           # "array"
typeof(func() end)      # "function"
```

---

## Variables

### `var` (Mutable)

```sino
var name = "Sino"
var count = 0
count = count + 1       # OK
```

### `fix` (Immutable Constant)

```sino
fix PI = 3.14159
# PI = 3.0             # Error: cannot reassign
```

### Variable Scope

```sino
var x = 10
if true:
    var y = 20          # y is local to this block
    echo x              # OK: x is accessible
end
# echo y                # Error: y is undefined
```

---

## Operators

### Arithmetic

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `5 + 3` → `8` |
| `-` | Subtraction | `5 - 3` → `2` |
| `*` | Multiplication | `5 * 3` → `15` |
| `/` | Division | `6 / 3` → `2` |
| `%` | Modulo | `7 % 3` → `1` |
| `**` | Power | `2 ** 10` → `1024` |
| `-` | Negation | `-5` |

### String Operations

```sino
"Hello" + ", " + "World!"   # "Hello, World!"
```

### Comparison

| Operator | Description | Example |
|----------|-------------|---------|
| `==` | Equal | `5 == 5` → `true` |
| `!=` | Not equal | `5 != 3` → `true` |
| `<` | Less than | `3 < 5` → `true` |
| `>` | Greater than | `5 > 3` → `true` |
| `<=` | Less or equal | `5 <= 5` → `true` |
| `>=` | Greater or equal | `5 >= 3` → `true` |

### Logical

| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Logical AND | `true and false` → `false` |
| `or` | Logical OR | `true or false` → `true` |
| `not` | Logical NOT | `not true` → `false` |

### Operator Precedence (Low to High)

1. `or`
2. `and`
3. `==`, `!=`
4. `<`, `>`, `<=`, `>=`
5. `+`, `-`
6. `*`, `/`, `%`
7. `**`
8. Prefix: `-`, `not`
9. Calls: `func()`, `arr[i]`

---

## Control Flow

### `if` / `elseif` / `else`

```sino
var x = 10

if x > 5:
    echo "Greater than 5"
elseif x > 2:
    echo "Greater than 2"
else:
    echo "Small"
end
```

### `while`

```sino
var i = 0
while i < 5:
    echo i
    i = i + 1
end
```

### `for`

```sino
for var i = 0; i < 10; i = i + 1:
    echo i
end
```

### `for...in`

```sino
var fruits = ["apple", "banana", "cherry"]
for var fruit in fruits:
    echo fruit
end
```

### `match` (Switch)

```sino
var x = 2

match x:
    case 1:
        echo "One"
    case 2:
        echo "Two"
    case 3:
        echo "Three"
    default:
        echo "Unknown"
end
```

### `break` and `continue`

```sino
for var i = 0; i < 100; i = i + 1:
    if i == 5:
        break              # Exit loop
    end
    if i % 2 == 0:
        continue           # Skip to next iteration
    end
    echo i
end
```

---

## Functions

### Basic Function (`func`)

```sino
func add(a, b):
    return a + b
end

echo add(3, 4)              # 7
```

### Anonymous Function (`fn`)

```sino
var square = fn(x):
    return x * x
end

echo square(5)              # 25
```

### Closures

```sino
func make_counter():
    var count = 0
    return {
        increment: fn():
            count = count + 1
        end,
        get_count: fn():
            return count
        end
    }
end

var counter = make_counter()
counter.increment()
counter.increment()
echo counter.get_count()    # 2
```

### Higher-Order Functions

```sino
func apply(f, x):
    return f(x)
end

var double = fn(x): return x * 2 end
echo apply(double, 5)       # 10
```

### Recursive Functions

```sino
func factorial(n):
    if n <= 1:
        return 1
    end
    return n * factorial(n - 1)
end

echo factorial(5)           # 120
```

---

## Classes

### Basic Class

```sino
class Person:
    func init(name, age):
        self.name = name
        self.age = age
    end

    func hello():
        echo "Hello, my name is ", self.name
    end

    func get_age():
        return self.age
    end
end
```

### Creating Instances

```sino
var john = Person("John", 25)
john.hello()                # "Hello, my name is John"
echo john.get_age()         # 25
```

### Methods

```sino
class Counter:
    func init():
        self.count = 0
    end

    func increment():
        self.count = self.count + 1
    end

    func get_count():
        return self.count
    end
end

var c = Counter()
c.increment()
c.increment()
echo c.get_count()          # 2
```

---

## Arrays

### Creating Arrays

```sino
var empty = []
var numbers = [1, 2, 3, 4, 5]
var mixed = [1, "hello", true, null]
```

### Accessing Elements

```sino
var arr = [10, 20, 30]
echo arr[0]                 # 10
echo arr[2]                 # 30
```

### Modifying Arrays

```sino
var arr = [1, 2, 3]
push(arr, 4)                # arr is now [1, 2, 3, 4]
var last = pop(arr)         # last is 4, arr is [1, 2, 3]
```

### Iterating Arrays

```sino
var fruits = ["apple", "banana", "cherry"]
for var fruit in fruits:
    echo fruit
end
```

---

## Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `echo(...)` | Print values to stdout | `echo("Hello", 42)` |
| `print(...)` | Print values to stdout | `print("Hello", 42)` |
| `input(prompt)` | Read input from stdin | `var name = input("Name: ")` |
| `len(x)` | Get length of array/string | `len("hello")` → `5` |
| `typeof(x)` | Get type name as string | `typeof(42)` → `"int"` |
| `int(x)` | Convert to integer | `int("42")` → `42` |
| `float(x)` | Convert to float | `float("3.14")` → `3.14` |
| `string(x)` | Convert to string | `string(42)` → `"42"` |
| `push(arr, val)` | Add element to array | `push([1], 2)` |
| `pop(arr)` | Remove and return last element | `pop([1,2])` → `2` |
| `join(arr, sep)` | Join array with separator | `join([1,2], "-")` → `"1-2"` |
| `sqrt(x)` | Square root | `sqrt(16)` → `4.0` |
| `abs(x)` | Absolute value | `abs(-5)` → `5` |
| `floor(x)` | Floor value | `floor(3.7)` → `3` |
| `ceil(x)` | Ceil value | `ceil(3.2)` → `4` |

### `echo` Examples

```sino
echo "Hello"                    # Hello
echo "x = ", 10                 # x = 10
echo 1, 2, 3                    # 1 2 3
echo true                       # true
echo null                       # null
```

### `input` Examples

```sino
var name = input("Enter your name: ")
echo "Hello, " + name

var age = int(input("Enter your age: "))
```

---

## Comments

```sino
# This is a single-line comment
var x = 10  # Comment after code

# Multi-line comments use # on each line
# Line 1
# Line 2
# Line 3
```

---

## Error Handling

Sino returns runtime errors for:

- Undefined variables
- Type mismatches
- Index out of bounds
- Division by zero
- Calling non-functions
- Too many/few arguments

```sino
echo x              # Error: Undefined variable
5 + "hello"         # Error: Cannot perform arithmetic on non-numbers
[1,2][5]            # Error: Index out of bounds
10 / 0              # Error: Division by zero
```

---

## Example Programs

### Hello World

```sino
echo "Hello, World!"
```

### Fibonacci

```sino
func fibonacci(n):
    if n <= 1:
        return n
    end
    return fibonacci(n - 1) + fibonacci(n - 2)
end

for var i = 0; i < 20; i = i + 1:
    echo "F(", i, ") = ", fibonacci(i)
end
```

### Bubble Sort

```sino
func bubble_sort(arr):
    var n = len(arr)
    for var i = 0; i < n - 1; i = i + 1:
        for var j = 0; j < n - i - 1; j = j + 1:
            if arr[j] > arr[j + 1]:
                var temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
            end
        end
    end
    return arr
end

var data = [64, 34, 25, 12, 22, 11, 90]
echo bubble_sort(data)
```

### Simple Class

```sino
class Person:
    func init(name, age):
        self.name = name
        self.age = age
    end

    func to_string():
        return self.name + " (" + string(self.age) + ")"
    end
end

var john = Person("John", 25)
echo john.to_string()
```

---

## File Extension

Sino source files use the **`.si`** extension.

---

## Quick Reference Card

```sino
# Variables
var x = 10
fix PI = 3.14

# Functions
func add(a, b):
    return a + b
end

# Anonymous functions
var square = fn(x): return x * x end

# Control
if cond:
elseif cond:
else:
end

while cond:
end

for var i = 0; i < n; i = i + 1:
end

for var item in arr:
end

match value:
    case 1:
    default:
end

break
continue

# Classes
class Person:
    func init(name):
        self.name = name
    end
end

# Data
[1, 2, 3]
"hello"
42
3.14
true
false
null

# Built-ins
echo()    input()   len()   typeof()
int()     float()   string()
push()    pop()     join()
sqrt()    abs()     floor()    ceil()
```
