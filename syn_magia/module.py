import inspect
from collections import Counter
from dataclasses import dataclass
from itertools import count
from string import Template
from typing import Optional

from .core import Synthesizable, Signal, SignalType, SignalDict
from .bundle import IOBundle


@dataclass
class ModuleConfig:
    module_class: type
    name: Optional[str] = None
    ...


@dataclass
class ModuleInstanceConfig:
    module: "Module"
    name: Optional[str] = None


class Module(Synthesizable):
    """
    A module is a collection of signals and operations. It can also include other modules.
    The module is the base class of specialized modules.
    Developers can define the generic behavior of the module in a dynamic way,
    while each `Module` objects is a specialized module initialized with specific parameters.

    The SystemVerilog Keyword `parameters` is not used here.
    It is because we can generate the code for the specialized module with parametrized values hard-coded.

    The module can be instantiated with the `instance` method.
    """
    MOD_DECL_TEMPLATE = Template("module $name (\n$io\n);")
    module_pool: dict[int, "Module"] = {}
    new_module_counter = count(0)

    def __init__(self, name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if name is None:
            name = f"{self.__class__.__name__}_{next(self.new_module_counter)}"
        if name in self._module_names():
            raise ValueError(f"Module name {name} is already used.")

        self._config = ModuleConfig(
            module_class=type(self),
            name=name,
        )
        self.io = IOBundle()
        self._signals: dict[str, Signal] = {}
        self._instance_counter = count(0)

        self.module_pool[id(self)] = self
        ...

    def __setitem__(self, key, value: Signal):
        if key in self._signals and value is not None:
            raise KeyError(f"Signal {key} is already defined.")
        if value is not None:
            value.set_name(key)
            self._signals[key] = value

    def __getitem__(self, item: str) -> Signal:
        signal = self._signals.get(item)
        if signal is None:
            raise KeyError(f"Signal {item} is not defined.")
        return signal

    def build(self):
        """
        Designer shall implement the module with this method.
        """
        ...

    def validate(self) -> bool:
        ...

    def elaborate(self) -> str:
        """
        Trace nets and operations from output ports
        This method generates the SystemVerilog code for the module, including the submodules.
        """
        # self.build()

        mod_decl = self.MOD_DECL_TEMPLATE.substitute(
            name=self.name,
            io=",\n".join(
                port.elaborate()
                for port in self.io.inputs() + self.io.outputs()
            ),
        )

        signals, insts = self.trace()
        mod_impl = [
            inst.elaborate()
            for inst in insts
        ]
        mod_impl += [
            signal.elaborate()
            for signal in signals
        ]

        mod_impl = "\n".join(mod_impl)

        mod_output_assignment = "\n".join(
            Signal.SIGNAL_ASSIGN_TEMPLATE.substitute(
                name=output.name,
                driver=output.driver().name,
            )
            for output in self.io.outputs()
        )

        mod_end = "endmodule"


    def trace(self) -> tuple[list[Signal], list["Instance"]]:
        """
        Trace nets and instances from output ports
        """
        traced_sig_id: set[int] = set()
        traced_inst_id: set[int] = set()
        traced_signal: list[Signal] = []
        traced_inst: list[Instance] = []
        sig_to_be_traced: dict[int, Signal] = {}

        for output in self.io.outputs():
            sig_to_be_traced |= {
                id(sig): sig
                for sig in output.drivers
            }
        while sig_to_be_traced:
            next_trace = {}
            for signal_id, signal in sig_to_be_traced.items():

                # Tracing Instances with Output connected
                if signal.type == SignalType.OUTPUT:
                    inst: Optional[Instance] = signal.owned_by
                    if inst is not None:
                        if id(inst) not in traced_inst_id:
                            traced_inst_id.add(id(inst))
                            traced_inst.append(inst)

                            # The Input port of the instance is skipped
                            # We will go directly to the driver as it must be driven by another signal.
                            input_drivers = [i.driver() for i in inst.inputs.values()]
                            next_trace |= {
                                id_sig: sig
                                for sig in input_drivers
                                if (id_sig := id(sig)) not in traced_sig_id
                            }

                elif signal.type != SignalType.INPUT and signal_id not in traced_sig_id:
                    traced_sig_id.add(signal_id)
                    traced_signal.append(signal)
                    next_trace |= {
                        id_sig: sig
                        for sig in signal.drivers
                        if sig.type in (SignalType.WIRE, SignalType.CONSTANT, SignalType.OUTPUT)
                           and (id_sig := id(sig)) not in traced_sig_id
                    }
            sig_to_be_traced = next_trace

        traced_signal.reverse()
        traced_inst.reverse()

        # Check if we have name conflict on the signals and instances
        sig_name_counter = Counter(sig.name for sig in traced_signal)
        inst_name_counter = Counter(inst.name for inst in traced_inst)
        sig_conflicts = [name for name, cnt in sig_name_counter.items() if cnt > 1]
        inst_conflicts = [name for name, cnt in inst_name_counter.items() if cnt > 1]
        if sig_conflicts:
            raise ValueError(f"Signal name conflict: {sig_conflicts}")
        if inst_conflicts:
            raise ValueError(f"Instance name conflict: {inst_conflicts}")

        return traced_signal, traced_inst

    def instance(
            self, name: Optional[str] = None,
            io: Optional[dict[str, Signal]] = None
    ) -> "Instance":
        """
        Create an instance of the module
        :return: The created instance
        """
        inst = Instance(
            module=self,
            name=name,
            io=io,
        )
        ...
        return inst

    @property
    def name(self) -> str:
        return self._config.name

    @classmethod
    def _module_names(cls):
        return [mod.name for mod in cls.module_pool.values()]

    @classmethod
    def elaborate_all(cls) -> dict[str, str]:
        return {
            module.name: module.elaborate()
            for module in cls.module_pool.values()
        }


class Instance(Synthesizable):
    """
    An instance of a module
    """
    INST_TEMPLATE = Template("$module_name $inst_name (\n$io\n);")
    IO_TEMPLATE = Template(".$port_name($signal_name)")

    new_inst_counter = count(0)

    def __init__(self,
                 module: "Module", name: Optional[str] = None,
                 io: Optional[dict[str, Signal]] = None,
                 **kwargs
                 ):
        if name is None:
            name = f"{module.name}_inst_{next(self.new_inst_counter)}"
        super().__init__(**kwargs)
        self._inst_config = ModuleInstanceConfig(
            module=module,
            name=name,
        )
        self._io = IOBundle(owned_by=self)
        self.outputs = SignalDict()
        self.inputs = SignalDict()

        self._io += module.io

        for input_port in module.io.input_names:
            self.inputs[input_port] = self._io[input_port]

        for output_port in module.io.output_names:
            self.outputs[output_port] = Signal(
                width=len(self._io[output_port]),
                signed=self._io[output_port].signed
            )
            self.outputs[output_port] <<= self._io[output_port]

        if io is not None:
            for name, signal in io.items():
                if self._io[name].type == SignalType.INPUT:
                    self.inputs[name] <<= signal
                if self._io[name].type == SignalType.OUTPUT:
                    signal <<= self.outputs[name]

    @property
    def input_names(self) -> list[str]:
        return self._io.input_names

    @property
    def output_names(self) -> list[str]:
        return self._io.output_names

    @property
    def name(self) -> str:
        return self._inst_config.name

    @property
    def module(self) -> Module:
        return self._inst_config.module

    def validate(self) -> list[Exception]:
        errors = []
        for signal in self.inputs.values():
            if signal.driver() is None:
                errors.append(ValueError(f"Input {signal.name} is not connected."))
        return errors

    def build(self):
        for port, signal in self.outputs.items():
            if signal.name is None:
                signal.set_name(f"{self._inst_config.name}_output_{port}")

    def elaborate(self) -> str:
        self.build()
        errors = self.validate()
        if errors:
            raise ValueError(f"Instance {self.name} is not valid.", errors)

        module_name = self.module.name
        inst_name = self.name

        io_list = []
        for port in self._io.inputs():
            io_list.append(self.IO_TEMPLATE.substitute(
                port_name=port.name,
                signal_name=port.driver().name,
            ))
        for port in self._io.outputs():
            io_list.append(self.IO_TEMPLATE.substitute(
                port_name=port.name,
                signal_name=self.outputs[port.name].name,
            ))

        io_list = ",\n".join(io_list)
        return self.INST_TEMPLATE.substitute(
            module_name=module_name,
            inst_name=inst_name,
            io=io_list,
        )


class Blackbox(Module):
    """
    A blackbox module is a module that is provided by the developer.
    Designer has to provide the SystemVerilog code for the module, in the elaborate() method.
    Designer has to ensure the interface provided to the module confine to the SystemVerilog code generated by the
    elaborate() method.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def elaborate(self) -> str:
        ...

    ...
