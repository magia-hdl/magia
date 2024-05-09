"""
Manual SystemVerilog Assertions statements.

It is used to create SystemVerilog assertions that are not supported by the magia library.
We assume the developer has the knowledge of SystemVerilog Assertions and can write the assertions manually.
"""
from contextlib import contextmanager
from string import Template

from .data_struct import PropType
from .signals import CodeSectionType, Signal, Synthesizable
from .utils import ModuleContext

SVA_MANUAL_TEMPLATE = Template(
    "$prop_name: $prop_type property (\n"
    "  @(posedge $clk)\n"
    "  $prop_statement\n"
    ");\n"
)
SVA_MANUAL_DISABLE_IFF_TEMPLATE = Template(
    "$prop_name: $prop_type property (\n"
    "  @(posedge $clk) disable iff($disable_iff)\n"
    "  $prop_statement\n"
    ");\n"
)


class SVAManual(Synthesizable):
    """Manual SystemVerilog Assertions statements."""

    assertion_count = 0

    def __init__(
            self, prop_statement: str,
            name: None | str, clk: Signal, disable_iff: None | Signal = None,
            prop_type: PropType = PropType.ASSERT,
            **kwargs
    ):
        super().__init__(**kwargs)
        if (module_context := ModuleContext().current) is not None:
            module_context.manual_sva_collected.append(self)

        if name is None:
            name = f"prop_{SVAManual.assertion_count}"
            SVAManual.assertion_count += 1
        self._name = f"{prop_type.value}_{name}"
        self.prop_statement = prop_statement
        self.clk = clk
        self.disable_iff = disable_iff
        self.prop_type = prop_type

    @classmethod
    @contextmanager
    def code_section(cls):
        """
        Context manager for Manual SVA code section.

        This code section activate `name_as_str` context, which allows developer use f-string
        referring to the signal name.

        e.g. f"{req} |=> {valid}"
        """
        with Synthesizable.code_section(CodeSectionType.SVA_MANUAL), Signal.name_as_str():
            yield

    @property
    def drivers(self) -> list[Signal]:
        """Return the clock domain driving signals of the assertion."""
        if self.disable_iff is not None:
            return [self.clk, self.disable_iff]
        return [self.clk]

    @property
    def name(self) -> str:
        """Return the name of the assertion."""
        return self._name

    def elaborate(self) -> str:
        """Elaborate the SystemVerilog assertion statement."""
        template = SVA_MANUAL_TEMPLATE if self.disable_iff is None else SVA_MANUAL_DISABLE_IFF_TEMPLATE
        return template.substitute(
            prop_name=self.name,
            prop_type=self.prop_type.value,
            clk=self.clk.name,
            disable_iff=self.disable_iff.name if self.disable_iff is not None else "",
            prop_statement=self.prop_statement
        )
