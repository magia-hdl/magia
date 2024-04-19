"""
Factory methods redirecting to other modules.

Calls in this module break the cyclic import dependencies between modules in magia by deferred imports.
Mostly called by core.py
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .comb_ops import Operation
    from .comb_select import Case, When
    from .constant import Constant
    from .core import Signal
    from .data_struct import OPType
    from .register import Register


def constant(value: int | bytes, width: int, signed: bool) -> Constant:
    """Create a constant."""
    return Constant(value, width, signed)


def constant_like(value: int | bytes, signal: Signal) -> Constant:
    """Create a constant signal with the same configuration as the given signal."""
    return constant(value, signal.width, signal.signed)


def sv_constant(value: None | int | bytes, width: int, signed: bool = False) -> str:
    """Redirect call to Constant.sv_constant, create SystemVerilog constant expression."""
    return Constant.sv_constant(value, width, signed)


def create_comb_op(op_type: OPType, x: Signal, y: None | Signal | slice | int | bytes) -> Operation:
    return Operation.create(op_type, x, y)


def create_when(condition: Signal, if_true: Signal, if_false: None | Signal | int | bytes, **kwargs) -> When:
    return When(condition, if_true, if_false, **kwargs)


def create_case(
        selector: Signal, cases: dict[int, Signal | int],
        default: None | Signal | int = None,
        **kwargs
) -> Case:
    return Case(selector, cases, default, **kwargs)


def register(
        width: int,
        enable: None | Signal = None,
        reset: None | Signal = None,
        reset_value: None | bytes | int = None,
        async_reset: None | Signal = None,
        async_reset_value: None | bytes | int = None,
        clk: None | Signal = None,
        name: None | str = None,
        **kwargs
) -> Register:
    """Create a register."""
    return Register(
        width=width,
        enable=enable,
        reset=reset,
        reset_value=reset_value,
        async_reset=async_reset,
        async_reset_value=async_reset_value,
        clk=clk,
        name=name,
        **kwargs
    )


def deferred_imports():
    from .comb_ops import Operation as OperationImported
    from .comb_select import Case as CaseImported
    from .comb_select import When as WhenImported
    from .constant import Constant as ConstantImported
    from .register import Register as RegisterImported
    globals().update({
        "Constant": ConstantImported,
        "Operation": OperationImported,
        "Register": RegisterImported,
        "Case": CaseImported,
        "When": WhenImported
    })
