# Elaborate designs

Elaboration in Magia is the process of generating SystemVerilog code from Magia modules.
Magia provides `Elaborator` for a simple elaboration flow.

During the elaboration, Magia will check the correctness of the design and raise exceptions if any.

Submodules instantiated under the top modules will be elaborated as well.
Therefore, the elaborated results may contain multiple modules.

`Elaborator` provides multiple methods, which suits different use cases.

- `to_string`: return all elaborated SystemVerilog code as a string.
- `to_dict`: return elaborated SystemVerilog code as a dictionary, in the form of `{"module_name": "sv_code"}`.
- `to_file`: write all elaborated SystemVerilog code to a single file.
- `to_files`: write elaborated SystemVerilog code to a directory.

## Elaborate Multiple Modules

All elaboration methods accept a list of modules as input.
Multiple modules can be elaborated at the same time.

```python
from magia import Module, Elaborator


class Adder(Module):
    def __init__(self, width, **kwargs):
        ...


Elaborator.to_string(Adder(width=8), Adder(width=16), ...)
```

## Naming the Module

The name of the top module can be specified by the `name` parameter in the constructor.
e.g. `TopModeule(name="my_top")` results in

```verilog
module my_top(
...
endmodule
```

The Elaborator generates unique name for each module if it is not specified.

## Specify the output file name

Each specialized module (`Module(param=123,...)`) is written to an individual file when using `Elaborator.to_files()`
The file name is the module name with `.sv` extension.

You can specify the output file name, and grouping multiple modules under the same class, by using the `file` decorator.

```python
from magia import Module, Elaborator


@Elaborator.file("adder.sv")
class Adder(Module): ...


@Elaborator.file("mult.sv")
class Multiplier(...): ...


Elaborator.to_files("output", Adder(10), Adder(16), Multiplier(10), Multiplier(16))  # Results in a file tree
# output/adder.sv: "Adder_0, Adder_1"
# output/mult.sv: "Multiplier_0, Multiplier_1"
```

## Examples

Given the following design:

```python
from magia import Module, Elaborator


class SubModule(Module):
    ...


class TopModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        s1 = SubModule(param=123).instance()
        s2 = SubModule(param=456).instance()
        ...


# Elaborate SystemVerilog code
Elaborator.elaborate____(TopModule(param1=1, param2=2))
```

### Elaborate to a string

```python
# result is a string containing the code for "TopModule", "SubModule(param=123)" and "SubModule(param=456)"
result = Elaborator.to_string(TopModule(param1=1, param2=2, name="TopModule"))
```

### Elaborate to a File

```python
Elaborator.to_file("/tmp/output.sv", TopModule(param1=1, param2=2, name="TopModule"))
```

```bash
$ cat /tmp/output.sv

module TopModule(
...
module SubModule_0(
...
module SubModule_1(
...
endmodule
``` 

### Elaborate to a Dict

```python
result = Elaborator.to_dict(TopModule(param1=1, param2=2, name="TopModule"))
result = {
    "TopModule": "SV Code for TopModule(...)",
    "SubModule_0": "SV Code for SubModule(param=123)",
    "SubModule_1": "SV Code for SubModule(param=456)",
}
```

### Elaborate to Files

`Elaborator.to_files()` contains the files for each modules, and return a list of the paths to the files.

```python
files = Elaborator.to_files("/tmp/output_dir", TopModule(param1=1, param2=2, name="TopModule"))
files = [
    Path("/tmp/output_dir/TopModule.sv"),
    Path("/tmp/output_dir/SubModule_0.sv"),
    Path("/tmp/output_dir/SubModule_1.sv"),
]
```
 