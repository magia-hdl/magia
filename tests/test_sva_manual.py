import cocotb
import pytest
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from magia_flow.simulation.general import Simulator

from magia import Input, Module, Output, Register
from magia.sva_manual import SVAManual
from tests.helper import simulate


@cocotb.test()
async def counter_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    dut.rst.value = 1
    await FallingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut.rst.value = 0

    for _ in range(1000):
        await FallingEdge(dut.clk)


class TestSVAManual:
    TOP = "Counter"
    sim_module_and_path = {
        "test_module": [Simulator.current_package()],
        "python_search_path": [Simulator.current_dir()],
    }

    class Counter(Module):
        def __init__(self, sva_fail=False, **kwargs):
            super().__init__(**kwargs)
            self.io += [
                Input("clk", 1),
                Input("rst", 1),
                Output("out", 8),
            ]

            clk = {"clk": self.io.clk}

            counter = Register(8, **clk)
            counter <<= (counter + 1).when(self.io.rst == 0, 0)
            self.io.out <<= counter

            with SVAManual.code_section():
                SVAManual(
                    f"{self.io.out == 10} |=> {self.io.out == (12 if sva_fail else 11)}",
                    name="count", **clk,
                )

    def test_assertion_success(self):
        simulate(
            self.TOP, self.Counter(name=self.TOP), testcase="counter_test",
            build_args=["--assert"], **self.sim_module_and_path,
        )

    def test_assertion_failed(self):
        with pytest.raises(SystemExit):
            simulate(
                self.TOP, self.Counter(name=self.TOP, sva_fail=True), testcase="counter_test",
                build_args=["--assert"], **self.sim_module_and_path,
            )
