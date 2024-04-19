"""
Factory methods redirecting to other modules.

Calls in this module break the cyclic import dependencies between modules in magia by deferred imports.
Mostly called by core.py
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .comb_ops import Operation
    from .constant import Constant
    from .core import Signal
    from .data_struct import OPType


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


def deferred_imports():
    from .comb_ops import Operation as OperationImported
    from .constant import Constant as ConstantImported
    globals().update({
        "Constant": ConstantImported,
        "Operation": OperationImported,
    })
