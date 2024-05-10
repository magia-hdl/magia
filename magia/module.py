from __future__ import annotations

import inspect
import logging
from collections import Counter, OrderedDict
from dataclasses import dataclass
from functools import cached_property, partial
from itertools import count
from os import PathLike
from string import Template
from typing import TYPE_CHECKING

from .data_struct import SignalDict, SignalType
from .io_ports import IOPorts
from .io_signal import Input, Output
from .memory import MemorySignal
from .signals import SIGNAL_ASSIGN_TEMPLATE, CodeSectionType, Signal, Synthesizable
from .sva_manual import SVAManual
from .utils import ModuleContext

if TYPE_CHECKING:
    from .bundle import Bundle

logger = logging.getLogger(__name__)


@dataclass
class ModuleConfig:
    module_class: type
    name: None | str = None


@dataclass
class ModuleInstanceConfig:
    module: Module
    name: None | str = None


MOD_DECL_TEMPLATE = Template("module $name (\n$io\n);")
INST_TEMPLATE = Template("$module_name $inst_name (\n$io\n);")
IO_TEMPLATE = Template(".$port_name($signal_name)")


class _ModuleMetaClass(type):
    def __call__(cls, *args, **kwargs):
        # Reset code section to Logic. Restore after creation.
        with Synthesizable.code_section(CodeSectionType.LOGIC):
            inst = super().__call__(*args, **kwargs)
            # Restore module stack after creation
            ModuleContext().pop()
            return inst


class Module(Synthesizable, metaclass=_ModuleMetaClass):
    """
    A module is a collection of signals and operations. It can also include other modules.

    The module is the base class of specialized modules.
    Developers can define the generic behavior of the module in a dynamic way,
    while each `Module` objects is a specialized module initialized with specific parameters.

    The SystemVerilog Keyword `parameters` is not used here.
    It is because we can generate the code for the specialized module with parametrized values hard-coded.

    The module can be instantiated with the `instance` method.

    Designers must implement the circuit logic in the `__init__` method.
    However, we highly recommend designers to extract the logic implementation into a seperated method.
    e.g.
    def __init__(self, **kwargs):
        self.io += Input("a", 8)
        self.io += Output("q", 8)
        self.implement()

    def implement(self):
        self.io.q <<= self.io.a + 1
    """

    _new_module_counter = count(0)
    output_file: None | PathLike = None

    formal_code = partial(Synthesizable.code_section, CodeSectionType.FORMAL)

    def __init__(self, name: None | str = None, **kwargs):
        super().__init__(**kwargs)
        ModuleContext().push(self)  # Push current module to the context stack

        # Get the arguments passed to the __init__ method of the inherited class
        # === DON'T REFACTOR BELOW. We are inspecting the stack and refactoring will affect the result ===
        children_local = inspect.stack(0)[1].frame.f_locals
        children_class = children_local.get("__class__")
        func_signature = inspect.signature(children_class.__init__) if children_class else {}
        self._mod_params = OrderedDict(**{
            arg: children_local[arg]
            for arg, param in func_signature.parameters.items()
            if param.kind not in (param.VAR_KEYWORD, param.VAR_POSITIONAL) and arg != "self"
        })
        # === DON'T REFACTOR ABOVE ===

        if name is None:
            name = f"{self.__class__.__name__}_{next(self._new_module_counter)}"

        self._config = ModuleConfig(
            module_class=type(self),
            name=name,
        )
        self.io = IOPorts()
        self.manual_sva_collected = []

    def validate(self) -> list[Exception]:
        undriven_outputs = [
            output.name
            for output in self.io.outputs
            if output.driver() is None
        ]
        if undriven_outputs:
            return [
                ValueError("Output not driven", output)
                for output in undriven_outputs
            ]
        return []

    def mod_declaration(self) -> str:
        mod_decl = MOD_DECL_TEMPLATE.substitute(
            name=self.name,
            io=",\n".join(
                port.elaborate()
                for port in self.io.inputs + self.io.outputs
            ),
        )
        return "\n".join((mod_decl, self._module_elab_doc))

    def elaborate(self) -> tuple[str, set[Module]]:
        """
        Trace nets and operations from output ports.

        This method generates the SystemVerilog code for the module.
        :returns: The SystemVerilog code for the module, and the list of submodules of the instance in the module.
        """
        violations = self.validate()
        if violations:
            raise ValueError(f"Module {self.name} is not valid.", violations)

        mod_decl = self.mod_declaration()

        trace_from = self.io.outputs
        trace_from += self.manual_sva_collected
        signals, insts = self.trace(trace_from)

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
            SIGNAL_ASSIGN_TEMPLATE.substitute(
                name=output.name,
                driver=output.driver().name,
            )
            for output in self.io.outputs
        )

        extra_code = self.post_elaborate()

        mod_end = "endmodule"

        sv_code = "\n".join((mod_decl, mod_impl, mod_output_assignment, extra_code, mod_end))
        submodules = {inst.module for inst in insts}

        return sv_code, submodules

    def post_elaborate(self) -> str:
        """
        Override this method to add extra code to the module.

        The code will be added after the elaboration of the module.
        Adding assertions to the module is a typical use case.
        :returns: The extra code to be added to the module.
        """
        _ = self  # Stub to avoid IDE/Lint warning
        return ""

    @staticmethod
    def trace(trace_from: list[Synthesizable]) -> tuple[list[Synthesizable], list[Instance]]:
        """Trace nets and instances from a set of synthesizable objects."""
        traced_obj_id: set[int] = set()
        traced_inst_id: set[int] = set()
        traced_obj: list[Synthesizable] = []
        traced_inst: list[Instance] = []
        obj_to_be_traced: dict[int, Synthesizable] = {
            id(obj): obj
            for obj in trace_from
        }

        while obj_to_be_traced:
            next_trace = {}
            for obj_id, obj in obj_to_be_traced.items():
                if obj_id in traced_obj_id:
                    continue
                if not isinstance(obj, (Input, Output)):
                    traced_obj_id.add(obj_id)
                    traced_obj.append(obj)

                match obj:
                    case Input():
                        continue

                    case Output():
                        owner_inst = obj.owner_instance
                        if owner_inst is None:
                            next_trace |= {
                                id_sig: sig for sig in obj.drivers
                                if (id_sig := id(sig)) not in traced_obj_id
                            }
                        else:
                            if id(owner_inst) in traced_inst_id:
                                continue
                            traced_inst_id.add(id(owner_inst))
                            traced_inst.append(owner_inst)
                            # Trace the IO Ports of an instance.
                            # Input port is driven by external signal, so we go for the driver.
                            # Output port is an extra signal placeholder,
                            # so we add the port itself and ensure the declaration exists.
                            port_drivers = [
                                port.driver() if port.type == SignalType.INPUT else port
                                for port in owner_inst.io.values()
                            ]
                            next_trace |= {
                                id_sig: sig for sig in port_drivers
                                if (id_sig := id(sig)) not in traced_obj_id
                            }

                    case MemorySignal() as obj_mem_sig:
                        next_trace |= {
                            id_sig: sig for sig in obj_mem_sig.drivers
                            if (id_sig := id(sig)) not in traced_obj_id
                        }

                        obj_mem = obj_mem_sig.memory
                        if id(obj_mem) in traced_obj_id:
                            continue

                        traced_obj_id.add(id(obj_mem))
                        traced_obj.append(obj_mem)
                        next_trace |= {
                            id_sig: sig for sig in obj_mem.drivers
                            if (id_sig := id(sig)) not in traced_obj_id
                        }

                    case Signal():
                        next_trace |= {
                            id_sig: sig for sig in obj.drivers
                            if (id_sig := id(sig)) not in traced_obj_id
                        }

                    case SVAManual():
                        next_trace |= {
                            id_sig: sig for sig in obj.drivers
                            if (id_sig := id(sig)) not in traced_obj_id
                        }

                    case _:
                        raise ValueError(f"Unsupported object type: {obj}")

            obj_to_be_traced = next_trace

        traced_obj.reverse()
        traced_inst.reverse()

        # Check if we have name conflict on the signals and instances
        sig_name_counter = Counter(sig.name for sig in traced_obj)
        inst_name_counter = Counter(inst.name for inst in traced_inst)
        sig_conflicts = [name for name, cnt in sig_name_counter.items() if cnt > 1]
        inst_conflicts = [name for name, cnt in inst_name_counter.items() if cnt > 1]
        if sig_conflicts:
            raise ValueError(f"Signal name conflict: {sig_conflicts}")
        if inst_conflicts:
            raise ValueError(f"Instance name conflict: {inst_conflicts}")

        return traced_obj, traced_inst

    def instance(
            self, name: None | str = None,
            io: None | dict[str, Signal] = None
    ) -> Instance:
        """
        Create an instance of the module.

        :returns: The created instance.
        """
        return Instance(
            module=self,
            name=name,
            io=io,
        )

    @property
    def name(self) -> str:
        return self._config.name

    @property
    def params(self) -> dict[str, object]:
        """Return the parameters used to specialize this module."""
        return self._mod_params

    @property
    def _module_elab_doc(self) -> str:
        """
        Generate the summary of a module and register it to the module.

        It will be written into the SystemVerilog code during elaboration.
        """
        doc = self._module_doc_str

        if self.params:
            doc += "\nModule Parameters:\n"
            doc += "-----------------\n"
            doc += "\n".join(
                f"{k}: {v}"
                for k, v in self.params.items()
            ) + "\n"

        if doc:
            doc = f"/*\n{doc}*/\n"
        return doc

    @property
    def _module_doc_str(self) -> str:
        doc = inspect.getdoc(self.__class__)
        if doc is None or doc == inspect.getdoc(Module):
            return ""
        if not doc.endswith("\n"):
            return doc + "\n"
        return doc

    @cached_property
    def _module_init_param_doc(self) -> dict[str, str]:
        params = [(k, f"{k}:") for k in self._mod_params]
        doc = inspect.getdoc(self.__init__)
        if doc is None:
            return {}

        result_doc = {}
        possible_param = [line.strip() for line in doc.split("\n") if ":" in line]
        for line in possible_param:
            for param, sep in params:
                if sep in line:
                    result_doc[param] = line.split(sep, 1)[-1].strip()
        return result_doc

    @property
    def spec(self) -> dict[str, object]:
        """
        Returns the "Specification" of a specialized Module.

        It is a dictionary which can be further processed.
        """
        return {
            "name": self.name,
            "description": self._module_doc_str.strip(),
            "parameters": [
                {
                    "name": k,
                    "value": v,
                    "description": self._module_init_param_doc.get(k, ""),
                }
                for k, v in self.params.items()
            ],
            "ports": [
                {
                    "name": alias,
                    "direction": signal.type.name,
                    "width": signal.width,
                    "signed": signal.signed,
                    "description": signal.description,
                }
                for alias, signal in self.io.signals.items()
            ],
        }


class Instance(Synthesizable):
    """An instance of a module."""

    _new_inst_counter = count(0)

    def __init__(self,
                 module: Module, name: None | str = None,
                 io: None | dict[str, Signal] = None,
                 **kwargs
                 ):
        if name is None:
            name = f"{module.name}_inst_{next(self._new_inst_counter)}"
        super().__init__(**kwargs)
        self._inst_config = ModuleInstanceConfig(
            module=module,
            name=name,
        )
        self._io_ports = IOPorts(owner_instance=self)
        self._io_ports += module.io
        self.io = SignalDict()

        for port_name, port in self._io_ports.signals.items():
            match port.type:
                case SignalType.INPUT:
                    self.io[port_name] = port
                case SignalType.OUTPUT:
                    self.io[port_name] = Signal(
                        width=port.width,
                        signed=port.signed,
                    )
                    self.io[port_name] <<= port

        if io is not None:
            for name, signal in io.items():
                match signal.type:
                    case SignalType.INPUT:
                        self.io[name] <<= signal
                    case SignalType.OUTPUT:
                        signal <<= self.io[name]

    @property
    def input_names(self) -> list[str]:
        return self._io_ports.input_names

    @property
    def output_names(self) -> list[str]:
        return self._io_ports.output_names

    @property
    def name(self) -> str:
        return self._inst_config.name

    @property
    def module(self) -> Module:
        return self._inst_config.module

    def validate(self) -> list[Exception]:
        errors = []
        for signal in self.io.values():
            if signal.type == SignalType.INPUT and signal.driver() is None:
                errors.append(ValueError(f"Input {signal.name} is not connected."))
        return errors

    def _fix_output_name(self):
        for port, signal in self.io.items():
            if signal.type != SignalType.INPUT and signal.name is None:
                signal.set_name(f"{self._inst_config.name}_output_{port}")

    def elaborate(self) -> str:
        self._fix_output_name()
        errors = self.validate()
        if errors:
            raise ValueError(f"Instance {self.name} is not valid.", errors)

        module_name = self.module.name
        inst_name = self.name

        io_list = []
        for port_name, port in self._io_ports.signals.items():
            signal_name = self.io[port_name].name
            if port.type == SignalType.INPUT:
                signal_name = port.driver().name

            io_list.append(IO_TEMPLATE.substitute(port_name=port_name, signal_name=signal_name))

        io_list = ",\n".join(io_list)
        return INST_TEMPLATE.substitute(
            module_name=module_name,
            inst_name=inst_name,
            io=io_list,
        )

    def __ilshift__(self, other: Bundle):
        other.connect_to(self)
        return self


class VerilogWrapper(Module):
    """
    VerilogWrapper creates a module that wraps a module in a Verilog Format.

    Some EDA tools do not support SystemVerilog as the top level or integrable IP.
    Wrapping the SV module in Verilog allows strict integration with those EDA tools.
    """

    def __init__(self, module: Module, **kwargs):
        """
        Create a Verilog Wrapper for a module.

        :param module: The module to be wrapped.
        """
        if kwargs.get("name") is None and module.name is not None:
            kwargs["name"] = f"{module.name}Wrapper"
        super().__init__(**kwargs)
        with self.code_section(CodeSectionType.VERILOG):
            self.module = module
            self.io += module.io
            module.instance(name="inst", io={
                name: self.io[name]
                for name in module.io.signals
            })
