from __future__ import annotations

import typing
from dataclasses import asdict

from .data_struct import SignalDict, SignalType
from .io_signal import Input, Output
from .signals import Signal

if typing.TYPE_CHECKING:
    from .bundle import Bundle
    from .module import Instance


class IOPorts:
    """
    Define a set of I/O, which can be used as the input or output of a module.

    An IOPorts can be added with Input and Output.
    However, the bundle cannot be used as normal signals.
    The actual signals can be accessed from `input` and `output` of the instance instead.

    We can use `signal_bundle()` to create a SignalBundle that turns all the ports into normal signals,
    which we can connect to the instance of the module and other destinations.
    It can be accessed by individual port by attributes, or connect to multiple instance directly.
    """

    def __init__(self, owner_instance: None | Instance = None, **kwargs):
        self.signals = SignalDict()
        self._owner_instance = owner_instance

    def __add__(self, other: IOPorts | list[Input | Output | IOPorts] | Input | Output) -> IOPorts:
        new_ports = IOPorts()
        new_ports += self
        new_ports += other
        return new_ports

    def __iadd__(self, other: IOPorts | list[Input | Output | IOPorts] | Input | Output) -> IOPorts:
        if isinstance(other, list):
            flatten = []
            for ports in other:
                if isinstance(ports, IOPorts):
                    flatten += ports.inputs + ports.outputs
                else:
                    flatten.append(ports)
            other = flatten
        else:
            if isinstance(other, IOPorts):
                other = other.inputs + other.outputs
            elif isinstance(other, (Input, Output)):
                other = [other]

        for port in other:
            self._add_port(port)

        return self

    def _add_port(self, port: Input | Output):
        """Copy the given port and add it into current IOPorts."""
        if port.name in self.signals:
            raise KeyError(f"Port {port.name} is already defined.")

        if port.type not in (SignalType.INPUT, SignalType.OUTPUT):
            raise TypeError(f"Signal Type {port.type} is forbidden in IOPorts.")

        self.signals[port.name] = port.__class__(
            **{
                k: v
                for k, v in asdict(port.signal_config).items()
                if k not in ("signal_type", "owner_instance",)
            },
            owner_instance=self._owner_instance,
        )

    def __getattr__(self, name: str) -> Input | Output:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self.signals:
            return self.__getitem__(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Input | Output):
        if name.startswith("_"):
            super().__setattr__(name, value)
        if isinstance(value, Signal):
            self.__setitem__(name, value)
        else:
            super().__setattr__(name, value)

    def __getitem__(self, item: str) -> Input | Output:
        return self.signals[item]

    def __setitem__(self, key, value):
        self.signals[key] = value

    @property
    def inputs(self) -> list[Signal]:
        return [
            signal for signal in self.signals.values()
            if signal.type == SignalType.INPUT
        ]

    @property
    def outputs(self) -> list[Signal]:
        return [
            signal for signal in self.signals.values()
            if signal.type == SignalType.OUTPUT
        ]

    @property
    def input_names(self) -> list[str]:
        return [
            name for name, port in self.signals.items()
            if port.type == SignalType.INPUT
        ]

    @property
    def output_names(self) -> list[str]:
        return [
            name for name, port in self.signals.items()
            if port.type == SignalType.OUTPUT
        ]

    def __ilshift__(self, other: Bundle):
        if self._owner_instance is not None:
            raise TypeError("Connect the bundle to an Instance directly, instead of `Instance.io <<= Bundle`.")
        other.connect_to(self)
        return self
