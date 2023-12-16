from typing import Optional, Union

from .constants import SignalType
from .core import Constant, Input, Output, Signal, SignalDict


class SignalBundleView:
    def __init__(self, **kwargs):
        self._signals = SignalDict()

    @property
    def signals(self) -> list[Signal]:
        return list(self._signals.values())

    @property
    def signal_alias(self) -> list[str]:
        return list(self._signals.keys())

    def __add__(self, other: Union["SignalBundle", "SignalBundleView", list[Signal], Signal]) -> "SignalBundleView":
        new_view = SignalBundleView()
        new_view += self
        new_view += other
        return new_view

    def __iadd__(self, other: Union["SignalBundle", "SignalBundleView", list[Signal], Signal]) -> "SignalBundleView":
        if isinstance(other, (SignalBundle, SignalBundleView)):
            other = other.signals
        if isinstance(other, Signal):
            other = [other]
        for signal in other:
            if not isinstance(signal, Signal):
                raise TypeError(f"Signal {signal} is not a Signal object.")
            if signal.name in self.signal_alias:
                raise KeyError(f"Signal {signal.name} is already defined.")
            if isinstance(signal, (Input, Output, Constant)):
                raise TypeError(f"Signal Type {signal.type} is forbidden in SignalBundleView.")
            self._signals[signal.name] = signal

        return self

    def __getattr__(self, alias: str) -> Signal:
        if alias.startswith("_"):
            return super().__getattribute__(alias)
        if alias in self.signal_alias:
            return self.__getitem__(alias)
        return super().__getattribute__(alias)

    def __setattr__(self, alias: str, value: Signal):
        """
        Avoid Bundle to be modified by mistake.
        """
        if alias.startswith("_"):
            super().__setattr__(alias, value)
        if isinstance(value, Signal):
            self.__setitem__(alias, value)
        else:
            super().__setattr__(alias, value)

    def __getitem__(self, item: str) -> Signal:
        return self._signals[item]

    def __setitem__(self, key, value):
        self._signals[key] = value

    def with_alias(self, prefix: str = "", suffix: str = "") -> "SignalBundleView":
        """
        Create a new SignalBundleView with a renamed alias.
        Each signal can be access with an alias prefixed with `prefix` and suffixed with `suffix`.
        The signal contained in the new bundle is the same as the original one.
        """
        new_bundle = SignalBundleView()
        for alias, signal in self._signals.items():
            new_bundle[f"{prefix}{alias}{suffix}"] = signal
        return new_bundle

    def select(self, *alias: list[str]) -> "SignalBundleView":
        """
        Select a subset of signals from the bundle and create a new SignalBundleView.
        """
        new_bundle = SignalBundleView()
        for signal_alias, signal in self._signals.items():
            if signal_alias in alias:
                new_bundle[signal_alias] = signal
        return new_bundle

    def exclude(self, *alias: list[str]) -> "SignalBundleView":
        """
        Exclude a subset of signals from the bundle and create a new SignalBundleView.
        """
        new_bundle = SignalBundleView()
        for signal_alias, signal in self._signals.items():
            if signal_alias not in alias:
                new_bundle[signal_alias] = signal
        return new_bundle


class SignalBundle(SignalBundleView):
    def __add__(self, other: Union["SignalBundle", list[Signal], Signal]) -> "SignalBundle":
        new_bundle = SignalBundle()
        new_bundle += self
        new_bundle += other
        return new_bundle

    def __iadd__(self, other: Union["SignalBundle", list[Signal], Signal]) -> "SignalBundle":

        if isinstance(other, SignalBundleView):
            raise TypeError("Cannot add SignalBundleView to SignalBundle.")

        if isinstance(other, SignalBundle):
            other = other.signals
        if isinstance(other, Signal):
            other = [other]
        for signal in other:
            if not isinstance(signal, Signal):
                raise TypeError(f"Signal {signal} is not a Signal object.")
            if signal.name in self.signal_alias:
                raise KeyError(f"Signal {signal.name} is already defined.")
            if isinstance(signal, (Input, Output, Constant)):
                raise TypeError(f"Signal Type {signal.type} is forbidden in SignalBundle.")
            self._signals[signal.name] = signal.copy(parent_bundle=self)
        return self

    def copy(self) -> "SignalBundle":
        """
        Create a new SignalBundle with the same signals alias as the original one.
        The signals contained in the new bundle are different from the original one.
        """
        new_bundle = SignalBundle()
        new_bundle += self
        return new_bundle

    def view(self) -> SignalBundleView:
        """
        Create a new SignalBundleView with the same signals alias as the original one.
        The signals contained in the new bundle are the same as the original one.
        """
        new_bundle = SignalBundleView()
        new_bundle += self
        return new_bundle


class IOBundle:
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

    def __add__(self, other: Union["IOBundle", list[Union[Input, Output]], Input, Output]) -> "IOBundle":
        new_bundle = IOBundle()
        new_bundle += self
        new_bundle += other
        return new_bundle

    def __iadd__(self, other: Union["IOBundle", list[Union[Input, Output]], Input, Output]) -> "IOBundle":
        if isinstance(other, IOBundle):
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
    def owner_instance(self) -> Optional["Instance"]:
        return self._owner_instance

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
        Return a SignalBundle that turns all the ports into normal signals
        The bundle can be connected to the instance of the module and other destinations.
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
