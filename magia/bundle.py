from typing import Optional, Union

from .constants import SignalType
from .core import Input, Output, Signal, SignalDict


class SignalBundle:
    def __init__(self, **kwargs):
        self._signals = SignalDict()

    @property
    def signals(self) -> list[Signal]:
        return list(self._signals.values())

    @property
    def signal_names(self) -> list[str]:
        return list(self._signals.keys())

    def __add__(self, other: Union["SignalBundle", list[Signal], Signal]) -> "SignalBundle":
        new_bundle = SignalBundle()
        new_bundle += self
        new_bundle += other
        return new_bundle

    def __iadd__(self, other: Union["SignalBundle", list[Signal], Signal]) -> "SignalBundle":
        if isinstance(other, SignalBundle):
            other = other.signals
        if isinstance(other, Signal):
            other = [other]
        for signal in other:
            if signal.name in self.signal_names:
                raise KeyError(f"Signal {signal.name} is already defined.")
            self._signals[signal.name] = signal.copy()
        return self

    def __getattr__(self, name: str) -> Signal:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self.signal_names:
            return self.__getitem__(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Signal):
        """
        Avoid IO Bundle to be modified by mistake.
        """
        if name.startswith("_"):
            return super().__setattr__(name, value)
        if isinstance(value, Signal):
            self.__setitem__(name, value)
        else:
            super().__setattr__(name, value)

    def __getitem__(self, item: str) -> Signal:
        return self._signals[item]

    def __setitem__(self, key, value):
        self._signals[key] = value


class IOBundle(SignalBundle):
    """
    Define a bundle of signals, which can be used as the input or output of a module.
    """

    def __init__(self, owned_by: Optional["Instance"] = None):
        super().__init__()
        self._input_names: list[str] = []
        self._output_names: list[str] = []
        self._owned_by: Optional["Instance"] = owned_by

    def __iadd__(self, other: Union["IOBundle", list[Union[Input, Output]], Input, Output]) -> "IOBundle":
        if isinstance(other, IOBundle):
            other = other.signals
        if isinstance(other, Signal):
            other = [other]

        for port in other:
            if port.type == SignalType.INPUT:
                self._input_names.append(port.name)
            elif port.type == SignalType.OUTPUT:
                self._output_names.append(port.name)
            else:
                raise TypeError(f"Signal Type {port.type} is forbidden in IOBundle.")
            if port.name in self.signal_names:
                raise KeyError(f"Port {port.name} is already defined.")
            self._signals[port.name] = port.copy(owned_by=self._owned_by)

        return self

    def inputs(self) -> list[Signal]:
        return [
            signal for signal in self._signals.values()
            if signal.type == SignalType.INPUT
        ]

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

    def flip(self, ignore: Optional[list[str]] = None) -> "IOBundle":
        """
        Create a new IOBundle with the Input and Output inverted.
        Ports specified in the `ignore` arguments will not be inverted.

        If `ignore` is not specified, default ports: "clk", "rst_n", "reset" are remain unchanged.
        """
        if ignore is None:
            ignore = ["clk", "rst_n", "reset"]
        new_bundle = IOBundle()
        for port in self.signals:
            if port.name in ignore:
                new_bundle += port
            else:
                new_port_type = {
                    SignalType.INPUT: Output,
                    SignalType.OUTPUT: Input,
                }[port.type]
                new_port = new_port_type(name=port.name, width=len(port), signed=port.signed)
                new_bundle += new_port
        return new_bundle

    def signal_bundle(self) -> SignalBundle:
        """
        Return a Signal Bundle that turns all the ports into normal signals
        """
        new_bundle = SignalBundle()
        for port in self.signals:
            new_bundle += Signal(name=port.name, width=len(port), signed=port.signed)
        return new_bundle

    def with_name(self, prefix: str = "", suffix: str = "") -> "IOBundle":
        """
        Create a new IOBundle with the name of each port prefixed with `prefix` and suffixed with `suffix`.
        """
        new_bundle = IOBundle()
        for port in self.signals:
            new_port_type = {
                SignalType.INPUT: Input,
                SignalType.OUTPUT: Output,
            }[port.type]
            new_port = new_port_type(name=f"{prefix}{port.name}{suffix}", width=len(port), signed=port.signed)
            new_bundle += new_port
        return new_bundle
