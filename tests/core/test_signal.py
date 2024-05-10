import random

import cocotb
import cocotb.clock
from magia_flow.simulation.general import Simulator

from magia import Elaborator, Input, Module, Output, Signal
from tests import helper


@cocotb.test()
async def adder_test(dut):
    for _ in range(50):
        a = random.randint(0, 0xF)
        b = random.randint(0, 0xF)

        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")

        assert dut.q.value == (a + b)


class TestSignalManipulate:
    TOP = "TopLevel"
    sim_module_and_path = {
        "test_module": [Simulator.current_package()],
        "python_search_path": [Simulator.current_dir()],
    }

    def test_naming(self):
        """Specifying a name for a signal should be reflected in the code generated."""

        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 8)
                self.io += Output("q", 8)

                c = Signal(8, name="intermediate")
                c <<= self.io.a

                d = Signal(8)
                d <<= c

                self.io.q <<= d.set_name("next_one")

        result = Elaborator.to_string(Top(name=self.TOP))
        assert "intermediate = a" in result
        assert "next_one = intermediate" in result

    def test_width(self):
        """Signal width can be changed by `signal.set_width()`."""

        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 5)

                # A + B usually has width of 4, but we can change it to 5
                self.io.q <<= (self.io.a + self.io.b).set_width(5)

        helper.simulate(
            self.TOP, Top(name=self.TOP), testcase="adder_test",
            **self.sim_module_and_path
        )

    def test_signed(self):
        """Signal sign can be changed by `signal.set_signed()`."""

        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 5, signed=True)

                self.io.q <<= (self.io.a + self.io.b).set_width(5).set_signed(True).set_name("next_one")

        result = Elaborator.to_string(Top(name=self.TOP))
        assert "logic signed [4:0] next_one;" in result

    def test_annotate(self):
        """Signal can be annotated by `signal.annotate()` with comment."""
        signal = Signal(8, name="a").annotate("This is a comment")
        signal <<= signal  # Stub just for elaboration
        result = f"{signal.signal_decl()}\n{signal.elaborate()}"
        assert "/*" in result, "There shall be a comment in the elaboration result"
        assert "Net name: a\nThis is a comment\n/" in result, "Net name does not exists in the elaboration result"
        assert __file__ in result, "The file name does not exists in the elaboration result"

    def test_annotate_without_comment(self):
        """Signal can be annotated by `signal.annotate()` without comment."""
        signal = Signal(8, name="a").annotate()
        signal <<= signal  # Stub just for elaboration
        result = f"{signal.signal_decl()}\n{signal.elaborate()}"
        assert "/*" in result, "There shall be a comment in the elaboration result"
        assert "Net name: a\n/" in result, "Net name does not exists in the elaboration result"
        assert __file__ in result, "The file name does not exists in the elaboration result"
