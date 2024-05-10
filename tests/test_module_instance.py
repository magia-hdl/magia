from pathlib import Path

from magia import CodeSectionType, Elaborator, Input, IOPorts, Module, Output, VerilogWrapper
from magia.signals import Synthesizable
from magia.utils import ModuleContext


class TestModSpecialize:
    def test_module_anonymous_init(self):
        class SubModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q", 8)

                self.io.q <<= self.io.d

        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q1", 8)
                self.io += Output("q2", 8)
                self.io += Output("q3", 8)

                SubModule().instance(io={
                    "d": self.io.d,
                    "q": self.io.q1,
                })
                SubModule().instance(io={
                    "d": self.io.d,
                    "q": self.io.q2,
                })
                SubModule().instance(io={
                    "d": self.io.d,
                    "q": self.io.q3,
                })

        result = Elaborator.to_dict(TopModule(name="top_module"))
        assert len(result) == 4, f"Expected 4 modules: Top + 3 SubModules, got {len(result)} modules."

    def test_reuse_specialized_module(self):
        class SubModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q", 8)

                self.io.q <<= self.io.d

        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("d", 8)
                self.io += Output("q1", 8)
                self.io += Output("q2", 8)
                self.io += Output("q3", 8)

                specialized = SubModule()
                specialized.instance(io={
                    "d": self.io.d,
                    "q": self.io.q1,
                })
                specialized.instance(io={
                    "d": self.io.d,
                    "q": self.io.q2,
                })
                specialized.instance(io={
                    "d": self.io.d,
                    "q": self.io.q3,
                })

        result = Elaborator.to_dict(TopModule(name="top_module"))
        assert len(result) == 2, f"Expected 2 modules: Top + 1 SubModules, got {len(result)} modules."


class TestElaboration:
    def test_elaborate_to_files(self, temp_build_dir):
        adder_file = "adder.sv"

        @Elaborator.file(adder_file)
        class Adder(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 5, signed=True)

                self.io.q <<= (self.io.a + self.io.b).set_width(5)

        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q0", 5, signed=True)
                self.io += Output("q1", 5, signed=True)
                self.io += Output("q2", 5, signed=True)

                Adder().instance("adder1", io={"a": self.io.a, "b": self.io.b, "q": self.io.q0})
                Adder().instance("adder2", io={"a": self.io.a, "b": self.io.b, "q": self.io.q1})
                Adder().instance("adder3", io={"a": self.io.a, "b": self.io.b, "q": self.io.q2})

        elaborated = Elaborator.to_files(temp_build_dir, Top(name="Top"), Top(name="Top2"), force=True)
        elaborated = [file.name for file in elaborated]
        assert len(elaborated) == 3, f"Expected 3 files, got {len(elaborated)} files."
        assert "Top.sv" in elaborated, "Top.sv is missing."
        assert "Top2.sv" in elaborated, "Top2.sv is missing."
        assert adder_file in elaborated, f"{adder_file} is missing."

        adder_conetxt = Path(temp_build_dir, adder_file).read_text()
        end_modules = [
            line for line in adder_conetxt.splitlines()
            if line.strip() == "endmodule"
        ]
        assert len(end_modules) == 6, f"Expected 6 modules in {adder_file}, got {len(end_modules)}."

    def test_elaborate_doc(self):
        class Top(Module):
            """This is a top module."""

            def __init__(self, width, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", width)
                self.io += Output("b", width)
                self.io.b <<= self.io.a

        doc = Elaborator.to_string(Top(width=7086))
        assert "This is a top module." in doc, "Module doc is missing."
        assert "width: 7086" in doc, "Module parameter is missing."

    def test_module_spec(self):
        class Top(Module):
            """This is a top module."""

            def __init__(self, width, **kwargs):
                """:param width: The width of the module."""
                super().__init__(**kwargs)
                self.io += Input("a", width, description="Input A")
                self.io += Output("b", width)
                self.io.b <<= self.io.a

        spec = Top(width=7086, name="TopLevel").spec
        assert spec["name"] == "TopLevel"
        assert spec["description"] == "This is a top module."
        assert spec["parameters"][0]["name"] == "width"
        assert spec["parameters"][0]["value"] == 7086
        assert spec["parameters"][0]["description"] == "The width of the module."
        for port in spec["ports"]:
            assert port["name"] in ["a", "b"]
            assert port["width"] == 7086
            if port["name"] == "a":
                assert port["direction"] == "Input"
                assert port["description"] == "Input A"
            else:
                assert port["direction"] == "Output"
                assert port["description"] == ""


def test_module_io_definition():
    io_set_1 = IOPorts()
    io_set_1 += Input("set1_a", 8)
    io_set_1 += Input("set1_b", 8)

    io_set_2 = IOPorts()
    io_set_2 += Input("set2_a", 8)
    io_set_2 += Input("set2_b", 8)

    io_set_3 = IOPorts()
    io_set_3 += Input("set3_a", 8)
    io_set_3 += Input("set3_b", 8)

    class Top(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # Adding IO one by one
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)
            # Adding list of IO
            self.io += [Input("in_b", 8), Output("out_b", 8)]
            # Adding Single IOPorts
            self.io += io_set_1
            # Adding a list of IOPorts
            self.io += [io_set_2, io_set_3]

    top = Top()

    assert len(top.io.signals) == 10
    # Assert all inputs in io
    for input_name in ["in_a", "in_b", "set1_a", "set1_b", "set2_a", "set2_b", "set3_a", "set3_b"]:
        assert input_name in top.io.input_names
    for output_name in ["out_a", "out_b"]:
        assert output_name in top.io.output_names


def test_logic_decl_with_unused_output():
    class Sub(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)
            self.io += Output("out_b", 8)

            self.io.out_a <<= self.io.in_a
            self.io.out_b <<= self.io.in_a

    class Top(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)

            sub_module = Sub(name="sub")
            sub_module.instance(io={"in_a": self.io.in_a, "out_a": self.io.out_a})

    top = Top(name="Top")
    code = Elaborator.to_dict(top)
    code_lines = code["Top"].splitlines()
    assignment = [line for line in code_lines if line.strip().startswith("assign ")]
    signal_decl = [line for line in code_lines if line.strip().startswith("logic ")]
    assert len(assignment) == 1, f"Expected 1 assignment, got {len(assignment)}."
    assert len(signal_decl) == 2, f"Expected 2 signal declarations, got {len(signal_decl)}."


def test_verilog_wrapper():
    class Top(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)

            self.io.out_a <<= self.io.in_a

    wrapper = VerilogWrapper(Top(name="Top"), name="TopWrapper")
    elaborated_lines = {
        name: [line.strip() for line in code.splitlines()]
        for name, code in Elaborator.to_dict(wrapper).items()
    }
    elaborated_io = {
        name: [
            line.replace("input", "").replace("output", "").strip()
            for line in lines
            if line.startswith("input") or line.startswith("output")
        ] for name, lines in elaborated_lines.items()
    }

    # SV Output: Only "logic" is valid in signal declarations.
    assert any(
        line.startswith("logic") for line in
        elaborated_lines["Top"] + elaborated_io["Top"]
    ), "No Signal declaration found in Elaborated SystemVerilog Code."
    assert not any(
        line.startswith("wire")
        for line in elaborated_lines["Top"]
    ), "Wire declaration found in Elaborated SystemVerilog Code."
    assert not all(
        "wire" in line for line in elaborated_io["Top"]
    ), "Wire declaration found in IO of Elaborated SystemVerilog Code."

    # Verilog Output: Only "wire" is valid in signal declarations.
    assert any(
        line.startswith("wire") for line in
        elaborated_lines["TopWrapper"] + elaborated_io["TopWrapper"]
    ), "No Signal declaration found in Elaborated Verilog Code."
    assert not any(
        line.startswith("logic")
        for line in elaborated_lines["TopWrapper"]
    ), "Logic declaration found in Elaborated Verilog Code."
    assert not all(
        "logic" in line for line in elaborated_io["TopWrapper"]
    ), "Logic declaration found in IO of Elaborated Verilog Code."


def test_code_section():
    class Sub(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)

            assert self.current_code_section == CodeSectionType.LOGIC
            with self.formal_code():
                assert self.current_code_section == CodeSectionType.FORMAL
            with self.code_section(CodeSectionType.VERILOG):
                assert self.current_code_section == CodeSectionType.VERILOG
                self.io.out_a <<= self.io.in_a

    class Top(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)

            assert self.current_code_section == CodeSectionType.LOGIC
            with self.formal_code():
                assert self.current_code_section == CodeSectionType.FORMAL
                _ = Sub()
            with self.code_section(CodeSectionType.VERILOG):
                assert self.current_code_section == CodeSectionType.VERILOG
                self.io.out_a <<= self.io.in_a
                _ = Sub()

    Top()
    Sub()


def test_auto_object_collection():
    class SpecialCode(Synthesizable):
        def __init__(self, code: str, **kwargs):
            super().__init__(**kwargs)
            if (module := ModuleContext().current) is not None:
                module.special_code.append(self)
            self.code = code

        def __str__(self):
            return f"SpecialCode: {self.code}"

    class Top(Module):
        def __init__(self, code_count: int, **kwargs):
            self.special_code = []
            super().__init__(**kwargs)
            self.io += Input("in_a", 8)
            self.io += Output("out_a", 8)

            for i in range(code_count):
                SpecialCode(f"code {i}")
            self.io.out_a <<= self.io.in_a

    top_5, top_10 = Top(5), Top(10)
    assert len(top_5.special_code) == 5, f"Expected 5 SpecialCode objects, got {len(top_5.special_code)}."
    assert len(top_10.special_code) == 10, f"Expected 10 SpecialCode objects, got {len(top_10.special_code)}."

    top_5_code = {str(code) for code in top_5.special_code}
    top_10_code = {str(code) for code in top_10.special_code}

    for i in range(5):
        assert f"SpecialCode: code {i}" in top_5_code, f"SpecialCode code {i} is missing in top_5."
    for i in range(10):
        assert f"SpecialCode: code {i}" in top_10_code, f"SpecialCode code {i} is missing in top_10."
