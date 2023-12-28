from pathlib import Path

from magia import Elaborator, Input, Module, Output


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
