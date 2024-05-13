"""Assertion cells used by formal verification tools."""
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from string import Template

from .signals import CodeSectionType, Signal, Synthesizable
from .utils import ModuleContext


class AssertionType(Enum):
    ASSERT = "assert"
    ASSUME = "assume"
    COVER = "cover"


ASSERTION_TEMPLATE = Template(
    "// $name_and_desc\n"
    "always @(posedge $clk) begin\n"
    "    $name: $type ($cond);\n"
    "end"
)
ASSERTION_EN_TEMPLATE = Template(
    "// $name_and_desc\n"
    "always @(posedge $clk) begin\n"
    "    if($en) begin\n"
    "        $name: $type ($cond);\n"
    "    end\n"
    "end"
)


@dataclass
class AssertionCellConfig:
    name: str
    cond: Signal
    clk: Signal
    assertion_type: AssertionType
    en: None | Signal = None
    desc: None | str = None


class AssertionCell(Synthesizable):
    """Assertion Cells for Formal Verification."""

    assertion_counter = 0

    def __init__(
            self,
            name: None | str,
            cond: Signal,
            clk: Signal,
            en: None | Signal = None,
            desc: None | str = None,
            assertion_type: AssertionType | str = AssertionType.ASSERT,
            **kwargs,
    ):
        if self.current_code_section != CodeSectionType.FORMAL:
            raise RuntimeError("AssertionCell can only be used inside a Formal code section.")
        super().__init__(**kwargs)
        if cond.width != 1:
            raise ValueError("Assertion condition must be 1-bit wide")
        if clk.width != 1:
            raise ValueError("Assertion clock must be 1-bit wide")
        if en is not None and en.width != 1:
            raise ValueError("Assertion enable must be 1-bit wide")
        if isinstance(assertion_type, str):
            assertion_type = AssertionType(assertion_type)
        if name is None:
            name = f"{assertion_type.value}_autogen_{AssertionCell.assertion_counter}"
            AssertionCell.assertion_counter += 1

        self.config = AssertionCellConfig(
            name=name,
            cond=cond,
            clk=clk,
            en=en,
            desc=desc,
            assertion_type=assertion_type,
        )
        if (module_context := ModuleContext().current) is not None:
            if self.name in module_context.assertions_collected:
                raise ValueError(f"Assertion name '{self.name}' already exists")
            module_context.assertions_collected[self.name] = self

    @property
    def name(self) -> str:
        """Return the name of the assertion."""
        return self.config.name

    @property
    def drivers(self) -> list[Signal]:
        """Return the driving signals of the assertion."""
        if self.config.en is not None:
            return [self.config.clk, self.config.cond, self.config.en]
        return [self.config.clk, self.config.cond]

    @classmethod
    @contextmanager
    def code_section(cls):
        with Synthesizable.code_section(CodeSectionType.FORMAL):
            yield

    def elaborate(self) -> str:
        """Elaborate the assertion into SystemVerilog code."""
        template = ASSERTION_EN_TEMPLATE if self.config.en is not None else ASSERTION_TEMPLATE

        return template.substitute(
            name=self.name,
            name_and_desc=f"{self.name}: {self.config.desc}" if self.config.desc is not None else self.name,
            type=self.config.assertion_type.value,
            cond=self.config.cond.name,
            clk=self.config.clk.name,
            en=self.config.en.name if self.config.en is not None else "",
        )
