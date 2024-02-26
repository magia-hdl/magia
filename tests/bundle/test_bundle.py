import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge, RisingEdge
from magia_flow.simulation.general import Simulator

from magia import Input, Module
from magia.std.bundles import valid_signal
from tests.helper import simulate


async def input_driver(dut):
    dut.reset.value = 1
    await FallingEdge(dut.clk)  # Synchronize with the clock
    await FallingEdge(dut.clk)
    dut.reset.value = 0

    for _ in range(1000):
        dut.in_data.value = random.randint(0, 2 ** 15)
        dut.in_valid.value = 1 if random.randint(0, 4) > 1 else 0
        await FallingEdge(dut.clk)
    for _ in range(5):
        dut.in_valid.value = 0
        await FallingEdge(dut.clk)


async def io_monitor(dut, end_of_sim: cocotb.triggers.Event):
    input_record, output_record = [], []
    await RisingEdge(dut.clk)
    await FallingEdge(dut.reset)
    while not end_of_sim.is_set():
        await RisingEdge(dut.clk)
        if dut.in_valid.value.integer == 1:
            input_record.append(dut.in_data.value.integer)
        await FallingEdge(dut.clk)
        if dut.out_valid.value.integer == 1:
            output_record.append(dut.out_data.value.integer)
    return input_record, output_record


@cocotb.test()
async def bundle_test(dut):
    clock = Clock(dut.clk, 10, units="ns")
    end_of_sim = cocotb.triggers.Event()

    cocotb.start_soon(clock.start())
    monitor = cocotb.start_soon(io_monitor(dut, end_of_sim))
    await cocotb.start_soon(input_driver(dut))
    end_of_sim.set()
    input_list, output_list = await monitor

    for in_data, out_data in zip(input_list, output_list):
        assert (in_data + 6) == out_data, f"Expected {in_data + 6}, got {out_data}"


def test_bundle_connections():
    top = "TopModule"
    width = 16
    data_bus_spec = valid_signal(width=width)

    class Incrementer(Module):
        def __init__(self, increment, **kwargs):
            super().__init__(**kwargs)

            self.io += Input("clk", 1)
            self.io += Input("reset", 1)
            self.io += data_bus_spec.slave_ports(prefix="in_")
            self.io += data_bus_spec.master_ports(prefix="out_")

            input_bus = data_bus_spec.bundle()
            output_bus = data_bus_spec.bundle()
            self.io <<= input_bus.with_name("in_")
            self.io <<= output_bus.with_name("out_")

            clock_domain = {
                "clk": self.io.clk,
                "reset": self.io.reset,
            }

            output_bus.valid <<= input_bus.valid.reg(**clock_domain)
            output_bus.data <<= (input_bus.data + increment).reg(**clock_domain, enable=input_bus.valid)

    class TopModule(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.io += Input("clk", 1)
            self.io += Input("reset", 1)
            self.io += data_bus_spec.slave_ports(prefix="in_")
            self.io += data_bus_spec.master_ports(prefix="out_")

            clock_domain = {
                "clk": self.io.clk,
                "reset": self.io.reset,
            }

            increments = [1, 2, 3]
            increments_insts = [
                Incrementer(inc).instance(
                    f"incrementer_{i}",
                    io=clock_domain,
                )
                for i, inc in enumerate(increments)
            ]

            input_bus = data_bus_spec.bundle()
            interconnects = [data_bus_spec.bundle() for _ in increments_insts]
            for i, incrementer in enumerate(increments_insts):
                incrementer <<= (
                    input_bus.with_name("in_")
                    if i == 0
                    else interconnects[i - 1].with_name("in_")
                )
                incrementer <<= interconnects[i].with_name("out_")
            self.io <<= input_bus.with_name("in_")
            self.io <<= interconnects[-1].with_name("out_")

    simulate(
        top, TopModule(name=top), testcase="bundle_test",
        test_module=[Simulator.current_package()],
        python_search_path=[Simulator.current_dir()],
    )
