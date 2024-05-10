"""This module provides the basic unary/binary combinational operations for the digital design."""
from __future__ import annotations

from dataclasses import dataclass
from string import Template

from .constant import Constant
from .data_struct import OPType
from .signals import Signal


@dataclass
class OperationConfig:
    slicing: None | slice = None
    shifting: None | int = None


OP_IMPL_TEMPLATE = {
    OPType.NOT: Template("$output = ~$a;"),
    OPType.OR: Template("$output = $a | $b;"),
    OPType.AND: Template("$output = $a & $b;"),
    OPType.XOR: Template("$output = $a ^ $b;"),
    OPType.ADD: Template("$output = $a + $b;"),
    OPType.MINUS: Template("$output = $a - $b;"),
    OPType.MUL: Template("$output = $a * $b;"),
    OPType.EQ: Template("$output = $a == $b;"),
    OPType.NEQ: Template("$output = $a != $b;"),
    OPType.LT: Template("$output = $a < $b;"),
    OPType.LE: Template("$output = $a <= $b;"),
    OPType.GT: Template("$output = $a > $b;"),
    OPType.GE: Template("$output = $a >= $b;"),

    OPType.LSHIFT: Template("$output = $a << $b;"),
    OPType.RSHIFT: Template("$output = $a >> $b;"),
    OPType.ALSHIFT: Template("$output = $a <<< $b;"),
    OPType.ARSHIFT: Template("$output = $a >>> $b;"),

    OPType.ANY: Template("$output = $a != 0;"),
    OPType.ALL: Template("$output = $a == '1;"),
    OPType.PARITY: Template("$output = ^$a;"),

    OPType.CONCAT: Template("$output = {$a, $b};"),

    OPType.SLICE: Template("$output = $a[$slice_start:$slice_stop];"),

}
OP_WIDTH_INFERENCE = {
    OPType.NOT: lambda x, y: x.width,
    OPType.OR: lambda x, y: max(x.width, y.width),
    OPType.AND: lambda x, y: max(x.width, y.width),
    OPType.XOR: lambda x, y: max(x.width, y.width),
    OPType.ADD: lambda x, y: max(x.width, y.width),
    OPType.MINUS: lambda x, y: max(x.width, y.width),
    OPType.MUL: lambda x, y: x.width + y.width,
    OPType.EQ: lambda x, y: 1,
    OPType.NEQ: lambda x, y: 1,
    OPType.LT: lambda x, y: 1,
    OPType.LE: lambda x, y: 1,
    OPType.GT: lambda x, y: 1,
    OPType.GE: lambda x, y: 1,

    OPType.LSHIFT: lambda x, s: x.width,
    OPType.RSHIFT: lambda x, s: x.width,

    OPType.ANY: lambda x, y: 1,
    OPType.ALL: lambda x, y: 1,
    OPType.PARITY: lambda x, y: 1,

    OPType.CONCAT: lambda x, y: x.width + y.width,

    OPType.SLICE: lambda x, s: abs(s.stop - s.start) + 1,

}
OP_SIGN_INFERENCE = {
    OPType.NOT: lambda x, y: x.signed,
    OPType.OR: lambda x, y: x.signed or y.signed,
    OPType.AND: lambda x, y: x.signed or y.signed,
    OPType.XOR: lambda x, y: x.signed or y.signed,
    OPType.ADD: lambda x, y: x.signed or y.signed,
    OPType.MINUS: lambda x, y: x.signed or y.signed,
    OPType.MUL: lambda x, y: x.signed or y.signed,
    OPType.EQ: lambda x, y: False,
    OPType.NEQ: lambda x, y: False,
    OPType.LT: lambda x, y: False,
    OPType.LE: lambda x, y: False,
    OPType.GT: lambda x, y: False,
    OPType.GE: lambda x, y: False,

    OPType.LSHIFT: lambda x, s: x.signed,
    OPType.RSHIFT: lambda x, s: x.signed,

    OPType.ANY: lambda x, y: False,
    OPType.ALL: lambda x, y: False,
    OPType.PARITY: lambda x, y: False,

    OPType.CONCAT: lambda x, y: x.signed,
    OPType.SLICE: lambda x, s: x.signed,

}
OP_BLOCK_TEMPLATE = Template("always_comb\n  $op_impl")


class Operation(Signal):
    """Representing a simply unary/binary operation."""

    def __init__(self, width: int, op_type: OPType, signed: bool = False, **kwargs):
        super().__init__(width=width, signed=signed, **kwargs)
        self.signal_config.op_type = op_type
        self._op_config = OperationConfig()

    def elaborate(self) -> str:
        """Declare the signal and elaborate the operation in the module implementation."""
        op_impl = ""
        if self.signal_config.op_type in OP_IMPL_TEMPLATE:
            impl_params = {
                "output": self.name,
                "a": self._drivers["a"].name,
            }

            if self._drivers.get("b") is not None:
                impl_params["b"] = self._drivers["b"].name

            # Slicing Operator
            if self._op_config.slicing is not None:
                impl_params["slice_start"] = self._op_config.slicing.start
                impl_params["slice_stop"] = self._op_config.slicing.stop

            # Shifting Operator
            if self._op_config.shifting is not None:
                impl_params["b"] = self._op_config.shifting

            op_impl = OP_IMPL_TEMPLATE[self.signal_config.op_type].substitute(**impl_params)
            op_impl = OP_BLOCK_TEMPLATE.substitute(op_impl=op_impl)

        return op_impl

    @staticmethod
    def create(op_type: OPType, x: Signal, y: None | Signal | slice | int | bytes) -> Operation:
        """Create common operation with single / two arguments."""
        if not isinstance(x, Signal):
            raise TypeError(f"Cannot perform operation on {type(x)}")

        if op_type not in OP_IMPL_TEMPLATE:
            raise ValueError(f"Operation {op_type} is not supported.")
        if op_type not in (OPType.NOT, OPType.ANY, OPType.ALL, OPType.PARITY) and y is None:
            raise ValueError(f"Operation {op_type} requires two operand.")

        if op_type == OPType.SLICE:
            if not isinstance(y, slice):
                raise TypeError("Slicing Operator requires a slice as 2nd operand.")
        elif op_type == OPType.LSHIFT or op_type == OPType.RSHIFT:
            if not isinstance(y, int):
                raise TypeError("Shifting Operator only support constant shifting with integer.")
        else:
            if isinstance(y, (int, bytes)):
                y = Constant(y, x.width, x.signed)
            if not isinstance(y, Signal) and y is not None:
                raise TypeError(f"Cannot perform operation on {type(y)}")

        # Check the Sign of the Operands
        if op_type in (
                OPType.ADD, OPType.MINUS, OPType.MUL, OPType.GT, OPType.GE, OPType.LT, OPType.LE
        ) and isinstance(y, Signal) and x.signed != y.signed:
            raise ValueError("Operands must have the same signedness.")

        if op_type == OPType.SLICE:
            y = Operation._legalize_slice(x, y)

        if op_type in (OPType.LSHIFT, OPType.RSHIFT, OPType.ALSHIFT, OPType.ARSHIFT):
            if x.signed:
                op_type = {
                    OPType.LSHIFT: OPType.ALSHIFT,
                    OPType.RSHIFT: OPType.ARSHIFT,
                }.get(op_type, op_type)
            else:
                op_type = {
                    OPType.ALSHIFT: OPType.LSHIFT,
                    OPType.ARSHIFT: OPType.RSHIFT,
                }.get(op_type, op_type)

        new_op = Operation(
            width=OP_WIDTH_INFERENCE[op_type](x, y),
            signed=OP_SIGN_INFERENCE[op_type](x, y),
            op_type=op_type,
        )
        new_op._drivers["a"] = x
        if isinstance(y, Signal):
            new_op._drivers["b"] = y

        if op_type == OPType.SLICE:
            new_op._op_config.slicing = y
        if op_type in (OPType.LSHIFT, OPType.RSHIFT, OPType.ALSHIFT, OPType.ARSHIFT):
            new_op._op_config.shifting = y
        return new_op

    @staticmethod
    def _legalize_slice(driver: Signal, slice_: slice):
        if slice_.step is not None:
            raise ValueError("Slice step is not implement.")

        if slice_.start is None:
            slice_ = slice(driver.width - 1, slice_.stop, None)
        if slice_.stop is None:
            slice_ = slice(slice_.start, 0, None)

        if slice_.start < 0:
            slice_ = slice(slice_.start + driver.width, slice_.stop, None)
        if slice_.stop < 0:
            slice_ = slice(slice_.start, slice_.stop + driver.width, None)

        return slice_
