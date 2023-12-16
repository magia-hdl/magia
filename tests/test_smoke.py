import pytest
from cocotb.runner import get_runner

from magia import Input, Module, Output


class TestSmokeCompile:
    TOP = "TopModule"

    def compile_sv(self, sv_file: str, build_dir):
        runner = get_runner("verilator")
        runner.build(
            verilog_sources=[sv_file],
            hdl_toplevel=self.TOP,
            always=True,
            build_dir=build_dir,  # temp build directory
        )

    @pytest.mark.parametrize("width", [8, 12, 16])
    def test_comb_operators(self, width, temp_build_dir):
        class TopModule(Module):
            def __init__(self, width, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", width)
                self.io += Input("b", width)
                self.io += Output("q_accumulated", width)

                ops = [
                    self.io.a + self.io.b,
                    self.io.a - self.io.b,
                    self.io.a * self.io.b,
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
                    self.io += Output(f"q_{i}", width)
                    self.io[f"q_{i}"] <<= op

                accumulator = self.io.a + self.io.b
                accumulator += self.io.a
                accumulator -= self.io.a
                accumulator *= self.io.a
                accumulator |= self.io.a
                accumulator &= self.io.a
                accumulator ^= self.io.a
                self.io.q_accumulated <<= accumulator

        with pytest.elaborate_to_file(
                TopModule(width=width, name=self.TOP)
        ) as filename:
            self.compile_sv(filename, temp_build_dir)
