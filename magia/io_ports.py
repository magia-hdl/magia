from __future__ import annotations

import typing

from .data_struct import SignalDict
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
                other = list(other.signals.values())
            elif other.is_input or other.is_output:
                other = [other]

        for port in other:
            self._add_port(port)

        return self

    def _add_port(self, port: Input | Output):
        """Copy the given port and add it into current IOPorts."""
        if port.name in self.signals:
            raise KeyError(f"Port {port.name} is already defined.")

        bundle_config = {
            "bundle": port.signal_config.bundle,
            "bundle_spec": port.signal_config.bundle_spec,
            "bundle_alias": port.signal_config.bundle_alias,
            "bundle_type": port.signal_config.bundle_type,
        }
        match port:
            case Input():
                self.signals[port.name] = Input.like(
                    port, owner_instance=self._owner_instance,
                    **bundle_config,
                )
            case Output():
                self.signals[port.name] = Output.like(
                    port, owner_instance=self._owner_instance,
                    **bundle_config,
                )
            case _:
                raise TypeError(f"Signal Type {type(port).__name__} is forbidden in IOPorts.")

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
            if signal.is_input
        ]

    @property
    def outputs(self) -> list[Signal]:
        return [
            signal for signal in self.signals.values()
            if signal.is_output
        ]

    @property
    def input_names(self) -> list[str]:
        return [
            name for name, port in self.signals.items()
            if port.is_input
        ]

    @property
    def output_names(self) -> list[str]:
        return [
            name for name, port in self.signals.items()
            if port.is_output
        ]

    def __ilshift__(self, other: Bundle):
        if self._owner_instance is not None:
            raise TypeError("Connect the bundle to an Instance directly, instead of `Instance.io <<= Bundle`.")
        other.connect_to(self)
        return self
