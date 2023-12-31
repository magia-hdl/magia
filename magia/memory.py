"""
Memory object
"""
import string
from dataclasses import dataclass
from itertools import count
from typing import Optional

from .constants import SignalType
from .core import Input, Output, Signal, SignalDict, Synthesizable


@dataclass
class MemoryConfig:
    address_width: int
    data_width: int
    name: str


class MemorySignal(Signal):
    """
    A signal that can be used to access a memory object.

    Args:
        memory (Memory): The memory object to access.
        name (str, optional): The name of the signal. Defaults to None.
    """

    def __init__(self, memory: "Memory", name: str, width: int, drive_by_mem: bool = False, **kwargs):
        super().__init__(name=name, width=width, **kwargs)
        self._config.signal_type = SignalType.MEMORY
        self._memory = memory
        self._drive_by_mem = drive_by_mem

    @property
    def memory(self) -> "Memory":
        return self._memory

    @property
    def drive_by_mem(self) -> bool:
        return self._drive_by_mem

    @property
    def drivers(self) -> list[Signal]:
        """
        Get the drivers of the signal.
        """
        if self.drive_by_mem:
            return self.memory.drivers
        return super().drivers

    def driver(self, driver_name: str = Signal.SINGLE_DRIVER_NAME) -> Optional["Signal"]:
        """
        Get the driver of the signal.
        :param driver_name: The name of the driver. Default to the single driver.
        :return: The driver signal.
        """
        if self.drive_by_mem:
            return Output("dummy", 1)
        return self._drivers.get(driver_name)


class MemPort:
    """
    Base class for memory ports.
    Args:
        memory (Memory): The memory object to write to.
        name (str, optional): The name of the write port.
    """

    def __init__(self, memory: "Memory", name: str, **kwargs):
        super().__init__(**kwargs)
        self._memory = memory
        self._name = name
        self._signals = SignalDict()

    @property
    def memory(self) -> "Memory":
        return self._memory

    @property
    def name(self) -> str:
        return self._name

    def wiring_dict(self) -> dict[str, str]:
        raise NotImplementedError

    @property
    def signals(self) -> list[MemorySignal]:
        return list(self._signals.values())

    def __getitem__(self, item: str) -> MemorySignal:
        return self._signals[item]

    def __setitem__(self, key, value):
        self._signals[key] = value

    def __getattr__(self, name: str) -> MemorySignal:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self._signals:
            return self.__getitem__(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: MemorySignal):
        if name.startswith("_"):
            super().__setattr__(name, value)
        if isinstance(value, MemorySignal):
            self.__setitem__(name, value)
        else:
            super().__setattr__(name, value)

    def elaborate(self) -> str:
        raise NotImplementedError


class MemWritePort(MemPort):
    """
    A write port for a memory object.

    Args:
        memory (Memory): The memory object to write to.
        name (str, optional): The name of the write port.
    """

    _IMPL_TEMPLATE = string.Template(
        "always_ff @(posedge $clk) begin\n"
        "  if ($wen) $mem[$addr] <= $din;\n"
        "end"
    )

    def __init__(self, memory: "Memory", name: str, **kwargs):
        super().__init__(memory=memory, name=name, **kwargs)
        self._signals = SignalDict(
            din=MemorySignal(memory, f"{memory.name}_w_data_{name}", memory.data_width),
            addr=MemorySignal(memory, f"{memory.name}_w_addr_{name}", memory.address_width),
            wen=MemorySignal(memory, f"{memory.name}_w_en_{name}", 1),
        )

    def elaborate(self) -> str:
        return self._IMPL_TEMPLATE.substitute(
            mem=self.memory.net_name,
            clk=self.memory.clk.net_name,
            din=self.din.net_name,
            addr=self.addr.net_name,
            wen=self.wen.net_name,
        )


class MemReadPort(MemPort):
    """
    A read port for a memory object.

    Args:
        memory (Memory): The memory object to read from.
        name (str, optional): The name of the read port.
        registered (bool, optional): Whether the reading output is registered. Defaults to False.
    """

    _IMPL_REG_TEMPLATE = string.Template(
        "always_ff @(posedge $clk) begin\n"
        "  if ($en) $dout <= $mem[$addr];\n"
        "end"
    )
    _IMPL_COMB_TEMPLATE = string.Template(
        "always_comb begin\n"
        "  $dout = $mem[$addr];\n"
        "end"
    )

    def __init__(self, memory: "Memory", name: str, registered: bool = False, **kwargs):
        super().__init__(memory=memory, name=name, **kwargs)
        self._signals = SignalDict(
            dout=MemorySignal(memory, f"{memory.name}_r_data_{name}", memory.data_width, True),
            addr=MemorySignal(memory, f"{memory.name}_r_addr_{name}", memory.address_width),
        )
        if registered:
            self._signals["en"] = MemorySignal(memory, f"{memory.name}_r_en_{name}", 1)
        self._registered = registered

    def elaborate(self) -> str:
        template = self._IMPL_REG_TEMPLATE if self._registered else self._IMPL_COMB_TEMPLATE
        return template.substitute(
            mem=self.memory.net_name,
            clk=self.memory.clk.net_name,
            addr=self.addr.net_name,
            dout=self.dout.net_name,
            en=self.en.net_name if self._registered else "NONE",
        )


class MemRWPort(MemPort):
    """
    A memory port for a memory object, it shared the read and write signals at the same time.
    The reading output is registered.

    Args:
        memory (Memory): The memory object to write to.
        name (str, optional): The name of the write port.
        write_through (bool, optional): Whether the write port is write through. Defaults to True.
    """
    _IMPL_TEMPLATE = string.Template(
        "always_ff @(posedge $clk) begin\n"
        "  if ($en) begin\n"
        "    if ($wen) $mem[$addr] $assignment $din;\n"
        "    $dout <= $mem[$addr];\n"
        "  end\n"
        "end\n"
    )

    def __init__(self, memory: "Memory", name: str, write_through: bool = True, **kwargs):
        super().__init__(memory=memory, name=name, **kwargs)
        self._write_through = write_through
        self._signals = SignalDict(
            addr=MemorySignal(memory, f"{memory.name}_rw_addr_{name}", memory.address_width),
            din=MemorySignal(memory, f"{memory.name}_rw_din_{name}", memory.data_width),
            dout=MemorySignal(memory, f"{memory.name}_rw_dout_{name}", memory.data_width, True),
            wen=MemorySignal(memory, f"{memory.name}_rw_wen_{name}", 1),
            en=MemorySignal(memory, f"{memory.name}_rw_en_{name}", 1),
        )

    def elaborate(self) -> str:
        return self._IMPL_TEMPLATE.substitute(
            mem=self.memory.net_name,
            clk=self.memory.clk.net_name,
            assignment="=" if self._write_through else "<=",
            addr=self.addr.net_name,
            din=self.din.net_name,
            dout=self.dout.net_name,
            wen=self.wen.net_name,
            en=self.en.net_name,
        )


class Memory(Synthesizable):
    """
    A memory object, storing an array of signals which can be accessed by another signal as an index.
    The memory object represents only the memory itself, not the logic to access it.

    This class is intended to be used to elaborate as a BRAM or Distributed RAM, especially on FPGA.
    In case of ASIC, consider to adopt the SRAM with `Blackbox`,
    especially when the memory module is created / compiled externally.

    A write port can be added to the memory object with the `write_port` method.
    A read port can be added to the memory object with the `read_port` method
    A read/write port can be added to the memory object with the `rw_port` method

    Args:
        address_width (int): The width of the address bus.
        data_width (int): The width of the data bus.
        name (str, optional): The name of the memory object. Defaults to None.
        r_port (int, optional): The number of read ports. Defaults to 0.
        w_port (int, optional): The number of write ports. Defaults to 0.
        rw_port (int, optional): The number of read/write ports. Defaults to 0.
        rw_write_through (bool, optional): Whether the read/write port is write through. Defaults to True.
        registered_read (bool, optional): Whether the reading output of the read port is registered. Defaults to False.
    """

    new_mem_counter = count(0)
    _MEM_DECL_TEMPLATE = string.Template("logic $width $name $size;")

    def __init__(
            self,
            clk: Input, address_width: int, data_width: int,
            name: Optional[str] = None,
            r_port: int = 0,
            w_port: int = 0,
            rw_port: int = 0,
            rw_write_through: bool = True,
            registered_read: bool = True,
            **kwargs
    ):
        if not r_port and not w_port and not rw_port:
            raise ValueError("Memory must have at least one port")
        if rw_port > 2:
            raise ValueError("Memory can have at most 2 read/write ports")
        if rw_port == 2 and (r_port or w_port):
            raise ValueError("Memory in True Dual Port mode cannot have read or write ports")
        if rw_port and w_port:
            raise ValueError("Memory with Read/Write port cannot have extra write port")
        if not rw_port and w_port and not r_port:
            raise ValueError("Memory with Write port must have at least one read port")
        if rw_port and not registered_read:
            raise ValueError("Memory with Read/Write port must have registered read port")

        memory_size = 1 << address_width
        if name is None:
            name = f"{memory_size}_{data_width}_{next(Memory.new_mem_counter)}"
        name = f"mem_{name}"

        super().__init__(**kwargs)

        self._config = MemoryConfig(
            address_width=address_width,
            data_width=data_width,
            name=name,
        )

        self._clk = clk

        self._read_ports = [MemReadPort(self, f"{i}", registered_read) for i in range(r_port)]
        self._write_ports = [MemWritePort(self, f"{i}") for i in range(w_port)]
        self._rw_ports = [MemRWPort(self, f"{i}", rw_write_through) for i in range(rw_port)]

    @property
    def port_count(self) -> tuple[int, int, int]:
        return len(self._read_ports), len(self._write_ports), len(self._rw_ports)

    def read_port(self, index: int = 0) -> MemReadPort:
        return self._read_ports[index]

    def write_port(self, index: int = 0) -> MemWritePort:
        return self._write_ports[index]

    def rw_port(self, index: int = 0) -> MemRWPort:
        return self._rw_ports[index]

    @property
    def drivers(self) -> list[Signal]:
        return [
            signal
            for port in self._read_ports + self._write_ports + self._rw_ports
            for signal in port.signals
            if not signal.drive_by_mem
        ]

    @property
    def clk(self) -> Input:
        return self._clk

    def elaborate(self) -> str:
        mem_decl = self._MEM_DECL_TEMPLATE.substitute(
            width=f"[{self.data_width - 1}:0]",
            name=self.net_name,
            size=f"[0:{self.size - 1}]",
        )
        port_impl = "\n".join(port.elaborate() for port in self._write_ports + self._rw_ports + self._read_ports)
        return "\n".join((mem_decl, port_impl))

    @property
    def size(self) -> int:
        return 1 << self._config.address_width

    @property
    def address_width(self) -> int:
        return self._config.address_width

    @property
    def data_width(self) -> int:
        return self._config.data_width

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def net_name(self) -> str:
        """
        Memory does not belong to any bundle.
        net_name is the same as name.
        """
        return self._config.name

    @classmethod
    def sdp(cls, clk: Input, address_width: int, data_width: int, **kwargs) -> "Memory":
        """
        Create a Simple Dual Port memory.
        """
        return cls(clk, address_width, data_width, r_port=1, w_port=1, **kwargs)

    @classmethod
    def tdp(cls, clk: Input, address_width: int, data_width: int, **kwargs) -> "Memory":
        """
        Create a True Dual Port memory.
        """
        return cls(clk, address_width, data_width, rw_port=2, registered_read=True, **kwargs)

    @classmethod
    def sp(cls, clk: Input, address_width: int, data_width: int, **kwargs) -> "Memory":
        """
        Create a Single Port memory.
        """
        return cls(clk, address_width, data_width, rw_port=1, registered_read=True, **kwargs)
