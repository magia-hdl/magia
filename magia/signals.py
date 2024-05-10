from __future__ import annotations

import inspect
from collections.abc import Iterable
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum, auto
from functools import cached_property
from itertools import count
from pathlib import Path
from string import Template
from typing import TYPE_CHECKING

from .data_struct import OPType, SignalDict, SignalType
from .factory import constant, constant_like, create_case, create_comb_op, create_when, register, signal_config_like
from .utils import ModuleContext

if TYPE_CHECKING:
    from .bundle import Bundle, BundleSpec, BundleType
    from .comb_select import Case, When
    from .module import Instance
    from .register import Register

CURRENT_DIR = Path(__file__).parent

SIGNAL_DECL_TEMPLATE = Template("logic $signed $width $name;")
SIGNAL_DECL_FORMAL_TEMPLATE = Template("logic $signed $width $name = 0;")
SIGNAL_DECL_VERILOG_TEMPLATE = Template("wire $signed $width $name;")
SIGNAL_ASSIGN_TEMPLATE = Template("assign $name = $driver;")
ANNOTATION_TEMPLATE = Template("/*\nNet name: $net_name\n$comment$loc\n*/")


class CodeSectionType(Enum):
    LOGIC = auto()
    VERILOG = auto()
    FORMAL = auto()
    SVA_MANUAL = auto()


@dataclass
class SignalConfig:
    name: None | str = None
    width: int = 0
    signed: bool = False
    signal_type: SignalType = SignalType.SIGNAL
    op_type: OPType = OPType.WIRE
    description: str = ""

    # The module instance that owns this signal
    # Applicable to input / output ports only
    owner_instance: None | Instance = None

    # Specification of the bundle, if the signal is part of it
    bundle: None | Bundle = None
    bundle_spec: None | BundleSpec = None
    bundle_alias: None | str = None
    bundle_type: None | BundleType = None


class Synthesizable:
    """
    The base class of all synthesizable objects.

    They can be elaborated into SystemVerilog code.
    """

    _current_code_section = CodeSectionType.LOGIC

    @classmethod
    @contextmanager
    def code_section(cls, section: CodeSectionType):
        """
        Specify the code section of the synthesizable objects created within this context manager.

        Code section specify how the object is elaborated in the SystemVerilog code.

        :param section: The type of code section.
        """
        prev_value, Synthesizable._current_code_section = Synthesizable._current_code_section, section
        yield
        Synthesizable._current_code_section = prev_value

    @classmethod
    @property
    def current_code_section(cls) -> CodeSectionType:
        return Synthesizable._current_code_section

    def __init__(self, **kwargs):
        self._init_callstack = [
            frame_info for frame_info in inspect.stack()[1:]
            if Path(frame_info.filename).parent != CURRENT_DIR
        ]
        self._annotated_from = None
        self._comment = None
        self._code_section = Synthesizable.current_code_section

    @property
    def name(self) -> str:
        """Full name of a signal, used for elaboration."""
        raise NotImplementedError

    @property
    def drivers(self) -> list[Signal]:
        """
        Get the drivers of a Synthesizable object.

        :returns: The driver signals.
        """
        raise NotImplementedError

    @cached_property
    def loc(self) -> str:
        """
        Get the location of the object in the code.

        This property only works if the object is annotated.
        """
        if not self.annotated:
            raise RuntimeError("Object is not annotated.")

        last_seen = None
        for i, frame_info in enumerate(self._init_callstack):
            last_seen = i if frame_info.filename == self._annotated_from else last_seen

        return "\n".join(
            f"{frame_info.filename}:{frame_info.lineno}"
            for frame_info in (
                self._init_callstack[:last_seen + 1]
                if last_seen is not None else self._init_callstack
            )
        )

    def elaborate(self) -> str:
        """
        Elaborate the object into SystemVerilog code.

        All configuration should be resolved before calling this method.
        :returns: SystemVerilog code.
        """
        return ""

    def annotate(self, comment: None | str = None) -> Synthesizable:
        """
        Annotate the object with a comment.

        :returns: The object itself.
        """
        self._annotated_from = inspect.stack()[1].filename
        self._comment = comment
        return self

    @property
    def annotated(self) -> bool:
        """Determine if the object is annotated."""
        return self._annotated_from is not None

    @property
    def elaborated_loc(self) -> str:
        """
        Return the elaborated location of the object.

        :returns: SV comments with Line number of the object in the elaborated code.
        """
        return ANNOTATION_TEMPLATE.substitute(
            net_name=self.name,
            comment=f"{self._comment}\n" if self._comment else "",
            loc=self.loc,
        )


class Signal(Synthesizable):
    """
    The general signal class. It has drivers, which is another signal.

    It can also drive other signals / module instances.
    """

    DEFAULT_DRIVER: str = "d"

    _new_signal_counter = count(0)
    _str_with_net_name_only = False

    def __init__(
            self,
            width: int = 0, signed: bool = False,
            name: None | str = None,
            description: None | str = None,
            bundle: None | Bundle = None,
            bundle_spec: None | BundleSpec = None,
            bundle_alias: None | str = None,
            bundle_type: None | BundleType = None,
            **kwargs
    ):
        if name is None:
            name = f"net_{next(self._new_signal_counter)}"

        super().__init__(**kwargs)
        self.signal_config = SignalConfig(
            name=name,
            width=width,
            signed=signed,
            description="" if description is None else description,
            bundle=bundle,
            bundle_spec=bundle_spec,
            bundle_alias=bundle_alias,
            bundle_type=bundle_type,
        )
        self._drivers = SignalDict()
        match self._code_section:
            case CodeSectionType.SVA_MANUAL:
                if (module_context := ModuleContext().current) is not None:
                    module_context.manual_sva_collected.append(self)

    @property
    def name(self) -> str:
        """Full name of a signal, used for elaboration."""
        return self.signal_config.name

    @property
    def description(self) -> str:
        """Description of the signal."""
        return self.signal_config.description

    @property
    def type(self) -> SignalType:
        return self.signal_config.signal_type

    @property
    def is_input(self) -> bool:
        """Check if the signal is an input signal."""
        return False

    @property
    def is_output(self) -> bool:
        """Check if the signal is an output signal."""
        return False

    @property
    def width(self):
        return self.signal_config.width

    @property
    def signed(self) -> bool:
        return self.signal_config.signed

    def driver(self, driver_name: str = DEFAULT_DRIVER) -> None | Signal:
        """
        Get the driver of the signal.

        :param driver_name: The name of the driver. Default to the single driver.
        :returns: The driver signal.
        """
        return self._drivers.get(driver_name)

    @property
    def drivers(self) -> list[Signal]:
        """
        Get the drivers of the signal.

        :returns: The driver signals.
        """
        return list(self._drivers.values())

    @property
    def owner_instance(self) -> None | Instance:
        """
        Get the module instance that owns this signal.

        It is applicable to input / output signals only.
        """
        return self.signal_config.owner_instance

    def set_width(self, width: int):
        self.signal_config.width = width
        return self

    def set_signed(self, signed: bool):
        self.signal_config.signed = signed
        return self

    def set_name(self, name: str):
        self.signal_config.name = name
        return self

    def with_signed(self, signed: bool) -> Signal:
        """
        Create a new signal with the same configuration, but with a different signedness.

        Connect the original signal to the new signal.
        New Signal is not added to the parent bundle.

        :returns: A new signal with the same configuration.
        """
        signal = Signal(
            width=self.width,
            signed=signed,
        )
        signal <<= self
        return signal

    def with_width(self, width: int) -> Signal:
        """
        Create a new signal with the same configuration, but with a different width.

        Connect the original signal to the new signal.
        New Signal is not added to the parent bundle.

        :returns: A new signal with the new configuration.
        """
        if width == self.width:
            signal = Signal(
                width=width,
                signed=self.signed,
            )
            signal <<= self
            return signal
        if width < self.width:
            return self[width - 1:]

        # Perform sign extension / padding according to the signedness of the signal
        padding_size = (width - self.width)
        if self.signed:
            return self[(-1,) * padding_size, :]
        return constant(0, padding_size, False) @ self

    def signal_decl(self) -> str:
        """
        Declare the signal in the module implementation.

        :returns: logic (signed) [...]SIGNAL_NAME.
        """
        if self.name is None:
            raise ValueError("Signal name is not set")
        if self.width == 0:
            raise ValueError("Signal width is not set and cannot be inferred")

        template: None | Template = None
        match self._code_section:
            case CodeSectionType.LOGIC:
                template = SIGNAL_DECL_TEMPLATE
            case CodeSectionType.VERILOG:
                template = SIGNAL_DECL_VERILOG_TEMPLATE
            case CodeSectionType.FORMAL:
                template = SIGNAL_DECL_FORMAL_TEMPLATE
            case CodeSectionType.SVA_MANUAL:
                template = SIGNAL_DECL_TEMPLATE

        if template is None:
            raise ValueError("Cannot determine the template.")

        decl = template.substitute(
            signed="signed" if self.signed else "",
            width=f"[{width - 1}:0]" if (width := self.width) > 1 else "",
            name=self.name,
        )
        if self.annotated:
            decl += f"\n{self.elaborated_loc}"
        return decl

    @classmethod
    @contextmanager
    def name_as_str(cls):
        """Declare a context that prints the net name of the signal only, but not the full representation."""
        prev_value, cls._str_with_net_name_only = cls._str_with_net_name_only, True
        yield
        cls._str_with_net_name_only = prev_value

    def __repr__(self):
        return f"{type(self).__name__}({self.name}:{self.width})"

    def __str__(self):
        if self._str_with_net_name_only:
            return self.name
        return repr(self)

    def elaborate(self) -> str:
        # Ignore assignment signal if it is not driven by any signal
        # or by an output of a module instance
        if (driving_signal := self.driver()) is None or driving_signal.owner_instance is not None:
            return ""

        return SIGNAL_ASSIGN_TEMPLATE.substitute(
            name=self.name,
            driver=self.driver().name,
        )

    def __ilshift__(self, other):
        """
        Connect the signal with the driver.

        :param other: Driving Signal
        :returns: Original Signal
        """
        if isinstance(other, (int, bytes)):
            other = constant_like(other, self)
        if not isinstance(other, Signal):
            raise TypeError(f"Cannot assign {type(other).__name__} to drive {type(self).__name__}")
        if self.driver() is not None:
            raise ValueError(f"Multiple driver on Signal {self.name}.")

        if other.is_input and other.owner_instance is not None:
            raise ValueError("Input of a module instance cannot drive other signal.")
        if other.is_output and other.owner_instance is None:
            raise ValueError("Output of a module type cannot drive other signal.")

        self._drivers[self.DEFAULT_DRIVER] = other
        if self.width == 0:
            self.signal_config.width = other.width
        elif other.width == 0:
            other.signal_config.width = self.width
        return self

    def __add__(self, other) -> Signal:
        return create_comb_op(OPType.ADD, self, other)

    def __iadd__(self, other) -> Signal:
        return self.__add__(other)

    def __sub__(self, other) -> Signal:
        return create_comb_op(OPType.MINUS, self, other)

    def __isub__(self, other) -> Signal:
        return self.__sub__(other)

    def __neg__(self) -> Signal:
        return create_comb_op(
            OPType.MINUS,
            constant_like(0, self),
            self
        )

    def __mul__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.MUL, self, other)

    def __imul__(self, other) -> Signal:
        return self.__mul__(other)

    def __eq__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.EQ, self, other)

    def __ne__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.NEQ, self, other)

    def __ge__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.GE, self, other)

    def __gt__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.GT, self, other)

    def __le__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.LE, self, other)

    def __lt__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.LT, self, other)

    def __and__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.AND, self, other)

    def __iand__(self, other) -> Signal:
        return self.__and__(other)

    def __or__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.OR, self, other)

    def __ior__(self, other) -> Signal:
        return self.__or__(other)

    def __xor__(self, other) -> Signal:
        if isinstance(other, int):
            other = constant_like(other, self)
        return create_comb_op(OPType.XOR, self, other)

    def __ixor__(self, other) -> Signal:
        return self.__xor__(other)

    def __invert__(self) -> Signal:
        return create_comb_op(OPType.NOT, self, None)

    def __cmp__(self, other) -> Signal:
        raise NotImplementedError("Comparison Operator is not implemented.")

    def __lshift__(self, other) -> Signal:
        if isinstance(other, int):
            return create_comb_op(OPType.LSHIFT, self, other)
        raise NotImplementedError("Only Constant Shift is implemented.")

    def __rshift__(self, other) -> Signal:
        if isinstance(other, int):
            return create_comb_op(OPType.RSHIFT, self, other)
        raise NotImplementedError("Only Constant Shift is implemented.")

    def __irshift__(self, other) -> Signal:
        raise NotImplementedError("`>>=` Operator is not defined.")

    def __getitem__(self, item) -> Signal:
        """Slicing Operator."""
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
            raise TypeError(f"Cannot perform operation on {type(item).__name__}")
        if item.step is not None:
            raise ValueError("Slice step is not implement.")

        return create_comb_op(OPType.SLICE, self, item)

    def __matmul__(self, other) -> Signal:
        """
        Concatenate two signals.

        This is a special operation for the `@`.
        """
        if isinstance(other, Signal):
            return create_comb_op(OPType.CONCAT, self, other)
        raise TypeError(f"Cannot perform operation on {type(other).__name__}")

    def __imatmul__(self, other) -> Signal:
        return self.__matmul__(other)

    def reg(
            self,
            clk: None | Signal = None,
            enable: None | Signal = None,
            reset: None | Signal = None,
            async_reset: None | Signal = None,
            reset_value: None | bytes | int = None,
            async_reset_value: None | bytes | int = None,
            name: None | str = None,
    ) -> Register:
        """Create a register from the signal."""
        new_register = register(
            width=self.width,
            enable=enable,
            reset=reset,
            async_reset=async_reset,
            reset_value=reset_value,
            async_reset_value=async_reset_value,
            clk=clk,
            signed=self.signed,
            name=name,
        )
        new_register <<= self
        return new_register

    def when(
            self,
            condition: Signal,
            else_: None | Signal | int | bytes = None,
    ) -> When:
        """
        Create a `Self if Condition else Else_` statement, similar to the ternary operator in C / Python.

        E.g. `gated = data.when(enable)`, `default_2 = data.when(enable, 2)`.
        """
        return create_when(
            condition=condition,
            if_true=self,
            if_false=else_,
        )

    def case(self, cases: dict[int, Signal | int], default: None | Signal | int = None, ) -> Case:
        """Create a `case` statement."""
        return create_case(
            selector=self,
            cases=cases,
            default=default,
        )

    def any(self) -> Signal:
        """Create an `any` statement."""
        return create_comb_op(OPType.ANY, self, None)

    def all(self) -> Signal:
        """Create an `all` statement."""
        return create_comb_op(OPType.ALL, self, None)

    def parity(self) -> Signal:
        """Create an `parity` statement."""
        return create_comb_op(OPType.PARITY, self, None)

    @classmethod
    def like(cls, signal: Signal, **kwargs) -> Signal:
        """Create a signal with the same configuration as the given signal."""
        return Signal(**signal_config_like(signal, **kwargs))
