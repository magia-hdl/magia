"""
Data structures used in the magia package.

It includes
- Enums defining the types of signals and operations.
- SignalDict class that is used to store signals in a dictionary.
"""
from __future__ import annotations

from collections import UserDict
from enum import Enum, IntEnum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .core import Signal


class SignalDict(UserDict):
    """
    Signal Dict contains a dictionary of signals keyed by their name / specific alias.

    They are read only after being assigned.
    Alias (i.e. key of the dict) cannot start with `_`.
    """

    def __getattr__(self, alias):
        if alias.startswith("_"):
            return super().__getattribute__(alias)
        if alias not in self.data:
            raise KeyError(f"Signal {alias} is not defined.")
        return self.data[alias]

    def __getitem__(self, alias) -> None | Signal:
        if alias not in self.data:
            raise KeyError(f"Signal {alias} is not defined.")
        return self.data[alias]

    def __setitem__(self, alias, value):
        cur = self.data.get(alias)
        if value is not None and not hasattr(value, "signal_config"):
            raise KeyError(f"Object {alias} is not a Signal.")
        if cur is not None and value is not cur:
            raise KeyError(f"Signal {alias} is read only. Are you trying to connect it with <<= Operator?")

        if value is not None:
            self.data[alias] = value


class SignalType(Enum):
    """Kinds of signals."""

    WIRE = 0
    INPUT = 1
    OUTPUT = 2
    MEMORY = 3
    CONSTANT = 4


class OPType(IntEnum):
    """List of operations that can be performed on signals."""

    ANY = auto()
    ALL = auto()
    PARITY = auto()

    NOT = auto()
    OR = auto()
    AND = auto()
    XOR = auto()
    LSHIFT = auto()
    RSHIFT = auto()
    ALSHIFT = auto()
    ARSHIFT = auto()
    ADD = auto()
    MINUS = auto()
    MUL = auto()
    EQ = auto()
    NEQ = auto()
    LT = auto()
    LE = auto()
    GT = auto()
    GE = auto()

    SLICE = auto()
    CONCAT = auto()

    REG = auto()
    WHEN = auto()
    CASE = auto()
    MUX = auto()


class RegType(IntEnum):
    DFF = auto()
    DFF_EN = auto()
    DFF_RST = auto()
    DFF_EN_RST = auto()
    DFF_ASYNC_RST = auto()
    DFF_EN_ASYNC_RST = auto()
    DFF_BOTH_RST = auto()
    DFF_EN_BOTH_RST = auto()
