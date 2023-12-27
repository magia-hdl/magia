# Memory Syntax

Memory in Magia is defined by `magia.Memory` class.
It is intended to generate Block RAMs and Distributed RAMs on FPGA.

## Example

```python
from magia import Memory, Module, Input, Output


# Define a 256x8 Block RAM
class MyModule(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Define IO ports
        self.io += [
            Input("clk", 1),
            Input("wen", 1),
            Input("addr", 8),
            Input("din", 8),
            Output("dout", 8),
        ]

        # Define memory
        mem = Memory(
            clk=self.io.clk,  # Specify the clock
            address_width=8, data_width=8,  # Define the size of the memory
            registered_read=True,  # Enable registered read, used to generate BRAM
            # Specify the amount of ports on the memory
            # Or using the shorthand function (Memory.SP/SDP/TDP)
            r_ports=1, w_ports=1,
        )

        # Access the signal of the port
        mem.read_port(0).addr <<= self.io.addr
        self.io.dout <<= mem.read_port(0).dout
        mem.read_port(0).en <<= 1

        for port in ["addr", "din", "wen"]:
            mem.write_port()[port] <<= self.io[port]
```

## Memory Ports

There are 3 types of memory ports: `ReadPort`, `WritePort` and `ReadWritePort`.
They are used to access the memory.

- `ReadPort`
    - Read data from the memory
- `WritePort`
    - Write data to the memory
- `ReadWritePort`
    - Read and write data from/to the memory. Only one of the operation can be performed per cycle.

| Port            | Signal | Direction | Description                                                                            |
|-----------------|--------|-----------|----------------------------------------------------------------------------------------|
| `ReadPort`      | `addr` | In        | Address of the memory                                                                  |
|                 | `dout` | Out       | Data read from the memory                                                              |
|                 | `en`   | In        | Read Enable. `dout` change only if `en` is 1 <br/> Available Only on Registered Output |
| `WritePort`     | `addr` | In        | Address of the memory                                                                  |
|                 | `din`  | In        | Data to be written to the memory                                                       |
|                 | `wen`  | In        | Write Enable. Data is written only when `wen` is 1                                     |
| `ReadWritePort` | `addr` | In        | Address of the memory                                                                  |
|                 | `din`  | In        | Data to be written to the memory                                                       |
|                 | `dout` | Out       | Data read from the memory                                                              |
|                 | `en`   | In        | Port Enable. Read and Writen is done only when `en` is 1                               |
|                 | `wen`  | In        | Write Enable. Data is written only when `wen` and `en` are 1                           |

### Accessing the memory port

The memory port can be accessed by using the `read_port`, `write_port` and `rw_port` methods.
If the memory has multiple ports, the index of the port can be specified.

```python
mem.read_port(0).addr <<= self.io.addr
```

### Memory Port Shorthand

| Type of Memory | Description                           | Equivalent         |
|----------------|---------------------------------------|--------------------|
| `Memory.SP()`  | Single Port with Read and Write       | rw_port=1          |
| `Memory.SDP()` | Simple Dual Ports. 1 read and 1 write | r_port=1, w_port=1 |
| `Memory.TDP()` | True Dual Ports.                      | rw_port=2          |

