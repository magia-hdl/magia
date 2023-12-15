from collections import UserDict
from collections.abc import Iterable

from dataclasses import dataclass
from itertools import count
from string import Template
from typing import Optional, Union

from .constants import SignalType, OPType, RegType
from .clock import get_cur_clock
from .util import sv_constant


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
    ...


@dataclass
class OperationConfig:
    op_type: OPType
    slicing: Optional[slice] = None
    shifting: Optional[int] = None
    ...


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

    def build(self):
        """
        Phase of defining the implementation details of a synthesizable object.
        e.g. resolving signal names, etc.
        """
        return

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
    _SINGLE_DRIVER_NAME: str = "d"
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
    def name(self) -> str:
        """
        Full name of a signal, used for elaboration.
        """
        if self._config.parent_bundle is not None:
            return f"bundle_{id(self._config.parent_bundle)}_{self._config.name}"
        return self._config.name

    @property
    def alias(self) -> str:
        """
        Alias of the signal, is used to identify the signal in a bundle
        """
        return self._config.name

    @property
    def type(self) -> SignalType:
        return self._config.signal_type

    @property
    def signed(self) -> bool:
        return self._config.signed

    def driver(self, driver_name: str = _SINGLE_DRIVER_NAME) -> Optional["Signal"]:
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

    ...

    def set_width(self, width: int):
        self._config.width = width

    def set_signed(self, signed: bool):
        self._config.signed = signed

    def set_name(self, name: str):
        self._config.name = name

    def signal_decl(self) -> str:
        """
        Declare the signal in the module implementation.
        :return: logic (signed) [...]SIGNAL_NAME
        """
        if self.name is None:
            raise ValueError("Signal name is not set")
        if len(self) == 0:
            raise ValueError("Signal width is not set and cannot be inferred")

        return self._SIGNAL_DECL_TEMPLATE.substitute(
            signed="signed" if self.signed else "",
            width=f"[{width - 1}:0]" if (width := len(self)) > 1 else "",
            name=self.name,
        )

    def elaborate(self) -> str:
        signal_decl = self.signal_decl()

        # Ignore assignment signal if it is driven by an output of a module instance
        if self._drivers[self._SINGLE_DRIVER_NAME].type != SignalType.OUTPUT:
            assignment = self._SIGNAL_ASSIGN_TEMPLATE.substitute(
                name=self.name,
                driver=self._drivers[self._SINGLE_DRIVER_NAME].name,
            )
            return "\n".join((signal_decl, assignment))
        else:
            return signal_decl

    def copy(self, parent_bundle: Optional["SignalBundle"] = None, **kwargs) -> "Signal":
        """
        Copy the signal. Driver is discarded.
        :return: A new signal with the same configuration.
        """
        new_signal = Signal(
            name=self.alias,
            width=len(self),
            signed=self.signed,
            parent_bundle=parent_bundle,
        )
        return new_signal

    def __ilshift__(self, other):
        """
        Connect the signal with the driver.
        :param other: Driving Signal
        :return: Original Signal
        """
        if not isinstance(other, Signal):
            raise TypeError(f"Cannot assign {type(other)} to drive {type(self)}")
        if self._drivers.get(self._SINGLE_DRIVER_NAME) is not None:
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

        self._drivers[self._SINGLE_DRIVER_NAME] = other
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
            op = Operation.create(OPType.LSHIFT, self, None)
            op._op_config.shifting = other
            return op
        raise NotImplementedError("Only Constant Shift is not implemented.")

    def __rshift__(self, other) -> "Signal":
        if isinstance(other, int):
            op = Operation.create(OPType.RSHIFT, self, None)
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

    def __contains__(self, item) -> "Signal":
        """
        Special operation for the `in` keyword, which check if there is any bit set to 1/0 in the Signal.
        This DOES NOT RETURN BOOLEAN.
        """
        if item == 1 or item is True:
            return Operation.create(OPType.ANY, self, None)
        if item == 0 or item is False:
            return ~Operation.create(OPType.ALL, self, None)
        raise ValueError(f"`in` operator only supports 0/1/True/False. Got {item}.")

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
            async_reset_value: Optional[Union[bytes, int]] = None
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
        )
        register <<= self
        return register


class SignalDict(UserDict):
    """
    Signal Dict contains a dictionary of signals keyed by their name.
    They are read only after being assigned.
    """

    def __getattr__(self, item):
        if item.startswith("_"):
            return super().__getattribute__(item)
        if item not in self.data:
            raise KeyError(f"Signal {item} is not defined.")
        return self.data[item]

    def __getitem__(self, item):
        if item not in self.data:
            raise KeyError(f"Signal {item} is not defined.")
        return self.data[item]

    def __setitem__(self, key, value):
        cur = self.data.get(key)
        if not isinstance(value, Signal) and value is not None:
            raise KeyError(f"Object {key} is not a Signal.")
        if cur is not None and value is not cur:
            raise KeyError(f"Signal {key} is read only. Are you trying to connect it with <<= Operator?")

        if value is not None:
            self.data[key] = value


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
        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self._config.signal_type = SignalType.INPUT
        self._config.owner_instance = owner_instance
        ...

    @property
    def name(self) -> str:
        """
        Name of I/O is the same with the alias, even they are within an IOBundle
        """
        return self._config.name

    def build(self):
        """
        I/O ports must have name and width well-defined by designers.
        """
        if self.name is None:
            raise ValueError("Input name is not set")
        if len(self) == 0:
            raise ValueError("Input width is not set")

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
        :return: A new input signal with the same configuration.
        """
        new_input = Input(
            name=self.name,
            width=len(self),
            signed=self.signed,
            owner_instance=owner_instance,
        )
        return new_input


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
        super().__init__(name=name, width=width, signed=signed, **kwargs)
        self._config.signal_type = SignalType.OUTPUT
        self._config.owner_instance = owner_instance
        ...

    @property
    def name(self) -> str:
        """
        Name of I/O is the same with the alias, even they are within an IOBundle
        """
        return self._config.name

    def build(self):
        """
        I/O ports must have name and width well-defined by designers.
        """
        if self.name is None:
            raise ValueError("Input name is not set")
        if len(self) == 0:
            raise ValueError("Input width is not set")

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
        :return: A new output signal with the same configuration.
        """
        new_output = Output(
            name=self.name,
            width=len(self),
            signed=self.signed,
            owner_instance=owner_instance,
        )
        return new_output


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
            name=self.name,
            driver=sv_constant(self.value, len(self), self.signed),
        )
        return "\n".join((signal_decl, assignment))


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

        OPType.ANY: Template("$output = $a != 0;"),
        OPType.ALL: Template("$output = $a == '1;"),

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

        OPType.ANY: lambda x, y: 1,
        OPType.ALL: lambda x, y: 1,

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

        OPType.ANY: lambda x, y: False,
        OPType.ALL: lambda x, y: False,

        OPType.CONCAT: lambda x, y: x.signed,
        OPType.SLICE: lambda x, s: x.signed,
    }
    _OP_BLOCK_TEMPLATE = Template("always_comb\n  $op_impl")

    def __init__(self, width: int, signed: bool = False, **kwargs):
        super().__init__(width=width, signed=signed, **kwargs)
        self._op_config = OperationConfig(
            ...
        )

    def elaborate(self) -> str:
        """
        Declare the signal and elaborate the operation in the module implementation.
        """
        signal_decl = self.signal_decl()
        op_impl = ""
        if self._op_config.op_type in self._OP_IMPL_TEMPLATE:
            impl_params = dict(
                output=self.name,
                a=self._drivers["a"].name,
            )

            if self._drivers.get("b") is not None:
                impl_params["b"] = self._drivers["b"].name

            # Slicing Operator
            if self._op_config.slicing is not None:
                impl_params["slice_start"] = self._op_config.slicing.start
                impl_params["slice_stop"] = self._op_config.slicing.stop

            op_impl = self._OP_IMPL_TEMPLATE[self._op_config.op_type].substitute(**impl_params)
            op_impl = self._OP_BLOCK_TEMPLATE.substitute(op_impl=op_impl)

        return "\n".join((signal_decl, op_impl))

    @staticmethod
    def create(op_type: OPType, x: "Signal", y: Optional[Union["Signal", slice]]) -> "Operation":
        """
        Factory method to create common operation with single / two arguments.
        """
        if not isinstance(x, Signal):
            raise TypeError(f"Cannot perform operation on {type(x)}")

        if op_type == OPType.SLICE:
            if not isinstance(y, slice):
                raise TypeError("Slicing Operator requires a slice as 2nd operand.")
        else:
            if not isinstance(y, Signal) and y is not None:
                raise TypeError(f"Cannot perform operation on {type(y)}")

        if op_type not in Operation._OP_IMPL_TEMPLATE:
            raise ValueError(f"Operation {op_type} is not supported.")
        if op_type not in (OPType.NOT, OPType.ANY, OPType.ALL) and y is None:
            raise ValueError(f"Operation {op_type} requires two operand.")

        if op_type == OPType.SLICE:
            y = Operation._legalize_slice(x, y)

        new_op = Operation(
            width=Operation._OP_WIDTH_INFERENCE[op_type](x, y),
            signed=Operation._OP_SIGN_INFERENCE[op_type](x, y),
        )
        new_op._drivers["a"] = x
        if isinstance(y, Signal):
            new_op._drivers["b"] = y
        new_op._op_config.op_type = op_type
        if op_type == OPType.SLICE:
            new_op._op_config.slicing = y
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

        super().__init__(width=width, name=name, **kwargs)
        self._config.op_type = OPType.REG

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
            clk = get_cur_clock()
        if clk is None:
            raise ValueError("Register requires a clock signal.")

        self._drivers["clk"] = clk
        self._drivers[Signal._SINGLE_DRIVER_NAME] = None

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

        if self._drivers[Signal._SINGLE_DRIVER_NAME] is None:
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
            raise ValueError(f"Register {self.name} is not valid.", errors)

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
            "output": self.name,
            "driver": self._drivers[Signal._SINGLE_DRIVER_NAME].name,
            "clk": self._drivers["clk"].name,
        }
        if self._reg_config.enable:
            connections["enable"] = self._drivers["enable"].name
        if self._reg_config.reset:
            connections["reset"] = self._drivers["reset"].name
            connections["reset_value"] = sv_constant(
                self._reg_config.reset_value, len(self), self._config.signed
            )
        if self._reg_config.async_reset_value:
            connections["async_reset"] = self._drivers["async_reset"].name
            connections["async_reset_value"] = sv_constant(
                self._reg_config.async_reset_value, len(self), self._config.signed
            )

        reg_impl = self._REG_TEMPLATE[reg_type].substitute(**connections)

        return "\n".join((reg_decl, reg_impl))
