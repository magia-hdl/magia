from pathlib import Path

from magia import Elaborator, ExternalModule, Input, Module, Output


class TestExternalModImport:
    code = """
    module TopModule #(
        parameter WIDTH = 8,
        parameter DEPTH = 8
    ) (
        input clk,
        input wen,
        input [WIDTH-1:0] addr,
        input signed [WIDTH-1:0] din,
        output signed [WIDTH-1:0] dout
    );
    endmodule
    """

    def test_from_file(self, temp_build_dir):
        sv_path = Path(temp_build_dir, "TopModule.sv")
        sv_path.write_text(self.code)
        mod = ExternalModule[sv_path, "TopModule"]()

        input_list = ["clk", "wen", "addr", "din"]
        assert len(mod.io.input_names) == len(mod.io.input_names)
        for name in input_list:
            assert name in mod.io.input_names
        assert mod.io.output_names == ["dout"]

    def test_io_name(self):
        mod = ExternalModule.from_code(self.code, "TopModule")()
        input_list = ["clk", "wen", "addr", "din"]
        assert len(mod.io.input_names) == len(mod.io.input_names)
        for name in input_list:
            assert name in mod.io.input_names
        assert mod.io.output_names == ["dout"]

    def test_io_width(self):
        mod = ExternalModule.from_code(self.code, "TopModule")()
        assert mod.io.clk.width == 1
        assert mod.io.wen.width == 1
        assert mod.io.addr.width == 8
        assert mod.io.din.width == 8
        assert mod.io.dout.width == 8

    def test_io_signed(self):
        mod = ExternalModule.from_code(self.code, "TopModule")()
        assert not mod.io.clk.signed
        assert not mod.io.wen.signed
        assert not mod.io.addr.signed
        assert mod.io.din.signed
        assert mod.io.dout.signed

    def test_default_params(self):
        mod_class = ExternalModule.from_code(self.code, "TopModule")
        assert mod_class.default_params() == {"WIDTH": 8, "DEPTH": 8}

    def test_params(self):
        mod_class = ExternalModule.from_code(self.code, "TopModule")
        mod = mod_class(WIDTH=16, DEPTH=32)
        assert mod.params == {"WIDTH": 16, "DEPTH": 32}

    def test_params_override(self):
        mod_class = ExternalModule.from_code(self.code, "TopModule")
        mod = mod_class(WIDTH=16)
        assert mod.io.clk.width == 1
        assert mod.io.wen.width == 1
        assert mod.io.addr.width == 16
        assert mod.io.din.width == 16
        assert mod.io.dout.width == 16


class TestExternalModElaborate:
    top_name = "top"
    code = f"""
            module {top_name} #(
                parameter width = 10,
                parameter height = 20
            )(
              input  logic [width-1:0] a,
              input  logic [width-1:0] b,
              output logic [width-1:0] c
            );
              assign c = a & b;
            endmodule
            """

    def test_elaborate(self):
        ext_module_class = ExternalModule.from_code(self.code, self.top_name)

        class TopLevel(Module):
            def __init__(self, width, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", width)
                self.io += Input("b", width)
                self.io += Output("c", width)
                self.io += Output("d", width)
                ext_module = ext_module_class(width=width)

                inputs = {"a": self.io.a, "b": self.io.b, }
                ext_module.instance(io={**inputs, "c": self.io.c, })
                ext_module.instance(io={**inputs, "c": self.io.d, })

        width = 17
        result = (Elaborator.to_string(TopLevel(width)))
        assert f"{self.top_name} #(" in result  # Check if the original module is being wrapped
        assert f".width({width})" in result  # Check if parameters are being passed

    def test_overriden_params_only(self):
        ext_module_class = ExternalModule.from_code(self.code, self.top_name)

        class TopLevel(Module):
            def __init__(self, height, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 10)
                self.io += Input("b", 10)
                self.io += Output("c", 10)
                self.io += Output("d", 10)
                ext_module = ext_module_class(height=height)

                inputs = {"a": self.io.a, "b": self.io.b, }
                ext_module.instance(io={**inputs, "c": self.io.c, })
                ext_module.instance(io={**inputs, "c": self.io.d, })

        height = 17
        result = Elaborator.to_string(TopLevel(height))
        assert f"{self.top_name} #(" in result  # Check if the original module is being wrapped
        assert f".height({height})" in result  # Check if parameters are being elaborated
        assert ".width" not in result  # Check if unused parameters are not being elaborated


def test_import_specific_mod():
    code = """
        module Mod1 (
            input clk,
            input wen,
            output signed [7:0] dout
        );
        endmodule
        module Mod2 (
            input clk,
            input wen,
            output signed [7:0] dout1,
            output signed [7:0] dout2
        );
        endmodule
        """
    mod = ExternalModule.from_code(code, "Mod1")()
    assert len(mod.io.input_names) == 2
    assert len(mod.io.output_names) == 1
    mod = ExternalModule.from_code(code, "Mod2")()
    assert len(mod.io.input_names) == 2
    assert len(mod.io.output_names) == 2


class TestExternalModSyntax:
    def test_empty_params(self):
        code = """
        module Mod1 (
            input clk,
            input wen,
            output signed [7:0] dout
        );
        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")()
        assert mod.params == {}

    def test_no_local_params(self):
        code = """
        module Mod1 (
            input clk,
            input wen,
            output signed [7:0] dout
        );
        localparam SHALL_NOT_IMPORT = 1;
        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")()
        assert mod.params == {}

    def test_port_def_in_body(self):
        code = """
        module Mod1 (
            clk, wen, dout
        );
        input clk;
        input wen;
        output signed [7:0] dout;

        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")()
        input_list = ["clk", "wen"]
        assert len(mod.io.input_names) == len(mod.io.input_names)
        for name in input_list:
            assert name in mod.io.input_names
        assert mod.io.output_names == ["dout"]
        assert mod.io.dout.width == 8
        assert mod.io.dout.signed

    def test_param_def_in_body(self):
        code = """
        module Mod1 (
            input clk,
            input wen,
            output signed [7:0] dout
        );
        parameter WIDTH = 8;
        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")()
        assert mod.params == {"WIDTH": 8}

    def test_param_propagation(self):
        code = """
        module Mod1 #(
            parameter BASE = 8,
            parameter WIDTH = 2 * BASE
        ) (
            input clk,
            input wen,
            output signed [WIDTH-1:0] dout
        );
        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")(BASE=16)
        assert mod.params == {"WIDTH": 32, "BASE": 16}
        assert mod.io.dout.width == 32

    def test_directive_propagation(self):
        code = """
        `define ABC 12+3
        module Mod1 #(
            parameter WIDTH = `ABC
        ) (
            input clk,
            input logic [WIDTH-1:0] addr,
            output logic [WIDTH-1:0] dout
        );
        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")()
        assert mod.io.addr.width == 15
        assert mod.io.dout.width == 15

    def test_clog2(self):
        code = """
        module Mod1 #(
            parameter MEM_SIZE = 1024
        ) (
            input clk,
            input logic [$clog2(MEM_SIZE)-1:0] addr,
            output logic [15:0] dout
        );
        endmodule
        """
        mod = ExternalModule.from_code(code, "Mod1")()
        assert mod.io.addr.width == 10
