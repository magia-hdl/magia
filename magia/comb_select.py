from __future__ import annotations

from dataclasses import dataclass
from string import Template

from .constant import Constant
from .data_struct import OPType
from .factory import constant_like
from .signal import Signal

IF_ELSE_TEMPLATE = Template(
    "always_comb\n"
    "  if ($condition) $output = $if_true;\n"
    "  else $output = $if_false;"
)

CASE_TEMPLATE = Template(
    "always_comb\n"
    "  $unique case ($selector)\n"
    "$cases\n"
    "  endcase"
)
CASE_ITEM_TEMPLATE = Template(
    "    $selector_value: $output = $driver;"
)
CASE_DEFAULT_VALUE_DRIVER = "default"


@dataclass
class CaseConfig:
    unique: bool = False
    default: Signal | None = None


class When(Signal):
    """Representing an if-else statement."""

    def __init__(self, condition: Signal, if_true: Signal, if_false: None | Signal | int | bytes, **kwargs):
        super().__init__(width=if_true.width, signed=if_true.signed, **kwargs)
        self.signal_config.op_type = OPType.WHEN

        if if_false is None:
            if_false = 0
        if isinstance(if_false, (int, bytes)):
            if_false = constant_like(if_false, if_true)

        if condition.width != 1:
            raise ValueError("Condition has to be a single bit signal.")

        self._drivers["condition"] = condition
        self._drivers[self.DEFAULT_DRIVER] = if_true
        self._drivers["d_false"] = if_false

    def elaborate(self) -> str:
        signal_decl = self.signal_decl()
        if_else = IF_ELSE_TEMPLATE.substitute(
            output=self.name,
            condition=self._drivers["condition"].name,
            if_true=self._drivers[self.DEFAULT_DRIVER].name,
            if_false=self._drivers["d_false"].name,
        )
        return "\n".join((signal_decl, if_else))


class Case(Signal):
    """
    Representing a case statement.

    The selector is a signal, and the cases is a dictionary of selector value and driver.
    Selector can only be an unsigned signal, and the key of the cases can only be int.
    All drivers must have the same width.
    If all drivers are int, infer the width of the output signal.

    The Case Operation requires all the width of the input signals are defined,
    before the creation of the Operation.
    """

    def __init__(
            self, selector: Signal, cases: dict[int, Signal | int],
            default: None | Signal | int = None,
            **kwargs
    ):
        # Validate input before calling super().__init__()
        if selector.signed:
            raise ValueError("Selector cannot be signed.")
        if any(not isinstance(k, int) for k in cases):
            raise ValueError("Selector value can only be int.")
        if any(k >= 2 ** selector.width for k in cases):
            raise ValueError("Selector value is out of range.")

        # Infer the width of the output signal
        output_signals = list(cases.values()) + ([] if default is None else [default])
        if any(isinstance(v, Signal) for v in output_signals):
            signal_width = {sig.width for sig in output_signals if isinstance(sig, Signal)}
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

        super().__init__(width=output_width, signed=output_signed, **kwargs)
        self.signal_config.op_type = OPType.CASE

        # Make a shallow copy of the cases
        self._cases = dict(cases.items())
        self._case_config = CaseConfig(
            unique=len(cases) == 2 ** selector.width,
            default=default,
        )

        # Assign the Drivers
        self._drivers[self.DEFAULT_DRIVER] = selector
        for sel_value, driver in self._cases.items():
            driver_name = self._driver_name(sel_value)
            if isinstance(driver, Signal):
                self._drivers[driver_name] = driver
        if isinstance(default, Signal):
            self._drivers[CASE_DEFAULT_VALUE_DRIVER] = default

    @staticmethod
    def _driver_name(case: int) -> str:
        return f"case_{case}"

    def elaborate(self) -> str:
        def driver_value(sig_or_const: Signal | int | None) -> str:
            if isinstance(sig_or_const, Signal):
                return sig_or_const.name
            return Constant.sv_constant(sig_or_const, self.width, self.signed)

        signal_decl = self.signal_decl()
        case_table = []

        for selector_value, driver in self._cases.items():
            driver = driver.name if isinstance(driver, Signal) else Constant.sv_constant(driver, self.width,
                                                                                         self.signed)
            case_table.append(
                CASE_ITEM_TEMPLATE.substitute(
                    selector_value=Constant.sv_constant(
                        selector_value,
                        self._drivers[self.DEFAULT_DRIVER].width, False
                    ),
                    output=self.name,
                    driver=driver,
                )
            )

        if not self._case_config.unique:
            case_table.append(
                CASE_ITEM_TEMPLATE.substitute(
                    selector_value="default",
                    output=self.name,
                    driver=driver_value(self._case_config.default),
                )
            )

        case_impl = CASE_TEMPLATE.substitute(
            selector=self._drivers[self.DEFAULT_DRIVER].name,
            cases="\n".join(case_table),
            unique="unique" if self._case_config.unique else "",
        )
        return "\n".join((signal_decl, case_impl))
