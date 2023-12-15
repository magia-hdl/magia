from typing import Optional, Union

from .constants import SignalType
from .core import Input, Output, Signal, SignalDict, Constant


class SignalBundle:
    def __init__(self, **kwargs):
        self._signals = SignalDict()

    @property
    def signals(self) -> list[Signal]:
        return list(self._signals.values())

    @property
    def signal_alias(self) -> list[str]:
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
            if signal.name in self.signal_alias:
                raise KeyError(f"Signal {signal.name} is already defined.")
            if isinstance(signal, Input) or isinstance(signal, Output) or isinstance(signal, Constant):
                raise TypeError(f"Signal Type {signal.type} is forbidden in SignalBundle.")
            self._signals[signal.name] = signal.copy()
        return self

    def __getattr__(self, name: str) -> Signal:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self.signal_alias:
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

    def with_alias(self, prefix: str = "", suffix: str = "") -> "SignalBundle":
        """
        Create a new SignalBundle with the alias of each signal prefixed with `prefix` and suffixed with `suffix`.
        The signal contained in the new bundle is the same as the original one.
        """
        new_bundle = SignalBundle()
        for alias, signal in self._signals.items():
            new_bundle._signals[f"{prefix}{alias}{suffix}"] = signal
        return new_bundle

    def copy(self) -> "SignalBundle":
        """
        Create a new SignalBundle with the same signals alias as the original one.
        The signals contained in the new bundle are different from the original one.
        """
        new_bundle = SignalBundle()
        new_bundle += self
        return new_bundle


class IOBundle:
    """
    Define a bundle of I/O, which can be used as the input or output of a module.
    """

    def __init__(self, owner_instance: Optional["Instance"] = None, **kwargs):
        self._signals = SignalDict()
        self._input_names: list[str] = []
        self._output_names: list[str] = []
        self._owner_instance: Optional["Instance"] = owner_instance

    @property
    def owner_instance(self) -> Optional["Instance"]:
        return self._owner_instance

    def __add__(self, other: Union["IOBundle", list[Union[Input, Output]], Input, Output]) -> "IOBundle":
        new_bundle = IOBundle()
        new_bundle += self
        new_bundle += other
        return new_bundle

    def __iadd__(self, other: Union["IOBundle", list[Union[Input, Output]], Input, Output]) -> "IOBundle":
        if isinstance(other, IOBundle):
            other = other.inputs + other.outputs
        if isinstance(other, Input) or isinstance(other, Output):
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

            self._signals[port.name] = port.copy(owner_instance=self.owner_instance)

        return self

    def __getattr__(self, name: str) -> Union[Input, Output]:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self.input_names + self.output_names:
            return self.__getitem__(name)
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Union[Input, Output]):
        if name.startswith("_"):
            return super().__setattr__(name, value)
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
