from os import PathLike
from pathlib import Path
from string import Template

import pyverilog.vparser.ast as ast
from pyverilog.vparser.parser import VerilogCodeParser

from .core import Input, Output
from .module import Blackbox, Module


class ExternalModule(Blackbox):
    """
    Imported SystemVerilog Module
    """
    _INST_TEMPLATE = Template("$module_name #(\n$params\n) inst (\n$io\n);")
    _IO_TEMPLATE = Template(".$port_name($port_name)")
    _PARAM_TEMPLATE = Template(".$param_name($param_value)")

    ports_from_code: dict[str, ast.Node] = {}
    params_from_code: dict[str, ast.Node] = {}
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
            key: ast.Parameter(name=key, value={
                int: ast.IntConst,
                float: ast.FloatConst,
                str: ast.StringConst,
            }[type(value)](value))
            for key, value in kwargs.items()
            if key in self.params_from_code
        }
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

        port_class = Input
        if isinstance(port, ast.Output):
            port_class = Output

        name = port.name
        signed = port.signed

        # Assume LSB == 0
        if not port.width:
            width = 1
        else:
            width = self._resolve_node(self.ports_from_code[port_name].width.msb) + 1
        return port_class(name=name, width=width, signed=signed)

    def _resolve_node(self, node: ast.Node):
        # Resolve Constants
        if isinstance(node, ast.IntConst):
            return int(node.value)
        if isinstance(node, ast.FloatConst):
            return float(node.value)
        if isinstance(node, ast.StringConst):
            return node.value

        # Resolve Parameter Identifier
        if isinstance(node, ast.Identifier):
            return self._resolve_param(node.name)
        # Resolve Variables
        if isinstance(node, ast.Rvalue):
            return self._resolve_node(node.var)

        # Resolve Operators
        if isinstance(node, ast.Operator):
            # Handle Conditional Operator
            if isinstance(node, ast.Cond):
                cond = self._resolve_node(node.cond)
                true_value = self._resolve_node(node.true_value)
                false_value = self._resolve_node(node.false_value)
                return true_value if cond else false_value
            # Unary Operators
            if isinstance(node, ast.UnaryOperator):
                rvalue = self._resolve_node(node.right)
                node_class = type(node)
                return {
                    ast.Uplus: lambda x: x,
                    ast.Uminus: lambda x: -x,
                    ast.Unot: lambda x: 0 if x else 1,
                }[node_class](rvalue)
            # Other Operators
            lvalue = self._resolve_node(node.left)
            rvalue = self._resolve_node(node.right)
            node_class = type(node)
            return {
                ast.Plus: lambda x, y: x + y,
                ast.Minus: lambda x, y: x - y,
                ast.Times: lambda x, y: x * y,
                ast.Divide: lambda x, y: x // y,
                ast.Mod: lambda x, y: x % y,
                ast.Power: lambda x, y: x ** y,
                ast.Sll: lambda x, y: x << y,
                ast.Srl: lambda x, y: x >> y,
                ast.Sla: lambda x, y: x << y,
                ast.Sra: lambda x, y: x >> y,
                ast.LessThan: lambda x, y: 1 if x < y else 0,
                ast.LessEq: lambda x, y: 1 if x <= y else 0,
                ast.GreaterThan: lambda x, y: 1 if x > y else 0,
                ast.GreaterEq: lambda x, y: 1 if x >= y else 0,
                ast.Eq: lambda x, y: 1 if x == y else 0,
                ast.NotEq: lambda x, y: 1 if x != y else 0,
                ast.Eql: lambda x, y: 1 if x == y else 0,
                ast.NotEql: lambda x, y: 1 if x != y else 0,
            }[node_class](lvalue, rvalue)

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
    def parse_sv(sv_code: str, top_name: str) -> tuple[dict[str, ast.Node], dict[str, ast.Node]]:
        """
        Parse SV Code and return a dictionary of ports and parameters
        """

        def bfs_over_ast(ast_root, node_type):
            search_list = [ast_root]
            result = []
            while search_list:
                node = search_list.pop()
                if isinstance(node, node_type):
                    result.append(node)
                else:
                    search_list += node.children()
            return result

        parser = VerilogCodeParser([], debug=False)

        # Hack: Get rid of the icarus verilog dependency
        # We ignore the preprocessor directives and go straight to the parser
        parser.preprocess = lambda: sv_code
        source = parser.parse()
        modules = [m for m in source.description.definitions if m.name == top_name]
        if not modules:
            raise ValueError(f"Could not find module {top_name} in {sv_code}")

        io_param_result = [
            node
            for node in bfs_over_ast(modules[0], (ast.Input, ast.Output, ast.Parameter))
            if not isinstance(node, (ast.Localparam, ast.Supply))
        ]
        params = [node for node in io_param_result if isinstance(node, ast.Parameter)]
        ports = [node for node in io_param_result if not isinstance(node, ast.Parameter)]

        if any(port.dimensions for port in ports):
            raise NotImplementedError("Array ports not supported")
        if any(
                port.width and (
                        not isinstance(port.width.lsb, ast.IntConst) or
                        int(port.width.lsb.value) != 0
                )
                for port in ports
        ):
            raise NotImplementedError("Ports with non-zero LSB not supported")

        port_dict = {
            port.name: port
            for port in ports
        }
        params_dict = {
            param.name: param
            for param in params
        }

        return port_dict, params_dict
