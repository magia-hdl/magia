from pathlib import Path

import cocotb.clock
import pytest
from cocotb_test.simulator import run as sim_run

import tests.helper as helper
from magia import Constant, Module, Output

test_constants = [
    # Format: (value, width, signed) # noqa: ERA001
    (0, 8, False),
    (0, 8, True),
    (0xFF, 8, False),
    (-1, 8, True),
    (0x0F, 8, False),
    (0x0F, 8, True),
    (0x0F, 4, False),
    (0x0F, 4, True),
    (0x0F, 2, False),
    (0x0F, 2, True),
    (0x0F, 1, False),
    (0x0F, 1, True),
    (0x0F, 16, False),
    (0x0F, 16, True),
    (0x0F, 32, False),
    (0x0F, 32, True),
    (0x0F, 64, False),
    (0x0F, 64, True),
    (-10, 3, True),
]
test_constants += [(i, 5, True) for i in range(-16, 16)]
test_constants += [(i, 5, False) for i in range(0, 32)]


class AssignmentModule(Module):
    def __init__(self, constant_list, **kwargs):
        super().__init__(**kwargs)

        for i, (value, width, signed) in enumerate(constant_list):
            port_name = f"q{i}"
            self.io += Output(port_name, width, signed=signed)
            self.io[port_name] <<= Constant(value, width, signed=signed)


@cocotb.test()
async def constant_test(dut):
    for i, (expected_value, width, signed) in enumerate(test_constants):
        await cocotb.clock.Timer(1, units="ns")
        actual_value = getattr(dut, f"q{i}").value

        if expected_value.bit_length() > width:
            expected_value = expected_value & ((1 << width) - 1)

        if signed:
            if expected_value > 0 and expected_value >> (width - 1) > 0:
                # The expected value is assigned in Hex format and therefore positive,
                # while the actual value is a negative number due to its width constraint.
                actual_value = actual_value.integer
            else:
                actual_value = actual_value.signed_integer
        else:
            actual_value = actual_value.integer
        assert actual_value == expected_value, f"Expected {expected_value}, got {actual_value} on Entry {i}."


class TestSvConstant:
    TOP = "AssignmentModule"

    def test_sv_constant_integers(self, temp_build_dir):
        with helper.elaborate_to_file(
                AssignmentModule(test_constants, name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="constant_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )

    @pytest.mark.parametrize("width, signed, expected", [
        (8, False, "8'hX"),
        (8, True, "8'shX"),
        (16, False, "16'hX"),
        (16, True, "16'shX"),
        (32, False, "32'hX"),
        (32, True, "32'shX"),
        (64, False, "64'hX"),
        (64, True, "64'shX"),
    ])
    def test_sv_constant_unknown(self, width, signed, expected):
        assert Constant.sv_constant(None, width, signed) == expected
