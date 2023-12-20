import random
from pathlib import Path

import cocotb.clock
import pytest
from cocotb_test.simulator import run as sim_run

from magia import Input, Module, Output, Signal


@cocotb.test()
async def inst_connect_test(dut):
    for i in range(10):
        dut.d.value = random.randint(0, 0xF0)
        await cocotb.clock.Timer(1, units="ns")

        actual_value = dut.q.value
        expected_value = dut.d.value + 2
        assert expected_value == actual_value, f"Expected {expected_value}, got {actual_value} on Entry {i}."


class TestBundle:
    TOP = "TopModule"

    def test_bundle_connect_inst(self, temp_build_dir):
        class SubModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("d", 8)
                self.io += Output("q", 8)
                self.io.q <<= self.io.d + 1

        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("d", 8)
                self.io += Output("q", 8)

                sub_mod = SubModule()
                bundles = [sub_mod.io.signal_bundle() for _ in range(2)]
                sub_insts = [sub_mod.instance() for i in range(2)]
                for bundle, inst in zip(bundles, sub_insts):
                    inst <<= bundle

                bundles[0].d <<= self.io.d
                bundles[1].d <<= bundles[0].q
                self.io.q <<= bundles[1].q

        with pytest.elaborate_to_file(
                TopModule(name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="inst_connect_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )

    def test_bundle_connect_inst_allow_extra(self, temp_build_dir):
        class SubModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("d", 8)
                self.io += Output("q", 8)
                self.io.q <<= self.io.d + 1

        class TopModule(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.io += Input("d", 8)
                self.io += Output("q", 8)

                sub_mod = SubModule()
                bundles = [sub_mod.io.signal_bundle() for _ in range(2)]
                for i, bundle in enumerate(bundles):
                    bundles[i] = bundle + Signal(8, name=f"extra{i}")
                sub_insts = [sub_mod.instance() for i in range(2)]
                for bundle, inst in zip(bundles, sub_insts):
                    inst <<= bundle

                bundles[0].d <<= self.io.d
                bundles[1].d <<= bundles[0].q
                self.io.q <<= bundles[1].q

        with pytest.elaborate_to_file(
                TopModule(name=self.TOP)
        ) as filename:
            sim_run(
                simulator="verilator",  # simulator
                verilog_sources=[filename],  # sources
                toplevel=self.TOP,  # top level HDL
                python_search=[str(Path(__name__).parent.absolute())],  # python search path
                module=Path(__name__).name,  # name of cocotb test module
                testcase="inst_connect_test",  # name of test function
                sim_build=temp_build_dir,  # temp build directory
                work_dir=temp_build_dir,  # simulation  directory
            )
