import random
from pathlib import Path

import cocotb
import pytest
from cocotb_test.simulator import run as sim_run

from magia import Elaborator, Input, Module, Output, Signal

cocotb_test_prefix = "coco_"


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

    def test_naming(self):
        """
        Specifying a name for a signal should be reflected in the code generated
        """

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

    def test_width(self, temp_build_dir):
        """
        Signal width can be changed by `signal.set_width()`
        """

        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 5)

                # A + B usually has width of 4, but we can change it to 5
                self.io.q <<= (self.io.a + self.io.b).set_width(5)

        with pytest.elaborate_to_file(Top(name=self.TOP)) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="adder_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )

    def test_signed(self):
        """
        Signal sign can be changed by `signal.set_signed()`
        """

        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 5, signed=True)

                self.io.q <<= (self.io.a + self.io.b).set_width(5).set_signed(True).set_name("next_one")

        result = Elaborator.to_string(Top(name=self.TOP))
        assert "logic signed [4:0] next_one;" in result
