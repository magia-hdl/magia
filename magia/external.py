from os import PathLike
from pathlib import Path
from string import Template

import hdlConvertorAst.hdlAst as Ast
from hdlConvertor import HdlConvertor
from hdlConvertorAst.language import Language

from .core import Input, Output
from .module import Module

_ACCEPTABLE_BINARY_OPS = {
    Ast.HdlOpType.SUB,
    Ast.HdlOpType.ADD,
    Ast.HdlOpType.DIV,
    Ast.HdlOpType.MUL,
    Ast.HdlOpType.MOD,
    Ast.HdlOpType.REM,
    Ast.HdlOpType.POW,
    Ast.HdlOpType.SLL,
    Ast.HdlOpType.SRL,
    Ast.HdlOpType.SLA,
    Ast.HdlOpType.SRA,
    Ast.HdlOpType.EQ,
    Ast.HdlOpType.NE,
    Ast.HdlOpType.GT,
    Ast.HdlOpType.GE,
    Ast.HdlOpType.LT,
    Ast.HdlOpType.LE,
    Ast.HdlOpType.DOWNTO,
}


class ExternalModule(Module):
    """
    Imported SystemVerilog Module
    """
    _INST_TEMPLATE = Template("$module_name #(\n$params\n) inst (\n$io\n);")
    _IO_TEMPLATE = Template(".$port_name($port_name)")
    _PARAM_TEMPLATE = Template(".$param_name($param_value)")

    ports_from_code: dict[str, Ast.iHdlObj] = {}
    params_from_code: dict[str, Ast.iHdlObj] = {}
    ext_module_name: str = ""

    def __init__(self, **kwargs):
        if not self.ports_from_code:
            raise ValueError(
                "No ports found from the module. "
                "Did you forget to call ExternalModule[file,top] or from_code?"
            )
        sub_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key not in self.params_from_code
        }
        super().__init__(**sub_kwargs)
        self._params_override = {
            key: Ast.HdlIdDef()
            for key in kwargs
            if key in self.params_from_code
        }

        for key, value in self._params_override.items():
            value.name = key
            if isinstance(kwargs[key], (str, float)):
                value.value = kwargs[key]
            if isinstance(kwargs[key], (str, int)):
                value.value = Ast.HdlValueInt(str(kwargs[key]), None, 10)

        self._params = {
            **self.params_from_code,
            **self._params_override,
        }
        for port in self.ports_from_code:
            self.io += self._create_port(port)

        self.register_module_doc(locals())

    def elaborate(self) -> tuple[str, set[Module]]:
        mod_decl = self.mod_declaration()
        mod_end = "endmodule"

        io_list = []
        for port in self.io.input_names:
            io_list.append(self._IO_TEMPLATE.substitute(port_name=port))
        for port in self.io.output_names:
            io_list.append(self._IO_TEMPLATE.substitute(port_name=port))
        io_list = ",\n".join(io_list)

        param_list = []
        for param in self._params_override:
            value = self._resolve_param(param)
            if isinstance(value, str):
                value = f'"{value}"'
            param_list.append(self._PARAM_TEMPLATE.substitute(
                param_name=param,
                param_value=value,
            ))
        param_list = ",\n".join(param_list)

        inst_impl = self._INST_TEMPLATE.substitute(
            module_name=self.ext_module_name,
            params=param_list,
            io=io_list,
        )

        sv_code = "\n".join((mod_decl, inst_impl, mod_end))
        return sv_code, set()

    @property
    def params(self):
        return {
            key: self._resolve_param(key)
            for key in self._params
        }

    @classmethod
    def default_params(cls):
        return cls().params

    def _create_port(self, port_name: str):
        port = self.ports_from_code[port_name]
        port_class = {
            Ast.HdlDirection.IN: Input,
            Ast.HdlDirection.OUT: Output,
            Ast.HdlDirection.INOUT: Input,  # Fix this one when we implement inout port support
        }[port.direction]

        name = port.name
        signed = False
        width = 1

        # More details from the port declaration
        if isinstance(port.type, Ast.HdlOp) and port.type.fn == Ast.HdlOpType.PARAMETRIZATION:
            # Determine if port is signed
            _, port_width, port_signed = port.type.ops
            signed = bool(self._resolve_node(port_signed))
            width = self._resolve_node(port_width) + 1

        return port_class(name=name, width=width, signed=signed)

    def _resolve_node(self, node: Ast.iHdlObj):
        # Resolve Constants
        if node is None:
            return 0
        if isinstance(node, (float, str)):
            return node
        if isinstance(node, Ast.HdlValueInt):
            return int(node.val, node.base) if isinstance(node.val, str) else node.val

        # Resolve Parameter Identifier
        if isinstance(node, Ast.HdlValueId):
            return self._resolve_param(node.val)

        # Resolve Operators
        if isinstance(node, Ast.HdlOp):
            if node.fn == Ast.HdlOpType.INDEX:
                raise NotImplementedError("Unpacked Port is not supported")
            if node.fn == Ast.HdlOpType.PARAMETRIZATION:
                _, width, _ = node.ops
                return self._resolve_node(width)
            if node.fn == Ast.HdlOpType.CALL:
                # Only support $clog2
                if node.ops[0].val == "$clog2":
                    op = self._resolve_node(node.ops[1])
                    return max((op - 1).bit_length(), 0)
                raise NotImplementedError(f"Function {node.ops[0].val} not supported")
            if node.fn == Ast.HdlOpType.MINUS_UNARY:
                return -self._resolve_node(node.ops[0])
            if node.fn in _ACCEPTABLE_BINARY_OPS:
                op1, op2 = node.ops
                op1 = self._resolve_node(op1)
                op2 = self._resolve_node(op2)
                return {
                    Ast.HdlOpType.SUB: lambda x, y: x - y,
                    Ast.HdlOpType.ADD: lambda x, y: x + y,
                    Ast.HdlOpType.DIV: lambda x, y: x // y,
                    Ast.HdlOpType.MUL: lambda x, y: x * y,
                    Ast.HdlOpType.MOD: lambda x, y: x % y,
                    Ast.HdlOpType.REM: lambda x, y: x % y,
                    Ast.HdlOpType.POW: lambda x, y: x ** y,
                    Ast.HdlOpType.SLL: lambda x, y: x << y,
                    Ast.HdlOpType.SRL: lambda x, y: x >> y,
                    Ast.HdlOpType.SLA: lambda x, y: x << y,
                    Ast.HdlOpType.SRA: lambda x, y: x >> y,
                    Ast.HdlOpType.EQ: lambda x, y: 1 if x == y else 0,
                    Ast.HdlOpType.NE: lambda x, y: 1 if x != y else 0,
                    Ast.HdlOpType.GT: lambda x, y: 1 if x > y else 0,
                    Ast.HdlOpType.GE: lambda x, y: 1 if x >= y else 0,
                    Ast.HdlOpType.LT: lambda x, y: 1 if x < y else 0,
                    Ast.HdlOpType.LE: lambda x, y: 1 if x <= y else 0,
                    Ast.HdlOpType.DOWNTO: lambda x, y: abs(x - y),
                }[node.fn](op1, op2)

            raise NotImplementedError(f"Operator {node.fn.name} not supported")

        raise NotImplementedError(f"Node {node.__class__.__name__} not supported")

    def _resolve_param(self, param_name: str):
        # We need to resolve parameters and operators here
        return self._resolve_node(self._params[param_name].value)

    def __class_getitem__(cls, item):
        """
        Return a new ExternalModule with the given file and Top Level Name

        Syntax:
            NewExternalModule = ExternalModule[PathLike, str]
            new_module = NewExternalModule(param1=value1, param2=value2, ...)
        """
        sv_file, top_name = item
        return cls.from_file(sv_file, top_name)

    @classmethod
    def from_file(cls, sv_file: PathLike, top_name: str):
        """
        Create a new ExternalModule from a SystemVerilog file and given Top Level
        """
        return cls.from_code(Path(sv_file).read_text(), top_name)

    @classmethod
    def from_code(cls, sv_code: str, top_name: str):
        """
        Create a new ExternalModule from SystemVerilog code and given Top Level
        """
        ports, params = cls.parse_sv(sv_code, top_name)
        return type(f"ExternalModule_{top_name}", (cls,), {
            "ports_from_code": ports,
            "params_from_code": params,
            "ext_module_name": top_name,
            "__doc__": cls.__doc__,
        })

    @staticmethod
    def parse_sv(sv_code: str, top_name: str) -> tuple[dict[str, Ast.iHdlObj], dict[str, Ast.iHdlObj]]:
        """
        Parse SV Code and return a dictionary of ports and parameters
        """
        parser = HdlConvertor()
        source = parser.parse_str(sv_code, Language.SYSTEM_VERILOG_2017, [], hierarchyOnly=False, debug=True)
        modules = [
            m.dec for m in source.objs
            if isinstance(m, Ast.HdlModuleDef) and m.dec.name == top_name
        ]
        if not modules:
            raise ValueError(f"Could not find module {top_name} in {sv_code}")

        port_dict = {
            port.name: port
            for port in modules[0].ports
        }
        params_dict = {
            p.name: p
            for p in modules[0].params
            if not (hasattr(p.type, "val") and p.type.val == "time")
        }

        return port_dict, params_dict
