import cocotb
from cocotb.clock import Clock
from cocotb.triggers import FallingEdge
from magia_flow.simulation.general import Simulator

from magia import Input, Memory, Module, Output


async def drive_spram(dut):
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await FallingEdge(dut.clk)  # Synchronize with the clock

    dut.wen.value = 1
    dut.addr.value = 0x12
    dut.din.value = 0xAB
    await FallingEdge(dut.clk)
    dut.din.value = 0xCD
    await FallingEdge(dut.clk)


@cocotb.test()
async def spram_write_through(dut):
    """
    Write through shall return the value of the intermediate write
    """
    await drive_spram(dut)
    assert dut.dout.value == 0xCD, "Failure on write through"


@cocotb.test()
async def ram_read_first(dut):
    """
    Read first shall return the value of the previous write
    """
    await drive_spram(dut)
    assert dut.dout.value == 0xAB, "Failure on write through"


@cocotb.test()
async def spram_en_over_wen(dut):
    """
    If en is False, wen shall be ignored
    """
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    await FallingEdge(dut.clk)

    dut.en.value = 1
    dut.wen.value = 1
    dut.addr.value = 0x12
    dut.din.value = 0xAB
    await FallingEdge(dut.clk)
    dut.en.value = 0
    dut.din.value = 0xCD
    await FallingEdge(dut.clk)
    dut.en.value = 1
    dut.wen.value = 0
    await FallingEdge(dut.clk)
    assert dut.dout.value == 0xAB, f"Expected 0xAB, got 0x{dut.dout.value.integer:02X}"


class TestMemory:
    TOP = "TopModule"
    sim_module_and_path = {
        "test_module": [Simulator.current_package()],
        "python_search_path": [Simulator.current_dir()],
    }

    class SPRAM(Module):
        def __init__(self, rw_write_through, en=False, **kwargs):
            super().__init__(**kwargs)

            self.io += [
                Input("clk", 1),
                Input("wen", 1),
                Input("addr", 8),
                Input("din", 8),
                Output("dout", 8),
            ]
            if en:
                self.io += Input("en", 1)

            mem = Memory.sp(
                self.io.clk, 8, 8,
                rw_write_through=rw_write_through,
            )

            for port in ["addr", "din", "wen"]:
                mem.rw_port()[port] <<= self.io[port]
            if en:
                mem.rw_port().en <<= self.io.en
            else:
                mem.rw_port().en <<= 1
            self.io.dout <<= mem.rw_port().dout

    class SDPRAM(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

            self.io += [
                Input("clk", 1),
                Input("wen", 1),
                Input("addr", 8),
                Input("din", 8),
                Output("dout", 8),
            ]

            mem = Memory.sdp(self.io.clk, 8, 8, )

            for port in ["addr", "din", "wen"]:
                mem.write_port()[port] <<= self.io[port]

            mem.read_port().addr <<= self.io.addr
            mem.read_port().en <<= 1
            self.io.dout <<= mem.read_port().dout

    def test_sp_write_through(self):
        ram = self.SPRAM(rw_write_through=True, name=self.TOP)
        sim = Simulator(self.TOP)
        sim.add_magia_module(ram)
        sim.compile()
        sim.sim(
            testcase="spram_write_through",  # name of test function
            **self.sim_module_and_path,
        )

    def test_sp_read_first(self):
        ram = self.SPRAM(rw_write_through=False, name=self.TOP)
        sim = Simulator(self.TOP)
        sim.add_magia_module(ram)
        sim.compile()
        sim.sim(
            testcase="ram_read_first",  # name of test function
            **self.sim_module_and_path,
        )

    def test_sp_en_over_wen(self):
        ram = self.SPRAM(rw_write_through=False, en=True, name=self.TOP)
        sim = Simulator(self.TOP)
        sim.add_magia_module(ram)
        sim.compile()
        sim.sim(
            testcase="spram_en_over_wen",  # name of test function
            **self.sim_module_and_path,
        )

    def test_sdp_read_first(self):
        ram = self.SDPRAM(name=self.TOP)
        sim = Simulator(self.TOP)
        sim.add_magia_module(ram)
        sim.compile()
        sim.sim(
            testcase="ram_read_first",  # name of test function
            **self.sim_module_and_path,
        )
