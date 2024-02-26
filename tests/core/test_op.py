import random
from itertools import product

import cocotb
import cocotb.clock
import pytest
from magia_flow.simulation.general import Simulator

import tests.helper as helper
from magia import Elaborator, Input, Module, Output

#############################
# Test for When and Case operations
#############################

@cocotb.test()
async def when_as_mux_test(dut):
    """ Test if the `when` operator works as a mux """
    for _ in range(50):
        a = random.randint(0, 0xFF)
        b = random.randint(0, 0xFF)
        sel = random.randint(0, 1)

        dut.a.value = a
        dut.b.value = b
        dut.sel.value = sel

        await cocotb.clock.Timer(1, units="ns")

        if sel == 1:
            assert dut.q.value == a
        else:
            assert dut.q.value == b


@cocotb.test()
async def when_as_mux_comp(dut):
    """ Test if the `when` operator works as a Comparator """
    for _ in range(16 * 16):
        a = random.randint(0, 0xF)
        b = random.randint(0, 0xF)

        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")

        if a != b:
            assert dut.q.value == a
        else:
            assert dut.q.value == 0xF


@cocotb.test()
async def case_as_mux(dut, selector, selection: dict[int, int]):
    """ Test if the `case` operator works as a mux """
    for _ in range(50):

        sel = random.randint(0, 2 ** selector - 1)
        dut.sel.value = sel
        for i in range(2 ** selector):
            getattr(dut, f"d_{i}").value = random.randint(1, 0xFF)

        await cocotb.clock.Timer(1, units="ns")

        if sel in selection:
            assert dut.q.value == getattr(dut, f"d_{selection[sel]}").value
        else:
            for i in range(2 ** selector):
                assert dut.q.value != getattr(dut, f"d_{i}").value


gen_test, case_as_mux_params, case_as_mux_values = helper.parameterized_testbench(
    case_as_mux, [
        (1, {1: 0}),
        (1, {0: 0, 1: 1}),
        (2, {0: 0, 3: 2}),
        (2, {0: 0, 1: 1, 3: 2}),
        (2, {0: 0, 1: 1, 2: 2, 3: 3}),
        (3, {0: 0, 4: 1}),
        (3, {i: i for i in range(8)}),
    ],
)
gen_test()


@cocotb.test()
async def case_as_lut(dut):
    """ Test if the `case` operator works as a LUT """
    for i in range(256 * 4):
        a = random.randint(0, 255)
        dut.a.value = a

        await cocotb.clock.Timer(1, units="ns")
        ref_out = getattr(dut, f"lut_{a}")

        assert dut.q.value == ref_out, f"Expected {ref_out}, got {dut.q.value} on Entry {i}."


#############################
# Arithmetic tests
#############################

def assert_not_extended(a, b, dut):
    assert dut.qadd.value == (a + b) & 0xFF
    assert dut.qsub.value == (a - b) & 0xFF
    assert dut.qmul.value == (a * b) & 0xFFFF
    assert dut.qge.value == int(a >= b)
    assert dut.qgt.value == int(a > b)
    assert dut.qle.value == int(a <= b)
    assert dut.qlt.value == int(a < b)
    assert dut.qeq.value == int(a == b)
    assert dut.qne.value == int(a != b)


@cocotb.test()
async def unsigned_op(dut):
    """ Test if the unsigned arithmetic works """
    for a, b in product(range(256), range(256)):
        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")
        assert_not_extended(a, b, dut)


@cocotb.test()
async def signed_op(dut):
    """ Test if the signed arithmetic works """
    for a, b in product(range(-128, 128), range(-128, 128)):
        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")
        assert_not_extended(a, b, dut)


@cocotb.test()
async def unsigned_op_extended(dut):
    """ Test if the unsigned arithmetic works """
    for a, b in product(range(256), range(256)):
        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")
        assert dut.qadd.value.integer == a + b
        assert dut.qsub.value.signed_integer == a - b
        assert dut.qmul.value.integer == a * b


@cocotb.test()
async def signed_op_extended(dut):
    """ Test if the signed arithmetic works """
    for a, b in product(range(-128, 128), range(-128, 128)):
        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")
        assert dut.qadd.value.signed_integer == a + b
        assert dut.qsub.value.signed_integer == a - b
        assert dut.qmul.value.signed_integer == a * b


@cocotb.test()
async def bitwise_op(dut):
    """ Test all bitwise operator """
    for a, b in product(range(256), range(256)):
        dut.a.value = a
        dut.b.value = b

        await cocotb.clock.Timer(1, units="ns")
        assert dut.bit_or.value.integer == (a | b) & 0xFF
        assert dut.bit_and.value.integer == (a & b) & 0xFF
        assert dut.bit_xor.value.integer == (a ^ b) & 0xFF

        assert dut.any.value.integer == ((a & 0xFF) > 0)
        assert dut.all.value.integer == ((a & 0xFF) == 0xFF)
        assert dut.parity.value.integer == ((bin(a & 0xFF).count("1")) % 2)


#############################
# Pytest testcases
#############################


class TestWhenCase:
    TOP = "TopModule"
    sim_module_and_path = {
        "test_module": [Simulator.current_package()],
        "python_search_path": [Simulator.current_dir()],
    }

    def test_when_mux(self):
        class SimpleMux(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8)
                self.io += Input("b", 8)
                self.io += Input("sel", 1)
                self.io += Output("q", 8)

                self.io.q <<= self.io.a.when(self.io.sel, else_=self.io.b)

        helper.simulate(
            self.TOP, SimpleMux(name=self.TOP), testcase="when_as_mux_test",
            **self.sim_module_and_path,
        )

    def test_when_cond(self):
        class Comparator(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 4)
                self.io += Input("b", 4)
                self.io += Output("q", 4)

                self.io.q <<= self.io.a.when(self.io.a != self.io.b, else_=0xF)

        helper.simulate(
            self.TOP, Comparator(name=self.TOP), testcase="when_as_mux_comp",
            **self.sim_module_and_path,
        )

    @pytest.mark.parametrize("width, cases, expected_default", [
        (4, 4, True),
        (4, 10, True),
        (4, 16, False),
        (8, 8, True),
        (8, 16, True),
        (8, 256, False),
        (10, 16, True),
        (10, 1024, False),
    ])
    def test_case_default_unique_detection(self, width, cases, expected_default):
        class CaseModule(Module):
            def __init__(self, width, cases, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", width)

                cases = {i: i + 1 for i in range(cases)}
                case_logic = self.io.a.case(cases)
                self.io += Output("q", len(case_logic))
                self.io.q <<= case_logic

        sv_code = Elaborator.to_string(CaseModule(width=width, cases=cases))
        if expected_default:
            # Expect default case to be generated
            assert "default:" in sv_code
            assert "'hX" in sv_code
        else:
            # All cases exist, no default case and unique case is apply-able
            assert "unique case" in sv_code

    @pytest.mark.parametrize(case_as_mux_params, case_as_mux_values)
    def test_case_as_mux(self, selector, selection, cocotb_testcase):
        class CaseMux(Module):
            def __init__(self, selector, selection, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("sel", selector)
                for i in range(2 ** selector):
                    self.io += Input(f"d_{i}", 8)
                self.io += Output("q", 8)

                self.io.q <<= self.io.sel.case(cases={
                    case: self.io[f"d_{select}"]
                    for case, select in selection.items()
                }, default=None)

        helper.simulate(
            self.TOP, CaseMux(selector, selection, name=self.TOP), testcase=cocotb_testcase,
            **self.sim_module_and_path,
        )

    def test_case_as_lut(self):
        class CaseLut(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8)
                self.io += Output("q", 16)

                case_as_lut_table = {i: random.randint(0, 0xFFFF) for i in range(256)}
                self.io += [
                    Output(f"lut_{i}", 16)
                    for i in case_as_lut_table
                ]

                self.io.q <<= self.io.a.case(cases=case_as_lut_table, default=None)
                for i in case_as_lut_table:
                    self.io[f"lut_{i}"] <<= case_as_lut_table[i]

        helper.simulate(
            self.TOP, CaseLut(name=self.TOP), testcase="case_as_lut",
            **self.sim_module_and_path,
        )


class TestArithmetic:
    TOP = "TopModule"
    sim_module_and_path = {
        "test_module": [Simulator.current_package()],
        "python_search_path": [Simulator.current_dir()],
    }

    def test_unsigned(self):
        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8)
                self.io += Input("b", 8)
                self.io += Output("qadd", 8)
                self.io += Output("qsub", 8)
                self.io += Output("qmul", 16)
                self.io += Output("qge", 1)
                self.io += Output("qgt", 1)
                self.io += Output("qle", 1)
                self.io += Output("qlt", 1)
                self.io += Output("qeq", 1)
                self.io += Output("qne", 1)

                self.io.qadd <<= self.io.a + self.io.b
                self.io.qsub <<= self.io.a - self.io.b
                self.io.qmul <<= self.io.a * self.io.b
                self.io.qge <<= self.io.a >= self.io.b
                self.io.qgt <<= self.io.a > self.io.b
                self.io.qle <<= self.io.a <= self.io.b
                self.io.qlt <<= self.io.a < self.io.b
                self.io.qeq <<= self.io.a == self.io.b
                self.io.qne <<= self.io.a != self.io.b

        helper.simulate(
            self.TOP, Top(name=self.TOP), testcase="unsigned_op",
            **self.sim_module_and_path,
        )

    def test_signed(self):
        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8, signed=True)
                self.io += Input("b", 8, signed=True)
                self.io += Output("qadd", 8, signed=True)
                self.io += Output("qsub", 8, signed=True)
                self.io += Output("qmul", 16, signed=True)
                self.io += Output("qge", 1)
                self.io += Output("qgt", 1)
                self.io += Output("qle", 1)
                self.io += Output("qlt", 1)
                self.io += Output("qeq", 1)
                self.io += Output("qne", 1)

                self.io.qadd <<= self.io.a + self.io.b
                self.io.qsub <<= self.io.a - self.io.b
                self.io.qmul <<= self.io.a * self.io.b
                self.io.qge <<= self.io.a >= self.io.b
                self.io.qgt <<= self.io.a > self.io.b
                self.io.qle <<= self.io.a <= self.io.b
                self.io.qlt <<= self.io.a < self.io.b
                self.io.qeq <<= self.io.a == self.io.b
                self.io.qne <<= self.io.a != self.io.b

        helper.simulate(
            self.TOP, Top(name=self.TOP), testcase="signed_op",
            **self.sim_module_and_path,
        )

    def test_unsigned_extended(self):
        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8)
                self.io += Input("b", 8)
                self.io += Output("qadd", 9)
                self.io += Output("qsub", 9)
                self.io += Output("qmul", 16)

                self.io.qadd <<= (self.io.a + self.io.b).set_width(9)
                self.io.qsub <<= (self.io.a - self.io.b).set_width(9)
                self.io.qmul <<= (self.io.a * self.io.b).set_width(16)

        helper.simulate(
            self.TOP, Top(name=self.TOP), testcase="unsigned_op_extended",
            **self.sim_module_and_path,
        )

    def test_signed_extended(self):
        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8, signed=True)
                self.io += Input("b", 8, signed=True)
                self.io += Output("qadd", 9, signed=True)
                self.io += Output("qsub", 9, signed=True)
                self.io += Output("qmul", 16, signed=True)

                self.io.qadd <<= (self.io.a + self.io.b).set_width(9)
                self.io.qsub <<= (self.io.a - self.io.b).set_width(9)
                self.io.qmul <<= (self.io.a * self.io.b).set_width(16)

        helper.simulate(
            self.TOP, Top(name=self.TOP), testcase="signed_op_extended",
            **self.sim_module_and_path,
        )

    def test_bitwise(self):
        class Top(Module):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)

                self.io += Input("a", 8)
                self.io += Input("b", 8)

                self.io += Output("bit_or", 8)
                self.io += Output("bit_and", 8)
                self.io += Output("bit_xor", 8)

                self.io += Output("any", 1)
                self.io += Output("all", 1)
                self.io += Output("parity", 1)

                self.io.bit_or <<= self.io.a | self.io.b
                self.io.bit_and <<= self.io.a & self.io.b
                self.io.bit_xor <<= self.io.a ^ self.io.b

                self.io.any <<= self.io.a.any()
                self.io.all <<= self.io.a.all()
                self.io.parity <<= self.io.a.parity()

        helper.simulate(
            self.TOP, Top(name=self.TOP), testcase="bitwise_op",
            **self.sim_module_and_path,
        )
