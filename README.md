# TailScript

**A grandma-friendly programming language that anyone can understand!**

TailScript is designed to be simple, intuitive, and use plain English commands. No cryptic symbols or confusing syntax - just natural language that makes sense.

## Quick Start

### Running TailScript Programs

```bash
python tailscript.py hello.tail
```

Or use the compiled executable:

```bash
tailscript.exe hello.tail
```

### Building the Executable

```bash
.\build_tailscript.bat
```

## Language Reference

### Variables

Store values with the `set` command:

```
set name to "Ethel"
set age to 82
set score to 100
```

### Printing

Display values with `print`:

```
print "Hello, World!"
print name
print age
```

### User Input

Ask questions and save responses:

```
ask "What is your name?" and save to name
ask "How old are you?" and save to age
```

### Arithmetic

Perform calculations with plain English:

```
set sum to 10 plus 5
set difference to 20 minus 8
set product to 6 times 7
set quotient to 20 divided by 4
```

### Variable Operations

Increase or decrease variables:

```
increase score by 10
decrease lives by 1
increase age by 1
```

### Conditions

Make decisions with `if` and `else`:

```
if age is 82
    print "You are 82 years old"
else
    print "Different age"
```

#### Comparison Operators

- `is` - equal to
- `is not` - not equal to
- `is greater than` - greater than
- `is less than` - less than

```
if score is greater than 100
    print "High score!"

if age is less than 18
    print "You are a minor"

if name is not "Bob"
    print "You're not Bob"
```

### Timing

Add delays to your program:

```
wait 5 seconds
wait 2 minutes
```

### Comments

Add notes that won't be executed:

```
# This is a comment
print "This runs"  # This is also a comment
```

### Blocks and Indentation

Use 4 spaces to indent code blocks:

```
if age is greater than 65
    print "Senior discount available"
    print "Welcome!"
else
    print "Regular price"
```

## Example Programs

### Hello World

```
print "Hello, World!"
```

### Simple Calculator

```
ask "Enter first number:" and save to num1
ask "Enter second number:" and save to num2

set sum to num1 plus num2
set product to num1 times num2

print "Sum:"
print sum
print "Product:"
print product
```

### Age Checker

```
ask "What is your age?" and save to age

if age is greater than 18
    print "You are an adult"
else
    print "You are a minor"

set next_year to age plus 1
print "Next year you will be:"
print next_year
```

### Score Tracker

```
set score to 0
print "Starting game..."

increase score by 10
print "Got a coin! Score:"
print score

increase score by 50
print "Found treasure! Score:"
print score

decrease score by 5
print "Hit by enemy! Score:"
print score
```

## Features

- **Plain English syntax** - No confusing symbols or keywords
- **Helpful error messages** - Clear guidance when something goes wrong
- **Typo detection** - Catches common mistakes like `pritn` instead of `print`
- **User-friendly** - Designed for beginners and non-programmers
- **No installation required** - Runs with Python or as standalone executable

## Technical Details

- **File extension**: `.tail`
- **Python version**: 3.6+
- **Dependencies**: None (uses only standard library)

## Error Handling

TailScript provides friendly error messages:

```
❌ Error on line 5: I don't know what 'xyz' is
⚠ Did you mean 'print'?
❌ Use: set name to value
```

## Contributing

TailScript is designed to be simple and accessible. When adding features, keep the language natural and grandma-friendly!

## License

Feel free to use, modify, and share TailScript!

---

**Made with ❤️ for everyone who wants to code without the complexity**
