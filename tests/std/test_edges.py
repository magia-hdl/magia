import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from magia_flow.simulation.general import Simulator

from magia import Input, Module, Output
from magia.std.edges import edge_detector
from tests.helper import simulate

sim_module_and_path = {
    "test_module": [Simulator.current_package()],
    "python_search_path": [Simulator.current_dir()],
}


@cocotb.test()
async def edge_detection(dut):
    """Check the functionality of edge detection."""
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await FallingEdge(dut.clk)

    dut.reset.value = 1
    dut.rst_n.value = 0
    await FallingEdge(dut.clk)
    dut.reset.value = 0
    dut.rst_n.value = 1

    for i in range(1000):
        # Drive signal and setup expectation
        cur_event, prev_event = random.randint(0, 1), (cur_event if i != 0 else None)
        dut.event_in.value = cur_event
        expectation = (
            1 if cur_event == 1 and prev_event == 0 else 0,
            1 if cur_event == 0 and prev_event == 1 else 0,
            1 if cur_event != prev_event else 0,
        ) if prev_event is not None else None

        await cocotb.clock.Timer(1)
        if expectation is not None:
            exp_rising_unreg, exp_falling_unreg, exp_both_unreg = expectation
            assert dut.rising_unreg.value == exp_rising_unreg or exp_rising_unreg is None, \
                f"Rising edge failed at {cur_event}, {prev_event}"
            assert dut.falling_unreg.value == exp_falling_unreg or exp_falling_unreg is None, \
                f"Falling edge failed at {cur_event}, {prev_event}"
            assert dut.both_unreg.value == exp_both_unreg or exp_both_unreg is None, \
                f"Both edge failed at {cur_event}, {prev_event}"

        # Wait for the next clock edge
        await FallingEdge(dut.clk)

        if expectation is not None:
            exp_rising, exp_falling, exp_both = expectation
            assert dut.rising.value == exp_rising or exp_rising is None, \
                f"Rising edge failed at {cur_event}, {prev_event}"
            assert dut.falling.value == exp_falling or exp_falling is None, \
                f"Falling edge failed at {cur_event}, {prev_event}"
            assert dut.both.value == exp_both or exp_both is None, \
                f"Both edge failed at {cur_event}, {prev_event}"
            assert dut.rising_async.value == exp_rising or exp_rising is None, \
                f"Rising edge failed at {cur_event}, {prev_event}"
            assert dut.falling_async.value == exp_falling or exp_falling is None, \
                f"Falling edge failed at {cur_event}, {prev_event}"
            assert dut.both_async.value == exp_both or exp_both is None, \
                f"Both edge failed at {cur_event}, {prev_event}"


class AllEdges(Module):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.io += [
            Input("clk", 1),
            Input("reset", 1),
            Input("rst_n", 1),
            Input("event_in", 1),
            Output("rising", 1),
            Output("falling", 1),
            Output("both", 1),
            Output("rising_unreg", 1),
            Output("falling_unreg", 1),
            Output("both_unreg", 1),
            Output("rising_async", 1),
            Output("falling_async", 1),
            Output("both_async", 1),
        ]

        sync_clock = {
            "signal": self.io.event_in,
            "clk": self.io.clk,
            "reset": self.io.reset,
        }
        async_clock = {
            "signal": self.io.event_in,
            "clk": self.io.clk,
            "async_reset": self.io.rst_n,
        }
        unregistered = {
            "clk": self.io.clk,
            "signal": self.io.event_in,
            "reset": self.io.reset,
            "registered": False,
        }

        self.io.rising <<= edge_detector(edge="rising", **sync_clock)
        self.io.falling <<= edge_detector(edge="falling", **sync_clock)
        self.io.both <<= edge_detector(edge="both", **sync_clock)

        self.io.rising_async <<= edge_detector(edge="rising", **async_clock)
        self.io.falling_async <<= edge_detector(edge="falling", **async_clock)
        self.io.both_async <<= edge_detector(edge="both", **async_clock)

        self.io.rising_unreg <<= edge_detector(edge="rising", **unregistered)
        self.io.falling_unreg <<= edge_detector(edge="falling", **unregistered)
        self.io.both_unreg <<= edge_detector(edge="both", **unregistered)


def test_edge_detector():
    all_edges = AllEdges(name="TopModule")
    simulate(
        "TopModule", all_edges, testcase="edge_detection",
        **sim_module_and_path,
    )
