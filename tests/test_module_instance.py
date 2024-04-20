from pathlib import Path

from magia import Elaborator, Input, IOPorts, Module, Output


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


def test_elaborate_to_files(temp_build_dir):
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


def test_elaborate_doc():
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


def test_module_spec():
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
            assert port["direction"] == "INPUT"
            assert port["description"] == "Input A"
        else:
            assert port["direction"] == "OUTPUT"
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
