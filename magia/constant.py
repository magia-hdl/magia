"""
Implementation of a constant signal with fixed value.

The constant signal is elaborated as a SystemVerilog constant expression.
"""
from __future__ import annotations

from itertools import count
from math import ceil

from .core import Signal
from .data_struct import SignalType


class Constant(Signal):
    """Representing a constant signal. The value stored in bytes representing the constance driver."""

    new_const_counter = count(0)

    def __init__(
            self,
            value: int | bytes, width: int, signed: bool = False,
            name: str | None = None,
            **kwargs
    ):
        if name is None:
            name = f"const_{next(self.new_const_counter)}"

        super().__init__(width=width, signed=signed, name=name, **kwargs)
        self.signal_config.signal_type = SignalType.CONSTANT
        self.value = value

    def elaborate(self) -> str:
        signal_decl = self.signal_decl()
        assignment = self._SIGNAL_ASSIGN_TEMPLATE.substitute(
            name=self.name,
            driver=self.sv_constant(self.value, self.width, self.signed),
        )
        return "\n".join((signal_decl, assignment))

    @staticmethod
    def sv_constant(value: None | int | bytes, width: int, signed: bool = False) -> str:
        """
        Convert a Python integer or bytes object to a SystemVerilog constant expression.

        If value is None, return "X", the SystemVerilog constant for an unknown value.
        :param value: The value to convert.
        :param width: The width of the constant.
        :param signed: If the constant is signed.
        :returns: The SystemVerilog constant expression.
        """
        byte_cnt = ceil(width / 8)
        if value is not None:
            if isinstance(value, int):
                value = value.to_bytes(byte_cnt, byteorder="big", signed=signed)
            byte_mask = (2 ** width - 1).to_bytes(byte_cnt, byteorder="big")
            value = bytes([x & y for x, y in zip(value, byte_mask)])
            value = value.hex()[-(ceil(width / 4)):].upper()
        else:
            value = "X"
        sign = "s" if signed else ""
        return f"{width}'{sign}h{value}"
