# Mozhi — Usage Guide

This guide explains how to use the Mozhi interpreter, including the REPL, running scripts, working with files, and using built-in features.

---

## Table of Contents

- [Starting the Interpreter](#starting-the-interpreter)
- [Using the REPL](#using-the-repl)
- [Running a Mozhi File](#running-a-mozhi-file)
- [File Extension](#file-extension)
- [Command-Line Arguments](#command-line-arguments)
- [Basic Examples](#basic-examples)
- [Working with Variables](#working-with-variables)
- [Working with Functions](#working-with-functions)
- [Working with Classes](#working-with-classes)
- [Working with Arrays](#working-with-arrays)
- [Built-in Functions](#built-in-functions)
- [Best Practices](#best-practices)
- [Common Errors](#common-errors)

---

## Starting the Interpreter

The `mozhi` command can be used in two modes:

1. **REPL mode** — Interactive Read-Eval-Print Loop. Type code line-by-line and see results immediately.
2. **File mode** — Run a Mozhi script file.

To check if Mozhi is installed:

```bash
mozhi --version
```

---

## Using the REPL

Launch the REPL by running `mozhi` with no arguments:

```bash
mozhi
```

You will see the Mozhi prompt:

```
>> 
```

### REPL Examples

```
>> var x = 10
>> echo x
10
>> var y = 20
>> echo x + y
30
>> var name = input("Your name: ")
Your name: Mozhi
>> echo "Hello, " + name
Hello, Mozhi
>> exit
```

### REPL Commands

| Command | Description |
|---------|-------------|
| `exit`  | Exit the REPL |
| `quit`  | Exit the REPL (alias) |
| Ctrl+D  | Send EOF to exit the REPL |
| Ctrl+C  | Cancel current input |

### Multi-line Statements in the REPL

Mozhi supports multi-line blocks in the REPL. After typing a block opener (`if`, `while`, `for`, `func`, `class`), press Enter and continue on the next line. The block continues until you type `end`.

```
>> func factorial(n):
...     if n <= 1:
...         return 1
...     end
...     return n * factorial(n - 1)
... end
>> echo factorial(5)
120
```

---

## Running a Mozhi File

To run a Mozhi script, pass the file path as an argument:

```bash
mozhi path/to/script.si
```

### Example

Create a file `hello.si`:

```mozhi
# Hello World in Mozhi
echo "Hello, World!"

# Variables
var name = "Mozhi"
echo "Welcome to ", name

# Arithmetic
var a = 10
var b = 3
echo "Sum: ", a + b
echo "Product: ", a * b
echo "Power: ", a ** b
```

Run it:

```bash
mozhi hello.si
```

Output:

```
Hello, World!
Welcome to Mozhi
Sum: 13
Product: 30
Power: 1000
```

---

## File Extension

Mozhi source files use the **`.si`** extension.

| Extension | Description |
|-----------|-------------|
| `.si` | Mozhi source file |

Example filenames:

- `hello.si`
- `fibonacci.si`
- `my_script.si`

---

## Command-Line Arguments

The Mozhi interpreter accepts the following command-line arguments:

| Argument | Description |
|----------|-------------|
| (none) | Start the interactive REPL |
| `<file>` | Run the specified Mozhi file |
| `--version`, `-v` | Print the Mozhi version and exit |
| `--help`, `-h` | Print help and exit |

### Examples

```bash
# Start REPL
mozhi

# Run a file
mozhi my_script.si

# Print version
mozhi --version

# Print help
mozhi --help
```

---

## Basic Examples

### Hello World

```mozhi
echo "Hello, World!"
```

### Variables and Arithmetic

```mozhi
var x = 10
var y = 20
echo "x + y =", x + y
echo "x * y =", x * y
```

### Conditionals

```mozhi
var age = 18

if age >= 18:
    echo "You are an adult."
elseif age >= 13:
    echo "You are a teenager."
else:
    echo "You are a child."
end
```

### Loops

```mozhi
# While loop
var i = 0
while i < 5:
    echo "i =", i
    i = i + 1
end

# For loop
for var j = 0; j < 3; j = j + 1:
    echo "j =", j
end

# For-in loop
var fruits = ["apple", "banana", "cherry"]
for var fruit in fruits:
    echo fruit
end
```

---

## Working with Variables

Mozhi supports two variable declarations:

### `var` — Mutable Variables

```mozhi
var name = "Mozhi"
var count = 0

count = count + 1     # OK - var can be reassigned
echo count            # 1
```

### `fix` — Immutable Constants

```mozhi
fix PI = 3.14159
fix GREETING = "Hello"

# PI = 3.0           # ERROR - fix cannot be reassigned
echo PI              # 3.14159
```

### Scope

Variables declared inside a block (e.g., inside `if`, `while`, `for`) are local to that block.

```mozhi
var x = 10
if true:
    var y = 20
    echo x           # OK - x is from outer scope
    echo y           # OK - y is local to this block
end
# echo y             # ERROR - y is undefined here
```

---

## Working with Functions

### Named Functions (`func`)

```mozhi
func add(a, b):
    return a + b
end

echo add(3, 4)       # 7
```

### Anonymous Functions (`fn`)

```mozhi
var square = fn(x):
    return x * x
end

echo square(5)       # 25
```

### Closures

Functions capture variables from their enclosing scope:

```mozhi
func make_counter():
    var count = 0
    return fn():
        count = count + 1
        return count
    end
end

var c = make_counter()
echo c()             # 1
echo c()             # 2
echo c()             # 3
```

### Recursion

```mozhi
func factorial(n):
    if n <= 1:
        return 1
    end
    return n * factorial(n - 1)
end

echo factorial(5)    # 120
```

### Higher-Order Functions

```mozhi
func apply(f, x):
    return f(x)
end

var double = fn(x): return x * 2 end
echo apply(double, 5)   # 10
```

---

## Working with Classes

```mozhi
class Person:
    func init(name, age):
        self.name = name
        self.age = age
    end

    func greet():
        echo "Hello, my name is ", self.name
    end

    func get_age():
        return self.age
    end
end

var john = Person("John", 25)
john.greet()                 # Hello, my name is John
echo john.get_age()          # 25
```

---

## Working with Arrays

```mozhi
# Creating arrays
var empty = []
var numbers = [1, 2, 3, 4, 5]
var mixed = [1, "hello", true, null]

# Accessing elements
echo numbers[0]              # 1
echo numbers[4]              # 5

# Modifying arrays
push(numbers, 6)             # numbers is now [1, 2, 3, 4, 5, 6]
var last = pop(numbers)      # last is 6, numbers is [1, 2, 3, 4, 5]

# Length
echo len(numbers)            # 5

# Iterating
for var n in numbers:
    echo n
end
```

---

## Built-in Functions

| Function | Description | Example |
|----------|-------------|---------|
| `echo(...)` | Print values to stdout | `echo("Hello", 42)` |
| `print(...)` | Same as echo | `print("Hello", 42)` |
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

For a complete list, see the [Language Reference](LANGUAGE_REFERENCE.md).

---

## Best Practices

### 1. Use `fix` for constants

```mozhi
fix PI = 3.14159
fix MAX_RETRIES = 5
```

### 2. Name variables clearly

```mozhi
# Good
var user_age = 25
var is_logged_in = true

# Bad
var a = 25
var b = true
```

### 3. Use functions to organize code

```mozhi
func calculate_area(width, height):
    return width * height
end

echo calculate_area(5, 3)
```

### 4. Add comments to explain non-obvious logic

```mozhi
# Calculate the nth Fibonacci number using recursion
func fibonacci(n):
    if n <= 1:
        return n
    end
    return fibonacci(n - 1) + fibonacci(n - 2)
end
```

### 5. Use `match` for multi-branch logic

```mozhi
var status = 200

match status:
    case 200:
        echo "OK"
    case 404:
        echo "Not Found"
    case 500:
        echo "Server Error"
    default:
        echo "Unknown"
end
```

---

## Common Errors

### Undefined variable

```
Error: Undefined variable 'x'
```

You tried to use a variable that hasn't been declared with `var` or `fix`. Check your spelling and scope.

### Type mismatch

```
Error: Cannot perform arithmetic on non-numbers
```

You tried to do math on a non-numeric value. Use `int()` or `float()` to convert strings to numbers first.

### Index out of bounds

```
Error: Index out of bounds
```

You tried to access an array element that doesn't exist. Check the array length with `len()` first.

### Division by zero

```
Error: Division by zero
```

You divided by zero. Check your divisor before dividing.

### Too many/few arguments

```
Error: Too many arguments
Error: Too few arguments
```

You called a function with the wrong number of arguments. Check the function definition.

---

## Next Steps

- Read the [Language Reference](LANGUAGE_REFERENCE.md) for the complete syntax.
- Browse the [Examples](examples/) to see real Mozhi programs.
- Try the [Quick Reference Card](LANGUAGE_REFERENCE.md#quick-reference-card) for a one-page cheat sheet.

---

## Need Help?

- 🐛 **Bug reports:** [Open an issue](https://github.com/crossberry-in/mozhi-doc/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/crossberry-in/mozhi-doc/discussions)
- 📖 **Full docs:** [Language Reference](LANGUAGE_REFERENCE.md)
