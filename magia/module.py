import inspect
import logging
from collections import Counter
from dataclasses import dataclass
from itertools import count
from os import PathLike
from pathlib import Path
from string import Template
from typing import Optional, Union

from .bundle import IOBundle, SignalBundleView
from .core import Signal, SignalDict, SignalType, Synthesizable
from .memory import Memory, MemorySignal

logger = logging.getLogger(__name__)


@dataclass
class ModuleConfig:
    module_class: type
    name: Optional[str] = None


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

    Designers shall implement the circuit logic in the `__init__` method.
    However, we highly recommend designers to extract the logic implementation into a seperated method.
    e.g.
    def __init__(self, **kwargs):
        self.io += Input("a", 8)
        self.io += Output("q", 8)
        self.implement()

    def implement(self):
        self.io.q <<= self.io.a + 1
    """
    _MOD_DECL_TEMPLATE = Template("module $name (\n$io\n);")
    _new_module_counter = count(0)
    output_file: Optional[PathLike] = None

    def __init__(self, name: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        if name is None:
            name = f"{self.__class__.__name__}_{next(self._new_module_counter)}"

        self._config = ModuleConfig(
            module_class=type(self),
            name=name,
        )
        self.io = IOBundle()
        self._signals: dict[str, Signal] = {}
        self._instance_counter = count(0)

        self._mod_doc: Optional[str] = None

    def validate(self) -> list[Exception]:
        undriven_outputs = [
            output.net_name
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
        mod_decl = self._MOD_DECL_TEMPLATE.substitute(
            name=self.name,
            io=",\n".join(
                port.elaborate()
                for port in self.io.inputs + self.io.outputs
            ),
        )
        mod_doc = "" if self._mod_doc is None else self._mod_doc
        return "\n".join((mod_decl, mod_doc))

    def elaborate(self) -> tuple[str, set["Module"]]:
        """
        Trace nets and operations from output ports
        This method generates the SystemVerilog code for the module.

        :return: The SystemVerilog code for the module, and the list of submodules of the instance in the module.
        """
        violations = self.validate()
        if violations:
            raise ValueError(f"Module {self.name} is not valid.", violations)

        mod_decl = self.mod_declaration()

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
            Signal._SIGNAL_ASSIGN_TEMPLATE.substitute(
                name=output.net_name,
                driver=output.driver().net_name,
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

        :return: The extra code to be added to the module.
        """
        _ = self  # Stub to avoid IDE/Lint warning
        return ""

    def trace(self) -> tuple[list[Union[Signal, Memory]], list["Instance"]]:
        """
        Trace nets and instances from output ports
        """
        traced_sig_id: set[int] = set()
        traced_inst_id: set[int] = set()
        traced_signal: list[Union[Signal, Memory]] = []
        traced_inst: list[Instance] = []
        sig_to_be_traced: dict[int, Signal] = {}

        for output in self.io.outputs:
            sig_to_be_traced |= {
                id(sig): sig
                for sig in output.drivers
            }
        while sig_to_be_traced:
            next_trace = {}
            for signal_id, signal in sig_to_be_traced.items():

                # Tracing Instances with Output connected
                if signal.type == SignalType.OUTPUT:
                    inst: Optional[Instance] = signal.owner_instance
                    if inst is not None and id(inst) not in traced_inst_id:
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
                        if sig.type not in (SignalType.INPUT,)
                           and (id_sig := id(sig)) not in traced_sig_id
                    }

                    if signal.type == SignalType.MEMORY:
                        signal: MemorySignal
                        if id(signal.memory) not in traced_sig_id:
                            traced_sig_id.add(id(signal.memory))
                            traced_signal.append(signal.memory)

                            next_trace |= {
                                id_sig: sig
                                for sig in signal.memory.drivers
                                if (id_sig := id(sig)) not in traced_sig_id
                            }

            sig_to_be_traced = next_trace

        traced_signal.reverse()
        traced_inst.reverse()

        # Check if we have name conflict on the signals and instances
        sig_name_counter = Counter(sig.net_name for sig in traced_signal)
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
        return Instance(
            module=self,
            name=name,
            io=io,
        )

    @property
    def name(self) -> str:
        return self._config.name

    def register_module_doc(self, locals_param: dict) -> str:
        """
        Generate the summary of a module and register it to the module.
        It will be written into the SystemVerilog code during elaboration.

        Calling this method in the __init__ method with the following:
        self.register_module_doc(locals())
        """
        doc = inspect.getdoc(self)
        if doc is None:
            doc = ""
        else:
            doc += "\n\n"

        signature = inspect.signature(self.__init__)
        args = {k: v for k, v in locals_param.items() if k in signature.parameters}

        doc += "Module Parameters:\n"
        doc += "-----------------\n"
        for k, v in args.items():
            doc += f"{k}: {v}\n"
        doc = f"/*\n{doc}*/\n"

        self._mod_doc = doc
        return doc


class Instance(Synthesizable):
    """
    An instance of a module
    """
    _INST_TEMPLATE = Template("$module_name $inst_name (\n$io\n);")
    _IO_TEMPLATE = Template(".$port_name($signal_name)")

    _new_inst_counter = count(0)

    def __init__(self,
                 module: "Module", name: Optional[str] = None,
                 io: Optional[dict[str, Signal]] = None,
                 **kwargs
                 ):
        if name is None:
            name = f"{module.name}_inst_{next(self._new_inst_counter)}"
        super().__init__(**kwargs)
        self._inst_config = ModuleInstanceConfig(
            module=module,
            name=name,
        )
        self._io = IOBundle(owner_instance=self)
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

    def __ilshift__(self, other: SignalBundleView):
        """
        Connect signals in the bundle to the instance I/O ports.
        """
        if not isinstance(other, SignalBundleView):
            raise TypeError(f"Cannot connect {type(other)} to {type(self)}")
        for port_name, signal in other.items():
            if port_name in self.inputs:
                self.inputs[port_name] <<= signal
            elif port_name in self.outputs:
                signal <<= self.outputs[port_name]
            else:
                logger.warning(f"Port {port_name} is not defined in {self.name}.")

    def validate(self) -> list[Exception]:
        errors = []
        for signal in self.inputs.values():
            if signal.driver() is None:
                errors.append(ValueError(f"Input {signal.name} is not connected."))
        return errors

    def _fix_output_name(self):
        for port, signal in self.outputs.items():
            if signal.name is None:
                signal.set_name(f"{self._inst_config.name}_output_{port}")

    def elaborate(self) -> str:
        self._fix_output_name()
        errors = self.validate()
        if errors:
            raise ValueError(f"Instance {self.name} is not valid.", errors)

        module_name = self.module.name
        inst_name = self.name

        io_list = []
        for port in self._io.inputs:
            io_list.append(self._IO_TEMPLATE.substitute(
                port_name=port.net_name,
                signal_name=port.driver().net_name,
            ))
        for port in self._io.outputs:
            io_list.append(self._IO_TEMPLATE.substitute(
                port_name=port.net_name,
                signal_name=self.outputs[port.net_name].net_name,
            ))

        io_list = ",\n".join(io_list)
        return self._INST_TEMPLATE.substitute(
            module_name=module_name,
            inst_name=inst_name,
            io=io_list,
        )


class Blackbox(Module):
    """
    A blackbox module is a module with elaboration defined by the developer.

    Designer has to provide the SystemVerilog code for the module, in the elaborate() method.
    Designer has to ensure the interface provided to the module confine to the SystemVerilog code generated by the
    elaborate() method.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def elaborate(self) -> tuple[str, set[Module]]:
        raise NotImplementedError("Blackbox module must implement elaborate() method.")


class Elaborator:
    """
    Elaborator is a helper class to elaborate modules.
    """
    name_to_module: dict[str, Module] = {}

    def __init__(self):
        raise NotImplementedError("Elaborator is a helper class and should not be instantiated.")

    @classmethod
    def to_dict(cls, *modules: Module) -> dict[str, str]:
        """
        Elaborate all modules in the list.
        Each module will be elaborated only once and return the SystemVerilog code, plus a list of submodules
        Duplicated submodules will not be elaborated again.
        The elaboration is done recursively, until all submodules are elaborated.

        :param modules: The modules to be elaborated.
        :return: A dictionary of the SystemVerilog code for each module.
        """
        cls.name_to_module = {}
        modules = list(modules)
        elaborated_modules: dict[str, str] = {}
        while modules:
            mod = modules.pop()
            cls.name_to_module[mod.name] = mod
            if mod.name not in elaborated_modules:
                sv_code, submodules = mod.elaborate()
                elaborated_modules[mod.name] = sv_code
                modules += submodules
        return elaborated_modules

    @classmethod
    def to_string(cls, *modules: Module) -> str:
        """
        Elaborate all modules in the list and return the SystemVerilog code as a string.
        """
        return "\n\n".join(cls.to_dict(*modules).values())

    @classmethod
    def to_file(cls, filename: PathLike, *modules: Module):
        """
        Elaborate all modules in the list and write the SystemVerilog code to a file.
        """
        sv_code = cls.to_string(*modules)
        Path(filename).write_text(sv_code)

    @classmethod
    def to_files(cls, output_dir: PathLike, /, *modules: Module, force: bool = False) -> list[Path]:
        """
        Elaborate all modules in the list and write the SystemVerilog code to files.
        The files are written to the output directory.

        :param output_dir: The output directory.
        :param modules: The modules to be elaborated.
        :param force: If True, files in the output directory will be overwritten if it exists.

        :return: A list of Path objects of the files written.
        """
        output_dir = Path(output_dir)
        if not force and output_dir.is_dir() and any(output_dir.iterdir()):
            raise FileExistsError(f"Directory {output_dir} already exists and not empty.")
        output_dir.mkdir(parents=True, exist_ok=True)

        result = cls.to_dict(*modules)
        result_by_file: dict[str, list[str]] = {}

        # Categorize by output file
        for fname, sv_code in result.items():
            module = cls.name_to_module[fname]
            output_file = f"{fname}.sv" if module.output_file is None else module.output_file

            if output_file not in result_by_file:
                result_by_file[output_file] = []
            result_by_file[output_file].append(sv_code)

        # Write to files
        for fname, sv_codes in result_by_file.items():
            sv_code = "\n\n".join(sv_codes)
            Path(output_dir, fname).write_text(sv_code)

        return [Path(output_dir, fname) for fname in result_by_file]

    @staticmethod
    def file(fname: PathLike):
        """
        Return a class decorator to register the filename of generated code to a Module.
        The effect is employed by the `to_files` method only.

        Example:
        @Elaborator.file("adder.sv")
        class Adder(Module):
            ...

        Elaborator.to_files("/tmp/output", Adder(name="adder1"), Adder(name="adder2"))
        # Result in /tmp/output/adder.sv with 2 adders.
        """
        fname = Path(fname)

        def decorator(cls: type[Module]):
            cls.output_file = fname
            return cls

        return decorator
