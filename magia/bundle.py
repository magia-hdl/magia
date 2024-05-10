from __future__ import annotations

import enum

from .data_struct import SignalDict
from .io_ports import IOPorts
from .io_signal import Input, Output
from .module import Instance
from .signals import Signal


class BundleType(enum.Enum):
    MASTER = 0
    SLAVE = 1
    MONITOR = 2


class BundleSpec:
    """
    Specification of a signal bundle.

    Use to spin up a bundle / IO ports
    """

    def __init__(self, **kwargs):
        self.bus_signature: str = ""  # Identifying different types of buses

        self.common = SignalDict()
        self.forward = SignalDict()
        self.backward = SignalDict()

        self.routing_map: dict[str, str] = {}
        self.prefix = self.suffix = ""

    def add_common(self, signal: Signal):
        """
        Adding a common signal into the bundle spec.

        Common signals are always with same direction on both master and slave.
        (e.g. Clocks, Resets, etc.)
        """
        name = signal.name
        if name is None:
            raise ValueError("Signal must have a name")
        if name in self.common or name in self.forward or name in self.backward:
            raise ValueError(f"Signal {name} already exists")
        match signal:
            case Input():
                self.common[name] = Input.like(signal)
            case Output():
                self.common[name] = Output.like(signal)
            case _:
                raise ValueError(f"Common signal {name} must be an input / output")

    def add_signal(self, signal: Signal):
        """
        Adding an Input/Output into the bundle spec.

        These signals will flip direction on master and slave.
        The direction of the signal is in the perspective of the master.
        """
        name = signal.name
        if name is None:
            raise ValueError("Signal must have a name")
        if name in self.common or name in self.forward or name in self.backward:
            raise ValueError(f"Signal {name} already exists in common")

        match signal:
            case Input():
                self.backward[name] = Signal.like(signal)
            case Output():
                self.forward[name] = Signal.like(signal)
            case _:
                raise ValueError(f"Unknown signal type {type(signal).__name__}")

    def __iadd__(self, other: Signal | list[Signal] | IOPorts):
        if isinstance(other, Signal):
            other = [other]
        elif isinstance(other, IOPorts):
            other = list(other.signals.values())
        for signal in other:
            self.add_signal(signal)
        return self

    def route_ports(self, src: str, dst: str):
        """
        Specify a connection between two signals, when they have different names on master and slave.

        e.g. connect("data_in", "data_out") will connect the signal "data_in" on master to "data_out" on slave,
        and vice versa.
        These signals must be specified as common signals in the bundle spec.
        """
        if src not in self.common or dst not in self.common:
            raise ValueError(f"Signal {src} and {dst} needs to be specified as common signals with `add_common()`")

        self.routing_map[src] = dst
        self.routing_map[dst] = src

    def _spec_gen(self, prefix: None | str = None, suffix: None | str = None) -> BundleSpec:
        new_spec = BundleSpec()
        if prefix is not None:
            new_spec.prefix = prefix
        if suffix is not None:
            new_spec.suffix = suffix
        for signal in self.common.values():
            new_spec.add_common(signal)
        new_spec += [Output.like(signal) for signal in self.forward.values()]
        new_spec += [Input.like(signal) for signal in self.backward.values()]
        return new_spec

    # IO Ports factory methods
    def _create_ports(
            self,
            prefix: None | str, suffix: None | str,
            inputs: list[Signal], outputs: list[Signal],
            bundle_type: BundleType,
    ) -> IOPorts:
        new_spec = self._spec_gen(prefix, suffix)
        new_ports = IOPorts()
        new_ports += [
            Input.like(
                port,
                name=new_spec.prefix + port.name + new_spec.suffix,
                bundle_spec=new_spec,
                bundle_alias=port.name,
                bundle_type=bundle_type,
            )
            for port in inputs
        ]
        new_ports += [
            Output.like(
                port,
                name=new_spec.prefix + port.name + new_spec.suffix,
                bundle_spec=new_spec,
                bundle_alias=port.name,
                bundle_type=bundle_type,
            )
            for port in outputs
        ]
        return new_ports

    def master_ports(self, prefix: None | str = None, suffix: None | str = None) -> IOPorts:
        input_signals = [
                            signal for signal in self.common.values()
                            if signal.is_input
                        ] + list(self.backward.values())
        output_signals = [
                             signal for signal in self.common.values()
                             if signal.is_output
                         ] + list(self.forward.values())
        return self._create_ports(prefix, suffix, input_signals, output_signals, BundleType.MASTER)

    def slave_ports(self, prefix: None | str = None, suffix: None | str = None) -> IOPorts:
        input_signals = [
                            signal for signal in self.common.values()
                            if signal.is_input
                        ] + list(self.forward.values())
        output_signals = [
                             signal for signal in self.common.values()
                             if signal.is_output
                         ] + list(self.backward.values())
        return self._create_ports(prefix, suffix, input_signals, output_signals, BundleType.SLAVE)

    def monitor_ports(self, prefix: None | str = None, suffix: None | str = None) -> IOPorts:
        input_signals = list(self.common.values()) + list(self.forward.values()) + list(self.backward.values())
        output_signals = []
        return self._create_ports(prefix, suffix, input_signals, output_signals, BundleType.MONITOR)

    # Signal Bundle factory method
    def bundle(self, name: None | str = None) -> Bundle:
        new_bundle = Bundle(new_spec := self._spec_gen(), name)
        new_signals = list(self.common.values()) + list(self.forward.values()) + list(self.backward.values())
        for signal in new_signals:
            new_bundle.signals[signal.name] = Signal.like(
                signal,
                name=None,
                bundle=new_bundle,
                bundle_spec=new_spec,
                bundle_alias=signal.name,
            )
        return new_bundle


class Bundle:
    """A signal bundle, containing a set of signals."""

    def __init__(
            self, spec: BundleSpec, name: None | str = None,
            prefix: None | str = None,
            suffix: None | str = None,
            **kwargs
    ):
        self._spec = spec
        self._name = name
        self._signals: SignalDict = SignalDict()
        self._prefix = prefix if prefix is not None else ""
        self._suffix = suffix if suffix is not None else ""

    def __getitem__(self, item: str) -> Signal:
        return self._signals[item]

    def __setitem__(self, key, value):
        self._signals[key] = value

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

    @property
    def name(self) -> str:
        return self._name

    @property
    def signals(self) -> SignalDict:
        return self._signals

    @property
    def prefix(self) -> str:
        return self._prefix

    @property
    def suffix(self) -> str:
        return self._suffix

    def with_name(self, prefix: None | str = None, suffix: None | str = None) -> Bundle:
        """
        Create a view of bundle with different signal names.

        The signals are not copied, only the names are changed.
        It is used to connect to IOPorts with multiple bundles with different names.
        """
        new_bundle = Bundle(self._spec, self._name, prefix, suffix)
        new_bundle._signals = self._signals
        return new_bundle

    def _connection_map(self, bundle_type: BundleType, connecting_instance: bool) -> dict[str, str]:
        """Return a map of signal names within the bundle to their target signal names on a module's IOPort."""
        bundle_names = list(self._signals.keys())
        port_names = {
            name: f"{self.prefix}{name}{self.suffix}"
            for name in bundle_names
        }
        if connecting_instance and bundle_type == BundleType.SLAVE:
            # Reroute signals in case of connecting to slave bundles on an instance.
            return {
                name: port_names[self._spec.routing_map.get(name, name)]
                for name in bundle_names
            }
        # No rerouting needed for master/monitor bundles or bundles on a module.
        return {
            name: port_names[name]
            for name in bundle_names
        }

    def connect_to(self, target_io: IOPorts | Instance):
        """Connect the bundle to an IOPorts, owned by an Instance / Module."""
        if not isinstance(target_io, (IOPorts, Instance)):
            raise ValueError(f"Target must be an IOPorts or an Instance, got {type(target_io).__name__}")

        # Find one of the port from the target IOPorts
        # to obtain the bundle type
        connect_to_instance = isinstance(target_io, Instance)
        first_port = next(iter(self.signals.keys()))
        target_name = f"{self.prefix}{first_port}{self.suffix}"
        target_port = (mod_io := target_io.module.io)[target_name] if connect_to_instance else target_io[target_name]

        # Obtain target bundle information
        target_type = target_port.signal_config.bundle_type
        connection_map = self._connection_map(target_type, connect_to_instance)

        ports_set = set(mod_io.signals.keys()) if connect_to_instance else set(target_io.signals.keys())
        # Check if any port is missing
        missing_ports = [
            target_name
            for target_name in connection_map.values()
            if target_name not in ports_set
        ]
        if missing_ports:
            raise ValueError(f"Missing ports: {missing_ports} in target IOPorts")

        if connect_to_instance:
            # IO ports owned by instance
            # Inputs are load, outputs are drivers
            for src_name, dst_name in connection_map.items():
                match mod_io[dst_name]:
                    case Input():
                        target_io.io[dst_name] <<= self[src_name]
                    case Output():
                        self[src_name] <<= target_io.io[dst_name]

        else:
            # IO ports owned by module
            # Inputs are drivers, outputs are loads
            for src_name, dst_name in connection_map.items():
                match target_io[dst_name]:
                    case Input():
                        self[src_name] <<= target_io[dst_name]
                    case Output():
                        target_io[dst_name] <<= self[src_name]
