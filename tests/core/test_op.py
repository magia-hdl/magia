import random
from pathlib import Path

import cocotb
import cocotb.clock
import pytest
from cocotb_test.simulator import run as sim_run

from magia import Input, Module, Output


@cocotb.test()
async def when_as_mux_test(dut):
    """ Test if the `when` operator works as a mux """
    for _ in range(50):
        a = random.randint(0, 0xFF)
        b = random.randint(0, 0xFF)
        sel = random.randint(0, 1)

        dut.a.value = a
        dut.b.value = b
        dut.sel.value = sel

        await cocotb.clock.Timer(1, units="ns")

        if sel == 1:
            assert dut.q.value == a
        else:
            assert dut.q.value == b


@cocotb.test()
async def when_as_mux_comp(dut):
    """ Test if the `when` operator works as a Comparator """
    for _ in range(16 * 16):
        a = random.randint(0, 0xF)
        b = random.randint(0, 0xF)

        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")

        if a != b:
            assert dut.q.value == a
        else:
            assert dut.q.value == 0xF


class TestOperations:
    TOP = "TopModule"

    def test_when_mux(self, temp_build_dir):
        class SimpleMux(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8)
                self.io += Input("b", 8)
                self.io += Input("sel", 1)
                self.io += Output("q", 8)

                self.io.q <<= self.io.a.when(self.io.sel, else_=self.io.b)

        with pytest.elaborate_to_file(
                SimpleMux(name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="when_as_mux_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )

    def test_when_cond(self, temp_build_dir):
        class Comparator(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 4)

                self.io.q <<= self.io.a.when(self.io.a != self.io.b, else_=0xF)

        with pytest.elaborate_to_file(
                Comparator(name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="when_as_mux_comp",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )
