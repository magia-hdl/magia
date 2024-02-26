import functools
import inspect
from typing import Callable, Optional, Sequence, Union

from cocotb.regression import TestFactory
from magia_flow.simulation.general import Simulator

from magia import Module

COCOTB_TEST_PREFIX = "coco_"


def parameterized_testbench(test_function, test_opts_val) -> tuple[Callable, list, list]:
    """
    Create a set of parameterized testbench for cocotb.
    Generated testbench will be named as `coco_<test_function>_<index>`, starting from 001.

    Parameters of the test function are inferred from the function signature.

    Caller has to call the returned generator function to populate the tests in the caller's module.
    The returned list of parameters and values are used to parametrize the pytest test function.

    :param test_function: cocotb test function
    :param test_opts_val: list of test options values
    """
    test_opts = inspect.getfullargspec(test_function.__wrapped__).args[1:]  # skip `dut`

    pytest_param = ",".join(test_opts + ["cocotb_testcase"])
    pytest_param_val = [
        val + (f"{COCOTB_TEST_PREFIX}{str(test_function)}_{i + 1:03d}",)
        for i, val in enumerate(test_opts_val)
    ]

    # TestFactory.generate_tests() inject tests into the caller's module
    # So we need to return the generator function to the caller and populate in the caller's module
    tf_reg_test = TestFactory(test_function=test_function)
    tf_reg_test.add_option(test_opts, test_opts_val)
    test_generator = functools.partial(tf_reg_test.generate_tests, prefix=COCOTB_TEST_PREFIX)
    return test_generator, pytest_param, pytest_param_val


def simulate(
        top_level_name: str,
        hdl_modules: Module,
        test_module: Union[str, Sequence[str]],
        python_search_path: Optional[Union[str, Sequence[str]]] = None,
        testcase: Optional[Union[str, Sequence[str]]] = None,
):
    sim = Simulator(top_level_name)
    sim.add_magia_module(hdl_modules)
    sim.compile()
    sim.sim(
        testcase=testcase,
        test_module=test_module,
        python_search_path=python_search_path,
    )


__all__ = [
    "parameterized_testbench",
    "simulate"
]
