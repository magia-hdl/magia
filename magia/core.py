from collections import UserDict
from collections.abc import Iterable
from dataclasses import dataclass
from itertools import count
from math import ceil
from string import Template
from typing import Optional, Union

from .constants import OPType, RegType, SignalType


@dataclass
class SignalConfig:
    name: Optional[str] = None
    width: int = 0
    signed: bool = False
    signal_type: SignalType = SignalType.WIRE

    # The module instance that owns this signal
    # Applicable to input / output ports only
    owner_instance: Optional["Instance"] = None

    # The signal bundle that owns this signal
    # Applicable to signals only
    parent_bundle: Optional["SignalBundle"] = None


@dataclass
class OperationConfig:
    op_type: OPType
    slicing: Optional[slice] = None
    shifting: Optional[int] = None


@dataclass
class CaseConfig:
    unique: bool = False
    default: Optional["Signal"] = None


@dataclass
class RegisterConfig:
    enable: bool
    reset: bool
    async_reset: bool
    reset_value: Optional[Union[bytes, int]] = None
    async_reset_value: Optional[Union[bytes, int]] = None


class Synthesizable:
    """
    The base class of all synthesizable objects.
    They can be elaborated into SystemVerilog code.
    """

    def __init__(self, **kwargs):
        ...

    @property
    def net_name(self) -> str:
        """
        Full name of a signal, used for elaboration.
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """
        Short name of the signal, is used to identify the signal in a bundle / SignalDict
        """
        raise NotImplementedError

    @property
    def drivers(self) -> list["Signal"]:
        """
        Get the drivers of a Synthesizable object.
        :return: The driver signals.
        """
        raise NotImplementedError

    def elaborate(self) -> str:
        """
        Elaborate the object into SystemVerilog code.
        All configuration should be resolved before calling this method.
        :return: SystemVerilog code
        """
        return ""


class Signal(Synthesizable):
    """
    The general signal class. It has drivers, which is another signal.
    It can also drive other signals / module instances.
    """
    SINGLE_DRIVER_NAME: str = "d"
    _SIGNAL_DECL_TEMPLATE = Template("logic $signed $width $name;")
    _SIGNAL_CONNECT_TEMPLATE = Template("always_comb\n  $name = $driver;")
    _SIGNAL_ASSIGN_TEMPLATE = Template("assign $name = $driver;")

    _new_signal_counter = count(0)

    def __init__(
            self,
            width: int = 0, signed: bool = False,
            name: Optional[str] = None,
            parent_bundle: Optional["SignalBundle"] = None,
            **kwargs
    ):
        if name is None:
            name = f"net_{next(self._new_signal_counter)}"

        super().__init__(**kwargs)
        self._config = SignalConfig(
            name=name,
            width=width,
            signed=signed,
            parent_bundle=parent_bundle,
        )
        self._drivers = SignalDict()

    @property
    def net_name(self) -> str:
        """
        Full name of a signal, used for elaboration.
        """
        if self._config.parent_bundle is not None:
            if self._config.parent_bundle.name is not None:
                return f"bundle_{self._config.parent_bundle.name}_{self.name}"
            return f"bundle_{id(self._config.parent_bundle)}_{self.name}"
        return self.name

    @property
    def name(self) -> str:
        """
        Short name of the signal, is used to identify the signal in a bundle / SignalDict
        """
        return self._config.name

    @property
    def type(self) -> SignalType:
        return self._config.signal_type

    @property
    def signed(self) -> bool:
        return self._config.signed

    def driver(self, driver_name: str = SINGLE_DRIVER_NAME) -> Optional["Signal"]:
        """
        Get the driver of the signal.
        :param driver_name: The name of the driver. Default to the single driver.
        :return: The driver signal.
        """
        return self._drivers.get(driver_name)

    @property
    def drivers(self) -> list["Signal"]:
        """
        Get the drivers of the signal.
        :return: The driver signals.
        """
        return list(self._drivers.values())

    @property
    def owner_instance(self) -> Optional["Instance"]:
        """
        Get the module instance that owns this signal.
        It is applicable to input / output signals only.
        """
        return self._config.owner_instance

    def set_width(self, width: int):
        self._config.width = width
        return self

    def set_signed(self, signed: bool):
        self._config.signed = signed
        return self

    def set_name(self, name: str):
        self._config.name = name
        return self

    def with_signed(self, signed: bool) -> "Signal":
        """
        Create a new signal with the same configuration, but with a different signedness.
        Connect the original signal to the new signal.

        New Signal is not added to the parent bundle.

        :return: A new signal with the same configuration.
        """
        signal = Signal(
            width=len(self),
            signed=signed,
            name=self.name,
            parent_bundle=None,
        )
        signal <<= self
        return signal

    def with_width(self, width: int) -> "Signal":
        """
        Create a new signal with the same configuration, but with a different width.
        Connect the original signal to the new signal.

        New Signal is not added to the parent bundle.

        :return: A new signal with the new configuration.
        """
        if width == len(self):
            signal = self.copy(
                parent_bundle=None,
            )
            signal <<= self
            return signal
        if width < len(self):
            return self[width - 1:]

        # Perform sign extension / padding according to the signedness of the signal
        padding_size = (width - len(self))
        if self.signed:
            return self[(-1,) * padding_size, :]
        return Constant(0, padding_size) @ self

    def signal_decl(self) -> str:
        """
        Declare the signal in the module implementation.
        :return: logic (signed) [...]SIGNAL_NAME
        """
        if self.net_name is None:
            raise ValueError("Signal name is not set")
        if len(self) == 0:
            raise ValueError("Signal width is not set and cannot be inferred")

        return self._SIGNAL_DECL_TEMPLATE.substitute(
            signed="signed" if self.signed else "",
            width=f"[{width - 1}:0]" if (width := len(self)) > 1 else "",
            name=self.net_name,
        )

    def elaborate(self) -> str:
        signal_decl = self.signal_decl()

        # Ignore assignment signal if it is driven by an output of a module instance
        if self.driver().type != SignalType.OUTPUT:
            assignment = self._SIGNAL_ASSIGN_TEMPLATE.substitute(
                name=self.net_name,
                driver=self.driver().net_name,
            )
            return "\n".join((signal_decl, assignment))
        return signal_decl

    def copy(self, parent_bundle: Optional["SignalBundle"] = None, **kwargs) -> "Signal":
        """
        Copy the signal. Driver is discarded.
        Signal can only be copied to a SignalBundle, not an IOBundle.
        :return: A new signal with the same configuration.
        """
        return Signal(
            name=self.name,
            width=len(self),
            signed=self.signed,
            parent_bundle=parent_bundle,
        )

    def __ilshift__(self, other):
        """
        Connect the signal with the driver.
        :param other: Driving Signal
        :return: Original Signal
        """
        if isinstance(other, (int, bytes)):
            other = Constant(other, len(self), self.signed)
        if not isinstance(other, Signal):
            raise TypeError(f"Cannot assign {type(other)} to drive {type(self)}")
        if self._drivers.get(self.SINGLE_DRIVER_NAME) is not None:
            raise ValueError(f"Multiple driver on Signal {self.name}.")
        if self.type == SignalType.OUTPUT and self.owner_instance is not None:
            raise ValueError("Cannot drive output of a module instance.")
        if other.type == SignalType.INPUT and other.owner_instance is not None:
            raise ValueError("Input of a module instance cannot drive other signal.")
        if self.type == SignalType.INPUT and self.owner_instance is None:
            raise ValueError("Cannot drive the Input of a module type.")
        if other.type == SignalType.OUTPUT and other.owner_instance is None:
            raise ValueError("Output of a module type cannot drive other signal.")
        if self.type == SignalType.CONSTANT:
            raise ValueError("Constant signal cannot be driven.")

        self._drivers[self.SINGLE_DRIVER_NAME] = other
        if len(self) == 0:
            self.set_width(len(other))
        elif len(other) == 0:
            other.set_width(len(self))
        return self

    def __add__(self, other) -> "Signal":
        return Operation.create(OPType.ADD, self, other)

    def __iadd__(self, other) -> "Signal":
        return self.__add__(other)

    def __sub__(self, other) -> "Signal":
        return Operation.create(OPType.MINUS, self, other)

    def __isub__(self, other) -> "Signal":
        return self.__sub__(other)

    def __neg__(self) -> "Signal":
        return Operation.create(
            OPType.MINUS,
            Constant(0, len(self), self.signed),
            self
        )

    def __mul__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.MUL, self, other)

    def __imul__(self, other) -> "Signal":
        return self.__mul__(other)

    def __eq__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.EQ, self, other)

    def __ne__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.NEQ, self, other)

    def __ge__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.GE, self, other)

    def __gt__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.GT, self, other)

    def __le__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.LE, self, other)

    def __lt__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.LT, self, other)

    def __and__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.AND, self, other)

    def __iand__(self, other) -> "Signal":
        return self.__and__(other)

    def __or__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.OR, self, other)

    def __ior__(self, other) -> "Signal":
        return self.__or__(other)

    def __xor__(self, other) -> "Signal":
        if isinstance(other, int):
            other = Constant(other, len(self), self.signed)
        return Operation.create(OPType.XOR, self, other)

    def __ixor__(self, other) -> "Signal":
        return self.__xor__(other)

    def __invert__(self) -> "Signal":
        return Operation.create(OPType.NOT, self, None)

    def __cmp__(self, other) -> "Signal":
        raise NotImplementedError("Comparison Operator is not implemented.")

    def __lshift__(self, other) -> "Signal":
        if isinstance(other, int):
            op = Operation.create(OPType.LSHIFT, self, other)
            op._op_config.shifting = other
            return op
        raise NotImplementedError("Only Constant Shift is not implemented.")

    def __rshift__(self, other) -> "Signal":
        if isinstance(other, int):
            op = Operation.create(OPType.RSHIFT, self, other)
            op._op_config.shifting = other
            return op
        raise NotImplementedError("Only Constant Shift is not implemented.")

    def __irshift__(self, other) -> "Signal":
        raise NotImplementedError("`>>=` Operator is not defined.")

    def __getitem__(self, item) -> "Signal":
        """ The Slicing Operator """
        # Return the concatenation of the sliced signals
        # If multiple slices are provided.
        if isinstance(item, Iterable):
            sliced = [self[i] for i in item]
            concat = None
            for s in sliced:
                if concat is None:
                    concat = s
                else:
                    concat @= s
            return concat

        if isinstance(item, int):
            item = slice(item, item, None)
        if item is Ellipsis:
            item = slice(None, None, None)

        if not isinstance(item, slice):
            raise TypeError(f"Cannot perform operation on {type(item)}")
        if item.step is not None:
            raise ValueError("Slice step is not implement.")

        return Operation.create(OPType.SLICE, self, item)

    def __matmul__(self, other) -> "Signal":
        """
        Special operation for the `@` operator, which is the concatenation operator.
        """
        if isinstance(other, Signal):
            return Operation.create(OPType.CONCAT, self, other)
        raise TypeError(f"Cannot perform operation on {type(other)}")

    def __imatmul__(self, other) -> "Signal":
        return self.__matmul__(other)

    def __len__(self):
        return self._config.width

    def reg(
            self,
            clk: Optional["Input"] = None,
            enable: Optional["Signal"] = None,
            reset: Optional["Signal"] = None,
            async_reset: Optional["Signal"] = None,
            reset_value: Optional[Union[bytes, int]] = None,
            async_reset_value: Optional[Union[bytes, int]] = None,
            name: Optional[str] = None,
    ) -> "Register":
        """
        Create a register from the signal.
        """
        register = Register(
            width=len(self),
            enable=enable,
            reset=reset,
            async_reset=async_reset,
            reset_value=reset_value,
            async_reset_value=async_reset_value,
            clk=clk,
            signed=self.signed,
            name=name,
        )
        register <<= self
        return register

    def when(
            self,
            condition: "Signal",
            else_: Optional["Signal"] = None,
    ) -> "When":
        """
        Create a `Self if Condition else Else_` statement, similar to the ternary operator in C / Python.
        E.g. `gated = data.when(enable)`, `default_2 = data.when(enable, 2)`
        """
        if else_ is None:
            else_ = 0
        return When(
            condition=condition,
            if_true=self,
            if_false=else_,
        )

    def case(self, cases: dict[int, Union["Signal", int]], default: Optional[Union["Signal", int]] = None, ) -> "Case":
        """
        Create a `case` statement.
        """
        return Case(
            selector=self,
            cases=cases,
            default=default,
        )

    def any(self) -> "Signal":
        """
        Create an `any` statement.
        """
        return Operation.create(OPType.ANY, self, None)

    def all(self) -> "Signal":
        """
        Create an `all` statement.
        """
        return Operation.create(OPType.ALL, self, None)

    def parity(self) -> "Signal":
        """
        Create an `parity` statement.
        """
        return Operation.create(OPType.PARITY, self, None)


class SignalDict(UserDict):
    """
    Signal Dict contains a dictionary of signals keyed by their name / specific alias.
    They are read only after being assigned.
    """

    def __getattr__(self, alias):
        if alias.startswith("_"):
            return super().__getattribute__(alias)
        if alias not in self.data:
            raise KeyError(f"Signal {alias} is not defined.")
        return self.data[alias]

    def __getitem__(self, alias):
        if alias not in self.data:
            raise KeyError(f"Signal {alias} is not defined.")
        return self.data[alias]

    def __setitem__(self, alias, value):
        cur = self.data.get(alias)
        if not isinstance(value, Signal) and value is not None:
            raise KeyError(f"Object {alias} is not a Signal.")
        if cur is not None and value is not cur:
            raise KeyError(f"Signal {alias} is read only. Are you trying to connect it with <<= Operator?")

        if value is not None:
            self.data[alias] = value


class Input(Signal):
    """
    Representing an input signal.
    It has no driver, but it is driving other signals.
    It is used by both the module declaration and the module instance.
    """

    def __init__(
            self,
            name: str, width: int, signed: bool = False,
            owner_instance: Optional["Instance"] = None,
            **kwargs
    ):
        """
        I/O ports must have name and width well-defined by designers.
        """
        if name is None:
            raise ValueError("Input name is not set")
        if width == 0:
            raise ValueError("Input width is not set")

        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self._config.signal_type = SignalType.INPUT
        self._config.owner_instance = owner_instance

    @property
    def net_name(self) -> str:
        """
        Net Name of I/O must be the same with the name, even they are within an IOBundle
        """
        return self.name

    def elaborate(self) -> str:
        """
        Elaborate the input signal in the module declaration.
        :return: input logic (signed) [...]PORT_NAME
        """
        port_decl = self.signal_decl().rstrip(";")
        return f"input  {port_decl}"

    def copy(self, owner_instance: Optional["Instance"] = None) -> "Input":
        """
        Copy the input signal. Driver is discarded.
        I/O port can only be assigned to an instance, not a SignalBundle / IOBundle.
        :return: A new input signal with the same configuration.
        """
        return Input(
            name=self.name,
            width=len(self),
            signed=self.signed,
            owner_instance=owner_instance,
        )


class Output(Signal):
    """
    Representing an output signal.
    They are the starting points when we elaborate the module.
    It is used by both the module declaration and the module instance.
    """

    def __init__(
            self,
            name: str, width: int, signed: bool = False,
            owner_instance: Optional["Instance"] = None,
            **kwargs
    ):
        """
        I/O ports must have name and width well-defined by designers.
        """
        if name is None:
            raise ValueError("Output name is not set")
        if width == 0:
            raise ValueError("Output width is not set")
        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self._config.signal_type = SignalType.OUTPUT
        self._config.owner_instance = owner_instance

    @property
    def net_name(self) -> str:
        """
        Net Name of I/O must be the same with the name, even they are within an IOBundle
        """
        return self.name

    def elaborate(self) -> str:
        """
        Elaborate the output signal in the module declaration.
        :return: output logic (signed) [...]PORT_NAME
        """
        port_decl = self.signal_decl().rstrip(";")
        return f"output {port_decl}"

    def copy(self, owner_instance: Optional["Instance"] = None, **kwargs) -> "Output":
        """
        Copy the output signal. Driver is discarded.
        I/O port can only be assigned to an instance, not a SignalBundle / IOBundle.
        :return: A new output signal with the same configuration.
        """
        return Output(
            name=self.name,
            width=len(self),
            signed=self.signed,
            owner_instance=owner_instance,
        )


class Constant(Signal):
    """
    Representing a constant signal. The value stored in bytes representing the constance driver.
    """
    new_const_counter = count(0)

    def __init__(
            self,
            value, width: int, signed: bool = False,
            name: Optional[str] = None,
            **kwargs
    ):
        if name is None:
            name = f"const_{next(self.new_const_counter)}"

        super().__init__(width=width, signed=signed, name=name, **kwargs)
        self._config.signal_type = SignalType.CONSTANT
        self.value: bytes = value

    def elaborate(self) -> str:
        signal_decl = self.signal_decl()
        assignment = self._SIGNAL_ASSIGN_TEMPLATE.substitute(
            name=self.net_name,
            driver=self.sv_constant(self.value, len(self), self.signed),
        )
        return "\n".join((signal_decl, assignment))

    @staticmethod
    def sv_constant(value: Optional[Union[int, bytes]], width: int, signed: bool = False) -> str:
        """
        Convert a Python integer or bytes object to a SystemVerilog constant expression.
        If value is None, return "X", the SystemVerilog constant for an unknown value.
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


class Operation(Signal):
    """
    Representing an operation, most likely a combination logic
    """
    _OP_IMPL_TEMPLATE = {
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
    _OP_WIDTH_INFERENCE = {
        OPType.NOT: lambda x, y: len(x),
        OPType.OR: lambda x, y: max(len(x), len(y)),
        OPType.AND: lambda x, y: max(len(x), len(y)),
        OPType.XOR: lambda x, y: max(len(x), len(y)),
        OPType.ADD: lambda x, y: max(len(x), len(y)),
        OPType.MINUS: lambda x, y: max(len(x), len(y)),
        OPType.MUL: lambda x, y: max(len(x), len(y)),
        OPType.EQ: lambda x, y: 1,
        OPType.NEQ: lambda x, y: 1,
        OPType.LT: lambda x, y: 1,
        OPType.LE: lambda x, y: 1,
        OPType.GT: lambda x, y: 1,
        OPType.GE: lambda x, y: 1,

        OPType.LSHIFT: lambda x, s: len(x),
        OPType.RSHIFT: lambda x, s: len(x),

        OPType.ANY: lambda x, y: 1,
        OPType.ALL: lambda x, y: 1,
        OPType.PARITY: lambda x, y: 1,

        OPType.CONCAT: lambda x, y: len(x) + len(y),

        OPType.SLICE: lambda x, s: abs(s.stop - s.start) + 1,

    }
    _OP_SIGN_INFERENCE = {
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
    _OP_BLOCK_TEMPLATE = Template("always_comb\n  $op_impl")

    def __init__(self, width: int, op_type: OPType, signed: bool = False, **kwargs):
        super().__init__(width=width, signed=signed, **kwargs)
        self._op_config = OperationConfig(
            op_type=op_type,
        )

    def elaborate(self) -> str:
        """
        Declare the signal and elaborate the operation in the module implementation.
        """
        signal_decl = self.signal_decl()
        op_impl = ""
        if self._op_config.op_type in self._OP_IMPL_TEMPLATE:
            impl_params = {
                "output": self.net_name,
                "a": self._drivers["a"].net_name,
            }

            if self._drivers.get("b") is not None:
                impl_params["b"] = self._drivers["b"].net_name

            # Slicing Operator
            if self._op_config.slicing is not None:
                impl_params["slice_start"] = self._op_config.slicing.start
                impl_params["slice_stop"] = self._op_config.slicing.stop

            # Shifting Operator
            if self._op_config.shifting is not None:
                impl_params["b"] = self._op_config.shifting

            op_impl = self._OP_IMPL_TEMPLATE[self._op_config.op_type].substitute(**impl_params)
            op_impl = self._OP_BLOCK_TEMPLATE.substitute(op_impl=op_impl)

        return "\n".join((signal_decl, op_impl))

    @staticmethod
    def create(op_type: OPType, x: Signal, y: Optional[Union[Signal, slice, int, bytes]]) -> "Operation":
        """
        Factory method to create common operation with single / two arguments.
        """
        if not isinstance(x, Signal):
            raise TypeError(f"Cannot perform operation on {type(x)}")

        if op_type not in Operation._OP_IMPL_TEMPLATE:
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
                y = Constant(y, len(x), x.signed)
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
            width=Operation._OP_WIDTH_INFERENCE[op_type](x, y),
            signed=Operation._OP_SIGN_INFERENCE[op_type](x, y),
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
            slice_ = slice(len(driver) - 1, slice_.stop, None)
        if slice_.stop is None:
            slice_ = slice(slice_.start, 0, None)

        if slice_.start < 0:
            slice_ = slice(slice_.start + len(driver), slice_.stop, None)
        if slice_.stop < 0:
            slice_ = slice(slice_.start, slice_.stop + len(driver), None)

        return slice_


class When(Operation):
    """
    Representing an if-else statement.
    """
    _IF_ELSE_TEMPLATE = Template(
        "always_comb\n"
        "  if ($condition) $output = $if_true;\n"
        "  else $output = $if_false;"
    )

    def __init__(self, condition: Signal, if_true: Signal, if_false: Optional[Union[Signal, int, bytes]], **kwargs):
        super().__init__(op_type=OPType.WHEN, width=len(if_true), signed=if_true.signed, **kwargs)

        if if_false is None:
            if_false = 0
        if isinstance(if_false, (int, bytes)):
            if_false = Constant(if_false, len(if_true), if_true.signed)

        if len(condition) != 1:
            raise ValueError("Condition has to be a single bit signal.")

        self._drivers["condition"] = condition
        self._drivers[self.SINGLE_DRIVER_NAME] = if_true
        self._drivers["d_false"] = if_false

    def elaborate(self) -> str:
        signal_decl = self.signal_decl()
        if_else = self._IF_ELSE_TEMPLATE.substitute(
            output=self.net_name,
            condition=self._drivers["condition"].net_name,
            if_true=self._drivers[self.SINGLE_DRIVER_NAME].net_name,
            if_false=self._drivers["d_false"].net_name,
        )
        return "\n".join((signal_decl, if_else))


class Case(Operation):
    """
    Representing a case statement.

    The selector is a signal, and the cases is a dictionary of selector value and driver.
    Selector can only be an unsigned signal, and the key of the cases can only be int.
    All drivers must have the same width.
    If all drivers are int, Inference the width of the output signal.

    The Case Operation requires all the width of the input signals are defined,
    before the creation of the Operation.
    """
    _CASE_TEMPLATE = Template(
        "always_comb\n"
        "  $unique case ($selector)\n"
        "$cases\n"
        "  endcase"
    )
    _CASE_ITEM_TEMPLATE = Template(
        "    $selector_value: $output = $driver;"
    )
    _DEFAULT_DRIVER_NAME = "default"

    def __init__(
            self, selector: Signal, cases: dict[Union[int], Union[Signal, int]],
            default: Optional[Union[Signal, int]] = None,
            **kwargs
    ):
        # Validate input before calling super().__init__()
        if selector.signed:
            raise ValueError("Selector cannot be signed.")
        if any(not isinstance(k, int) for k in cases):
            raise ValueError("Selector value can only be int.")
        if any(k >= 2 ** len(selector) for k in cases):
            raise ValueError("Selector value is out of range.")

        # Inference the width of the output signal
        output_signals = list(cases.values()) + ([] if default is None else [default])
        if any(isinstance(v, Signal) for v in output_signals):
            signal_width = {len(sig) for sig in output_signals if isinstance(sig, Signal)}
            signal_signed = {sig.signed for sig in output_signals if isinstance(sig, Signal)}
            if len(signal_width) != 1:
                raise ValueError("All drivers must have the same width.")
            if len(signal_signed) != 1:
                raise ValueError("All drivers must have the same signedness.")
            output_width = next(iter(signal_width))
            output_signed = next(iter(signal_signed))

            if output_width == 0:
                raise ValueError("Width of the output signal cannot be inferred.")
        else:
            # All drivers are int
            output_width = max(max(v.bit_length() for v in output_signals), 1)
            output_signed = any(v < 0 for v in output_signals)

        super().__init__(op_type=OPType.CASE, width=output_width, signed=output_signed, **kwargs)

        # Make a shallow copy of the cases
        self._cases = dict(cases.items())
        self._case_config = CaseConfig(
            unique=len(cases) == 2 ** len(selector),
            default=default,
        )

        # Assign the Drivers
        self._drivers[self.SINGLE_DRIVER_NAME] = selector
        for sel_value, driver in self._cases.items():
            driver_name = self._driver_name(sel_value)
            if isinstance(driver, Signal):
                self._drivers[driver_name] = driver
        if isinstance(default, Signal):
            self._drivers[self._DEFAULT_DRIVER_NAME] = default

    @staticmethod
    def _driver_name(case: int) -> str:
        return f"case_{case}"

    def elaborate(self) -> str:
        def driver_value(sig_or_const: Optional[Union[Signal, int]]) -> str:
            if isinstance(sig_or_const, Signal):
                return sig_or_const.net_name
            return Constant.sv_constant(sig_or_const, len(self), self.signed)

        signal_decl = self.signal_decl()
        case_table = []

        for selector_value, driver in self._cases.items():
            driver = driver.net_name if isinstance(driver, Signal) else Constant.sv_constant(driver, len(self),
                                                                                             self.signed)
            case_table.append(
                self._CASE_ITEM_TEMPLATE.substitute(
                    selector_value=Constant.sv_constant(
                        selector_value,
                        len(self._drivers[self.SINGLE_DRIVER_NAME]), False
                    ),
                    output=self.net_name,
                    driver=driver,
                )
            )

        if not self._case_config.unique:
            case_table.append(
                self._CASE_ITEM_TEMPLATE.substitute(
                    selector_value="default",
                    output=self.net_name,
                    driver=driver_value(self._case_config.default),
                )
            )

        case_impl = self._CASE_TEMPLATE.substitute(
            selector=self._drivers[self.SINGLE_DRIVER_NAME].net_name,
            cases="\n".join(case_table),
            unique="unique" if self._case_config.unique else "",
        )
        return "\n".join((signal_decl, case_impl))


class Register(Operation):
    """
    Representing a register, most likely DFF
    """
    _REG_TEMPLATE = {
        RegType.DFF: Template("always_ff @(posedge $clk) begin\n  $output <= $driver;\nend"),
        RegType.DFF_EN: Template("always_ff @(posedge $clk) begin\n  if ($enable) $output <= $driver;\nend"),
        RegType.DFF_RST: Template(
            "always_ff @(posedge $clk) begin\n"
            "  if ($reset) $output <= $reset_value;\n"
            "  else $output <= $driver;\n"
            "end"
        ),
        RegType.DFF_EN_RST: Template(
            "always_ff @(posedge $clk) begin\n"
            "  if ($reset) $output <= $reset_value;\n"
            "  else if ($enable) $output <= $driver;\n"
            "end"
        ),
        RegType.DFF_ASYNC_RST: Template(
            "always_ff @(posedge $clk, negedge $async_reset) begin\n"
            "  if ($async_reset == 1'b0) $output <= $async_reset_value;\n"
            "  else $output <= $driver;\n"
            "end"
        ),
        RegType.DFF_EN_ASYNC_RST: Template(
            "always_ff @(posedge $clk, negedge $async_reset) begin\n"
            "  if ($async_reset == 1'b0) $output <= $async_reset_value;\n"
            "  else if ($enable) $output <= $driver;\n"
            "end"
        ),
        RegType.DFF_BOTH_RST: Template(
            "always_ff @(posedge $clk, negedge $async_reset) begin\n"
            "  if ($async_reset == 1'b0) $output <= $async_reset_value;\n"
            "  else if ($reset) $output <= $reset_value;\n"
            "  else $output <= $driver;\n"
            "end"
        ),
        RegType.DFF_EN_BOTH_RST: Template(
            "always_ff @(posedge $clk, negedge $async_reset) begin\n"
            "  if ($async_reset == 1'b0) $output <= $async_reset_value;\n"
            "  else if ($reset) $output <= $reset_value;\n"
            "  else if ($enable) $output <= $driver;\n"
            "end"
        ),
    }

    _new_reg_counter = count(0)

    def __init__(self, width: int,
                 enable: Optional[Signal] = None,
                 reset: Optional[Signal] = None,
                 reset_value: Optional[Union[bytes, int]] = None,
                 async_reset: Optional[Signal] = None,
                 async_reset_value: Optional[Union[bytes, int]] = None,
                 clk: Optional[Input] = None,
                 name: Optional[str] = None,
                 **kwargs
                 ):
        if name is None:
            name = f"reg_{next(self._new_reg_counter)}"

        super().__init__(op_type=OPType.REG, width=width, name=name, **kwargs)

        self._reg_config = RegisterConfig(
            enable=enable is not None,
            reset=reset is not None,
            async_reset=async_reset is not None,
            reset_value=reset_value,
            async_reset_value=async_reset_value,
        )
        if self._reg_config.reset_value is None:
            self._reg_config.reset_value = 0
        if self._reg_config.async_reset_value is None:
            self._reg_config.async_reset_value = 0

        if clk is None:
            raise ValueError("Register requires a clock signal.")

        self._drivers["clk"] = clk
        self._drivers[Signal.SINGLE_DRIVER_NAME] = None

        if self._reg_config.enable:
            self._drivers["enable"] = enable
        if self._reg_config.reset:
            self._drivers["reset"] = reset
        if self._reg_config.async_reset:
            self._drivers["async_reset"] = async_reset

    def validate(self) -> list[Exception]:
        errors = []
        if self._drivers["clk"] is None:
            errors.append(ValueError("Register requires a clock signal."))
        if len(self._drivers["clk"]) != 1:
            errors.append(ValueError("Clock has to be a single bit."))

        if self._drivers[Signal.SINGLE_DRIVER_NAME] is None:
            errors.append(ValueError("Register requires a driver."))

        if self._reg_config.enable:
            if self._drivers["enable"] is None:
                errors.append(ValueError("Register requires an enable signal."))
            if len(self._drivers["enable"]) != 1:
                errors.append(ValueError("Enable signal has to be a single bit."))

        if self._reg_config.reset:
            if self._drivers["reset"] is None:
                errors.append(ValueError("Register requires a reset signal."))
            if len(self._drivers["reset"]) != 1:
                errors.append(ValueError("Reset signal has to be a single bit."))

        if self._reg_config.async_reset:
            if self._drivers["async_reset"] is None:
                errors.append(ValueError("Register requires an async reset signal."))
            if len(self._drivers["async_reset"]) != 1:
                errors.append(ValueError("Async Reset signal has to be a single bit."))

        return errors

    def elaborate(self) -> str:
        errors = self.validate()
        if errors:
            raise ValueError(f"Register {self.net_name} is not valid.", errors)

        reg_decl = self.signal_decl()

        reg_type = {
            (False, False, False): RegType.DFF,
            (True, False, False): RegType.DFF_EN,
            (False, True, False): RegType.DFF_RST,
            (True, True, False): RegType.DFF_EN_RST,
            (False, False, True): RegType.DFF_ASYNC_RST,
            (True, False, True): RegType.DFF_EN_ASYNC_RST,
            (False, True, True): RegType.DFF_BOTH_RST,
            (True, True, True): RegType.DFF_EN_BOTH_RST,
        }[(self._reg_config.enable, self._reg_config.reset, self._reg_config.async_reset)]

        connections = {
            "output": self.net_name,
            "driver": self._drivers[Signal.SINGLE_DRIVER_NAME].net_name,
            "clk": self._drivers["clk"].net_name,
        }
        if self._reg_config.enable:
            connections["enable"] = self._drivers["enable"].net_name
        if self._reg_config.reset:
            connections["reset"] = self._drivers["reset"].net_name
            connections["reset_value"] = Constant.sv_constant(
                self._reg_config.reset_value, len(self), self._config.signed
            )
        if self._reg_config.async_reset:
            connections["async_reset"] = self._drivers["async_reset"].net_name
            connections["async_reset_value"] = Constant.sv_constant(
                self._reg_config.async_reset_value, len(self), self._config.signed
            )

        reg_impl = self._REG_TEMPLATE[reg_type].substitute(**connections)

        return "\n".join((reg_decl, reg_impl))
