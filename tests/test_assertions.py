from tempfile import TemporaryDirectory

from magia_flow.formal import SbyTask

from magia import Constant, Input, Module, Output
from magia.assertions import AssertionCell


class TestAssertionCells:
    class DUT(Module):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.io += [
                Input("clk", 1),
                Input("start", 1),
                Output("out", 2),
            ]
            self.io.out <<= Constant(2, 2).when(self.io.start, 1)
            self.clocking = {"clk": self.io.clk}

    def test_formal_success(self):
        class Top(self.DUT):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with AssertionCell.code_section():
                    AssertionCell(
                        name="a_out_is_1_or_2",
                        cond=(self.io.out == 2) | (self.io.out == 1),
                        desc="Output is 1 or 2",
                        **self.clocking
                    )
                    for i in [1, 2]:
                        AssertionCell(
                            name=f"c_out_{i}",
                            assertion_type="cover",
                            cond=(self.io.out == i),
                            clk=self.io.clk,
                            desc=f"Output {i} is covered",
                        )

        top_name = "Top"
        top = Top(name=top_name)
        with TemporaryDirectory(prefix="magia-sby-") as workdir:
            task = SbyTask.from_module(top_name, top, work_dir=workdir)
            task.run()
            assert task.result.passed, "Formal BMC mode failed"

            task = SbyTask.from_module(top_name, top, work_dir=workdir, mode="prove")
            task.run()
            assert task.result.passed, "Formal Prove mode failed"

            task = SbyTask.from_module(top_name, top, work_dir=workdir, mode="cover")
            task.run()
            assert task.result.passed, "Formal Cover mode failed"

    def test_formal_assertion_failure(self):
        class Top(self.DUT):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with AssertionCell.code_section():
                    AssertionCell(
                        name="a_out_is_1_or_3",
                        cond=(self.io.out == 3) | (self.io.out == 1),
                        desc="Output is 1 or 3, which is not true in the design",
                        **self.clocking,
                    )
                    for i in [1, 2]:
                        AssertionCell(
                            name=f"c_out_{i}", assertion_type="cover",
                            cond=(self.io.out == i),
                            desc=f"Output {i} is covered",
                            **self.clocking,
                        )

        top_name = "Top"
        top = Top(name=top_name)
        with TemporaryDirectory(prefix="magia-sby-") as workdir:
            task = SbyTask.from_module(top_name, top, work_dir=workdir)
            task.run()
            assert not task.result.passed, "Formal BMC mode shall failed but passed"

            task = SbyTask.from_module(top_name, top, work_dir=workdir, mode="prove")
            task.run()
            assert not task.result.passed, "Formal Prove mode shall failed but passed"

            task = SbyTask.from_module(top_name, top, work_dir=workdir, mode="cover")
            task.run()
            assert not task.result.passed, "Formal Cover mode shall failed but passed"

    def test_formal_cover_failed_by_assumption(self):
        class Top(self.DUT):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                with AssertionCell.code_section():
                    AssertionCell(
                        name="a_out_is_1_or_2",
                        cond=(self.io.out == 2) | (self.io.out == 1),
                        desc="Output is 1 or 2",
                        **self.clocking
                    )
                    AssertionCell(
                        name="assm_start_true", assertion_type="assume",
                        cond=self.io.start,
                        desc="Assume start signal is always true. out == 1 will not be covered.",
                        **self.clocking,
                    )
                    for i in [1, 2]:
                        AssertionCell(
                            name=f"c_out_{i}", assertion_type="cover",
                            cond=(self.io.out == i),
                            desc=f"Output {i} is covered",
                            **self.clocking,
                        )

        top_name = "Top"
        top = Top(name=top_name)
        with TemporaryDirectory(prefix="magia-sby-") as workdir:
            task = SbyTask.from_module(top_name, top, work_dir=workdir)
            task.run()
            assert task.result.passed, "Formal BMC mode failed"

            task = SbyTask.from_module(top_name, top, work_dir=workdir, mode="prove")
            task.run()
            assert task.result.passed, "Formal Prove mode failed"

            task = SbyTask.from_module(top_name, top, work_dir=workdir, mode="cover")
            task.run()
            assert not task.result.passed, "Formal Cover mode shall failed but passed"
