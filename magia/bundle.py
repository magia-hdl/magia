from .constants import SignalType
from .core import Signal, SignalConfig, SignalDict
from .module import IOPorts


class BundleSpec:
    """
    Specification of a signal bundle.
    Use to spin up a bundle / IO ports
    """

    def __init__(self, **kwargs):
        self.common_signals: dict[str, SignalConfig] = {}
        self.forward_signals: dict[str, SignalConfig] = {}
        self.backward_signals: dict[str, SignalConfig] = {}

    def add_common(self, signal: Signal):
        name = signal.name
        if name is None:
            raise ValueError("Signal must have a name")
        if name in self.common_signals or name in self.forward_signals or name in self.backward_signals:
            raise ValueError(f"Signal {name} already exists in common")
        self.common_signals[name] = SignalConfig(
            name=name,
            width=signal.width,
            signed=signal.signed,
            description=signal.description,
            type=SignalType.INPUT,
        )

    def add_signal(self, signal: Signal):
        name = signal.name
        if name is None:
            raise ValueError("Signal must have a name")
        if name in self.common_signals or name in self.forward_signals or name in self.backward_signals:
            raise ValueError(f"Signal {name} already exists in common")

        if signal.type == SignalType.INPUT:
            target = self.backward_signals
        elif signal.type == SignalType.OUTPUT:
            target = self.forward_signals
        else:
            raise ValueError(f"Unknown signal type {signal.type}")
        target[name] = SignalConfig(
            name=name,
            width=signal.width,
            signed=signal.signed,
            description=signal.description,
            type=signal.type,
        )

    # IO Ports factory methods
    def master_ports(self) -> IOPorts:
        ...

    def slave_ports(self) -> IOPorts:
        ...

    def monitor_ports(self) -> IOPorts:
        ...

    # Signal Bundle factory method
    def bundle(self) -> "Bundle":
        ...


class Bundle:
    """
    A signal bundle, containing a set of signals
    """
    def __init__(self, **kwargs):
        self._spec = BundleSpec()
        self._signals: SignalDict = SignalDict()
