"""
Factory methods redirecting to other modules.

Calls in this module break the cyclic import dependencies between modules in magia by deferred imports.
Mostly called by core.py
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .constant import Constant
    from .core import Signal


def constant(value: int | bytes, width: int, signed: bool) -> Constant:
    """Create a constant."""
    import magia.constant
    return magia.constant.Constant(value, width, signed)


def constant_like(value: int | bytes, signal: Signal) -> Constant:
    """Create a constant signal with the same configuration as the given signal."""
    return constant(value, signal.width, signal.signed)


def sv_constant(value: None | int | bytes, width: int, signed: bool = False) -> str:
    """Redirect call to Constant.sv_constant, create SystemVerilog constant expression."""
    import magia.constant
    return magia.constant.Constant.sv_constant(value, width, signed)
