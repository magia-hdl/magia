from __future__ import annotations

from dataclasses import dataclass
from itertools import count
from string import Template

from data_struct import OPType, RegType

from .constant import Constant
from .core import Signal


@dataclass
class RegisterConfig:
    enable: bool
    reset: bool
    async_reset: bool
    reset_value: bytes | int | None = None
    async_reset_value: bytes | int | None = None


class Register(Signal):
    """Representing a register, most likely DFF."""

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
                 enable: None | Signal = None,
                 reset: None | Signal = None,
                 reset_value: None | bytes | int = None,
                 async_reset: None | Signal = None,
                 async_reset_value: None | bytes | int = None,
                 clk: None | Signal = None,
                 name: None | str = None,
                 **kwargs
                 ):
        if name is None:
            name = f"reg_{next(self._new_reg_counter)}"

        super().__init__(width=width, name=name, **kwargs)
        self.signal_config.op_type = OPType.REG

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
        self._drivers[Signal.DEFAULT_DRIVER] = None

        if self._reg_config.enable:
            self._drivers["enable"] = enable
        if self._reg_config.reset:
            self._drivers["reset"] = reset
        if self._reg_config.async_reset:
            self._drivers["async_reset"] = async_reset

    def validate(self) -> list[Exception]:
        errors = []
        clk = self.driver("clk")
        enable = self.driver("enable")
        reset = self.driver("reset")
        async_reset = self.driver("async_reset")

        if self.driver() is None:
            errors.append(ValueError("Register requires a driver."))

        if clk is None:
            errors.append(ValueError("Register requires a clock signal."))
        if clk.width != 1:
            errors.append(ValueError("Clock has to be a single bit."))

        if self._reg_config.enable:
            if enable is None:
                errors.append(ValueError("Register requires an enable signal."))
            if enable.width != 1:
                errors.append(ValueError("Enable signal has to be a single bit."))

        if self._reg_config.reset:
            if reset is None:
                errors.append(ValueError("Register requires a reset signal."))
            if reset.width != 1:
                errors.append(ValueError("Reset signal has to be a single bit."))

        if self._reg_config.async_reset:
            if async_reset is None:
                errors.append(ValueError("Register requires an async reset signal."))
            if async_reset.width != 1:
                errors.append(ValueError("Async Reset signal has to be a single bit."))

        return errors

    def elaborate(self) -> str:
        errors = self.validate()
        if errors:
            raise ValueError(f"Register {self.name} is not valid.", errors)

        reg_decl = self.signal_decl()

        match self._reg_config.enable, self._reg_config.reset, self._reg_config.async_reset:
            case (False, False, False):
                reg_type = RegType.DFF
            case (True, False, False):
                reg_type = RegType.DFF_EN
            case (False, True, False):
                reg_type = RegType.DFF_RST
            case (True, True, False):
                reg_type = RegType.DFF_EN_RST
            case (False, False, True):
                reg_type = RegType.DFF_ASYNC_RST
            case (True, False, True):
                reg_type = RegType.DFF_EN_ASYNC_RST
            case (False, True, True):
                reg_type = RegType.DFF_BOTH_RST
            case (True, True, True):
                reg_type = RegType.DFF_EN_BOTH_RST

        connections = {
            "output": self.name,
            "driver": self.driver().name,
            "clk": self.driver("clk").name,
        }
        for control_signals in ("enable", "reset", "async_reset"):
            if (control := self.driver(control_signals)) is not None:
                connections[control_signals] = control.name
        if self._reg_config.reset:
            connections["reset_value"] = Constant.sv_constant(
                self._reg_config.reset_value, self.width, self.signed
            )
        if self._reg_config.async_reset:
            connections["async_reset_value"] = Constant.sv_constant(
                self._reg_config.async_reset_value, self.width, self.signed
            )

        reg_impl = self._REG_TEMPLATE[reg_type].substitute(**connections)

        return "\n".join((reg_decl, reg_impl))
