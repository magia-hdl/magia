import random
from pathlib import Path

import cocotb
import pytest
from cocotb.clock import Clock
from cocotb.regression import TestFactory
from cocotb.triggers import FallingEdge
from cocotb_test.simulator import run as sim_run

from magia import Input, Module, Output
from magia.clock import clock as clock_input

cocotb_test_prefix = "coco_"
RESET_VALUE = 0xFF
ASYNC_RESET_VALUE = 0xEE


@cocotb.test()
async def reg_feature_test(dut, enable, reset, async_reset):
    """ Test that d propagates to q """

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())  # Start the clock

    if async_reset:
        dut.rst_n.value = 0
        await cocotb.clock.Timer(1, units="ns")  # Wait 11 ns
        dut.rst_n.value = 1
        assert dut.q.value == ASYNC_RESET_VALUE, "Failure on Async Reset"

    await FallingEdge(dut.clk)  # Synchronize with the clock

    dut.d.value = prev_q = 0x00
    if reset:
        dut.reset.value = 0
    if enable:
        dut.en.value = 1
    await FallingEdge(dut.clk)

    for i in range(50):
        reset_val = 1
        enable_val = 1

        # Decide whether to reset or enable the register randomly
        if reset:
            reset_val = random.randint(0, 5)
            dut.reset.value = 1 if reset_val == 0 else 0
        if enable:
            enable_val = random.randint(0, 5)
            dut.en.value = 0 if enable_val == 0 else 1

        # Assign a random value to d
        val = random.randint(0, 0xFF)
        dut.d.value = val

        expected_q = val
        if reset_val == 0:
            expected_q = RESET_VALUE
        elif enable_val == 0:
            expected_q = prev_q

        await FallingEdge(dut.clk)
        assert dut.q.value == expected_q, f"output q was incorrect on the {i}th cycle"

        prev_q = dut.q.value


reg_test_opts = ["enable", "reset", "async_reset"]
reg_test_opts_val = [
    (False, False, False),
    (False, False, True),
    (False, True, False),
    (False, True, True),
    (True, False, False),
    (True, False, True),
    (True, True, False),
    (True, True, True),
]
reg_test_pytest_param = ",".join(reg_test_opts + ["cocotb_testcase"])
reg_test_pytest_param_val = [
    val + (f"{cocotb_test_prefix}reg_feature_test_{i + 1:03d}",)
    for i, val in enumerate(reg_test_opts_val)
]

tf_reg_test = TestFactory(test_function=reg_feature_test)
tf_reg_test.add_option(reg_test_opts, reg_test_opts_val)
tf_reg_test.generate_tests(prefix=cocotb_test_prefix)


@cocotb.test()
async def reg_multi_reg_test(dut):
    """ Test that d propagates to q """

    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    data_len = 50
    reg_stages = 3

    tx_record = []
    rx_record = []

    for i in range(data_len):
        # Assign a random value to d
        val = random.randint(0, 0xFF)
        tx_record.append(val)

        dut.d.value = val

        await FallingEdge(dut.clk)
        rx_record.append(dut.q.value)

    tx_record = tx_record[:-reg_stages]
    rx_record = rx_record[reg_stages-1:]

    for i in range(len(tx_record)):
        assert tx_record[i] == rx_record[i], f"output q was incorrect on the {i}th cycle"


class TestRegisters:
    TOP = "TopModule"

    class ParamRegister(Module):
        def __init__(self, enable=False, reset=False, async_reset=False, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("clk", 1)

            if enable:
                self.io += Input("en", 1)
            if reset:
                self.io += Input("reset", 1)
            if async_reset:
                self.io += Input("rst_n", 1)

            self.io += Input("d", self.width)
            self.io += Output("q", self.width)

            reg_spec = {
                "enable": self.io.en if enable else None,
                "reset": self.io.reset if reset else None,
                "async_reset": self.io.rst_n if async_reset else None,
                "reset_value": RESET_VALUE,
                "async_reset_value": ASYNC_RESET_VALUE,
            }
            with clock_input(self.io.clk):
                self.io.q <<= self.io.d.reg(**reg_spec)

        @property
        def width(self):
            return 8

    class MultiStageRegister(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += Input("clk", 1)
            self.io += Input("d", self.width)
            self.io += Output("q", self.width)

            with clock_input(self.io.clk):
                self.io.q <<= self.io.d.reg().reg().reg()

        @property
        def width(self):
            return 8

    @pytest.mark.parametrize(reg_test_pytest_param, reg_test_pytest_param_val)
    def test_register_features(self, enable, reset, async_reset, cocotb_testcase, temp_build_dir):
        with pytest.elaborate_to_file(
                self.ParamRegister(enable, reset, async_reset, name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase=cocotb_testcase,  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )

    def test_register_multi_stage(self, temp_build_dir):
        with pytest.elaborate_to_file(
                self.MultiStageRegister(name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="reg_multi_reg_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )
