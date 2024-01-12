import random
from pathlib import Path

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from cocotb_test.simulator import run as sim_run

import tests.helper as helper
from magia import Input, Module
from magia.std.bundles import StdIO


@cocotb.test()
async def stdio_valid_bundle_on_register_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())  # Start the clock

    last_valid_out = None

    for i in range(128):
        dut.din.value = random.randint(0, 0xFFFF)
        if last_valid_out is not None:
            dut.din_valid.value = random.randint(0, 1)
        else:
            dut.din_valid.value = 1
            last_valid_out = dut.din.value

        await FallingEdge(dut.clk)

        assert dut.dout_valid.value == dut.din_valid.value, \
            f"Expected {dut.din_valid.value}, got {dut.dout_valid.value} on Entry {i}."

        if dut.din_valid.value == 1:
            assert dut.dout.value == dut.din.value, f"Expected {dut.din.value}, got {dut.dout.value} on Entry {i}."
            last_valid_out = dut.dout.value
        else:
            assert dut.dout.value == last_valid_out, \
                f"Expected {last_valid_out}, got {dut.dout.value} on Entry {i}."


class TestStdIOBundle:
    TOP = "TopModule"

    def test_stdio_valid_bundle_on_register(self, temp_build_dir):
        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("clk", 1)
                self.io += StdIO().valid("din", 16).flip()
                self.io += StdIO().valid("dout", 16)

                reg = self.io.din.reg(
                    clk=self.io.clk,
                    enable=self.io.din_valid,
                )
                self.io.dout <<= reg
                self.io.dout_valid <<= self.io.din_valid

        with helper.elaborate_to_file(
                TopModule(name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="stdio_valid_bundle_on_register_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )
