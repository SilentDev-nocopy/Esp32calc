# Resiris — Current Development Status

## Project Overview

Resiris currently has a working first PC-side interpreter prototype. The current architecture is:

```
Resiris Source (.resy)
        ↓
     Tokenizer
        ↓
      Parser
        ↓
       AST
        ↓
   Interpreter
        ↓
     Runtime
```

The current prototype is being developed and tested on PC first, with the eventual goal of implementing the interpreter in C/C++ for the ESP32.

The current project files include:

| File | Purpose |
|---|---|
| `tokenizer.py` | `.resy` source → tokens |
| `ast_nodes.py` | AST structures |
| `parser.py` | tokens → AST |
| `interpreter.py` | AST → execution |
| `run_resiris.py` | runs the complete pipeline |
| `main.resy` | runnable Resiris program/test |
| `test_frontend.py` | Tokenizer + Parser tests |

## Current Implementation Status

| Component | Status |
|---|---|
| Tokenizer | ✅ |
| Parser | ✅ |
| AST | ✅ |
| Interpreter | ✅ |
| Runtime | ✅ |

| Feature | Status |
|---|---|
| `v` / varints | ✅ |
| `c` / constants | ✅ |
| `UnknownObject` | ✅ |

| Type | Status |
|---|---|
| `int` | ✅ |
| `float` | ✅ |
| `string` | ✅ |
| `bool` | ✅ |

| Assignment Operator | Status |
|---|---|
| `=` | ✅ |
| `+=` | ✅ |
| `-=` | ✅ |
| `*=` | ✅ |
| `/=` | ✅ |

| Arithmetic Operator | Status |
|---|---|
| `+` | ✅ |
| `-` | ✅ |
| `*` | ✅ |
| `/` | ✅ |
| `%` | ✅ |

| Unary Operator | Status |
|---|---|
| unary `+` | ✅ |
| unary `-` | ✅ |

| Comparison Operator | Status |
|---|---|
| `==` | ✅ |
| `!=` | ✅ |
| `>` | ✅ |
| `<` | ✅ |
| `>=` | ✅ |
| `<=` | ✅ |

| Feature | Status |
|---|---|
| operator precedence | ✅ |
| `if` | ✅ |
| `elif` | ✅ |
| `else` | ✅ |
| `fn` | ✅ |
| function parameters | ⚠️ PROPOSAL |
| function calls | ✅ |
| `return` | ✅ |
| `pass` | ✅ |
| local scope | ✅ |
| global variable access | ✅ |
| `print_cmd` | ✅ |
| type checking | ✅ |
| runtime error handling | ✅ |
| `c` as a varint name | ✅ |
| `UnknownObject` type inference | ✅ |

## Tested Functionality

### Variables and Assignments

The following have been tested successfully:

| Test | Result |
|---|---|
| Basic varint declarations | ✅ PASS |
| Initial values | ✅ PASS |
| Variable reassignment | ✅ PASS |
| Compound assignments | ✅ PASS |
| Unknown variable detection | ✅ PASS |

Supported assignment operators: `=`, `+=`, `-=`, `*=`, `/=`

### Constants

Constants are implemented and tested:

```resy
c limit int = 100
```

Tested:

| Test | Result |
|---|---|
| Constant declaration | ✅ PASS |
| Reading constants | ✅ PASS |
| Constant reassignment | ✅ PASS |
| `ConstantAssignmentError` | ✅ PASS |

Attempting to modify a constant correctly produces a `ConstantAssignmentError`.

### `c` as a Varint Name

A tokenizer/parser edge case was discovered and fixed.

Both of these are valid in their respective contexts:

```resy
c limit int = 100
```

and:

```resy
v c int = 5
```

The parser now distinguishes the context correctly.

Tested:

| Test | Result |
|---|---|
| `c` as constant declaration | ✅ PASS |
| `c` as varint name | ✅ PASS |
| `c` varint + constant together | ✅ PASS |
| constant protection still works | ✅ PASS |

### Types

Currently implemented: `UnknownObject`, `int`, `float`, `string`, `bool`

Tested:

| Test | Result |
|---|---|
| int values | ✅ PASS |
| float values | ✅ PASS |
| string values | ✅ PASS |
| bool values | ✅ PASS |
| type checking | ✅ PASS |
| invalid type assignment | ✅ PASS |

### `UnknownObject`

`UnknownObject` is implemented with first-value type inference.

Example:

```resy
v value UnknownObject = 10
```

The first value determines the actual type: `10 → int`

After that, incompatible assignments are rejected.

Tested:

| Test | Result |
|---|---|
| `UnknownObject` → int | ✅ PASS |
| `UnknownObject` → string | ✅ PASS |
| same-type reassignment | ✅ PASS |
| wrong-type reassignment | ✅ PASS |
| `UnknownObject` from function return | ✅ PASS |
| local `UnknownObject` | ✅ PASS |

Example:

```resy
fn get_value():
    return 42

v result UnknownObject = get_value()
```

correctly results in: `result = 42 (int)`

The same behavior was tested with a string return value.

### Boolean Values

Boolean literals are implemented: `true`, `false`

Tested:

| Test | Result |
|---|---|
| `true` | ✅ PASS |
| `false` | ✅ PASS |
| bool variable | ✅ PASS |
| bool output | ✅ PASS |
| bool in if conditions | ✅ PASS |

### Strings

Strings are implemented.

Tested:

| Test | Result |
|---|---|
| string variables | ✅ PASS |
| string literals | ✅ PASS |
| string output | ✅ PASS |
| string + string | ✅ PASS |

Example:

```resy
v first string = "Hello "
v second string = "Resiris"

v text string = first + second
```

produces:

```
Hello Resiris
```

Invalid combinations are rejected:

```resy
"Hello" + 10
```

```
→ TypeErrorResiris
```

Tested:

| Test | Result |
|---|---|
| string + string | ✅ PASS |
| string + int | ❌ correctly rejected |

### Arithmetic

Implemented: `+`, `-`, `*`, `/`, `%`

All have passed individual tests.

| Test | Result |
|---|---|
| int arithmetic | ✅ PASS |
| float arithmetic | ✅ PASS |
| int + float | ✅ PASS |
| division | ✅ PASS |
| modulo | ✅ PASS |
| division by zero | ✅ PASS |
| modulo by zero | ✅ PASS |

Division currently produces a float: `20 / 4 → 5.0`

Division and modulo by zero produce a Resiris runtime error instead of exposing a raw Python exception.

### Unary Operators

Implemented and tested: `+x`, `-x`

| Test | Result |
|---|---|
| unary `+` | ✅ PASS |
| unary `-` | ✅ PASS |

### Operator Precedence

Operator precedence has been tested using combined expressions.

Example:

```resy
print_cmd(a + b * 2)
```

correctly evaluates multiplication before addition.

| Test | Result |
|---|---|
| `+` with `*` | ✅ PASS |
| `*` with `+` | ✅ PASS |
| `-` with `-` | ✅ PASS |
| `/` with `*` | ✅ PASS |

Operators with the same precedence level currently evaluate from left to right.

### Comparison Operators

All current comparison operators have been tested:

| Operator | Result |
|---|---|
| `==` | ✅ PASS |
| `!=` | ✅ PASS |
| `>` | ✅ PASS |
| `<` | ✅ PASS |
| `>=` | ✅ PASS |
| `<=` | ✅ PASS |

Comparison results are boolean values.

### Conditional Statements

Implemented:

```resy
if condition:
    ...
elif condition:
    ...
else:
    ...
```

Tested:

| Test | Result |
|---|---|
| if true path | ✅ PASS |
| if false path | ✅ PASS |
| else | ✅ PASS |
| elif | ✅ PASS |
| multiple conditions | ✅ PASS |
| boolean conditions | ✅ PASS |
| comparison conditions | ✅ PASS |

### Functions

Functions are implemented in the current PC prototype.

Example:

```resy
fn add(a, b):
    return a + b
```

Tested:

| Test | Result |
|---|---|
| function definition | ✅ PASS |
| function calls | ✅ PASS |
| parameters | ✅ PASS |
| return values | ✅ PASS |
| arithmetic inside functions | ✅ PASS |
| functions without return | ✅ PASS |
| wrong argument count | ✅ PASS |
| wrong return type | ✅ PASS |

Function parameter syntax `fn add(a, b):` is currently a technical prototype / **PROPOSAL**, not a final Resiris language decision.

### Function Scope

The current prototype supports local function scope.

| Test | Result |
|---|---|
| local variables | ✅ PASS |
| local variable modification | ✅ PASS |
| global variable access | ✅ PASS |
| local/global separation | ✅ PASS |
| local variable outside function | ✅ correctly rejected |

Example:

```resy
v number int = 10

fn change():
    v number int = 20
    number += 5
    print_cmd(number)

change()

print_cmd(number)
```

Result:

```
25
10
```

The local `number` does not overwrite the global `number`.

### `return`

`return` is implemented and tested.

| Test | Result |
|---|---|
| return without value | ✅ PASS |
| return with value | ✅ PASS |
| return expression | ✅ PASS |
| return from if | ✅ PASS |
| return from elif | ✅ PASS |
| return from else | ✅ PASS |
| return type checking | ✅ PASS |

`return` correctly stops execution of the current function.

Example:

```resy
fn test():
    print_cmd("before")
    return
    print_cmd("after")
```

Only `before` is produced.

### `pass`

`pass` is implemented as a no-op.

Tested behavior:

```resy
print_cmd("before")

pass

print_cmd("after")
```

Result:

```
before
after
```

Therefore:

| Behavior | Result |
|---|---|
| `pass` does nothing | ✅ |
| execution continues | ✅ |
| function does not exit | ✅ |

### `print_cmd`

`print_cmd` is implemented as a built-in command for terminal output.

| Test | Result |
|---|---|
| string output | ✅ PASS |
| number output | ✅ PASS |
| boolean output | ✅ PASS |
| expression output | ✅ PASS |
| output inside functions | ✅ PASS |
| local variable output | ✅ PASS |

It is separate from the module system.

### Error Handling

The following Resiris-specific error behavior has been tested:

| Error | Result |
|---|---|
| `UnknownVariableError` | ✅ PASS |
| `TypeErrorResiris` | ✅ PASS |
| `ConstantAssignmentError` | ✅ PASS |
| `RuntimeErrorResiris` | ✅ PASS |

Tested error situations include:

- undeclared varint ✅
- invalid type assignment ✅
- constant modification ✅
- invalid string + int ✅
- division by zero ✅
- modulo by zero ✅
- wrong function argument count ✅
- wrong function return type ✅

### Combined Tests

Several features have also been tested together:

- function + parameters ✅
- function + arithmetic ✅
- function + return ✅
- function + if ✅
- function + elif ✅
- function + else ✅
- function + global variables ✅
- function + local variables ✅
- function + UnknownObject ✅
- function + type checking ✅

Example:

```resy
fn check(number):
    if number > 10:
        return 100
    elif number == 10:
        return 50
    else:
        return 0
```

Tested with:

| Input | Output | Result |
|---|---|---|
| 20 | 100 | ✅ |
| 10 | 50 | ✅ |
| 5 | 0 | ✅ |

## Current Core

```
Resiris Source
      ↓
   Tokenizer     ✅
      ↓
    Parser       ✅
      ↓
     AST         ✅
      ↓
  Interpreter    ✅
      ↓
   Runtime       ✅
```

The current PC prototype therefore has a substantial working interpreter core rather than only a tokenizer/parser prototype.

## Not Implemented Yet

The following parts are still ahead:

| Feature | Status |
|---|---|
| `mat` | ⏳ |
| `await` | ⏳ |
| `include` | ⏳ |
| module system | ⏳ |
| `ResirisModuleObject` | ⏳ |
| ESP32 interpreter | ⏳ |
| ESP32 C/C++ implementation | ⏳ |
| OLED integration | ⏳ |
| Keyboard integration | ⏳ |
| Storage | ⏳ |
| Calculator engine | ⏳ |
| GameEngine | ⏳ |
| Games | ⏳ |
| Plugins | ⏳ |

`include` is intentionally postponed. `mat` is not being implemented yet because its final syntax/semantics are not sufficiently defined.

## Important Status Notes

| Item | Status |
|---|---|
| Function parameter syntax | ⚠️ PROPOSAL |
| `mat` syntax | ⚠️ UNDEFINED |
| returnless function semantics | ⚠️ Not fully finalized |
| `await` behavior | ⏳ Not implemented |
| `include` system | ⏳ Postponed |
| module system | ⏳ Not implemented |
| ESP32 implementation | ⏳ Not started |

## Overall Status

| Component | Status |
|---|---|
| Resiris PC Interpreter Core | 🟢 WORKING / TESTED |
| Tokenizer | 🟢 TESTED |
| Parser | 🟢 TESTED |
| AST | 🟢 IMPLEMENTED |
| Interpreter | 🟢 SUBSTANTIALLY TESTED |
| Runtime error handling | 🟢 TESTED |
| Core types | 🟢 IMPLEMENTED |
| Variables / constants | 🟢 IMPLEMENTED |
| Expressions | 🟢 IMPLEMENTED |
| Operators | 🟢 IMPLEMENTED |
| Conditions | 🟢 IMPLEMENTED |
| Functions | 🟢 IMPLEMENTED |
| Scope | 🟢 IMPLEMENTED |
| Return / pass | 🟢 IMPLEMENTED |
| Basic I/O | 🟢 IMPLEMENTED |
| Extended language features | 🟡 IN PROGRESS |
| `mat` | 🟡 UNDEFINED |
| `await` | 🟡 NOT IMPLEMENTED |
| Modules | 🔴 NOT IMPLEMENTED |
| ESP32 integration | 🔴 NOT IMPLEMENTED |
| Calculator engine | 🔴 NOT IMPLEMENTED |
| GameEngine / Games | 🔴 NOT IMPLEMENTED |
| Plugins | 🔴 NOT IMPLEMENTED |

**Current conclusion:** the Resiris PC prototype has a solid, tested core. The next development stage should focus on finishing and defining the remaining language-core behavior before moving into modules, hardware integration, and the ESP32 implementation.