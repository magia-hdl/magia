import logging
from typing import Optional, Union

from .constants import SignalType
from .core import Constant, Input, Output, Signal, SignalDict

logger = logging.getLogger(__name__)


class IOPorts:
    """
    Define a bundle of I/O, which can be used as the input or output of a module.
    An IOBundle can be added with Input and Output.
    However, the bundle cannot be used as normal signals.
    The actual signals can be accessed from `input` and `output` of the instance instead.

    We can use `signal_bundle()` to create a SignalBundle that turns all the ports into normal signals,
    which we can connect to the instance of the module and other destinations.
    It can be accessed by individual port by attributes, or connect to multiple instance directly.
    """

    def __init__(self, owner_instance: Optional["Instance"] = None, **kwargs):
        self._signals = SignalDict()
        self._input_names: list[str] = []
        self._output_names: list[str] = []
        self._owner_instance: Optional["Instance"] = owner_instance

    def __add__(self, other: Union["IOPorts", list[Union[Input, Output]], Input, Output]) -> "IOPorts":
        new_ports = IOPorts()
        new_ports += self
        new_ports += other
        return new_ports

    def __iadd__(self, other: Union["IOPorts", list[Union[Input, Output]], Input, Output]) -> "IOPorts":
        if isinstance(other, IOPorts):
            other = other.inputs + other.outputs
        if isinstance(other, (Input, Output)):
            other = [other]

        for port in other:
            if port.name in self.input_names + self.output_names:
                raise KeyError(f"Port {port.name} is already defined.")

            if port.type == SignalType.INPUT:
                self._input_names.append(port.name)
            elif port.type == SignalType.OUTPUT:
                self._output_names.append(port.name)
            else:
                raise TypeError(f"Signal Type {port.type} is forbidden in IOBundle.")

            self._signals[port.name] = port.copy(owner_instance=self._owner_instance)

        return self

    def __getattr__(self, name: str) -> Union[Input, Output]:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self.input_names + self.output_names:
            return self.__getitem__(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Union[Input, Output]):
        if name.startswith("_"):
            super().__setattr__(name, value)
        if isinstance(value, Signal):
            self.__setitem__(name, value)
        else:
            super().__setattr__(name, value)

    def __getitem__(self, item: str) -> Union[Input, Output]:
        return self._signals[item]

    def __setitem__(self, key, value):
        self._signals[key] = value

    @property
    def inputs(self) -> list[Signal]:
        return [
            signal for signal in self._signals.values()
            if signal.type == SignalType.INPUT
        ]

    @property
    def outputs(self) -> list[Signal]:
        return [
            signal for signal in self._signals.values()
            if signal.type == SignalType.OUTPUT
        ]

    @property
    def input_names(self) -> list[str]:
        return self._input_names

    @property
    def output_names(self) -> list[str]:
        return self._output_names

    @property
    def signals(self) -> SignalDict:
        return self._signals
