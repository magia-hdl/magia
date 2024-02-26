import pytest
from magia_flow.simulation.general import Simulator

from magia import Input, Module, Output


class TestSmokeCompile:
    TOP = "TopModule"

    @pytest.mark.parametrize("width", [8, 12, 16])
    def test_comb_operators(self, width):
        class TopModule(Module):
            def __init__(self, width, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", width)
                self.io += Input("b", width)
                self.io += Output("q_accumulated", width)

                ops = [
                    self.io.a + self.io.b,
                    self.io.a - self.io.b,
                    self.io.a & self.io.b,
                    self.io.a | self.io.b,
                    self.io.a ^ self.io.b,

                    self.io.a + 0x0F,
                    self.io.a - 0x0F,
                    self.io.a * 0x0F,
                    self.io.a & 0x0F,
                    self.io.a | 0x0F,
                    self.io.a ^ 0x0F,

                    self.io.a << 2,
                    self.io.a >> 2,
                ]

                for i, op in enumerate(ops):
                    self.io += Output(f"q_{i}", op.width)
                    self.io[f"q_{i}"] <<= op

                accumulator = self.io.a + self.io.b
                accumulator += self.io.a
                accumulator -= self.io.a
                accumulator *= self.io.a
                accumulator = accumulator[width - 1:0]
                accumulator |= self.io.a
                accumulator &= self.io.a
                accumulator ^= self.io.a
                self.io.q_accumulated <<= accumulator

        sim = Simulator(self.TOP)
        sim.add_magia_module(TopModule(width, name=self.TOP))
        sim.compile()
