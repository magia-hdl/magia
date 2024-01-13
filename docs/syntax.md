# Magia Syntax

## Declare a Module

Inherit a class from `magia.Module` and define IO ports in `__init__` method.

```python
from magia import Input, Output, Module


class MyModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Define IO ports
        self.io += Input("clk", 1)
        self.io += Input("d", 8)
        self.io += Output("q", 8) 
```

## Specialize a Module

Specialize a module by calling the class with parameters.

```python
from magia import Input, Output, Module


class Adder(Module):
    def __init__(self, width, **kwargs):
        super().__init__(**kwargs)
        self.io += Input("a", width)
        self.io += Input("b", width)
        self.io += Output("q", width)


# Specialize 3 adders with different widths
adders = {
    8: Adder(8),
    16: Adder(16),
    32: Adder(32),
}
```

## Define and connect Signals

```python
from magia import Input, Output, Module, Signal


class MyModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Define IO ports
        self.io += Input("d", 8)
        self.io += Output("q", 8)

        # Define a signal in advance
        counter = Signal(8)

        # Connect signals
        self.io.q <<= counter
        counter <<= self.io.d
```

## Operations

Operations are defined by using builtin operators.
They generate new signals.

```python
from magia import Input, Output, Module


class MyModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Define IO ports
        self.io += Input("a", 8)
        self.io += Input("b", 8)
        self.io += Output("q0", 8)
        self.io += Output("q1", 8)
        self.io += Output("q2", 8)

        # Define operations

        self.io.q0 <<= self.io.a + self.io.b
        self.io.q1 <<= self.io.a - self.io.b

        # Expression will generate a signal
        # So we don't need to define it in advance or connect it with `<<=`
        multiplier = self.io.a * self.io.b
        # Operators can be chained, and work with literal constants
        self.io.q2 <<= multiplier + multiplier + 4

        # Obtain the width of a signal
        print(f"q0 width: {len(multiplier)}")

```

### Supported Operators

| Operator                   | Description                                                                        |
|----------------------------|------------------------------------------------------------------------------------|
| `<<=`                      | *Connect signals. This is not a Left Shift*                                        |
| `+`, `+=`                  | Addition                                                                           |
| `-`, `-=`                  | Subtraction                                                                        |
| `-signal`                  | Negation                                                                           |
| `*`, `*=`                  | Multiplication                                                                     |
| `&`, `&=`                  | Bitwise AND                                                                        |
| `\|` , `\|=`               | Bitwise OR                                                                         |
| `^`, `^=`                  | Bitwise XOR                                                                        |
| `~`                        | Bitwise NOT                                                                        |
| `<<`                       | Left shift (Only on Python Integer, Constant Shift)                                |
| `>>`                       | Right shift (Only on Python Integer, Constant Shift)                               |
| `==`                       | Equality                                                                           |
| `!=`                       | Inequality                                                                         |
| `<`                        | Less than                                                                          |
| `<=`                       | Less than or equal                                                                 |
| `>`                        | Greater than                                                                       |
| `>=`                       | Greater than or equal                                                              |
| `@` , `@=`                 | Concatenation                                                                      |
| `[y:x]`                    | Slicing (`[:]` and `[...]` represents the whole signal)                            |
|                            | Beware of endianness when slicing                                                  |
| `signal.reg()`             | Register a signal                                                                  |
| `signal.when(cond, else_)` | Gate the signal with a condition. Equivalent to `signal if cond else else_`        |
| `signal.case(cases)`       | Using the signal as a switch. Equivalent to `cases[signal]`                        |
| `signal.any()`             | Check if any bit in the signal is 1                                                |
| `signal.all()`             | Check if all bits in the signal are 1                                              |
| `signal.parity()`          | Compute the parity of the signal (Reduced XOR)                                     |
| `len(signal)`              | Get the width of a signal in Python                                                |
| `signal.with_width()`      | Create and connect to the new signal with specific width, trimming/padding is done |
| `signal.with_signed()`     | Create and connect to the new signal with specific signedness                      |

### Exceptions:

| Statements       | Description                                                                                  |
|------------------|----------------------------------------------------------------------------------------------|
| `<<=`            | **Connect signals. This is not a Left Shift**                                                |
| `>>=`            | This is not implemented.                                                                     |
| `//`, `/`, `%`   | Division related operator are not implemented.                                               |
| `if signal: ...` | Signal is an object, which is always `True`. Doesn't work with Python Expectation.           |
| `<=, <, >=, >`   | These operators return `Signal` **but not boolean.** Don't use it with `if signal < 10: ...` |

## Creating a Register

```python
from magia import Input, Output, Module, Signal


class MyModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Define IO ports
        self.io += Input("clk", 1)
        self.io += Input("d", 8)
        self.io += Output("q1", 8)
        self.io += Output("q2", 8)

        # Define a register
        self.io.q <<= self.io.d.reg(clk=self.io.clk)
```

## Instantiate a Module

```python
from magia import Input, Output, Module


class Adder(Module):
    def __init__(self, width, **kwargs):
        super().__init__(**kwargs)
        self.io += Input("a", width)
        self.io += Input("b", width)
        self.io += Output("q", width)


class TopLevel(Module):
    """
    Top level module with 2 adders
    """

    def __init__(self, width, **kwargs):
        super().__init__(**kwargs)
        self.io += Input("a", width)
        self.io += Input("b", width)
        self.io += Input("c", width)
        self.io += Output("q", width)

        # Specialize an adder
        adder = Adder(width)

        # Instantiate adders
        # Connect IO ports with `io` argument
        # We can skip part of ports and connect them in later steps
        adder1 = adder.instance(
            io={
                "a": self.io.a,
                "b": self.io.b,
            }
        )
        adder.instance(
            io={
                "a": adder1.outputs.q,
                "b": self.io.c,
                "q": self.io.q,
            }
        )

```
